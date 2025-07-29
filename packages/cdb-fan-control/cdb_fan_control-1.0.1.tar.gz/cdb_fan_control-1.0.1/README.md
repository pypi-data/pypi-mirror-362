# CDB Fan Control

Simple Python package to control Coral Dev Board fan.

## Installation

### Install from PyPI

```bash
pip install cdb-fan-control
```

### Install from source

```bash
pip install .
```

## Usage

### Command Line

```bash
# Enable fan
cdb_fan_control enable

# Disable fan
cdb_fan_control disable
```

### Python

```python
from cdb_fan_control import enable_cdb_fan, disable_cdb_fan

# Enable fan
enable_cdb_fan()

# Disable fan
disable_cdb_fan()
```

## Requirements

- Python 3.7+
- Coral Dev Board
- sudo permissions
