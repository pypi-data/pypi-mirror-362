import lhagrid


def test_read_grid():
    lhagrid.LHAGrid.from_file("tests/test_grid.dat")
