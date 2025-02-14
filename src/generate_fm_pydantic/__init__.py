from lxml import etree
from typing import Dict
import click

# Mapping FileMaker field types to Python types
FILEMAKER_TO_PYTHON_TYPES: Dict[str, str] = {
    "Text": "str",
    "Number": "float",
    "Date": "datetime.date",
    "Time": "datetime.time",
    "TimeStamp": "datetime.datetime",
    "Container": "bytes",
    "Binary": "bytes",
    "Calculation": "Any",
    "Summary": "Any",
}

FM_COMPLEX_FIELD_TYPES = ("Container", "Calculation", "Summary", "Binary")

PYDANTIC_IMPORTS = """from pydantic import BaseModel, Field
import datetime
from typing import Any
"""
def parse_fm_ddr(xml_file: str) -> Dict[str, Dict[str, Dict[str, str]]]:
    """Parses the FileMaker DDR XML file and extracts tables with their fields."""
    with open(xml_file, "rb") as f:
        tree = etree.parse(f)

    tables = {}

    # Find all Table elements
    for table in tree.xpath("//BaseTableCatalog/BaseTable"):
        table_name = table.attrib["name"]
        fields = {}

        # Find all Field elements within the table
        for field in table.xpath(".//FieldCatalog/Field"):
            field_name = field.attrib["name"]
            field_type = field.attrib.get("dataType", "Text")  # Default to Text
            field_comment = field.xpath(".//Comment/text()")
            field_comment = field_comment[0] if field_comment else None
            fields[field_name] = {
                "field_type": field_type,
                "field_comment": field_comment
            }

        tables[table_name] = fields

    return tables

def generate_pydantic_models(tables: Dict[str, Dict[str, Dict[str, str]]], skip_field_types: tuple = ()) -> str:
    """Generates Pydantic models as Python code."""
    models_code = PYDANTIC_IMPORTS

    for table_name, fields in tables.items():
        model_name = ''.join(word.capitalize() for word in table_name.split())
        models_code += f"\n\nclass {model_name}(BaseModel):\n"
        for field_name, field_info in fields.items():
            field_type = field_info["field_type"]
            if field_type in skip_field_types:
                continue
            field_python_type = FILEMAKER_TO_PYTHON_TYPES.get(field_type, "str")

            snake_cased_field_name = field_name.lower().replace(" ", "_")
            # Avoid conflicts with Python import names
            if snake_cased_field_name in FILEMAKER_TO_PYTHON_TYPES:
                snake_cased_field_name += f"_{snake_cased_field_name}"

            field_comment = field_info["field_comment"]
            default_value = None
            args = [default_value]
            if field_comment:
                args.append(f"description=\"{field_comment}\"")
            args_str = ", ".join(map(str, args))
            models_code += f"    {snake_cased_field_name}: {field_python_type} = Field({args_str})\n"

    return models_code

def generate_models_from_ddr(input_file, all_field_types=None):
    tables = parse_fm_ddr(input_file)
    if all_field_types:
        return generate_pydantic_models(tables)
    return generate_pydantic_models(tables, skip_field_types=FM_COMPLEX_FIELD_TYPES)

def save_models_to_file(models_code, output_file):
    """Saves the generated models to a Python file."""
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(models_code)

@click.command()
@click.option("--all-fields", is_flag=True, default=False, help="Include more complicated FM fields such as calculated and binary")
@click.argument("input_file")
@click.argument("output_file")
def main(input_file, output_file, all_fields):
    """Generate pydantic models from FileMaker Database Design Report (xml)"""
    models_code = generate_models_from_ddr(input_file, all_field_types=all_fields)
    save_models_to_file(models_code, output_file)

    print(f"Pydantic models generated at {output_file}")

if __name__ == "__main__":
    main()
