"""
Fixed-width layout file importer
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd
from pydantic import BaseModel


class FieldDefinition(BaseModel):
    """Definition of a field in a fixed-width layout"""
    name: str
    start: int
    length: int
    dtype: str = "str"


class LayoutDefinition(BaseModel):
    """Definition of a complete fixed-width file layout"""
    fields: List[FieldDefinition]
    encoding: str = "utf-8"
    skip_rows: int = 0


class LayoutImporter:
    """Handles importing of fixed-width layout files"""

    def __init__(self):
        """Initialize layout importer"""
        self.layouts: Dict[str, LayoutDefinition] = {}

    def register_layout(self, name: str, layout: LayoutDefinition) -> None:
        """Register a new layout definition
        
        Args:
            name: Name to identify this layout
            layout: Layout definition object
        """
        self.layouts[name] = layout

    def import_file(
        self,
        file_path: Union[str, Path],
        layout_name: str,
        nrows: Optional[int] = None
    ) -> pd.DataFrame:
        """Import a fixed-width file using a registered layout
        
        Args:
            file_path: Path to the fixed-width file
            layout_name: Name of the registered layout to use
            nrows: Number of rows to read (optional)
            
        Returns:
            Pandas DataFrame with the imported data
            
        Raises:
            KeyError: If layout_name is not registered
        """
        if layout_name not in self.layouts:
            raise KeyError(f"Layout '{layout_name}' not found")
            
        layout = self.layouts[layout_name]
        colspecs = [(f.start, f.start + f.length) for f in layout.fields]
        names = [f.name for f in layout.fields]
        dtypes = {f.name: f.dtype for f in layout.fields}
        
        df = pd.read_fwf(
            file_path,
            colspecs=colspecs,
            names=names,
            dtype=dtypes,
            encoding=layout.encoding,
            skiprows=layout.skip_rows,
            nrows=nrows
        )
        
        return df