"""
This is our main driver file.
It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import ChessEngine
from os import path

WIDTH =  HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    ''' 
    INITIALIZE a global dictionary of images.This will be called only once in the main.
    '''
    pieces = ['wp', 'wR', 'wN', 'wK', 'wQ', 'wB', 'bp', 'bR', 'bN', 'bK', 'bQ', 'bB']
    for piece in pieces:
        image_path = path.join("chess", "images", f"{piece}.png")
        IMAGES[piece] = p.transform.scale(p.image.load(image_path), (SQ_SIZE, SQ_SIZE))
    #Note: We can access an image by saying 'IMAGES['wp']'

def main():
    '''
    The main driver for our code. This will handle user input and graphic update
    '''
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves() 
    moveMade = False #Flag variable for when a move is made
    
    loadImages() #Only do this once, before the while loop
    running = True
    sqSelected = () #no square is selected, keep track of user last click: (row, col)
    playerClicks = []#keep track of user clicks: [(2,3), (4,5)]
    while running:
        for e in p.event.get(): 
            if e.type == p.QUIT:
                running = False
                
            #Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()#(x, y) position of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):#user clicked on the same spot
                    sqSelected = ()         #Deselect square
                    playerClicks = []      #clear user clicks                    
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if playerClicks != [] and len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makesMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []

            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_BACKSPACE:
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
                    
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
    drawBoard(screen)

def drawGameState(screen, gs):
    '''
    Responsible for all the the graphics in the current game state.
    '''
    drawBoard(screen)#Draw squares on board
    #Add pieces highlighter and moves tips
    drawPieces(screen, gs.board)#Draw the pieces on top of these squares

def drawBoard(screen):
    '''
    Draw the squares on board.
    '''
    colors = [p.Color("white"), p.Color("dark gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    '''
    Draw the pieces on board using the current GameState.board
    '''
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":#Not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))




if __name__ == "__main__":
    main()