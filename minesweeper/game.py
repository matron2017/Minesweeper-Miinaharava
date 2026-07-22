"""Board generation and pure game-state logic for Minesweeper."""

from enum import Enum, auto
import random

MINE = "*"


class GameStatus(Enum):
    IN_PROGRESS = auto()
    WON = auto()
    LOST = auto()


class MinesweeperGame:
    """Manage immutable board data and the current game state."""

    def __init__(self, board):
        if not board or any(not row for row in board):
            raise ValueError("The board must contain at least one cell.")

        width = len(board[0])
        if any(len(row) != width for row in board):
            raise ValueError("The board must be rectangular.")

        self._board = tuple(tuple(row) for row in board)
        self._width = width
        self._height = len(self._board)
        self._mine_count = sum(row.count(MINE) for row in self._board)
        self._status = GameStatus.IN_PROGRESS
        self._revealed_cells = set()
        self._flagged_cells = set()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def mine_count(self):
        return self._mine_count

    @property
    def status(self):
        return self._status

    @property
    def revealed_cells(self):
        return frozenset(self._revealed_cells)

    @property
    def flagged_cells(self):
        return frozenset(self._flagged_cells)

    @property
    def remaining_mines(self):
        return self._mine_count - len(self._flagged_cells)

    def _validate_coordinates(self, row, column):
        if not (0 <= row < self._height and 0 <= column < self._width):
            raise IndexError("Board coordinates are out of bounds.")

    def cell_value(self, row, column):
        self._validate_coordinates(row, column)
        return self._board[row][column]

    def is_revealed(self, row, column):
        self._validate_coordinates(row, column)
        return (row, column) in self._revealed_cells

    def is_flagged(self, row, column):
        self._validate_coordinates(row, column)
        return (row, column) in self._flagged_cells

    def toggle_flag(self, row, column):
        self._validate_coordinates(row, column)
        coordinate = (row, column)

        if self._status is not GameStatus.IN_PROGRESS:
            return
        if coordinate in self._revealed_cells:
            return

        if coordinate in self._flagged_cells:
            self._flagged_cells.remove(coordinate)
        else:
            self._flagged_cells.add(coordinate)

    def _neighbors(self, row, column):
        for row_offset in (-1, 0, 1):
            for column_offset in (-1, 0, 1):
                if row_offset == 0 and column_offset == 0:
                    continue

                neighbor_row = row + row_offset
                neighbor_column = column + column_offset
                if 0 <= neighbor_row < self._height and 0 <= neighbor_column < self._width:
                    yield neighbor_row, neighbor_column

    def reveal(self, row, column):
        self._validate_coordinates(row, column)
        coordinate = (row, column)

        if self._status is not GameStatus.IN_PROGRESS:
            return set()
        if coordinate in self._revealed_cells:
            return set()
        if coordinate in self._flagged_cells:
            return set()

        if self._board[row][column] == MINE:
            self._revealed_cells.add(coordinate)
            self._status = GameStatus.LOST
            return {coordinate}

        newly_revealed = set()
        pending = [coordinate]

        while pending:
            current = pending.pop()
            if current in self._revealed_cells or current in self._flagged_cells:
                continue

            current_row, current_column = current
            if self._board[current_row][current_column] == MINE:
                continue

            self._revealed_cells.add(current)
            newly_revealed.add(current)

            if self._board[current_row][current_column] != 0:
                continue

            for neighbor in self._neighbors(current_row, current_column):
                if neighbor in self._revealed_cells or neighbor in self._flagged_cells:
                    continue

                neighbor_row, neighbor_column = neighbor
                if self._board[neighbor_row][neighbor_column] != MINE:
                    pending.append(neighbor)

        if len(self._revealed_cells) == self._width * self._height - self._mine_count:
            self._status = GameStatus.WON

        return newly_revealed


def generate_board(width, height, max_mines_per_row):
    """Create a Minesweeper board and return it with its dimensions."""

    if width < 1 or height < 1:
        raise ValueError("Board width and height must be at least 1.")
    if max_mines_per_row < 1 or max_mines_per_row > width:
        raise ValueError("Maximum mines per row must be between 1 and width.")

    board = []

    for row_index in range(height):
        board.append([])

        for column_index in range(width):
            board[row_index].append(0)

    for row in board:
        mines_in_row = random.randint(1, max_mines_per_row)

        for column in random.sample(range(width), mines_in_row):
            row[column] = MINE

    for row_index in range(height):
        for column_index in range(width):
            if board[row_index][column_index] == MINE:
                continue

            adjacent_mines = 0

            for row_offset in range(-1, 2, 1):
                if (row_index + row_offset < 0
                        or row_index + row_offset > height - 1):
                    continue

                for column_offset in range(-1, 2, 1):
                    if (column_index + column_offset < 0
                            or column_index + column_offset > width - 1):
                        continue

                    if (board[row_index + row_offset]
                            [column_index + column_offset] == MINE):
                        adjacent_mines += 1

            board[row_index][column_index] = adjacent_mines

    return board, width, height
