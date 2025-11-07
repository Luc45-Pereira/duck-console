"""
DuckDB engine core functionality
"""
from pathlib import Path
from typing import Optional, Union

import duckdb
import pandas as pd
from pydantic import BaseModel

class TableInfo(BaseModel):
    """Information about a table in DuckDB"""
    name: str
    columns: list[str]
    row_count: int

class DuckEngine:
    """Core DuckDB engine wrapper"""
    
    def __init__(self, database_path: Optional[Union[str, Path]] = None):
        """Initialize DuckDB connection
        
        Args:
            database_path: Path to DuckDB database file. If None, use in-memory database.
        """
        self.database_path = database_path
        self.conn = duckdb.connect(database=database_path)
        self.tables: dict[str, TableInfo] = {}

    def create_table_from_df(self, table_name: str, df: pd.DataFrame) -> TableInfo:
        """Create a table from a pandas DataFrame
        
        Args:
            table_name: Name for the new table
            df: Pandas DataFrame with the data
            
        Returns:
            TableInfo with details about the created table
        """
        self.conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")
        
        info = TableInfo(
            name=table_name,
            columns=list(df.columns),
            row_count=len(df)
        )
        self.tables[table_name] = info
        return info

    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute a SQL query and return results as DataFrame
        
        Args:
            query: SQL query string to execute
            
        Returns:
            Pandas DataFrame with query results
        """
        return self.conn.execute(query).fetchdf()

    def get_table_names(self) -> list[str]:
        """Get list of all tables in the database
        
        Returns:
            List of table names
        """
        tables = self.conn.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'main'
        """).fetchall()
        return [t[0] for t in tables]

    def get_table_schema(self, table_name: str) -> pd.DataFrame:
        """Get schema information for a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            DataFrame with column name, type and other schema info
        """
        return self.conn.execute(f"DESCRIBE {table_name}").fetchdf()

    def get_table_info(self, table_name: str) -> TableInfo:
        """Get information about a table
        
        Args:
            table_name: Name of the table
            
        Returns:
            TableInfo object with table details
        """
        if table_name not in self.tables:
            schema = self.get_table_schema(table_name)
            count = self.conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            self.tables[table_name] = TableInfo(
                name=table_name,
                columns=list(schema['column_name']),
                row_count=count
            )
        return self.tables[table_name]

    def close(self):
        """Close the database connection"""
        self.conn.close()