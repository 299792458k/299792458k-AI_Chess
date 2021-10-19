import pygame
from pygame import draw
from pygame import image
from pygame.constants import MOUSEBUTTONDOWN
import pygame as p

import chessEngine

WIDTH = 640
HEIGHT = 640
BLOCK = 8
SQ_SIZE = HEIGHT // BLOCK

MAX_FPS = 15

IMAGES = {}


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]

    for piece in pieces:
        img = p.image.load('images/' + piece + '.png')  # 'chess/images/Br.png'

        IMAGES[piece] = p.transform.scale(img, (SQ_SIZE, SQ_SIZE))


def main():
    p.init()

    screen = p.display.set_mode((WIDTH, HEIGHT))

    p.display.set_caption("chess")

    # create an object to help track time
    clock = p.time.Clock()

    screen.fill((96, 91, 84))

    gS = chessEngine.GameState()
    validMoves = gS.getValidMoves()
    moveMade = False  # flag var for when a move is made (to regenerate the validMoves)

    loadImages()

    running = True
    sqSelected = ()  # no square is selected, keep track of the last click of the user( tuple (row,col))
    playerClicks = []  # keep track of player clicks (two tuples[(6,4),(4,4)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()  # (x,y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the same square twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # clear the player clicks
                else:
                    sqSelected = (row, col)
                    # phong TH click o trong
                    if (gS.board[row][col] != '--' or len(playerClicks) != 0):
                        playerClicks.append(sqSelected)  # append for both 1st and 2nd clicks
                if len(playerClicks) == 2:  # after 2nd click

                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gS.board)

                    if move in validMoves:
                        print(move.getChessNotation())
                        gS.makeMove(move)
                        moveMade = True
                        sqSelected = ()  # reset the clicks
                        playerClicks = []
                    else:  # Click vao con khac cung mau thi thanh click thu nhat cua con khac luon
                        playerClicks = [sqSelected]

            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when press 'z
                    gS.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gS.getValidMoves()  # Di chuyen den o moi => thay doi
            moveMade = False

        drawGameState(screen, gS)
        clock.tick(MAX_FPS)
        p.display.flip()


def drawGameState(screen, gS):
    # draw board
    drawBoard(screen)
    # draw chess on board
    drawPieces(screen, gS.board)


def drawBoard(screen):
    colors = [(240, 240, 240), (66, 63, 59)]

    for r in range(BLOCK):
        for c in range(BLOCK):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, [(r) * 80, c * 80, SQ_SIZE, SQ_SIZE])


def drawPieces(screen, board):
    for r in range(BLOCK):
        for c in range(BLOCK):
            piece = board[r][c]
            if piece != "--":
                # show this image
                screen.blit(IMAGES[piece], p.Rect((c) * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


main()