"""
Handling the AI moves.
"""
import random
from typing import Counter

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]
                        }

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

# put next move to a queue and it will be get in main when machine turn is called
def findBestMove(game_state, valid_moves, return_queue):
    global next_move
    next_move = None
    # global count_move 
    # count_move = 0
    random.shuffle(valid_moves)
    if game_state.white_to_move :
        findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE,CHECKMATE)
    else :
        findMoveNegaMinAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE,CHECKMATE)
    
    return_queue.put(next_move)


# return score and show next move
def findMoveNegaMinAlphaBeta(game_state, valid_moves, depth, alpha, beta):
    global next_move
    # global count_move
    # count_move = count_move + 1
    if depth == 0:
        return  scoreBoard(game_state)
    # move ordering - implement later //TODO
    min_score = CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, alpha, beta)
        
        if score < min_score :
            if depth == DEPTH:
                next_move = move 
            min_score = score  
        
        game_state.undoMove()  
         
        if score < beta:
            beta = score
            
        if min_score <= alpha :
           break
                      
    return min_score
            
        # if score < min_score:
        #     min_score = score
        #     if depth == DEPTH:
        #         next_move = move
        # game_state.undoMove()
        # if min_score < beta:
        #     beta = min_score
        # if score <= alpha:
        #     return score
    # return min_score

def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta):
    global next_move
    # global count_move
    # count_move = count_move + 1
    if depth == 0:
        return scoreBoard(game_state)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = findMoveNegaMinAlphaBeta(game_state, next_moves, depth - 1, alpha, beta)
           
        if score > max_score:
            if depth == DEPTH:
                next_move = move
            max_score = score
        
        game_state.undoMove()
            
        if score > alpha :
            alpha = score 
            
        if max_score >= beta : 
            break
            
    return max_score
    #     if score > max_score:
    #         max_score = score
    #     game_state.undoMove()
    #     if max_score > alpha:
    #         alpha = max_score
    #     if score >= beta:
    #         return score
    # return max_score
    
# def findBestMove(game_state, valid_moves, return_queue):
#     global next_move
#     next_move = None
#     random.shuffle(valid_moves)
#     findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
#                              1 if game_state.white_to_move else -1)
#     return_queue.put(next_move)


# def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
#     global next_move
#     if depth == 0:
#         return turn_multiplier * scoreBoard(game_state)
#     # move ordering - implement later //TODO
#     max_score = -CHECKMATE
#     for move in valid_moves:
#         game_state.makeMove(move)
#         next_moves = game_state.getValidMoves()
#         score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
#         if score > max_score:
#             max_score = score
#             if depth == DEPTH:
#                 next_move = move
#         game_state.undoMove()
#         if max_score > alpha:
#             alpha = max_score
#         if alpha >= beta:
#             break
#     return max_score


# score for each move : white's score and black's
def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    
    # duyet ca bang
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score


def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)