# Marco Polo

A Python implementation of the classic game of Marco Polo.

## Description

This library provides a simple Python function that implements the Marco Polo game logic. When you call "Marco", it responds with "Polo"!

## Installation

Install the package using pip:

```bash
pip install juancobo6-marco-polo-timeseries
```

Or if you're using uv:

```bash
uv add juancobo6-marco-polo-timeseries
```

## Requirements

- Python 3.12 or higher
- pandas >= 2.3.1

## Usage

```python
from juancobo6_marco_polo_timeseries import marco_polo

# Basic usage
result = marco_polo("Marco", pd.Timestamp("2025-01-01 11:00:00"))
print(result)  # Output: "Polo"

# Other inputs return None
result = marco_polo("Hello", pd.Timestamp("2025-01-01 11:00:00"))
print(result)  # Output: None
```

## API Reference

### `marco_polo(name: str, time: pd.Timestamp) -> str | None`

Returns "Polo" if the name is "Marco", otherwise returns None.

**Parameters:**
- `name` (str): The name to check
- `time` (pd.Timestamp): The time to check

**Returns:**
- `str | None`: "Polo" if the name is "Marco", otherwise None

**Example:**
```python
from juancobo6_marco_polo_timeseries import marco_polo

assert marco_polo("Marco", pd.Timestamp("2025-01-01 11:00:00")) == "Polo"
assert marco_polo("Polo", pd.Timestamp("2025-01-01 11:00:00")) is None
assert marco_polo("John", pd.Timestamp("2025-01-01 11:00:00")) is None
```

## Development

This project uses:
- **Build system**: Hatchling
- **Dependencies**: pandas
- **Type hints**: Fully typed with py.typed marker

## License

This project is open source. See the license file for details.

## Author

- **JuanCobo** - juan.cobo@baobabsoluciones.es

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
