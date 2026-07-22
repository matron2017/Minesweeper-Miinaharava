import unittest

from minesweeper.game import GameStatus, MINE, MinesweeperGame


class TestMinesweeperGame(unittest.TestCase):
    def setUp(self):
        self.board = [
            [MINE, 1, 0],
            [1, 1, 0],
        ]

    def test_initialization_reports_board_state(self):
        game = MinesweeperGame(self.board)

        self.assertEqual(game.width, 3)
        self.assertEqual(game.height, 2)
        self.assertEqual(game.mine_count, 1)
        self.assertIs(game.status, GameStatus.IN_PROGRESS)
        self.assertEqual(game.revealed_cells, frozenset())
        self.assertEqual(game.flagged_cells, frozenset())
        self.assertEqual(game.remaining_mines, 1)

    def test_board_is_copied_at_initialization(self):
        game = MinesweeperGame(self.board)
        self.board[0][1] = MINE

        self.assertEqual(game.cell_value(0, 1), 1)

    def test_invalid_boards_raise_value_error(self):
        invalid_boards = [[], [[]], [[MINE], [1, 0]]]

        for board in invalid_boards:
            with self.subTest(board=board):
                with self.assertRaises(ValueError):
                    MinesweeperGame(board)

    def test_flagging_and_unflagging_update_flags_and_remaining_mines(self):
        game = MinesweeperGame(self.board)

        game.toggle_flag(0, 1)
        self.assertEqual(game.flagged_cells, frozenset({(0, 1)}))
        self.assertEqual(game.remaining_mines, 0)

        game.toggle_flag(0, 1)
        self.assertEqual(game.flagged_cells, frozenset())
        self.assertEqual(game.remaining_mines, 1)

    def test_flagged_cell_cannot_be_revealed(self):
        game = MinesweeperGame(self.board)
        game.toggle_flag(0, 1)

        self.assertEqual(game.reveal(0, 1), set())
        self.assertEqual(game.revealed_cells, frozenset())
        self.assertIs(game.status, GameStatus.IN_PROGRESS)

    def test_revealed_cell_cannot_be_flagged(self):
        game = MinesweeperGame(self.board)
        game.reveal(0, 1)

        game.toggle_flag(0, 1)

        self.assertEqual(game.flagged_cells, frozenset())

    def test_revealing_safe_numbered_cell_reveals_only_that_cell(self):
        game = MinesweeperGame(self.board)

        self.assertEqual(game.reveal(0, 1), {(0, 1)})
        self.assertEqual(game.revealed_cells, frozenset({(0, 1)}))
        self.assertIs(game.status, GameStatus.IN_PROGRESS)
        self.assertEqual(game.cell_value(0, 1), 1)

    def test_revealing_same_cell_twice_returns_empty_set(self):
        game = MinesweeperGame(self.board)
        game.reveal(0, 1)

        self.assertEqual(game.reveal(0, 1), set())

    def test_revealing_mine_loses_the_game(self):
        game = MinesweeperGame(self.board)

        self.assertEqual(game.reveal(0, 0), {(0, 0)})
        self.assertIs(game.status, GameStatus.LOST)

    def test_revealing_every_safe_cell_wins_the_game(self):
        game = MinesweeperGame([[MINE, 1]])

        game.reveal(0, 1)

        self.assertIs(game.status, GameStatus.WON)

    def test_operations_do_nothing_after_game_is_won_or_lost(self):
        won_game = MinesweeperGame([[MINE, 1]])
        won_game.reveal(0, 1)

        self.assertEqual(won_game.reveal(0, 0), set())
        won_game.toggle_flag(0, 0)
        self.assertEqual(won_game.flagged_cells, frozenset())

        lost_game = MinesweeperGame([[MINE, 1]])
        lost_game.reveal(0, 0)

        self.assertEqual(lost_game.reveal(0, 1), set())
        lost_game.toggle_flag(0, 1)
        self.assertEqual(lost_game.flagged_cells, frozenset())

    def test_coordinate_methods_reject_out_of_bounds_positions(self):
        game = MinesweeperGame(self.board)
        methods = (
            game.cell_value,
            game.is_revealed,
            game.is_flagged,
            game.toggle_flag,
            game.reveal,
        )

        for method in methods:
            with self.subTest(method=method):
                with self.assertRaises(IndexError):
                    method(2, 0)


if __name__ == "__main__":
    unittest.main()
