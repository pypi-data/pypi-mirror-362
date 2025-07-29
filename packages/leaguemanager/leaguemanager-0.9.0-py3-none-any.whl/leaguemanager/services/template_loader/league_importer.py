from pathlib import Path
from typing import Protocol, runtime_checkable

from attrs import define, field, validators

__all__ = [
    "ExcelLoader",
    "CSVLoader",
    "JSONLoader",
    "GoogleSheetsLoader",
    "MemoryLoader",
]


@runtime_checkable
class Importer(Protocol):
    """Protocol for importers that can load data into the database."""

    def load(self) -> None:
        """Load data into the database."""

    def validate(self) -> None:
        """Validate the data before loading it into the database."""


def convert_str_to_path(value: str | Path) -> Path:
    """Convert a string to a Path object."""
    if isinstance(value, str):
        return Path(value)
    return value


@define
class ExcelLoader:
    """A class to load data from Excel files into the database."""

    file_path: str | Path | None = field(default=None, converter=convert_str_to_path)

    def load(self, data: dict) -> None:
        """Load data from an Excel file into the database."""
        # Implementation for loading data from Excel
        raise NotImplementedError("Excel loading not implemented yet.")

    def validate(self, data: dict) -> None:
        """Validate the data before loading it into the database."""
        # Implementation for validating Excel data
        raise NotImplementedError("Excel loading not implemented yet.")


@define
class CSVLoader:
    """A class to load data from CSV files into the database."""

    file_path: str | Path | None = field(default=None, converter=convert_str_to_path)

    def load(self, data: dict) -> None:
        """Load data from a CSV file into the database."""
        # Implementation for loading data from CSV
        raise NotImplementedError("CSV loading not implemented yet.")

    def validate(self, data: dict) -> None:
        """Validate the data before loading it into the database."""
        # Implementation for validating CSV data
        raise NotImplementedError("CSV loading not implemented yet.")


@define
class JSONLoader:
    """A class to load data from JSON files into the database."""

    file_path: str | Path | None = field(default=None, converter=convert_str_to_path)

    def load(self, data: dict) -> None:
        """Load data from a JSON file into the database."""
        # Implementation for loading data from JSON
        raise NotImplementedError("JSON loading not implemented yet.")

    def validate(self, data: dict) -> None:
        """Validate the data before loading it into the database."""
        # Implementation for validating JSON data
        raise NotImplementedError("JSON loading not implemented yet.")


@define
class GoogleSheetsLoader:
    """A class to load data from Google Sheets into the database."""

    sheet_id: str | None = field(default=None)
    spreadsheet_name: str | None = field(default=None)
    """Name of the Google Sheets spreadsheet to load data from."""

    def load(self, data: dict) -> None:
        """Load data from a Google Sheet into the database."""
        # Implementation for loading data from Google Sheets
        raise NotImplementedError("Google Sheets loading not implemented yet.")

    def validate(self, data: dict) -> None:
        """Validate the data before loading it into the database."""
        # Implementation for validating Google Sheets data
        raise NotImplementedError("Google Sheets loading not implemented yet.")


@define
class MemoryLoader:
    """A class to load data from memory into the database."""

    data: dict | None = field(default=None)

    def load(self, data: dict) -> None:
        """Load data from memory into the database."""
        # Implementation for loading data from memory

        return data

    def validate(self, data: dict) -> None:
        """Validate the data before loading it into the database."""
        # Implementation for validating memory data
        raise NotImplementedError("Memory loading not implemented yet.")
