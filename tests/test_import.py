"""
Tests for file import functionality
"""
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
import pytest

from duck_console.core.layout_importer import FieldDefinition, LayoutDefinition, LayoutImporter


@pytest.fixture
def sample_layout():
    """Fixture providing a sample fixed-width layout"""
    return LayoutDefinition(
        fields=[
            FieldDefinition(name="id", start=0, length=5, dtype="int"),
            FieldDefinition(name="name", start=5, length=10),
            FieldDefinition(name="value", start=15, length=8, dtype="float")
        ]
    )


@pytest.fixture
def sample_data():
    """Fixture providing sample fixed-width data"""
    return (
        "00001John      123.45\n"
        "00002Alice     234.56\n"
        "00003Bob       345.67\n"
    )


def test_layout_import(sample_layout, sample_data):
    """Test importing fixed-width data with layout"""
    importer = LayoutImporter()
    importer.register_layout("test", sample_layout)
    
    # Create temp file with sample data
    with NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(sample_data)
        temp_path = f.name
    
    try:
        # Import the file
        df = importer.import_file(temp_path, "test")
        
        # Verify data
        assert len(df) == 3
        assert list(df.columns) == ["id", "name", "value"]
        assert df.iloc[0]["id"] == 1
        assert df.iloc[0]["name"].strip() == "John"
        assert df.iloc[0]["value"] == 123.45
        
    finally:
        Path(temp_path).unlink()  # Clean up temp file


def test_invalid_layout():
    """Test error handling for invalid layout name"""
    importer = LayoutImporter()
    with pytest.raises(KeyError):
        importer.import_file("dummy.txt", "nonexistent_layout")