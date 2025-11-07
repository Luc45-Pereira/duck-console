# Duck Console 🦆

[![PyPI version](https://badge.fury.io/py/duck-console.svg)](https://badge.fury.io/py/duck-console)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

An interactive web-based SQL console powered by DuckDB. Import data from CSV and fixed-width files, run SQL queries, and analyze results with ease.

## Features

- 🚀 Web-based SQL console using Streamlit
- 📊 Import CSV and fixed-width files
- 💾 Create temporary named tables
- 📝 Execute SQL queries with DuckDB
- 📈 View and export results
- 🎯 Support for custom file layouts

## Installation

Install using pip:

```bash
pip install duck-console
```

## Usage

### Web Console

Start the web interface:

```bash
duck-console web
```

This will open a browser window with the interactive console.

### Python API

```python
from duck_console.core.duck_engine import DuckEngine
from duck_console.core.layout_importer import LayoutImporter

# Initialize engine
engine = DuckEngine()

# Import CSV
import pandas as pd
df = pd.read_csv("data.csv")
engine.create_table_from_df("my_table", df)

# Run query
result = engine.execute_query("""
    SELECT column1, COUNT(*) as count
    FROM my_table
    GROUP BY column1
    ORDER BY count DESC
""")

print(result)
```

### Fixed-width Files

```python
from duck_console.core.layout_importer import FieldDefinition, LayoutDefinition

# Define layout
layout = LayoutDefinition(
    fields=[
        FieldDefinition(name="date", start=0, length=8),
        FieldDefinition(name="value", start=8, length=10, dtype="float")
    ]
)

# Import data
importer = LayoutImporter()
importer.register_layout("my_layout", layout)
df = importer.import_file("data.txt", "my_layout")
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/Luc45-Pereira/duck-console.git
cd duck-console
```

2. Install dependencies:
```bash
poetry install
```

3. Run tests:
```bash
poetry run pytest
```

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) first.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## Roadmap

- [ ] FastAPI backend option
- [ ] S3/cloud storage integration
- [ ] Plugin system for custom importers
- [ ] Interactive data visualization
- [ ] Dashboard creation
- [ ] Query history and favorites

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
