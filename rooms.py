from dataclasses import dataclass
from collections import Counter
from typing import List, Tuple


@dataclass
class Cell:
    """
    Структура, описывающая комнату (вид сверху),
    содержит признаки наличия стен (границ):
    слева, справа, сверху и снизу,
    а так же номер области, к которой принадлежит комната.
    Область - совокупность комнат, в каждую из которых
    можно попасть из другой комнаты области.
    Все комнаты в области должны иметь одинаковый номер.
    """
    l_border: bool          # Наличие левой границы
    r_border: bool          # Наличие правой границы
    u_border: bool          # Наличие верхней границы
    d_border: bool          # Наличие нижней границы
    n_array: int            # Номер области


def read_lines(grid: str) -> List[str]:
    """
    Функция формирует список линий (строк)
    плана (входного параметра).
    :param grid: План комнат в виде строки, содержащей, в том числе '\n'.
    :return: Список строк плана комнат. Строки не содержат '\n'.
    """
    return grid.splitlines()


def get_plus_indices(lines: List[str]) -> List[int]:
    """
    Функция формирует списки индексов базовых символов ('+') в строке плана.
    Во всех строках плана базовые символы стоят на одних и тех же местах.
    :param lines: Список строк плана.
    :return: Список индексов базовых элементов в каждой строке плана.
    """

    return [index for index, char in enumerate(lines[0]) if char == '+']


def get_cells(lines: List[str]) -> List[List[Cell]]:
    """
    Функция формирует и возвращает логическое представление плана комнат в виде матрицы,
    элементом которой является комната.
    Каждой комнате соответствует объект класса Cell с признаками наличия границ и номером области.
    :param lines: Список строк плана.
    :return:
    2-мерная матрица логического представления плана комнат.
    """
    plus_indices = get_plus_indices(lines)
    num_rows = len(lines) // 2 + 1          # количество строк логического представления плана
    num_cols = len(plus_indices)            # количество столбцов логического представления плана
    # Инициализация ячеек
    cells = [[Cell(False, False, False, False, 0) for _ in range(num_cols)] for _ in range(num_rows)]

    # Сканирования преобразованной входной таблицы для поиска границ (стен) комнат.
    for n_line, line in enumerate(lines):
        row_cells = n_line // 2
        for col_cells, plus_indic in enumerate(plus_indices):

            #  Для вертикальных границ (стен)
            if line[plus_indic] == '|':
                cells[row_cells][col_cells].l_border = True             # Для текущей комнаты это левая граница
                if col_cells > 0:
                    cells[row_cells][col_cells - 1].r_border = True     # Для комнаты левее, это правая граница

            #  Для горизонтальных границ (стен). На плане (вид сверху) проверяется наличие стены под комнатой.
            if plus_indic + 1 < len(line) and line[plus_indic + 1] == '-':
                cells[row_cells][col_cells].u_border = True             # Для текущей комнаты это верхняя граница
                if row_cells > 0:
                    cells[row_cells - 1][col_cells].d_border = True     # Для комнаты выше, это нижняя граница

    # Возвращаем матрицу логического плана комнат, за исключением последних строки и столбца, которые служебные
    return [row[:-1] for row in cells[:-1]]


def setting_area_numbers(cells: List[List[Cell]], row: int, col: int, num_array: int) -> None:
    """
    Функция обходит все смежные комнаты, начиная с заданной в параметре,
    и проставляет каждой комнате, заданный в параметре, номер области.
    :param cells: Логический план комнат.
    :param row: Номер строки начальной комнаты.
    :param col: Номер колонки начальной комнаты.
    :param num_array: Номер области.
    """
    # Если мы уже были в этой комнате (n_array != 0), то ничего не делаем
    if not (0 <= row < len(cells)) or not (0 <= col < len(cells[0])) or cells[row][col].n_array:
        return

    cell = cells[row][col]
    cell.n_array = num_array            # Для комнаты устанавливаем номер области

    if not cell.u_border:                                       # Если нет верней границы,
        setting_area_numbers(cells, row - 1, col, num_array)    # идём в верхнюю комнату
    if not cell.r_border:                                       # Если нет правой границы,
        setting_area_numbers(cells, row, col + 1, num_array)    # идём в правую комнату
    if not cell.d_border:                                       # Если нет нижней границы,
        setting_area_numbers(cells, row + 1, col, num_array)    # идём в нижнюю комнату
    if not cell.l_border:                                       # Если нет левой границы,
        setting_area_numbers(cells, row, col - 1, num_array)    # идём в левую комнату


def components(grid: str) -> List[Tuple[int, int]]:
    """
    Программа получает план комнат в виде строки и возвращает количество смежных областей комнат
     и количество таких областей.
    :param grid: План комнат в виде строки.
    :return: Список кортежей вида (количество смежных комнат, количество таких областей),
    отсортированный по убыванию количества комнат.
    """
    lines = read_lines(grid)                                    # Читаем строки графического плана
    cells = get_cells(lines)                                    # Строим матрицу логического плана
    num_areas = 0                                               # Начальный номер комнаты
    for row in range(len(cells)):                               # Обходим все комнаты
        for col in range(len(cells[row])):
            if cells[row][col].n_array == 0:                    # Если в комнате ещё не были,
                num_areas += 1                                  # Увеличиваем номер области
                setting_area_numbers(cells, row, col, num_areas)    # Устанавливаем номера смежным комнатам

    # Определяем и возвращаем список картежей вида (количество смежных комнат, количество областей)
    area_sizes = Counter(cell.n_array for row in cells for cell in row)
    area_counts = Counter(area_sizes.values())
    return sorted(area_counts.items(), reverse=True)


# Пример использования (ожидаемый результат [(3, 1), (2, 1), (1, 1)]):
print(components('''\
+--+--+--+
|  |     |
+  +  +--+
|  |  |  |
+--+--+--+'''))
