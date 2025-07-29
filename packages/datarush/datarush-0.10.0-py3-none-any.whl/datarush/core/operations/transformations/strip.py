"""Strip operation - remove leading and trailing whitespace from string values."""

from typing import Literal

from pydantic import Field

from datarush.core.dataflow import Operation, Tableset
from datarush.core.types import BaseOperationModel, ColumnStr, TableStr


class StripModel(BaseOperationModel):
    """Model for Strip operation."""

    table: TableStr = Field(title="Table", description="Table to modify")
    columns: list[ColumnStr] = Field(
        title="Columns",
        description="Columns to strip whitespace from. If empty, all string columns are used.",
        default_factory=list,
    )
    strip_type: Literal["both", "left", "right"] = Field(
        title="Strip Type",
        description="Type of stripping to apply: both (both sides), left (left only), right (right only)",
        default="both",
    )
    chars: str = Field(
        title="Characters to Remove",
        description="Specific characters to remove (default: whitespace). Leave empty for default whitespace removal.",
        default="",
    )


class Strip(Operation):
    """Remove leading and trailing whitespace from string values in specified columns."""

    name = "strip"
    title = "Strip"
    description = (
        "Remove leading and trailing whitespace (or specified characters) from string values"
    )
    model: StripModel

    def summary(self) -> str:
        """Provide operation summary."""
        cols = (
            ", ".join(f"**{col}**" for col in self.model.columns)
            if self.model.columns
            else "all string columns"
        )
        chars_desc = f" characters '{self.model.chars}'" if self.model.chars else " whitespace"
        return f"Strip {self.model.strip_type}{chars_desc} from {cols} in `{self.model.table}`"

    def operate(self, tableset: Tableset) -> Tableset:
        """Run operation."""
        df = tableset.get_df(self.model.table)

        # Determine which columns to process
        if self.model.columns:
            target_columns = self.model.columns
        else:
            # Use all string columns if no specific columns provided
            target_columns = df.select_dtypes(include=["object"]).columns.tolist()

        # Check if all target columns exist
        missing_columns = [col for col in target_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Columns not found in table: {missing_columns}")

        # Apply strip transformation to each target column
        for column in target_columns:
            # Convert to string and apply strip transformation
            if self.model.strip_type == "both":
                method = "strip"
            elif self.model.strip_type == "left":
                method = "lstrip"
            else:  # right
                method = "rstrip"

            str_method = getattr(df[column].astype(str).str, method)
            if self.model.chars:
                df[column] = str_method(self.model.chars)
            else:
                df[column] = str_method()

        tableset.set_df(self.model.table, df)
        return tableset
