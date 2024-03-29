"""
Tic Tac Toe Player
"""

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def get_moves_played(board):
    moves_played = 0
    for row in board:
        for cell in row:
            if cell is not EMPTY:
                moves_played += 1

    return moves_played


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    moves_played = get_moves_played(board)
    next_player = X if moves_played%2 == 0 else O
    return next_player


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves_to_play = set()
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if cell is EMPTY:
                moves_to_play.add((i, j))

    return moves_to_play


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    p = player(board)
    i, j = action

    if i < 0 or i > 2 or j < 0 or j > 2:
        raise ValueError(f"Invalid action {action} for board \n {board}")
    
    new_board = [[element for element in row] for row in board]
    if new_board[i][j] is not EMPTY:
        raise ValueError(f"Invalid action {action} for board \n {board}")
    
    new_board[i][j] = p
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    
    # check the rows
    for row in board:
        all_x = all([cell == X for cell in row])
        if all_x:
            return X

        all_o = all([cell == O for cell in row])
        if all_o:
            return O
        
    # check the columns
    for j in range(len(board[0])):
        column = [board[i][j] for i in range(len(board))]
        all_x = all([cell == X for cell in column])
        if all_x:
            return X

        all_o = all([cell == O for cell in column])
        if all_o:
            return O
        
    # check the diagonals
    diagonals = [
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    for diagonal in diagonals:
        all_x = all([cell == X for cell in diagonal])
        if all_x:
            return X

        all_o = all([cell == O for cell in diagonal])
        if all_o:
            return O
        
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    moves_played = get_moves_played(board)
    if moves_played == 9:
        return True
    
    w = winner(board)
    return w is not None


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    elif w == O:
        return -1
    return 0


def minimax(board, alpha=None, beta=None, return_value=False):
    """
    Returns the optimal action for the current player on the board.

    **Given a state s**

    - The maximizing player picks action *a* in *Actions(s)* that produces the highest value of *Min-Value(Result(s, a))*.
    - The minimizing player picks action *a* in *Actions(s)* that produces the lowest value of *Max-Value(Result(s, a))*.

    **Function *Max-Value(state)***

    - *v = -∞*
    - if *Terminal(state)*:

        return *Utility(state)*

    - for *action* in *Actions(state)*:
        
        *v = Max(v, Min-Value(Result(state, action)))*
        
        return *v*
        

    **Function *Min-Value(state)*:**

    - *v = ∞*
    - if *Terminal(state)*:
        
        return *Utility(state)*
        
    - for *action* in *Actions(state)*:
        
        *v = Min(v, Max-Value(Result(state, action)))*
        
        return *v*
    """

    def __return(options, f):
        if return_value:
            if len(options) > 0:
                return f(options, key=lambda x: x['value'])['value']
            return options[0]['value']
        
        best_move = f(options, key=lambda x: x['value'])['action']
        return best_move


    _board = [[element for element in row] for row in board]
    if terminal(_board) and not return_value:
        return None
    if terminal(_board):
        return utility(_board)
    
    p = player(_board)
    values_by_action = []
    actions_to_play = actions(_board)

    
    if p == X:
        alpha = None
        for action in actions_to_play: 
            result_of_action = result(_board, action)
            
            eva = minimax(result_of_action, alpha=alpha, return_value=True)
            values_by_action.append({ 'action': action, 'value': eva })

            alpha = max(values_by_action, key=lambda x: x['value'])['value']
            if beta is not None and eva>beta:
               break
        
        return __return(values_by_action, max)
    else:
        beta = None
        for action in actions_to_play: 
            result_of_action = result(_board, action)
            
            eva = minimax(result_of_action, beta=beta, return_value=True)
            values_by_action.append({ 'action': action, 'value': eva })

            beta = min(values_by_action, key=lambda x: x['value'])['value']
            if alpha is not None and eva<alpha:
               break
    
        return __return(values_by_action, min)
    
