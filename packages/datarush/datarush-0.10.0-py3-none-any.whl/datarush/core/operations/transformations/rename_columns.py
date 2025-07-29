"""Rename columns operation."""

from pydantic import Field

from datarush.core.dataflow import Operation, Tableset
from datarush.core.types import BaseOperationModel, StringMap, TableStr


class RenameColumnsModel(BaseOperationModel):
    """Model for Rename Columns operation."""

    table: TableStr = Field(title="Table", description="Table to modify")
    column_mapping: StringMap = Field(
        title="Column Mapping (old -> new)",
        description="Map of column names to rename: {old_column_name: new_column_name}",
        default_factory=StringMap,
    )


class RenameColumns(Operation):
    """Rename columns in a table."""

    name = "rename_columns"
    title = "Rename Columns"
    description = "Rename columns using a mapping of old names to new names"
    model: RenameColumnsModel

    def summary(self) -> str:
        """Provide operation summary."""
        if not self.model.column_mapping:
            return f"No columns to rename in `{self.model.table}`"

        mappings = [f"**{old}** → **{new}**" for old, new in self.model.column_mapping.items()]
        return f"Rename columns in `{self.model.table}`: {', '.join(mappings)}"

    def operate(self, tableset: Tableset) -> Tableset:
        """Run operation."""
        df = tableset.get_df(self.model.table)

        # Check if all old column names exist
        missing_columns = [
            col for col in self.model.column_mapping.keys() if col not in df.columns
        ]
        if missing_columns:
            raise ValueError(f"Columns not found in table: {missing_columns}")

        # Rename columns
        df = df.rename(columns=self.model.column_mapping)

        tableset.set_df(self.model.table, df)
        return tableset
