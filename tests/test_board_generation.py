import random
import unittest

from Miinaharava import minesweeper


class TestBoardGeneration(unittest.TestCase):
    def setUp(self):
        self.random_state = random.getstate()
        random.seed(12345)

    def tearDown(self):
        random.setstate(self.random_state)

    @staticmethod
    def _count_adjacent_mines(board, row, column):
        height = len(board)
        width = len(board[0])
        mine_count = 0

        for row_offset in (-1, 0, 1):
            for column_offset in (-1, 0, 1):
                neighbor_row = row + row_offset
                neighbor_column = column + column_offset
                if (0 <= neighbor_row < height
                        and 0 <= neighbor_column < width
                        and board[neighbor_row][neighbor_column] == "*"):
                    mine_count += 1

        return mine_count

    def test_board_shape_contents_and_neighbor_counts(self):
        width = 8
        length = 6
        maxmines = 3

        board, returned_width, returned_length = minesweeper(
            width, length, maxmines
        )

        self.assertEqual(returned_width, width)
        self.assertEqual(returned_length, length)
        self.assertEqual(len(board), length)
        self.assertTrue(all(len(row) == width for row in board))

        for row in board:
            self.assertTrue(all(cell == "*" or isinstance(cell, int)
                                and 0 <= cell <= 8 for cell in row))
            self.assertGreaterEqual(row.count("*"), 1)
            self.assertLessEqual(row.count("*"), maxmines)

        for row_index, row in enumerate(board):
            for column_index, cell in enumerate(row):
                if cell != "*":
                    self.assertEqual(
                        cell,
                        self._count_adjacent_mines(
                            board, row_index, column_index
                        ),
                    )


if __name__ == "__main__":
    unittest.main()
