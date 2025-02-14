from generate_fm_pydantic import parse_fm_ddr, generate_models_from_ddr
import pytest

def test_parse_xml():
    tables = parse_fm_ddr("tests/data/inventory_test_fmp12.xml")
    assert list(tables.keys()) == ["Products", "Inventory Transactions"]
    assert tables["Products"]["Date"]["field_type"] == "datetime.date"
    assert tables["Products"]["CreationTimestamp"]["field_type"] == "str"
    assert tables["Products"]["CreationTimestamp"]["field_comment"] == "Date and time each record was created"
    print(tables)

def test_generate_code():
    models_code = generate_models_from_ddr("tests/data/inventory_test_fmp12.xml")
    with open("tests/data/inventory_test_models.py", "r") as f:
        expected_code = f.read()
    assert models_code == expected_code
