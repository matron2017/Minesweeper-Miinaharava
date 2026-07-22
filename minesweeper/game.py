"""Board-generation logic for Minesweeper."""

import random


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
            row[column] = "*"

    for row_index in range(height):
        for column_index in range(width):
            if board[row_index][column_index] == "*":
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
                            [column_index + column_offset] == "*"):
                        adjacent_mines += 1

            board[row_index][column_index] = adjacent_mines

    return board, width, height
