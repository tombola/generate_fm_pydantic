import argparse
from lxml import etree
from typing import Dict

# Mapping FileMaker field types to Python types
FILEMAKER_TO_PYTHON_TYPES: Dict[str, str] = {
    "Text": "str",
    "Number": "float",
    "Date": "date",
    "Time": "time",
    "Timestamp": "datetime",
    "Container": "bytes",
    "Calculation": "Any",
    "Summary": "Any",
}

PYDANTIC_IMPORTS = """from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Any
"""

def parse_fm_ddr(xml_file: str) -> list[list[str, str, str]]:
    """Parses the FileMaker DDR XML file and extracts tables with their fields."""
    with open(xml_file, "rb") as f:
        tree = etree.parse(f)

    tables = []

    # Find all Table elements
    for table in tree.xpath("//BaseTableCatalog/BaseTable"):
        table_name = table.attrib["name"]
        fields = []

        # Find all Field elements within the table
        for field in table.xpath(".//FieldCatalog/Field"):
            field_name = field.attrib["name"]
            field_type = field.attrib.get("dataType", "Text")  # Default to Text
            field_comment = field.xpath(".//Comment/text()")
            field_comment = field_comment[0] if field_comment else None
            python_type = FILEMAKER_TO_PYTHON_TYPES.get(field_type, "str")
            fields.append([field_name, python_type, field_comment])

        tables.append([table_name, fields])

    return tables

def generate_pydantic_models(tables):
    """Generates Pydantic models as Python code."""
    models_code = PYDANTIC_IMPORTS

    for table_name, fields in tables:
        model_name = table_name.capitalize()
        models_code += f"\n\nclass {model_name}(BaseModel):\n"
        for field_name, field_type, field_comment in fields:
            snake_cased_field_name = field_name.lower().replace(" ", "_")

            default_value=None
            args = [default_value]
            if field_comment:
                args.append(f"description=\"{field_comment}\"")
            args_str = ", ".join(map(str, args))
            models_code += f"    {snake_cased_field_name}: {field_type} = Field({args_str})\n"

    return models_code

def save_models_to_file(models_code, output_file):
    """Saves the generated models to a Python file."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(models_code)

def main():
    parser = argparse.ArgumentParser(description="Generate pydantic models from FileMaker Database Design Report (xml)")
    parser.add_argument("input_file", help="FileMaker DDR XML file")
    parser.add_argument("output_file", help="Destination path for generated Pydantic models file")

    args = parser.parse_args()

    tables = parse_fm_ddr(args.input_file)
    models_code = generate_pydantic_models(tables)
    save_models_to_file(models_code, args.output_file)

    print(f"Pydantic models generated at {args.output_file}")

if __name__ == "__main__":
    main()
