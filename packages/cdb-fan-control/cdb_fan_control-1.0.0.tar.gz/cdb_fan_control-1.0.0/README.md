# CDB Fan Control

Simple Python package to control Coral Dev Board fan.

## Installation

```bash
pip install .
```

## Usage

### Command Line

```bash
# Enable fan
sudo cdb_fan_control enable

# Disable fan
sudo cdb_fan_control disable
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
