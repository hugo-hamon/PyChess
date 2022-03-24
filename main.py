from src import Board, Pawn, WINDOW_SIZE, WHITE, BLACK, \
    PIECE_PATH, SQUARE_SIZE, get_square, get_piece_from_square
import pygame as pg

PIECES_TYPE = Pawn


pg.init()
window = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pg.display.set_caption("Chess")

# Board
board = Board()

# Make pieces
white_pawns = [Pawn(SQUARE_SIZE*k, SQUARE_SIZE*6, WHITE, f'{PIECE_PATH}white_pawn.png')
               for k in range(8)]
black_pawns = [Pawn(SQUARE_SIZE*k, SQUARE_SIZE, BLACK, f'{PIECE_PATH}black_pawn.png')
               for k in range(8)]
pawns = white_pawns + black_pawns

pieces = pawns

# Var
start_piece = None
run = True
while run:
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            square_x, square_y = get_square(x, y)
            p = get_piece_from_square(square_x, square_y, pieces)
            
            if start_piece is not None:
                # Check if piece can move
                if start_piece.can_move(square_x, square_y, pieces):
                    start_piece.move(square_x, square_y)
                else:
                    print("can't moving.")
                start_piece = None
            else:
                start_piece = p

        elif event.type == pg.QUIT:
            run = False

        # Display board
        board.display(window)

        # Display pieces
        for piece in pieces:
            piece.display(window)

        pg.display.update()
pg.quit()
