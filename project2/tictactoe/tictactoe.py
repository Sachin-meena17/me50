"""
Tic Tac Toe Player
"""

import math

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


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    no_of_empty = 0
    no_of_X=0
    np_of_O=0
    for index1 in range(3):
        for index2 in range(3):
            if board[index1][index2] == EMPTY:
                no_of_empty += 1
            elif board[index1][index2] == X:
                no_of_X += 1
            else:
                np_of_O+=1



    if no_of_empty%2 == 0:
        return X
    else:
        return O

    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    answer =set()
    for index1 in range(3):
        for index2 in range(3):
            if board[index1][index2] == EMPTY:
                answer.add((index1,index2))
    #print("in acton board")
    #print(answer)
    return answer
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    copied_board = board
    player_chance=player(copied_board)
    #print("in action""")
    #print(action)

    if terminal(board) == False:
        if copied_board[action[0]][action[1]] == EMPTY:
            if player_chance == X:
                copied_board[action[0]][action[1]] = X
            else:
                copied_board[action[0]][action[1]] = O
        else:
            raise Exception


    return copied_board

    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for index in range(3):
        if board[index][0] == board[index][1] and board[index][1] == board[index][2]:
            return board[index][0]

    for index in range(3):
        if board[0][index] == board[1][index] and board[1][index] == board[2][index]:
            return board[0][index]


    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]

    if board[2][0] == board[1][1] and board[1][1] == board[0][2]:
        return board[1][1]

    return None

    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    for index1 in range(3):
        for index2 in range(3):
            if board[index1][index2] == EMPTY:
                return False

    return True

    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    player = winner(board)
    if player == X:
        return 1
    elif player == O:
        return -1
    else:
        return 0

    raise NotImplementedError


def reset_board(copied_board,board):
    for index1 in range(3):
        for index2 in range(3):
            copied_board[index1][index2] = board[index1][index2]



def Max_value(board,depth):
    if terminal(board):
        return utility(board)*10-depth

    v = -100
    for action in actions(board):
        v = max(v, Min_value(result(board, action), depth+1))

    return v

def Max_value(board,depth,alpha,beta):
    if terminal(board):
        return utility(board)*10-depth
    copied_board=[[EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY,EMPTY]]
    reset_board(copied_board,board)
    v = -100
    for action in actions(board):
        v = max(v, Min_value(result(copied_board, action), depth+1,alpha,beta))
        reset_board(copied_board,board)
        alpha = max(alpha,v)
        if beta <= alpha:
            break

    return v

def Min_value(board,depth,alpha,beta):
    if terminal(board):
        return utility(board)*10+depth
    copied_board=[[EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY,EMPTY]]
    reset_board(copied_board,board)
    v =100

    for action in actions(board):
        v = min(v, Max_value(result(copied_board, action), depth+1,alpha,beta))
        reset_board(copied_board,board)
        beta = min(beta,v)
        if beta <= alpha:
            break
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """


    alpha=-100
    beta=+100
    copied_board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
    for index1 in range(3):
        for index2 in range(3):
            copied_board[index1][index2] = board[index1][index2]

    bestmove = None
    answer1=0



    for action in actions(board):
        result_board = result(copied_board,action)

        if bestmove != None:
            if player(result_board) == X:
                answer = Max_value(result_board, 0, alpha, beta)
                if answer <= answer1:
                    bestmove = action
                    answer1 = answer
            else:
                answer = Min_value(result_board, 0, alpha, beta)
                if answer >= answer1:
                    bestmove = action
                    answer1 = answer
            reset_board(copied_board, board)
        else:
            bestmove=action
            if player(result_board) == X:
                answer1 = Max_value(result_board, 0, alpha, beta)
            else:
                answer1 = Min_value(result_board, 0, alpha, beta)
            reset_board(copied_board, board)

    return bestmove
    raise NotImplementedError
