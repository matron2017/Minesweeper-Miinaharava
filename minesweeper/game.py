"""Board-generation logic for Minesweeper."""

import random


def generate_board(width, length, maxmines):
    """Create a Minesweeper board and return it with its dimensions."""

    board = []
    minmines = 1


    totalmines = 0

    # Create the board, with length rows and width cells per row.

    for i in range(length):

        board.append([])

        for j in range(width):

            board[i].append(0)

    # Determine the number of mines and place them on the board.

    #

    for row in board:

        minesperline = random.randint(minmines, maxmines)

        totalmines += minesperline

        for i in range (0, minesperline):

            index = random.randint(0, width-1)

            if "*" != row[index]:

                row[index] = "*"

                minesperline -= 1

            if minesperline == 0:

                break

    # Count the mines around each non-mine cell.

    for y in range(0, length):

        for x in range(0, width):

            if board[y][x] == "*":

                continue

            else:

                minesaround = 0

                for j in range(-1,2,1):

                    if y+j < 0 or y+j > length-1:

                        continue

                    else:

                        for i in range(-1, 2, 1):

                            if x+i < 0 or x+i > width-1:

                                continue

                            else:

                                if board[y+j][x+i] == "*":

                                     minesaround += 1

                board[y][x] = minesaround

    return board, width, length
