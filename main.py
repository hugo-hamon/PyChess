from src import Board, WINDOW_SIZE, WHITE, BLACK, get_square, get_piece_from_square, \
    make_pieces, get_kings_from_pieces, Pieces, King
from typing import List
import pygame as pg

# -- Functions --


def game_loop(piece_to_move: Pieces, piece_at_the_end: Pieces, pieces: List[Pieces],
              kings: List[King], ex: int, ey: int) -> bool:
    # Move the piece if the king is not in check
    sx, sy = piece_to_move.get_square()
    piece_to_move.move(ex, ey)
    if piece_at_the_end is not None:
        pieces.remove(piece_at_the_end)
    for king in kings:
        if king.color != piece_to_move.color and king.is_checkmate(pieces):
            color = "White" if king.color else "Black"
            print(f"{color} win king is checkmate!")
            return False
        if king.color == piece_to_move.color and king.is_check(pieces):
            piece_to_move.move(sx, sy)
            color = "Black" if king.color else "White"
            print(f"{color} king is in check!")
            return False
    
    return True


# -- Main --
pg.init()
window = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pg.display.set_caption("Chess")

# Board
board = Board()


# Make pieces
pieces = make_pieces()
kings = get_kings_from_pieces(pieces)

# Var
pieces_to_move = None
play_turn = WHITE

run = True
while run:
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            square_x, square_y = get_square(x, y)
            p = get_piece_from_square(square_x, square_y, pieces)
            if pieces_to_move is None:
                if p is not None and p.color == play_turn:
                    pieces_to_move = p
            elif pieces_to_move.can_move(square_x, square_y, pieces):
                r = game_loop(pieces_to_move, p, pieces, kings, square_x, square_y)
                if r:
                    play_turn = WHITE if play_turn == BLACK else BLACK
                pieces_to_move = None
            else:
                pieces_to_move = p
        elif event.type == pg.QUIT:
            run = False

        # Display board
        board.display(window)

        # Display pieces
        for piece in pieces:
            piece.display(window)

        pg.display.update()
pg.quit()
