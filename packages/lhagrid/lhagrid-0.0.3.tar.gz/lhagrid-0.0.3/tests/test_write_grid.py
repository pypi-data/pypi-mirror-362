import lhagrid


def test_read_grid():
    grid = lhagrid.LHAGrid.from_file("tests/test_grid.dat")
    with open("tests/test_grid.dat", encoding="utf-8") as f:
        reference = f.read()
    assert grid.to_string() == reference
