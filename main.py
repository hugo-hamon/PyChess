from src import Board, Pawn, WINDOW_SIZE, WHITE, PIECE_PATH
import pygame as pg


if __name__ == '__main__':
    pg.init()
    window = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pg.display.set_caption("Chess")

    # Board
    board = Board()

    # Make pieces
    pawn_list = [Pawn(0, 0, WHITE, PIECE_PATH + "white_pawn.png")]


    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                # Move pieces
                pass
            elif event.type == pg.QUIT:
                run = False
        
        #Display board
        board.display(window)

        # Display pieces
        for pawn in pawn_list:
            pawn.display(window)

        pg.display.update()

        

    pg.quit()
