"""Change case operation."""

from typing import Literal

from pydantic import Field

from datarush.core.dataflow import Operation, Tableset
from datarush.core.types import BaseOperationModel, ColumnStr, TableStr

CaseType = Literal["upper", "lower", "capitalize", "title", "swapcase", "casefold"]


class ChangeCaseModel(BaseOperationModel):
    """Model for Change Case operation."""

    table: TableStr = Field(title="Table", description="Table to modify")
    columns: list[ColumnStr] = Field(
        title="Columns",
        description="Columns to change case. If empty, all string columns are used.",
        default_factory=list,
    )
    case: CaseType = Field(
        title="Case Type",
        description="Case transformation to apply: upper, lower, capitalize, title, swapcase, casefold",
        default="lower",
    )


class ChangeCase(Operation):
    """Change the case of string values in specified columns."""

    name = "change_case"
    title = "Change Case"
    description = "Change the case of string values in specified columns"
    model: ChangeCaseModel

    def summary(self) -> str:
        """Provide operation summary."""
        cols = (
            ", ".join(f"**{col}**" for col in self.model.columns)
            if self.model.columns
            else "all string columns"
        )
        return f"Change case to **{self.model.case}** in {cols} of `{self.model.table}`"

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

        # Apply case transformation to each target column
        for column in target_columns:
            # Convert to string and apply case transformation
            df[column] = getattr(df[column].astype(str).str, self.model.case)()

        tableset.set_df(self.model.table, df)
        return tableset
