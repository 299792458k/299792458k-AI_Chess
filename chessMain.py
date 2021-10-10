import pygame
from pygame import draw
from pygame import image
from pygame.constants import MOUSEBUTTONDOWN

import chess_boad

WIDTH = 800
HEIGHT = 640
BLOCK = 8
SQ_SIZE = HEIGHT // BLOCK 

MAX_FPS = 15

IMAGES = {}  

def loadImages():
    
    pieces = ["bR","bN","bB","bQ","bK","bp","wp","wR","wN","wB","wQ","wK"]

    for piece in pieces: 
        img = pygame.image.load('images/' + piece + '.png')  #'chess/images/Br.png'

        IMAGES[piece] = pygame.transform.scale(img,(SQ_SIZE,SQ_SIZE))
        
def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    
    pygame.display.set_caption("chess")

    #create an object to help track time
    clock = pygame.time.Clock()

    screen.fill((96,91,84))


    gS = chess_boad.gameState()
    
    loadImages()

    # sqSelected = () #null if no square is selected; keep track of the last click of th user
    # playerClicked = [] # keep track of player click

    running = True
    
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            # elif e.type == MOUSEBUTTONDOWN:
            #     location = pygame.mouse.get_pos() #get (x,y) of mouse
            #     col = location[0]//SQ_SIZE
            #     row = location[1]//SQ_SIZE - 1 #screen size = 800x640
                # if (sqSelected == (row,col)):
                #     sqSelected = () #double click then deselected
                #     playerClicked = [] # then clear player click
                # else:
                #     sqSelected = (row,col)
                #     playerClicked.append(sqSelected)
                # if len(playerClicked) == 2: #if playerClick has 2 element ~ 2 click in different square
                #     aaa = 1

        drawGameState(screen,gS)
        clock.tick(MAX_FPS)
        
        pygame.display.flip()
        pygame.display.update()

def drawGameState(screen, gS):
    #draw board
    drawBoard(screen)
    #draw chess on board 
    drawPieces(screen, gS.board) 

def drawBoard(screen):
    colors = [(240,240,240),(66,63,59)]

    for r in range(BLOCK):
        for c in range(BLOCK):
            color = colors[(r+c)%2]
            pygame.draw.rect(screen, color, [(r+1)*80, c*80, SQ_SIZE, SQ_SIZE])


def drawPieces(screen, board):
    for r in range(BLOCK):
        for c in range(BLOCK):
            piece = board[r][c]
            if piece != "--": 
                #show this image
                screen.blit(IMAGES[piece], pygame.Rect((c+1)*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




main()