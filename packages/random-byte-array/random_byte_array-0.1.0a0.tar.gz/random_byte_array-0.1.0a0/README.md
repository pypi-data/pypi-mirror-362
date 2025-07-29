# Random Byte Array

A lightweight Python utility for generating random byte arrays.

## Features

- Simple, dependency-free implementation
- Useful for testing, simulations, and data generation
- Supports Python 2+

## Installation

```bash
pip install random-byte-array
```

## Usage

```python
from random_byte_array import random_byte_array

# Generate a random bytearray
data = random_byte_array()
# Example output: bytearray(b'\x12\xa3\x7f\x00\xe4...')
```

## How It Works

The algorithm:
1. Generates values in range `[0, 256]`
2. Appends values `0-255` as bytes
3. Stops when encountering 256 (≈0.39% chance per iteration)

Average output size: ~255 bytes (geometric distribution)

## Use Cases

- Test data for binary protocols
- Fuzz testing
- Cryptographic simulations
- Generating random binary payloads

## Contributing

Contributions are welcome! Please submit pull requests or open issues on GitHub.

## License

MIT