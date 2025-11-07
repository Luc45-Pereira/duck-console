"""
Example demonstrating fixed-width layout import
"""
import pandas as pd
from duck_console.core.duck_engine import DuckEngine
from duck_console.core.layout_importer import FieldDefinition, LayoutDefinition, LayoutImporter

# Define a layout for a hypothetical fixed-width transaction file
TRANSACTION_LAYOUT = LayoutDefinition(
    fields=[
        FieldDefinition(name="date", start=0, length=8),
        FieldDefinition(name="account", start=8, length=10),
        FieldDefinition(name="transaction_type", start=18, length=3),
        FieldDefinition(name="amount", start=21, length=10, dtype="float"),
        FieldDefinition(name="description", start=31, length=30),
    ],
    encoding="utf-8",
    skip_rows=1  # Skip header row
)

def main():
    # Initialize components
    importer = LayoutImporter()
    engine = DuckEngine()
    
    # Register the layout
    importer.register_layout("transaction", TRANSACTION_LAYOUT)
    
    # Import sample file
    print("Importing transactions.txt...")
    df = importer.import_file("transactions.txt", "transaction")
    print(f"Imported {len(df)} rows")
    
    # Load into DuckDB
    print("\nCreating DuckDB table...")
    info = engine.create_table_from_df("transactions", df)
    print(f"Created table '{info.name}' with {info.row_count:,} rows")
    
    # Run a sample query
    print("\nRunning sample query...")
    result = engine.execute_query("""
        SELECT transaction_type,
               COUNT(*) as count,
               SUM(amount) as total_amount
        FROM transactions
        GROUP BY transaction_type
        ORDER BY total_amount DESC
    """)
    
    print("\nTransaction Summary:")
    print(result.to_string(index=False))

if __name__ == "__main__":
    main()