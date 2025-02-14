from generate_fm_pydantic import parse_fm_ddr


def test_parse_xml():
    tables = parse_fm_ddr("tmp/test_ddr.xml")
    assert tables == [
        ("Table1", [("Field1", "str"), ("Field2", "float")]),
        ("Table2", [("Field1", "str"), ("Field2", "date")]),
    ]