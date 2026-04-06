"""
Homework: Reading Code with State / Transitions / Invariants (Tic-Tac-Toe)

This program brute-forces tic-tac-toe WITHOUT recursion.

What it actually counts:
- It explores all possible games where X starts and players alternate.
- The search STOPS as soon as someone wins (a terminal state).
- It also records full boards that end in a tie.
- It tracks UNIQUE *terminal* boards "up to symmetry" (rotations + reflections),
  meaning rotated/flipped versions are treated as the same terminal board.

YOUR TASKS:

RULE:  Do not change any executable code (no reformatting logic, no renaming variables, no moving lines). 
       Only add/replace comments and docstrings.
       
1) Define STATE for this program.
   - What variables change as the program runs?

   The state of the program is made up of these variables:
   - board: the current 9-cell tic-tac-toe board, updated with each move and undone after
   - unique_seen: the list of unique terminal boards seen so far in standard form
   - full_boards: running count of fully filled boards reached
   - x_wins_on_full_board: running count of full boards where X won
   - draws_on_full_board: running count of full boards that were draws
   - x_wins, o_wins, ties: counts of unique terminal boards by outcome

2) Explain where TRANSITIONS happen.
   - Where does the state change? (where in the code, which functions)

   Transitions happen in two main places:
   - In the nested for loops: each loop places a piece on the board (board[x1] = 'X', board[o1] = 'O', etc.)
     and then undoes it after exploring that branch (board[x1] = ' '). These are forward and backward transitions
     through game states.
   - In record_unique_board() and record_full_board(): these functions update the global counters
     (x_wins, o_wins, ties, full_boards, etc.) when a terminal state is reached. That is where
     the counting state transitions happen.

3) Identify 4 INVARIANTS.

   Invariant 1: The board always has exactly as many X's as O's, or one more X than O's,
   since X always goes first and players alternate. This is enforced by the alternating loop structure.

   Invariant 2: We never continue exploring past a winning board. should_continue() checks
   has_winner() before allowing deeper loops to run, so no moves are placed after a win.

   Invariant 3: unique_seen only ever contains standard forms of terminal boards (wins or ties).
   record_unique_board() is only ever called from should_continue() (on a win) or record_full_board()
   (on a full board), never mid-game.

   Invariant 4: Every board stored in unique_seen is the minimum across all its rotations and
   reflections. standard_form() always returns the same representative no matter which orientation
   the board was in when it was recorded, so duplicates are never added.

4) Function docstrings -- see below in the code

5) Inline comments -- see below in the code

6) Non-obvious explanation (chosen: why we undo moves):

   The program uses a single shared list called board to represent the current game state. Instead
   of making a copy of the board for every possible move, it places a piece, explores all games
   that follow from that move, and then removes the piece to restore the board to its previous state.
   This is called backtracking. It works because the nested loops go one level deeper each time,
   and when the inner loop finishes, the outer loop needs the board back in the state it was before
   that move was made. If we did not undo moves, the board would accumulate pieces from previous
   branches and the results would be wrong. The undo step is what makes it safe to reuse a single
   board variable across the entire search instead of creating thousands of copies.

7) Output explanation:
   The two print statements produce:
       127872
       138 81792 46080 91 44 3

   - 127872: the total number of fully filled boards (all 9 squares filled) found across all game paths.
   - 138: the total number of unique terminal boards when rotations and reflections are removed.
   - 81792: the number of full boards where X won (X placed the 9th move).
   - 46080: the number of full boards that were draws (no winner on a full board).
   - 91: the number of unique terminal boards (up to symmetry) where X won.
   - 44: the number of unique terminal boards (up to symmetry) where O won.
   - 3: the number of unique terminal boards (up to symmetry) that were ties/draws.

"""

# ----------------------------
# Global running totals (STATE)
# ----------------------------

unique_seen = []             # Stores the standard form of every unique terminal board seen so far.
                             # We store standard forms so that rotationally equivalent boards are
                             # treated as the same board and not double counted.

board = [' '] * 9            # Represents the current tic-tac-toe board as a flat list of 9 cells.
                             # We undo moves after exploring each branch so the same list can be
                             # reused across all game paths without making copies.

full_boards = 0              # Counts every fully filled board (all 9 moves made) reached during the search.
x_wins_on_full_board = 0     # Counts full boards where X has won (X makes the last move so X can win on move 9).
draws_on_full_board = 0      # Counts full boards where neither player has won (a draw).

x_wins = 0                   # Counts unique terminal boards (up to symmetry) where X won.
o_wins = 0                   # Counts unique terminal boards (up to symmetry) where O won.
ties = 0                     # Counts unique terminal boards (up to symmetry) that ended in a draw.


# ----------------------------
# Board representation helpers
# ----------------------------

def to_grid(flat_board: list[str]) -> list[list[str]]:
    """Converts the flat 9-element board list into a 3x3 grid (list of lists).
    Each row is built by taking three consecutive elements from the flat list.
    This makes it easier to apply rotations and reflections."""
    grid = []
    for row in range(3):
        row_vals = []
        for col in range(3):
            row_vals.append(flat_board[row * 3 + col])
        grid.append(row_vals)
    return grid


def rotate_clockwise(grid: list[list[str]]) -> list[list[str]]:
    """Returns a new 3x3 grid that is the input grid rotated 90 degrees clockwise.
    This is used to generate all four rotational variants of a board when computing
    its standard form."""
    rotated = [[' '] * 3 for _ in range(3)]
    for r in range(3):
        for c in range(3):
            rotated[c][2 - r] = grid[r][c]
    return rotated


def flip_vertical(grid: list[list[str]]) -> list[list[str]]:
    """Returns a new 3x3 grid that is the input grid flipped vertically (top row becomes bottom row).
    Combined with rotations, this generates the reflected variants of a board."""
    return [grid[2], grid[1], grid[0]]


def standard_form(flat_board: list[str]) -> list[list[str]]:
    """Returns a canonical representation of a board by generating all 8 symmetrical variants
    (4 rotations and their vertical flips) and returning the minimum one.
    This ensures that two boards that are rotations or reflections of each other
    always map to the same standard form."""
    grid = to_grid(flat_board)
    flipped = flip_vertical(grid)

    variants = []
    for _ in range(4):
        variants.append(grid)
        variants.append(flipped)
        grid = rotate_clockwise(grid)
        flipped = rotate_clockwise(flipped)

    return min(variants)


def record_unique_board(flat_board: list[str]) -> None:
    """Records a terminal board if it has not been seen before (up to symmetry).
    It computes the standard form of the board and checks whether it is already in unique_seen.
    If it is new, it appends it and increments the appropriate win/loss/tie counter."""
    global x_wins, o_wins, ties

    rep = standard_form(flat_board)

    # We check rep not in unique_seen to avoid counting rotationally equivalent boards more than once.
    # Two boards that are rotations or reflections of each other will have the same standard form.
    if rep not in unique_seen:
        unique_seen.append(rep)

        # Once we know the board is unique, we check who won and increment the right counter.
        winner = who_won(flat_board)
        if winner == 'X':
            x_wins += 1
        elif winner == 'O':
            o_wins += 1
        else:
            ties += 1


# ----------------------------
# Game logic
# ----------------------------

def has_winner(flat_board: list[str]) -> bool:
    """Returns True if either X or O has won the game on the given board.
    It checks all 8 possible winning lines (3 rows, 3 columns, 2 diagonals)
    using a scoring system where X scores +10 and O scores -10 per cell.
    A score of 30 means X won that line, -30 means O won."""
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [6, 4, 2],             # diagonals
    ]

    for line in winning_lines:
        score = 0
        for idx in line:
            if flat_board[idx] == 'X':
                score += 10
            elif flat_board[idx] == 'O':
                score -= 10
        if abs(score) == 30:
            return True

    return False


def who_won(flat_board: list[str]) -> str:
    """Returns 'X' if X has won, 'O' if O has won, or 'TIE' if neither has won.
    Uses the same scoring logic as has_winner() but distinguishes between the two players
    by checking whether the line score is +30 (X) or -30 (O)."""
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [6, 4, 2],             # diagonals
    ]

    for line in winning_lines:
        score = 0
        for idx in line:
            if flat_board[idx] == 'X':
                score += 10
            elif flat_board[idx] == 'O':
                score -= 10

        if score == 30:
            return 'X'
        elif score == -30:
            return 'O'

    return 'TIE'


def should_continue(flat_board: list[str], move_number: int) -> bool:
    """Returns True if the search should keep going deeper (no winner yet).
    If the board already has a winner, it records the board as a unique terminal state
    and returns False to stop the nested loops from placing any more moves."""
    # If there is already a winner, this is a terminal state. Record it and stop exploring.
    if has_winner(flat_board):
        record_unique_board(flat_board)
        return False
    return True


def record_full_board(flat_board: list[str]) -> None:
    """Records a fully filled board (all 9 squares used) as a terminal state.
    It always calls record_unique_board to handle symmetry deduplication,
    then increments full_boards and either x_wins_on_full_board or draws_on_full_board."""
    global full_boards, x_wins_on_full_board, draws_on_full_board

    # A full board is always a terminal state, so we record it for uniqueness tracking.
    record_unique_board(flat_board)
    full_boards += 1

    # On a full board, either X won on the last move or no one won (draw).
    if has_winner(flat_board):
        x_wins_on_full_board += 1
    else:
        draws_on_full_board += 1


# ----------------------------
# Brute force search (9 nested loops)
# ----------------------------

# Transitions in the loops: every time we assign board[x1] = 'X' or board[o1] = 'O',
# that is a state transition -- the board moves from one game state to the next.
# The undo lines (board[x1] = ' ') are reverse transitions, restoring the previous state.
# Additional transitions happen inside should_continue() and record_full_board(),
# where the global counters (x_wins, o_wins, ties, full_boards, etc.) are updated.

# Move 1: X
for x1 in range(9):
    board[x1] = 'X'
    if should_continue(board, 1):

        # Move 2: O
        for o1 in range(9):
            if board[o1] == ' ':
                board[o1] = 'O'
                if should_continue(board, 2):

                    # Move 3: X
                    for x2 in range(9):
                        if board[x2] == ' ':
                            board[x2] = 'X'
                            if should_continue(board, 3):

                                # Move 4: O
                                for o2 in range(9):
                                    if board[o2] == ' ':
                                        board[o2] = 'O'
                                        if should_continue(board, 4):

                                            # Move 5: X
                                            for x3 in range(9):
                                                if board[x3] == ' ':
                                                    board[x3] = 'X'
                                                    if should_continue(board, 5):

                                                        # Move 6: O
                                                        for o3 in range(9):
                                                            if board[o3] == ' ':
                                                                board[o3] = 'O'
                                                                if should_continue(board, 6):

                                                                    # Move 7: X
                                                                    for x4 in range(9):
                                                                        if board[x4] == ' ':
                                                                            board[x4] = 'X'
                                                                            if should_continue(board, 7):

                                                                                # Move 8: O
                                                                                for o4 in range(9):
                                                                                    if board[o4] == ' ':
                                                                                        board[o4] = 'O'
                                                                                        if should_continue(board, 8):

                                                                                            # Move 9: X
                                                                                            for x5 in range(9):
                                                                                                if board[x5] == ' ':
                                                                                                    board[x5] = 'X'

                                                                                                    # Full board reached (terminal)
                                                                                                    record_full_board(board)

                                                                                                    # undo move 9
                                                                                                    board[x5] = ' '

                                                                                        # undo move 8
                                                                                        board[o4] = ' '

                                                                            # undo move 7
                                                                            board[x4] = ' '

                                                                # undo move 6
                                                                board[o3] = ' '

                                                    # undo move 5
                                                    board[x3] = ' '

                                        # undo move 4
                                        board[o2] = ' '

                            # undo move 3
                            board[x2] = ' '

                # undo move 2
                board[o1] = ' '

    # undo move 1
    board[x1] = ' '


print(full_boards)
print(len(unique_seen), x_wins_on_full_board, draws_on_full_board, x_wins, o_wins, ties)