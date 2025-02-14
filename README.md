# Generate Filemaker Pydantic models

Provides a command to parse a FileMaker Database Design Report (DDR) XML file
and generate Pydantic models from it.

## Usage

`generate_fm_pydantic INPUT_FILE.xml OUTPUT_FILE.py`

### Options

`--all-fields` Include more complicated FM fields such as calculated and binary.

These are skipped by default, search constant `FM_COMPLEX_FIELD_TYPES`.