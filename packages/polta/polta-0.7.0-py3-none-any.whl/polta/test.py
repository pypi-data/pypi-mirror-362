from dataclasses import dataclass, field
from polars import DataFrame

from polta.check import Check
from polta.enums import CheckAction


@dataclass
class Test:
  check: Check
  column: str
  check_action: CheckAction
  kwargs: dict = field(default_factory=lambda: {})

  result_column: str = field(init=False)

  def __post_init__(self) -> None:
    self.result_column: str = self.check.build_result_column(self.column)

  def run(self, df: DataFrame) -> DataFrame:
    if self.check.simple_function:
      return self.check.function(df, self.column)
    else:
      return self.check.function(df, self.column, **self.kwargs)
