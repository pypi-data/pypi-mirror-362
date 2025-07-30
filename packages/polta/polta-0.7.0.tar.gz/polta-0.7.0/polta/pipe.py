import polars as pl

from dataclasses import dataclass, field
from datetime import datetime, UTC
from deltalake import DeltaTable
from polars import DataFrame
from typing import Optional, Union
from uuid import uuid4

from polta.enums import WriteLogic, TableQuality
from polta.exceptions import (
  EmptyPipe,
  TableQualityNotRecognized,
  WriteLogicNotRecognized
)
from polta.exporter import Exporter
from polta.ingester import Ingester
from polta.table import Table
from polta.transformer import Transformer


@dataclass
class Pipe:
  """Changes and moves data in the metastore
  
  Positional Args:
    logic (Union[Ingester, Exporter, Transformer]): the pipe logic to handle data
  
  Initialized fields:
    id (str): the unique ID of the pipe for the pipeline
    table (Table): the destination Table
    write_logic (Optional[WriteLogic]): how the data should be placed in target table
  """
  logic: Union[Exporter, Ingester, Transformer]

  id: str = field(init=False)
  table: Table = field(init=False)
  write_logic: Optional[WriteLogic] = field(init=False)

  def __post_init__(self) -> None:
    self.id: str = '.'.join([
      'pp',
      self.logic.pipe_type.value,
      self.logic.table.id
    ])
    self.table: Table = self.logic.table
    self.write_logic = self.logic.write_logic

  def execute(self, dfs: dict[str, DataFrame] = {}, in_memory: bool = False,
              strict: bool = False) -> tuple[DataFrame, DataFrame, DataFrame]:
    """Executes the pipe

    Args:
      dfs (dict[str, DataFrame]): if applicable, source DataFrames (default {})
      in_memory (bool): indicates whether to run without saving (default False)
      strict (bool): indicates whether to fail on empty result (default False)

    Returns:
      passed, failed, quarantined (tuple[DataFrame, DataFrame, DataFrame]): the resulting DataFrames
    """
    print(f'Executing pipe {self.id}')
    
    # Record when the execution began
    execution_start: datetime = datetime.now(UTC)

    # Load in any extra data before transformation
    dfs.update(self.logic.get_dfs())

    # For in-memory exports, just carry over the table data
    # Otherwise, run the transformation/pre-load steps
    if isinstance(self.logic, Exporter) and in_memory:
      df: DataFrame = dfs[self.table.id]
    else:
      df: DataFrame = self.logic.transform(dfs)
      df: DataFrame = self.add_metadata_columns(df)
      df: DataFrame = self.conform_schema(df)

    # Run any tests and return the three data results
    passed, failed, quarantined = self.table.apply_tests(df)

    # Handle any quarantined records
    if not quarantined.is_empty():
      self.quarantine(quarantined)

    # If strict mode is enabled and dataset is empty, raise EmptyPipe
    succeeded: bool = (not strict) or (not passed.is_empty())

    # For standard runs and non-exports, save the passed data
    if isinstance(self.logic, (Ingester, Transformer)) and not in_memory:
      self.save(passed)
    
    # For exports, export the data
    if isinstance(self.logic, Exporter):
      self.logic.export(passed)

    # Print results
    print(f'  - Records passed: {passed.shape[0]}')
    print(f'  - Records failed: {failed.shape[0]}')
    print(f'  - Records quarantined: {quarantined.shape[0]}')

    # Log the pipe execution in the system table
    self.table.metastore.write_pipe_history(
      pipe_id=self.id,
      execution_start_ts=execution_start,
      strict=strict,
      succeeded=succeeded,
      in_memory=in_memory,
      passed_count=passed.shape[0],
      failed_count=failed.shape[0],
      quarantined_count=quarantined.shape[0]
    )

    # If the pipe failed, raise the EmptyPipe exception
    if not succeeded:
      raise EmptyPipe()
    # Otherwise, return remaining passed records
    return passed, failed, quarantined
  
  def add_metadata_columns(self, df: DataFrame) -> DataFrame:
    """Adds relevant metadata columns to the DataFrame before loading

    This method presumes the DataFrame carries its original metadata
    
    Args:
      df (DataFrame): the DataFrame before metadata columns
    
    Returns:
      df (DataFrame): the resulting DataFrame
    """
    id: str = str(uuid4())
    now: datetime = datetime.now(UTC)
    
    if self.table.quality.value == TableQuality.RAW.value:
      df: DataFrame = df.with_columns([
        pl.lit(id).alias('_raw_id'),
        pl.lit(now).alias('_ingested_ts')
      ])
    elif self.table.quality.value == TableQuality.CONFORMED.value:
      df: DataFrame = df.with_columns([
        pl.lit(id).alias('_conformed_id'),
        pl.lit(now).alias('_conformed_ts')
      ])
    elif self.table.quality.value == TableQuality.CANONICAL.value:
      df: DataFrame = df.with_columns([
        pl.lit(id).alias('_canonicalized_id'),
        pl.lit(now).alias('_created_ts'),
        pl.lit(now).alias('_modified_ts')
      ])
    else:
      raise TableQualityNotRecognized(self.table.quality.value)

    return df
  
  def conform_schema(self, df: DataFrame) -> DataFrame:
    """Conforms the DataFrame to the expected schema
    
    Args:
      df (DataFrame): the transformed, pre-conformed DataFrame
    
    Returns:
      df (DataFrame): the conformed DataFrame
    """
    df: DataFrame = self.add_metadata_columns(df)
    return df.select(*self.table.schema.polars.keys())

  def save(self, df: DataFrame) -> None:
    """Saves a DataFrame into the target Delta Table
    
    Args:
      df (DataFrame): the DataFrame to load
    """
    self.table.create_if_not_exists(
      table_path=self.table.table_path,
      schema=self.table.schema.deltalake
    )
    print(f'Loading {df.shape[0]} record(s) into {self.table.table_path}')

    if self.write_logic.value == WriteLogic.APPEND.value:
      self.table.append(df)
    elif self.write_logic.value == WriteLogic.OVERWRITE.value:
      self.table.overwrite(df)
    elif self.write_logic.value == WriteLogic.UPSERT.value:
      self.table.upsert(df)
    else:
      raise WriteLogicNotRecognized(self.write_logic)

  def quarantine(self, df: DataFrame) -> None:
    """Handles quarantined records from a save attempt

    The records get upserted into the corresponding quarantine table
    
    Args:
      df (DataFrame): the DataFrame of quarantined records
    """
    print(f'  - {df.shape[0]} record(s) got quarantined: {self.table.quarantine_path}')
    # Merge if the quarantine table exists
    # Otherwise, just append this time
    if DeltaTable.is_deltatable(self.table.quarantine_path):
      (df
        .write_delta(
          target=self.table.quarantine_path,
          mode='merge',
          delta_merge_options={
            'predicate': f's.{self.table.schema.failure_column} = t.{self.table.schema.failure_column}',
            'source_alias': 's',
            'target_alias': 't'
          }
        )
        .when_matched_update_all()
        .when_not_matched_insert_all()
        .execute()
      )
    else:
      df.write_delta(self.table.quarantine_path, mode='append')
