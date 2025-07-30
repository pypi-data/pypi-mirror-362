# phenosentry

A Python package for ensuring data quality in phenopackets and collections of phenopackets.

## Features
- Validate phenopacket with quality checks

## Installation

Install with [Poetry](https://python-poetry.org/):

```bash
poetry add phenosentry
```
or with pip:

```bash
pip install phenosentry
```

# Usage
command line interface (CLI):
```bash
phenosentry validate
```

or in Python code:

```python
from phenosentry.model import AuditorLevel
from phenosentry.validation import get_phenopacket_auditor
from phenosentry.io import read_phenopacket
from pathlib import Path
import logging
# Single Phenopacket Validation
path = "path/to/phenopacket.json"
logger = logging.getLogger("phenosentry")
phenopacket = read_phenopacket(
        directory=Path(path),
        logger=logger
)
# Strict Validation
auditor = get_phenopacket_auditor(AuditorLevel.STRICT)
notepad = auditor.prepare_notepad(auditor.id())
auditor.audit(
    item=phenopacket,
    notepad=notepad,
)
if notepad.has_errors_or_warnings(include_subsections=True):
    return "Not Valid Phenopacket"
else:
    return "Valid Phenopacket"
```

# Development
Run tests with:

```bash
poetry run pytest
```

Run lint with:
```bash
poetry run ruff check phenosentry
```

# License 
MIT License