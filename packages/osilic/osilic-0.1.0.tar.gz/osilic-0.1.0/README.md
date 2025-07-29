# osilicense: OSI License CLI & Python Package

osilicense is a Python package and command-line tool for listing, searching, and viewing details of OSI Approved Licenses® using the official OSI API.

## Features
- List all OSI Approved Licenses®
- View details for a specific license by SPDX ID
- Search licenses by name
- Automatic suggestions for similar licenses if a license is not found
- Usable as a standalone CLI or as a Python package

## Installation

### Using pip (editable mode for development)
```bash
pip install -e .
```
Or with [uv](https://github.com/astral-sh/uv):
```bash
uv pip install -e .
```

### Requirements
- Python 3.8+
- `requests` and `tabulate` Python packages

## Usage

### CLI
After installation, use the `osilic` command:

- List all licenses:
  ```bash
  osilic
  ```
- Show details for a license by SPDX ID:
  ```bash
  osilic gpl-3-0
  ```
- Search licenses by name:
  ```bash
  osilic -s gpl
  ```
- If a license is not found, the CLI will suggest similar licenses automatically.

### As a Python Package
You can also use OLC in your own Python code:
```python
from olc.model import license_from_dict, print_licenses_table, print_license_details_table
import requests

resp = requests.get("https://opensource.org/api/license")
licenses = license_from_dict(resp.json())
print_licenses_table(licenses)
```

## API Reference
- List all licenses: `https://opensource.org/api/license`
- License details: `https://opensource.org/api/license/{spdx-id}`
- Search licenses: `https://opensource.org/api/license?name={search_key}`

## Reference & Further Reading
- Official OSI API Blog Post: [Introducing the New API for OSI Approved Licenses](https://opensource.org/blog/introducing-the-new-api-for-osi-approved-licenses)
- For more information on OSI licenses, visit [opensource.org](https://opensource.org/licenses).

## Development
- Source code: [GitHub](https://github.com/dineshr93/olc)
- Issues and contributions welcome!

## License
This project is licensed under the Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0) License.

Copyright © 2025 Dinesh R

See [LICENSE](LICENSE) for details.

## Author
- Dinesh R

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for a list of all commits and changes.

---
For more information on OSI licenses, visit [opensource.org](https://opensource.org/licenses).
