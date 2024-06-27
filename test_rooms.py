import pytest
from rooms import read_lines, get_plus_indices, get_cells, setting_area_numbers, components, Cell


def test_read_lines():
    grid = '''\
+--+--+--+
|  |     |
+  +  +--+
|  |  |  |
+--+--+--+'''
    expected_lines = [
        '+--+--+--+',
        '|  |     |',
        '+  +  +--+',
        '|  |  |  |',
        '+--+--+--+'
    ]
    assert read_lines(grid) == expected_lines


def test_get_plus_indices():
    lines = [
        '+--+--+--+',
        '|  |     |',
        '+  +  +--+'
    ]
    expected_base_horizont = [0, 3, 6, 9]
    assert get_plus_indices(lines) == expected_base_horizont


def test_get_cells():
    lines = [
        '+--+--+--+',
        '|  |     |',
        '+  +  +--+',
        '|  |  |  |',
        '+--+--+--+'
    ]
    cells = get_cells(lines)
    expected_borders = [
        [(True, True, True, False), (True, False, True, False), (False, True, True, True)],     # Строка 0
        [(True, True, False, True), (True, True, False, True), (True, True, True, True)],       # Строка 1
    ]
    for row in range(len(cells) - 1):
        for col in range(len(cells[row])):
            assert (cells[row][col].l_border, cells[row][col].r_border, cells[row][col].u_border,
                    cells[row][col].d_border) == expected_borders[row][col]


def test_setting_area_numbers():
    cells = [
        [Cell(False, False, False, False, 0), Cell(False, False, False, False, 0)],
        [Cell(False, False, False, False, 0), Cell(False, False, False, False, 0)]
    ]
    setting_area_numbers(cells, 0, 0, 1)
    expected_areas = [
        [1, 1],
        [1, 1]
    ]
    for row in range(len(cells)):
        for col in range(len(cells[row])):
            assert cells[row][col].n_array == expected_areas[row][col]


def test_components():
    grid = '''\
+--+--+--+
|  |     |
+  +  +--+
|  |  |  |
+--+--+--+'''
    expected_result = [(3, 1), (2, 1), (1, 1)]
    assert components(grid) == expected_result

    grid2 = '''\
+--+--+--+
|  |     |
+--+--+--+
|  |     |
+--+--+--+'''
    expected_result2 = [(2, 2), (1, 2)]
    assert components(grid2) == expected_result2


if __name__ == '__main__':
    pytest.main()
