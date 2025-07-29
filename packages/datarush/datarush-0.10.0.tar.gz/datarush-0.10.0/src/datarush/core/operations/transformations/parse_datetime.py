"""Parse datetime operation."""

from datetime import date, datetime
from typing import Literal

import dateparser
import pandas as pd
from pydantic import Field

from datarush.core.dataflow import Operation, Tableset
from datarush.core.types import BaseOperationModel, ColumnStr, TableStr


class ParseDatetimeModel(BaseOperationModel):
    """Model for Parse Datetime operation."""

    table: TableStr = Field(title="Table", description="Table to modify")
    column: ColumnStr = Field(
        title="Column", description="Column containing datetime strings to parse"
    )
    format: str = Field(
        title="Explicit Format",
        description="Datetime format (e.g., '%Y-%m-%d', '%m/%d/%Y', etc). If empty, uses dateparser's automatic detection",
        default="",
    )
    date_order: Literal["DMY", "MDY", "YMD"] = Field(
        title="Date Order", description="Day/Month/Year order", default="DMY"
    )
    timezone: str = Field(
        title="Timezone",
        description="Timezone for parsing (e.g., 'UTC', 'America/New_York'). See https://en.wikipedia.org/wiki/List_of_tz_database_time_zones for full list",
        default="UTC",
    )
    language: Literal["en", "es", "fr", "de", "it", "pt", "ru", "ja", "zh", "ar"] = Field(
        title="Language to use for auto-parsing", default="en"
    )
    return_type: Literal["datetime", "date", "timestamp"] = Field(
        title="Return Type", default="datetime"
    )
    on_error: Literal["null", "error"] = Field(
        title="Error Handling", description="What to do on parsing errors", default="null"
    )


class ParseDatetime(Operation):
    """Parse datetime strings in a column using dateparser."""

    name = "parse_datetime"
    title = "Parse Datetime"
    description = "Parse datetime strings in a column using dateparser with configurable settings"
    model: ParseDatetimeModel

    def summary(self) -> str:
        """Provide operation summary."""
        result = [
            f"Parse **{self.model.column}** as {self.model.return_type} in `{self.model.table}`"
        ]

        if self.model.timezone:
            result.append(f"in timezone `{self.model.timezone}`")

        if self.model.format:
            result.append(f"with format `{self.model.format}`")
        else:
            result.append(
                f"using language={self.model.language}, date_order={self.model.date_order}"
            )

        return " ".join(result)

    def operate(self, tableset: Tableset) -> Tableset:
        """Run operation."""
        df = tableset.get_df(self.model.table)

        # Check if column exists
        if self.model.column not in df.columns:
            raise ValueError(f"Column '{self.model.column}' not found in table")

        # Configure dateparser settings
        settings = {
            "DEFAULT_LANGUAGES": [self.model.language],
            "DATE_ORDER": self.model.date_order,
            "TIMEZONE": self.model.timezone,
            "FUZZY": False,
        }

        def parse_datetime(value: str | None) -> datetime | date | float | None:
            """Parse a single datetime value."""
            if pd.isna(value):
                return None

            value = str(value)

            try:
                if self.model.format:
                    parsed = datetime.strptime(value, self.model.format)
                else:
                    parsed = dateparser.parse(value, settings=settings)  # type: ignore
                    if parsed is None:
                        raise ValueError(value)

                return self._convert_return_type(parsed)

            except Exception as e:
                if self.model.on_error == "error":
                    raise ValueError(f"Could not parse datetime: {value}") from e
                return None

        # Apply parsing to the column
        df[self.model.column] = df[self.model.column].apply(parse_datetime)

        tableset.set_df(self.model.table, df)
        return tableset

    def _convert_return_type(self, parsed_datetime: datetime) -> datetime | date | float:
        """Convert parsed datetime to the requested return type."""
        if self.model.return_type == "datetime":
            return parsed_datetime
        elif self.model.return_type == "date":
            return parsed_datetime.date()
        elif self.model.return_type == "timestamp":
            return parsed_datetime.timestamp()
        else:
            return parsed_datetime
