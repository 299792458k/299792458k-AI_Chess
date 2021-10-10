import pygame
from pygame import draw
from pygame import image
from pygame.constants import MOUSEBUTTONDOWN

import chessEngine

WIDTH = 640
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


    gS = chessEngine.gameState()
    
    loadImages()

    running = True
    sqSelected = ()  #no square is selected, keep track of the last click of the user( tuple (row,col))
    playerClicks = [] #keep track of player clicks (two tuples[(6,4),(4,4)])
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() #(x,y) location of the mouse
                col = location[0]//SQ_SIZE        # only with full size board
                row = location[1]//SQ_SIZE
                if sqSelected==(row,col):         #the user clicked the same square twice
                    sqSelected=()                 #deselect
                    playerClicks=[]             #clear the player clicks
                else:
                    sqSelected=(row,col)
                    playerClicks.append(sqSelected)
                if len(playerClicks)==2:        #the 2nd click
                    move = chessEngine.Move(playerClicks[0],playerClicks[1],gS.board)
                    print(move.getChessNotation())
                    gS.makeMove(move)
                    sqSelected = ()     #reset player clicks
                    playerClicks = []   
                    
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
            pygame.draw.rect(screen, color, [(r)*80, c*80, SQ_SIZE, SQ_SIZE])


def drawPieces(screen, board):
    for r in range(BLOCK):
        for c in range(BLOCK):
            piece = board[r][c]
            if piece != "--": 
                #show this image
                screen.blit(IMAGES[piece], pygame.Rect((c)*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




main()