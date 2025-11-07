"""
Tests for DuckDB query functionality
"""
import pandas as pd
import pytest

from duck_console.core.duck_engine import DuckEngine


@pytest.fixture
def engine():
    """Fixture providing a DuckDB engine instance"""
    return DuckEngine()


@pytest.fixture
def sample_df():
    """Fixture providing a sample DataFrame"""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'value': [100, 200, 300]
    })


def test_create_table_from_df(engine, sample_df):
    """Test creating a table from DataFrame"""
    info = engine.create_table_from_df('test', sample_df)
    assert info.name == 'test'
    assert info.row_count == 3
    assert 'id' in info.columns
    assert 'name' in info.columns
    assert 'value' in info.columns


def test_execute_query(engine, sample_df):
    """Test executing SQL query"""
    engine.create_table_from_df('test', sample_df)
    
    # Test SELECT
    result = engine.execute_query('SELECT * FROM test ORDER BY id')
    assert len(result) == 3
    assert list(result['name']) == ['Alice', 'Bob', 'Charlie']
    
    # Test aggregation
    result = engine.execute_query('SELECT SUM(value) as total FROM test')
    assert result.iloc[0]['total'] == 600


def test_get_table_names(engine, sample_df):
    """Test listing table names"""
    engine.create_table_from_df('test1', sample_df)
    engine.create_table_from_df('test2', sample_df)
    
    tables = engine.get_table_names()
    assert 'test1' in tables
    assert 'test2' in tables


def test_get_table_schema(engine, sample_df):
    """Test getting table schema"""
    engine.create_table_from_df('test', sample_df)
    
    schema = engine.get_table_schema('test')
    assert len(schema) == 3  # Three columns
    
    # Check column names
    column_names = list(schema['column_name'])
    assert 'id' in column_names
    assert 'name' in column_names
    assert 'value' in column_names