# Minesweeper

A desktop Minesweeper game written in Python using Tkinter. Players can choose
the board dimensions and the maximum number of mines generated in each row.

## Features

- Configurable board width and height
- Configurable maximum number of mines per row
- Unique randomly selected mine positions within each row
- Adjacent-mine counts in all eight directions
- Left-click cell revealing
- Right-click flagging and unflagging
- Iterative empty-area revealing without recursive flood fill
- Win and loss detection
- Restart and exit controls
- Game rules separated from the Tkinter interface
- Automated tests using Python's standard `unittest` framework

## Requirements

- Python 3
- Tkinter

The application otherwise uses only the Python standard library.

You can verify that Tkinter is available by running:

```bash
python3 -m tkinter
```

This should open a small Tkinter demonstration window. On some Linux
distributions, Tkinter is provided as a separate operating-system package.

## Run the game

From the repository root, run:

```bash
python3 -m minesweeper
```

Enter the following settings in the setup window:

- **Board width:** number of columns
- **Board height:** number of rows
- **Maximum mines per row:** upper limit for mines generated in each row

The width and height must be between 1 and 30. The maximum mines per row must
be between 1 and the selected board width.

## Controls

- **Left click:** reveal a cell
- **Right click:** place or remove a flag
- **Restart:** close the current board and configure a new game
- **Exit:** close the application

Revealing an empty cell also reveals its connected empty area and the numbered
cells surrounding that area.

## How board generation works

Each row receives a random number of mines between one and the configured
maximum. Mine columns are selected without replacement, so one cell cannot
receive more than one mine.

After placing the mines, the generator calculates the value of every safe
cell by counting mines in its eight neighboring positions.

Because the setting is a maximum per row rather than an exact total, the
number of mines can differ between games.

## Project structure

```text
.
├── minesweeper/
│   ├── __init__.py
│   ├── __main__.py
│   ├── game.py
│   └── ui.py
├── tests/
│   ├── test_board_generation.py
│   ├── test_game_state.py
│   └── test_ui_integration.py
├── .gitignore
└── README.md
```

### `minesweeper/game.py`

Contains board generation and the `MinesweeperGame` state model. The model
tracks revealed cells, flags, mine count, and whether the game is in progress,
won, or lost. It does not depend on Tkinter.

### `minesweeper/ui.py`

Contains the Tkinter setup dialog and game interface. It translates player
input into operations on `MinesweeperGame` and renders the resulting state.

### `minesweeper/__main__.py`

Provides the package entry point used by:

```bash
python3 -m minesweeper
```

### `tests/`

Contains regression tests for board generation, game-state transitions,
flagging, mine detection, win detection, iterative empty-area revealing, and
the connection between the interface and game state.

## Run the tests

From the repository root, run:

```bash
python3 -m unittest discover -s tests -v
```

The test suite does not require starting the complete graphical application.
