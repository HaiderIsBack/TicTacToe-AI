import math, copy

board = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' '],
]

humanPlays = True

def printBoard(board: list) -> None:
    i = 1
    print()
    for row in board:
        print(f"{row[0]} | {row[1]} | {row[2]}")
        if(i < 3):
            print(f"---------")
            i+=1
    print()

# Identifies and Returns next players turn (X or O)
def Player(board: list) -> str:
    t = 1
    for row in board:
        for col in row:
            if(col == "X" or col == "O"):
                t = 1 if t == 2 else 2
    return "X" if t == 1 else "O"

# Returns a list of possible actions (Actions)
def Actions(s: list) -> list:
    actions = []
    for i in range(3):
        for j in range(3):
            if(s[i][j] == ' '):
                actions.append((i, j))
    return actions

def isBoardFilled(board):
    for row in board:
        if any(cell == '' or cell == ' ' for cell in row):  # Check for empty cells ('' or ' ')
            return False
    return True

# Checks if the game is over. Returns (True or False)
def Terminal(s: list) -> bool:
    if(isBoardFilled(s)):
        return True

    tl = s[0][0]
    tc = s[0][1]
    tr = s[0][2]
    ml = s[1][0]
    mc = s[1][1]
    mr = s[1][2]
    bl = s[2][0]
    bc = s[2][1]
    br = s[2][2]
    
    for turn in ["X", "O"]:
        # Rows Check
        topRowCheck = (tl == turn and tc == turn and tr == turn)
        middleRowCheck = (ml == turn and mc == turn and mr == turn)
        bottomRowCheck = (bl == turn and bc == turn and br == turn)
        # Column Check
        topColCheck = (tl == turn and ml == turn and bl == turn)
        middleColCheck = (tc == turn and mc == turn and bc == turn)
        bottomColCheck = (tr == turn and mr == turn and br == turn)
        # Diagonal Checks
        leftDiagonalCheck = (tl == turn and mc == turn and br == turn)
        rightDiagonalCheck = (bl == turn and mc == turn and tr == turn)

        if(topRowCheck or middleRowCheck or bottomRowCheck or topColCheck or middleColCheck or bottomColCheck or leftDiagonalCheck or rightDiagonalCheck):
            return True
    return False

# Returns a Winning Player (X or O)
def Utility(s: list) -> int:
    tl = s[0][0]
    tc = s[0][1]
    tr = s[0][2]
    ml = s[1][0]
    mc = s[1][1]
    mr = s[1][2]
    bl = s[2][0]
    bc = s[2][1]
    br = s[2][2]
    
    for turn in ["X", "O"]:
        # Rows Check
        topRowCheck = (tl == turn and tc == turn and tr == turn)
        middleRowCheck = (ml == turn and mc == turn and mr == turn)
        bottomRowCheck = (bl == turn and bc == turn and br == turn)
        # Column Check
        topColCheck = (tl == turn and ml == turn and bl == turn)
        middleColCheck = (tc == turn and mc == turn and bc == turn)
        bottomColCheck = (tr == turn and mr == turn and br == turn)
        # Diagonal Checks
        leftDiagonalCheck = (tl == turn and mc == turn and br == turn)
        rightDiagonalCheck = (bl == turn and mc == turn and tr == turn)

        if(topRowCheck or middleRowCheck or bottomRowCheck or topColCheck or middleColCheck or bottomColCheck or leftDiagonalCheck or rightDiagonalCheck):
            return 1 if turn == "X" else -1
    return 0

def Winner(s: list):
    tl = s[0][0]
    tc = s[0][1]
    tr = s[0][2]
    ml = s[1][0]
    mc = s[1][1]
    mr = s[1][2]
    bl = s[2][0]
    bc = s[2][1]
    br = s[2][2]
    
    for turn in ["X", "O"]:
        # Rows Check
        topRowCheck = (tl == turn and tc == turn and tr == turn)
        middleRowCheck = (ml == turn and mc == turn and mr == turn)
        bottomRowCheck = (bl == turn and bc == turn and br == turn)
        # Column Check
        topColCheck = (tl == turn and ml == turn and bl == turn)
        middleColCheck = (tc == turn and mc == turn and bc == turn)
        bottomColCheck = (tr == turn and mr == turn and br == turn)
        # Diagonal Checks
        leftDiagonalCheck = (tl == turn and mc == turn and br == turn)
        rightDiagonalCheck = (bl == turn and mc == turn and tr == turn)

        if(topRowCheck or middleRowCheck or bottomRowCheck or topColCheck or middleColCheck or bottomColCheck or leftDiagonalCheck or rightDiagonalCheck):
            return turn
    return None

# Returns a State (s)
def Result(s: list, a: tuple) -> int:
    copyState = copy.deepcopy(s)
    copyState[a[0]][a[1]] = Player(s)
    return copyState

# Returns a value (v)
def MinValue(state: list) -> tuple[int, tuple]:
    if(Terminal(state)):
        return Utility(state), ()
    v = math.inf
    bestMove = ()
    for action in Actions(state):
        # v = min(v, MaxValue(Result(state, action)))
        aux, move = MaxValue(Result(state, action))
        if aux < v:
            v = aux
            bestMove = action
            if v == -1:
                return v, bestMove
    return v, bestMove

# Returns a value and move (v)
def MaxValue(state: list) -> tuple[int, tuple]:
    if(Terminal(state)):
        return Utility(state), ()
    v = -math.inf
    bestMove = ()
    for action in Actions(state):
        # v = max(v, MinValue(Result(state, action)))
        aux, move = MinValue(Result(state, action))
        if aux > v:
            v = aux
            bestMove = action
            if v == 1:
                return v, bestMove
    return v, bestMove

def main() -> None:
    while(not Terminal(board)):
        turn = Player(board)
        if(humanPlays and turn == "O"):
            while(True):
                humanTurn = int(input('\nEnter your turn [1 - 9]: '))
                if humanTurn < 1 or humanTurn > 9:
                    continue
                adjTurn = humanTurn - 1
                r = adjTurn // 3
                c = adjTurn % 3
                if(board[r][c] == ' '):
                    board[r][c] = "O"
                    break
        elif(turn == "X"):
            val, move = MaxValue(board)
            board[move[0]][move[1]] = "X"
        elif(turn == "O"):
            val, move = MinValue(board)
            board[move[0]][move[1]] = "O"

        printBoard(board)
    if(Winner(board) == "X"):
        print("Congratulation! 'X' is the Winner.")
    elif(Winner(board) == "O"):
        print("Congratulation! 'O' is the Winner.")
    else:
        print("Nobody won, Game is Draw!")
    print()
            

if(__name__ == "__main__"):
    printBoard(board)
    main()