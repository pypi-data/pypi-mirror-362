import polars as pl

from dataclasses import dataclass, field
from datetime import datetime
from deltalake import DeltaTable, Schema, TableFeatures
from os import makedirs, path
from pathlib import Path
from polars import DataFrame
from shutil import rmtree
from typing import Optional

from polta.test import Test
from polta.enums import CheckAction, TableQuality
from polta.exceptions import PoltaDataFormatNotRecognized
from polta.metastore import Metastore
from polta.table_schema import TableSchema
from polta.types import RawPoltaData


@dataclass
class Table:
  """Stores all applicable information for a Polars + Delta Table dataset
  
  Positional Args:
    domain (str): the kind of data this table contains
    quality (TableQuality): the quality of the data
    name (str): the name of the table
    
  Optional Args:
    raw_schema (Optional[Schema]): the raw table schema (default None)
    metastore (Metastore): The metastore (default Metastore())
    primary_keys (list[str]): for upserts, the primary keys of the table (default [])
    tests (list[Test]): test checks before loading any data
  
  Initialized fields:
    id (str): the unique identifier for the table
    schema (TableSchema): the table schema object
    table_path (str): the absolute path to the Table in the metastore
    ingestion_zone_path (str): the path to the ingestion zone
    state_file_directory (str): the absolute path to the state files directory
    state_file_path (str): the absolute path to the Table state file
    schema.polars (dict[str, DataType]): the table schema as a Polars object
    schema.deltalake (Schema): the table schema as a deltalake object
    columns (list[str]): the table columns
    merge_predicate (str): the SQL merge predicate for upserts
    quarantine_path (str): the path to the corresponding quarantine table
    schema.quarantine (Schema): the schema of the corresponding quarantine table
    failure_column (str): the column name for identifying failure records
  """
  domain: str
  quality: TableQuality
  name: str
  raw_schema: Optional[Schema] = field(default_factory=lambda: None)
  metastore: Metastore = field(default_factory=lambda: Metastore())
  primary_keys: list[str] = field(default_factory=lambda: [])
  tests: list[Test] = field(default_factory=lambda: [])

  id: str = field(init=False)
  schema: TableSchema = field(init=False)
  table_path: str = field(init=False)
  ingestion_zone_path: str = field(init=False)
  state_file_directory: str = field(init=False)
  state_file_path: str = field(init=False)
  quarantine_path: str = field(init=False)
  merge_predicate: Optional[str] = field(init=False)

  def __post_init__(self) -> None:
    self.id: str = '.'.join([
      self.domain,
      self.quality.value,
      self.name
    ])
    self.schema: TableSchema = TableSchema(self.raw_schema, self.quality)
    self.table_path: str = path.join(
      self.metastore.tables_directory,
      self.domain,
      self.quality.value,
      self.name
    )
    self.ingestion_zone_path: str = path.join(
      self.metastore.volumes_directory,
      'ingestion',
      self.domain,
      self.name
    )
    self.state_file_directory: str = path.join(
      self.metastore.volumes_directory,
      'state',
      self.domain,
      self.quality.value,
      self.name            
    )
    self.state_file_path: str = path.join(
      self.state_file_directory,
      '.STATE'
    )
    self.quarantine_path: str = path.join(
      self.metastore.volumes_directory,
      'quarantine',
      self.domain,
      self.quality.value,
      self.name
    )

    if self.primary_keys:
      self.merge_predicate: Optional[str] = Table.build_merge_predicate(self.primary_keys)
    else:
      self.merge_predicate: Optional[str] = None
    if self.quality.value == TableQuality.RAW.value:
      self._build_ingestion_zone_if_not_exists()

  @staticmethod
  def create_if_not_exists(table_path: str, schema: Schema) -> None:
    """Creates a Delta Table if it does not exist

    Args:
        table_path (str): the path of the Delta Table
        schema (Schema): the table schema, in case the Delta Table needs to be created
    """
    if not isinstance(table_path, str):
      raise TypeError('Error: table_path must be of type <str>')
    if not isinstance(schema, Schema):
      raise TypeError('Error: schema must be of type <Schema>')

    # If it exists already, return
    if DeltaTable.is_deltatable(table_path):
      return

    dt: DeltaTable = DeltaTable.create(table_path, schema, mode='ignore')
    dt.alter.add_feature(
      feature=TableFeatures.TimestampWithoutTimezone,
      allow_protocol_versions_increase=True
    )   

  @staticmethod
  def build_merge_predicate(primary_keys: list[str]) -> str:
    """Constructs a merge predicate based on the source/target aliases and primary keys

    Args:
      primary_keys (list[str]): the primary keys for the merge

    Returns:
      merge_predicate (str): the merge predicate as a conjunction of SQL conditions matching on primary keys
    """
    return ' AND '.join([f's.{k} = t.{k}' for k in primary_keys])

  def enforce_dataframe(self, data: RawPoltaData) -> DataFrame:
    """Takes either a DataFrame or record(s) and returns the DataFrame representation
    
    Args:
      data (RawPoltaData): the data to enforce
    
    Returns:
      df (DataFrame): the DataFrame representation
    """
    if isinstance(data, dict):
      return DataFrame([data], self.schema.polars)
    elif isinstance(data, list) and all(isinstance(r, dict) for r in data):
      return DataFrame(data, self.schema.polars)
    elif isinstance(data, DataFrame):
      return data
    else:
      raise PoltaDataFormatNotRecognized(type(data))

  def apply_tests(self, df: DataFrame) -> tuple[DataFrame, DataFrame, DataFrame]:
    """Applies each test case to the data
    
    Args:
      df (DataFrame): the DataFrame to test
        
    Returns:
      passed, failed, quarantined (DataFrame): the resulting DataFrames
    """
    # Build three empty DataFrames to hold results
    passed: DataFrame = DataFrame([], self.schema.polars)
    failed: DataFrame = DataFrame([], self.schema.quarantine)
    quarantined: DataFrame = DataFrame([], self.schema.quarantine)

    # Skip all tests they do not exist
    if not self.tests:
      return df, failed, quarantined

    # Iterate the available tests
    for test in self.tests:
      # Execute the test against the original DataFrame or the remaining records
      res_df: DataFrame = test.run(df if passed.is_empty() else passed)

      # Store the results either in a passed DataFrame or failed DataFrame
      passed: DataFrame = res_df.filter(pl.col(test.result_column) == 1).drop(test.result_column)
      failed_test: DataFrame = (res_df
        .filter(pl.col(test.result_column) == 0)
        .drop(test.result_column)
        .with_columns(pl.lit(test.check.name).alias('failed_test'))
      )

      # Depending on the action, place the failed tests in the appropriate DataFrame
      if test.check_action.value == CheckAction.FAIL.value:
        failed: DataFrame = pl.concat([failed, failed_test])
      elif test.check_action.value == CheckAction.QUARANTINE.value:
        quarantined: DataFrame = pl.concat([quarantined, failed_test])

    # Return the resulting DataFrames
    return passed, failed, quarantined

  def truncate(self) -> None:
    """Truncates the table"""
    self.overwrite(DataFrame([], self.schema.polars))
    self.metastore.clear_file_history(self.id)

  def drop(self) -> None:
    """Drops the table"""
    if path.exists(self.table_path) and DeltaTable.is_deltatable(self.table_path):
      rmtree(self.table_path)

  def clear_quarantine(self) -> None:
    """Clears the quarantine table if it exists"""
    if path.exists(self.quarantine_path) and \
     DeltaTable.is_deltatable(self.quarantine_path):
      df: DataFrame = DataFrame([], self.schema.quarantine)
      df.write_delta(self.quarantine_path, mode='overwrite')

  def get_as_delta_table(self) -> DeltaTable:
    """Retrieves the DeltaTable object for the Table
    
    Returns:
      delta_table (DeltaTable): the resulting Delta Table
    """
    self.create_if_not_exists(self.table_path, self.schema.deltalake)
    return DeltaTable(self.table_path)

  def get(self, filter_conditions: dict = {}, partition_by: list[str] = [], order_by: list[str] = [],
          order_by_descending: bool = True, select: list[str] = [], sort_by: list[str] = [], limit: int = 0,
          unique: bool = False) -> DataFrame:
    """Retrieves a record, or records, by a specific condition, expecting only one record to return
      
    Args:
      filter_conditions (optional) (dict): if applicable, the filter conditions (e.g., {file_path: 'path.json'})
      partition_by (optional) (list[str]): if applicable, the keys by which to partition during deduplication
      order_by (optional) (list[str]): if applicable, the columns by which to order during deduplication
      order_by_descending (optional) (bool): if applicable, whether to ORDER BY DESC
      select (optional) (list[str]): if applicable, the columns to return after retrieving the DataFrame
      sort_by (optional) (list[str]): if applicable, the columns by which to sort the output
      limit (optional) (int): if applicable, a limit to the number of rows to return
      unique (optional) (bool): if applicable, remove any duplicate records

    Returns:
      df (DataFrame): the resulting DataFrame
    """
    if not isinstance(filter_conditions, dict):
      raise TypeError('Error: filter_conditions must be of type <dict>')
    if not isinstance(partition_by, list):
      raise TypeError('Error: partition_by must be of type <list>')
    if not isinstance(order_by, list):
      raise TypeError('Error: order_by must be of type <list>')
    if not isinstance(order_by_descending, bool):
      raise TypeError('Error: order_by_descending must be of type <bool>')
    if not isinstance(select, list):
      raise TypeError('Error: select must be of type <list>')
    if not isinstance(sort_by, list):
      raise TypeError('Error: sort_by must be of type <list>')
    if not isinstance(limit, int):
      raise TypeError('Error: limit must be of type <int>')
    if not isinstance(unique, bool):
      raise TypeError('Error: unique must be of type <bool>')
    if not all(isinstance(c, str) for c in partition_by):
      raise TypeError('Error: all values in partition_by must be of type <str>')
    if not all(isinstance(c, str) for c in order_by):
      raise TypeError('Error: all values in order_by must be of type <str>')
    if not all(isinstance(c, str) for c in select):
      raise TypeError('Error: all values in select must be of type <str>')
    if not all(isinstance(c, str) for c in sort_by):
      raise TypeError('Error: all values in sort_by must be of type <str>')

    # Create the Delta Table if it does not exist
    self.create_if_not_exists(self.table_path, self.schema.deltalake)

    # Retrieve Delta Table as a Polars DataFrame
    df: DataFrame = pl.read_delta(self.table_path)

    # Apply the filter condition if applicable
    if filter_conditions:
      df: DataFrame = df.filter(**filter_conditions)

    # Filter columns if applicable
    if select:
      df: DataFrame = df.select(select)

    # Apply a simple deduplication if applicable        
    if partition_by and order_by:
      df: DataFrame = df \
        .sort(order_by, descending=order_by_descending) \
        .unique(subset=partition_by, keep='first')
    
    # Apply a limit if applicable
    if limit:
      df: DataFrame = df.limit(limit)
    
    # Remove duplicate records if applicable
    if unique:
      df: DataFrame = df.unique()
      
    # Sort the results if applicable
    if sort_by:
      df: DataFrame = df.sort(sort_by)

    return df
  
  def upsert(self, data: RawPoltaData) -> None:
    """Upserts a DataFrame into the Delta Table

    self.primary_keys must be specified for this method to run
    
    Args:
      data (RawPoltaData): the data to upsert
    """
    if not self.primary_keys:
      raise ValueError('Error: Delta Table does not have primary keys')

    # Ensure table exists first
    self.create_if_not_exists(self.table_path, self.schema.deltalake)

    # Ensure DataFrame type
    df: DataFrame = self.enforce_dataframe(data)

    # Merge the DataFrame into its respective Delta Table
    # This merge logic is a simple upsert based on the table's primary keys
    (df
      .write_delta(
        target=self.table_path,
        mode='merge',
        delta_merge_options={
          'predicate': self.merge_predicate,
          'source_alias': 's',
          'target_alias': 't',
        }
      )
      .when_matched_update_all()
      .when_not_matched_insert_all()
      .execute()
    )
    self.touch_state_file()

  def overwrite(self, data: RawPoltaData) -> None:
    """Overwrites the Delta Table with the inputted DataFrame
    
    Args:
      data (RawPoltaData): the data with which to overwrite
    """
    # Ensure table exists first
    self.create_if_not_exists(self.table_path, self.schema.deltalake)

    # Ensure DataFrame type
    df: DataFrame = self.enforce_dataframe(data)

    df.write_delta(
      target=self.table_path,
      mode='overwrite'
    )
    self.touch_state_file()

  def append(self, data: RawPoltaData) -> None:
    """Appends a DataFrame to the Delta Table

    Args:
      data (RawPoltaData): the data with which to append
    """
    # Ensure table exists first
    self.create_if_not_exists(self.table_path, self.schema.deltalake)

    # Ensure DataFrame type
    df: DataFrame = self.enforce_dataframe(data)

    df.write_delta(
      target=self.table_path,
      mode='append'
    )
    self.touch_state_file()

  def touch_state_file(self) -> None:
    """Touches the state file to update the last modified datetime"""
    try:
      Path(self.state_file_path).touch()
    except FileNotFoundError:
      makedirs(self.state_file_directory, exist_ok=True)        
      Path(self.state_file_path).touch()

  def get_last_modified_datetime(self) -> datetime:
    """Retrieves the last modified datetime of the table
    
    Returns:
      last_modified_datetime (datetime): the last modified datetime of the table
    """
    modified_time: float = path.getmtime(self.state_file_path)
    return datetime.fromtimestamp(modified_time)

  def get_last_modified_record(self) -> dict[str, any]:
    """Builds a dict record for last modified information

    Returns:
      last_modified_record (dict[str, any]): the metadata of the table's last modified timestamp
    """
    return {
      'domain': self.domain,
      'quality': self.quality.value,
      'table': self.name,
      'path': self.table_path,
      'last_modified_datetime': self.get_last_modified_datetime()
    }

  def _build_ingestion_zone_if_not_exists(self) -> None:
    """Builds an empty directory for ingesting files"""
    if not path.exists(self.ingestion_zone_path):
      makedirs(self.ingestion_zone_path, exist_ok=True)
      print(f'Ingestion zone created: {self.ingestion_zone_path}')
