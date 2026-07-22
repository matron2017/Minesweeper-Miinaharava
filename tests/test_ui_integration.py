import unittest
from unittest.mock import Mock

from minesweeper.game import GameStatus, MINE, MinesweeperGame
from minesweeper.ui import MinesweeperUI


class FakeButton:
    def __init__(self):
        self.options = {"background": "white"}

    def config(self, **options):
        self.options.update(options)

    configure = config

    def cget(self, option):
        return self.options[option]

    def destroy(self):
        self.options["destroyed"] = True


class FakeLabel(FakeButton):
    pass


class FakeRoot:
    def cget(self, option):
        if option == "background":
            return "white"
        raise KeyError(option)

    def destroy(self):
        pass


def make_ui(game):
    ui = MinesweeperUI.__new__(MinesweeperUI)
    ui._game = game
    ui._width = game.width
    ui._height = game.height
    ui._cell_buttons = [
        [FakeButton() for _ in range(game.width)]
        for _ in range(game.height)
    ]
    ui._root = FakeRoot()
    ui._control_frame = object()
    ui._mine_count_label = FakeLabel()
    ui._flags_label = FakeLabel()
    ui._exit_button = FakeButton()
    ui._restart_button = FakeButton()
    return ui


class TestMinesweeperUIIntegration(unittest.TestCase):
    def test_reveal_delegates_and_renders_all_returned_cells(self):
        game = Mock()
        game.width = 2
        game.height = 2
        game.reveal.return_value = {(0, 0), (1, 0)}
        game.status = GameStatus.IN_PROGRESS
        game.cell_value.side_effect = lambda row, column: row + column
        ui = make_ui(game)

        ui.reveal(0, 0)

        game.reveal.assert_called_once_with(0, 0)
        self.assertEqual(
            ui._cell_buttons[0][0].options,
            {"background": "white", "text": "  0  ", "state": "disabled"},
        )
        self.assertEqual(
            ui._cell_buttons[1][0].options,
            {"background": "white", "text": "  1  ", "state": "disabled"},
        )
        self.assertNotIn("state", ui._cell_buttons[0][1].options)
        self.assertEqual(game.cell_value.call_count, 2)

    def test_reveal_uses_values_from_the_game_and_does_not_mutate_board(self):
        board = [[0, 1], [1, MINE]]
        game = MinesweeperGame(board)
        ui = make_ui(game)
        ui.show_win = Mock()

        ui.reveal(0, 0)

        self.assertEqual(board, [[0, 1], [1, MINE]])
        self.assertEqual(game.cell_value(0, 0), 0)
        self.assertEqual(game.cell_value(0, 1), 1)
        self.assertEqual(game.cell_value(1, 0), 1)

    def test_toggle_flag_updates_game_and_flag_label(self):
        game = MinesweeperGame([[MINE, 1]])
        ui = make_ui(game)

        ui.toggle_flag(0, 1)

        self.assertEqual(game.flagged_cells, frozenset({(0, 1)}))
        self.assertEqual(ui._cell_buttons[0][1].cget("background"), "red")
        self.assertEqual(ui._flags_label.cget("text"), "Flags: 1")

    def test_unflagging_restores_unflagged_visual_state(self):
        game = MinesweeperGame([[MINE, 1]])
        ui = make_ui(game)
        ui.toggle_flag(0, 1)

        ui.toggle_flag(0, 1)

        self.assertEqual(game.flagged_cells, frozenset())
        self.assertEqual(ui._cell_buttons[0][1].cget("background"), "white")
        self.assertEqual(ui._flags_label.cget("text"), "Flags: 0")

    def test_flagged_reveal_does_not_render_the_cell(self):
        game = MinesweeperGame([[MINE]])
        game.toggle_flag(0, 0)
        ui = make_ui(game)

        ui.reveal(0, 0)

        self.assertNotIn("text", ui._cell_buttons[0][0].options)

    def test_terminal_status_selects_loss_or_win_display(self):
        for status, method_name in (
            (GameStatus.LOST, "show_loss"),
            (GameStatus.WON, "show_win"),
        ):
            with self.subTest(status=status):
                game = Mock()
                game.width = 1
                game.height = 1
                game.reveal.return_value = {(0, 0)}
                game.status = status
                game.cell_value.return_value = 1
                ui = make_ui(game)
                ui.show_loss = Mock()
                ui.show_win = Mock()

                ui.reveal(0, 0)

                getattr(ui, method_name).assert_called_once_with()

    def test_show_all_mines_uses_game_values(self):
        game = Mock()
        game.width = 2
        game.height = 1
        game.cell_value.side_effect = [MINE, 1]
        ui = make_ui(game)

        ui.show_all_mines()

        self.assertEqual(ui._cell_buttons[0][0].cget("text"), "  *  ")
        self.assertNotIn("text", ui._cell_buttons[0][1].options)
        self.assertEqual(game.cell_value.call_count, 2)


if __name__ == "__main__":
    unittest.main()
