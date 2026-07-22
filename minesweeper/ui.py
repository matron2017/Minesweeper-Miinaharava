"""Tkinter user interface for Minesweeper."""

import tkinter as tk
from minesweeper.game import (
    GameStatus,
    MINE,
    MinesweeperGame,
    generate_board,
)


def restart():
    setup_dialog = GameSetupDialog()
    try:
        width, height, max_mines_per_row = setup_dialog.start()
    except tk.TclError:
        return
    board, width, height = generate_board(
        int(width), int(height), int(max_mines_per_row)
    )
    setup_dialog.destroy()
    game = MinesweeperGame(board)
    game_ui = MinesweeperUI(game)
    game_ui.start()


class GameSetupDialog:
    """Collect and validate the board settings entered by the player."""

    def __init__(self):
        self._root = tk.Tk()
        self._root.title("Minesweeper")
        self._width = tk.Entry(self._root)
        self._width_label = tk.Label(text="Board width")
        self._width.grid(row=0, column=2)
        self._width_label.grid(row=0, column=0)
        self._height = tk.Entry(self._root)
        self._height_label = tk.Label(text="Board height")
        self._height_label.grid(row=2, column=0)
        self._height.grid(row=2, column=2)
        self._max_mines_entry = tk.Entry(self._root)
        self._max_mines_label = tk.Label(text="Maximum mines per row")
        self._max_mines_entry.grid(row=4, column=2)
        self._max_mines_label.grid(row=4, column=0)
        self._start_button = tk.Button(
            text="Start game", command=self.validate_inputs
        )
        self._start_button.grid(row=7, column=2)
        self._integer_label = tk.Label(text="Enter all values as integers.")
        self._integer_label.grid(row=7, column=0)

    def start(self):
        self._root.mainloop()
        return self._width.get(), self._height.get(), self._max_mines_entry.get()

    def stop(self):
        self._root.quit()

    def destroy(self):
        self._root.destroy()

    def validate_inputs(self):
        error_message = (
            "Board width and height must be between 1 and 30. "
            "Maximum mines per row must be between 1 and the board width."
        )

        try:
            width = int(self._width.get())
            height = int(self._height.get())
            max_mines_per_row = int(self._max_mines_entry.get())
        except ValueError:
            self._warning_label = tk.Label(text=error_message)
            self._warning_label.grid(row=9, column=0)
            return

        if (
            1 <= width <= 30
            and 1 <= height <= 30
            and 1 <= max_mines_per_row <= width
        ):
            self.stop()
        else:
            self._warning_label = tk.Label(text=error_message)
            self._warning_label.grid(row=9, column=0)


class MinesweeperUI:
    """Display the board and handle player interaction."""

    def __init__(self, game):
        self._game = game
        self._cell_buttons = []
        self._width = game.width
        self._height = game.height
        self._root = tk.Tk()
        self._root.title("Minesweeper")
        self._grid_frame = tk.Frame(self._root)
        self._control_frame = tk.Frame(self._root)
        self._mine_count_label = tk.Label(
            self._control_frame, text="Mines: {}".format(game.mine_count)
        )
        self._mine_count_label.grid(row=0, column=0)
        self._exit_button = tk.Button(self._control_frame, text="Exit", command=exit)
        self._exit_button.grid(row=0, column=5)
        for row in range(self._height):
            self._grid_frame.rowconfigure(row, weight=1)
            self._cell_buttons.append([])
            for column in range(self._width):
                cell_button = tk.Button(self._grid_frame, text="      ")
                cell_button.grid(row=row, column=column)
                # Bind coordinates as defaults so each button keeps its own position.
                cell_button.config(
                    command=lambda column=column, row=row: self.reveal(row, column)
                )
                cell_button.bind(
                    "<Button-3>",
                    lambda event, column=column, row=row: self.toggle_flag(
                        row, column
                    ),
                )
                self._cell_buttons[row].append(cell_button)
        self._grid_frame.grid(row=1, sticky=tk.EW)
        self._control_frame.grid(row=0)
        self._flags_label = tk.Label(
            self._control_frame,
            text="Flags: {}".format(len(self._game.flagged_cells)),
        )
        self._flags_label.grid(row=0, column=7)
        restart_button = tk.Button(self._control_frame, text="Restart", command=self.restart)
        restart_button.grid(row=0, column=2)
        self._restart_button = restart_button

    def toggle_flag(self, row, column):
        self._game.toggle_flag(row, column)

        if self._game.is_flagged(row, column):
            self._cell_buttons[row][column].config(background="red")
        else:
            self._cell_buttons[row][column].config(
                background=self._root.cget("background")
            )

        self._flags_label.config(
            text="Flags: {}".format(len(self._game.flagged_cells))
        )

    def stop(self):
        self._root.destroy()

    def show_all_mines(self):
        for row in range(self._height):
            for column in range(self._width):
                if self._game.cell_value(row, column) == MINE:
                    self._cell_buttons[row][column].config(
                        text="  {}  ".format(MINE)
                    )

    def show_win(self):
        self.show_all_mines()
        self._exit_button.destroy()
        self._restart_button.destroy()
        self._flags_label.destroy()
        self._mine_count_label.destroy()
        win_button = tk.Button(
            self._control_frame,
            text="You revealed every safe cell. Play again?",
            command=self.restart,
        )
        win_button.grid(row=0, column=3)
        quit_button = tk.Button(
            self._control_frame, text="Quit playing?", command=self.stop
        )
        quit_button.grid(row=0, column=7)
        for row in self._cell_buttons:
            for button in row:
                button.configure(state='disable')

    def show_loss(self):
        self.show_all_mines()
        self._exit_button.destroy()
        self._restart_button.destroy()
        self._flags_label.destroy()
        self._mine_count_label.destroy()

        loss_button = tk.Button(
            self._control_frame,
            text="BOOM! You stepped into a mine. Restart game?",
            command=self.restart,
        )
        quit_button = tk.Button(
            self._control_frame, text="Quit playing?", command=self.stop
        )
        quit_button.grid(row=0, column=7)
        loss_button.grid(row=0, column=3)

        for row in self._cell_buttons:
            for button in row:
                button.configure(state="disable")

    def reveal(self, row, column):
        newly_revealed = self._game.reveal(row, column)

        for revealed_row, revealed_column in newly_revealed:
            cell_value = self._game.cell_value(revealed_row, revealed_column)
            self._cell_buttons[revealed_row][revealed_column].config(
                text="  {}  ".format(cell_value), state="disabled"
            )

        if not newly_revealed:
            return

        if self._game.status is GameStatus.LOST:
            self.show_loss()
        elif self._game.status is GameStatus.WON:
            self.show_win()

    def start(self):
        self._root.mainloop()

    def restart(self):
        self._root.destroy()
        restart()


def main():
    setup_dialog = GameSetupDialog()
    try:
        width, height, max_mines_per_row = setup_dialog.start()
    except tk.TclError:
        return
    setup_dialog.destroy()
    board, width, height = generate_board(
        int(width), int(height), int(max_mines_per_row)
    )
    game = MinesweeperGame(board)
    game_ui = MinesweeperUI(game)
    game_ui.start()
