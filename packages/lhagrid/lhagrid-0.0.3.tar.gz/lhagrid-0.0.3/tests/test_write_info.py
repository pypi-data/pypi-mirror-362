import lhagrid


def test_read_grid():
    grid = lhagrid.LHAInfo.from_file("tests/test_info.info")
    with open("tests/test_info.info", encoding="utf-8") as f:
        reference = f.read()
    grid.to_file("tests/test_info_out.info")
    assert grid.to_string() == reference
