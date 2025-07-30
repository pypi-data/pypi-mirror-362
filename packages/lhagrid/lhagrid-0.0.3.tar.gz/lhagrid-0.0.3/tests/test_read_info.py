import lhagrid


def test_read_grid():
    lhagrid.LHAInfo.from_file("tests/test_info.info")
