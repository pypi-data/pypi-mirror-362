"""Split table on column operation."""

from pydantic import Field

from datarush.core.dataflow import Operation, Tableset
from datarush.core.types import BaseOperationModel, ColumnStr, TableStr


class SplitTableOnColumnModel(BaseOperationModel):
    """Model for Split Table On Column operation."""

    table: TableStr = Field(title="Table", description="Table to split")
    split_column: ColumnStr = Field(title="Split Column", description="Column to split on")
    drop_original_table: bool = Field(
        title="Drop Original Table",
        description="Whether to remove the original table after splitting",
        default=False,
    )
    drop_split_column: bool = Field(
        title="Drop Split Column",
        description="Whether to remove the split column from resulting tables",
        default=False,
    )


class SplitTableOnColumn(Operation):
    """Split a table into multiple tables based on unique values in a column."""

    name = "split_table_on_column"
    title = "Split Table On Column"
    description = "Split a table into multiple tables based on unique values in a column"
    model: SplitTableOnColumnModel

    def summary(self) -> str:
        """Provide operation summary."""
        drop_original = "drop original" if self.model.drop_original_table else "keep original"
        drop_split = "drop split column" if self.model.drop_split_column else "keep split column"
        return (
            f"Split `{self.model.table}` on column **{self.model.split_column}** "
            f"({drop_original}, {drop_split})"
        )

    def operate(self, tableset: Tableset) -> Tableset:
        """Run operation."""
        df = tableset.get_df(self.model.table)

        # Check if split column exists
        if self.model.split_column not in df.columns:
            raise ValueError(f"Column '{self.model.split_column}' not found in table")

        # Get unique values in split column
        unique_values = df[self.model.split_column].unique()

        # Create a new table for each unique value
        for value in unique_values:
            # Filter rows where split_column equals this value
            filtered_df = df[df[self.model.split_column] == value].copy()

            # Drop split column if requested
            if self.model.drop_split_column:
                filtered_df = filtered_df.drop(columns=[self.model.split_column])

            # Reset index to get clean 0, 1, 2... sequence
            filtered_df = filtered_df.reset_index(drop=True)

            # Use the value as the new table name
            table_name = str(value)
            tableset.set_df(table_name, filtered_df)

        # Drop original table if requested
        if self.model.drop_original_table:
            del tableset[self.model.table]

        return tableset
