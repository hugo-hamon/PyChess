from .const import WHITE, BLACK, PIECE_MARGIN, SQUARE_SIZE, PIECE_PATH
from .functions import get_square, get_piece_from_square
from typing import Union, Tuple, Any, List
from itertools import chain
import pygame as pg
import sys


def abs(x: int) -> int:
    return x if x >= 0 else x * -1


class Pieces:

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        if (x < 0 or y < 0 or color not in [WHITE, BLACK]):
            sys.exit("Wrong cordinate or bad color value.")
        self.color = color
        self.pos = {"x": x, "y": y}
        self.sprite = pg.image.load(sprite_path)
        self.already_play = False

    def display(self, window: pg.surface.Surface):
        """Display the pieces on the surface window"""
        window.blit(
            self.sprite, (self.pos["x"] + PIECE_MARGIN,
                          self.pos["y"] + PIECE_MARGIN)
        )

    def get_square(self) -> Tuple[int, int]:
        """Return square at x, y from (0, 0) to (8, 8)."""
        return get_square(self.pos["x"], self.pos["y"])

    def move(self, square_x: int, square_y: int):
        self.play = True
        self.pos["x"] = square_x * SQUARE_SIZE
        self.pos["y"] = square_y * SQUARE_SIZE

    def is_valid_coordinate(self, ex: int, ey: int) -> bool:
        """Return True if the coordinates are valid."""
        return (ex >= 0 and ex < 8 and ey >= 0 and ey < 8)


# Pieces class

class Pawn(Pieces):

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        super().__init__(x, y, color, sprite_path)

    def can_move(self, ex: int, ey: int, pieces: List[Pieces]) -> bool:
        """Return true if can move otherwise false"""
        sx, sy = self.get_square()
        moves = self.get_all_pawn_move(sx, sy, pieces)
        if moves is None:
            return False
        return (ex, ey) in moves

    def get_all_pawn_move(self, sx: int, sy: int, pieces: List[Pieces]) -> Union[List[Tuple[int, int]], None]:
        """Return a list of all move that a pawn can do"""
        moves1 = self.get_verticaly_moves(sx, sy, pieces)
        moves2 = self.get_diagolaly_moves(sx, sy, pieces)
        moves: List[Tuple[int, int]] = []
        if moves1 is not None:
            moves = list(chain(moves, moves1))
        if moves2 is not None:
            moves = list(chain(moves, moves2))
        return moves or None

    def get_diagolaly_moves(self, sx: int, sy: int, pieces: List[Pieces]) -> Union[List[Tuple[int, int]], None]:
        """Return a list of all diagonal move that a pawn can do"""
        c = -1 if self.color == WHITE else 1
        p1 = get_piece_from_square(sx - 1, sy + c, pieces)
        p2 = get_piece_from_square(sx + 1, sy + c, pieces)
        moves: List[Tuple[int, int]] = []
        if p1 is not None and p1.color != self.color:
            moves.append((sx - 1, sy + c))
        if p2 is not None and p2.color != self.color:
            moves.append((sx + 1, sy + c))
        return moves or None

    def get_verticaly_moves(self, sx: int, sy: int, pieces: List[Pieces]) -> Union[List[Tuple[int, int]], None]:
        """Return a list of all vertical move that a pawn can do"""
        c = -1 if self.color == WHITE else 1
        p1 = get_piece_from_square(sx, sy + c, pieces)
        p2 = get_piece_from_square(sx, sy + 2 * c, pieces)
        moves: List[Tuple[int, int]] = []
        if not self.already_play:
            if p1 is None:
                moves.append((sx, sy + c))
            if p2 is None:
                moves.append((sx, sy + 2 * c))
        else:
            if (7 - sy) % 7 == 0:
                return None
            if p1 is None:
                moves.append((sx, sy + c))
        return moves or None


class Rook(Pieces):

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        super().__init__(x, y, color, sprite_path)

    def can_move(self, ex: int, ey: int, pieces: List[Pieces]) -> bool:
        """Return true if can move otherwise false"""
        sx, sy = self.get_square()
        moves = self.get_all_rook_move(sx, sy, pieces)
        if moves is None:
            return False
        return (ex, ey) in moves

    def get_all_rook_move(self, sx: int, sy: int, pieces: List[Pieces]) -> Union[List[Tuple[int, int]], None]:
        """Return a list of all rook move that a rook can do"""
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1))
        moves: List[Tuple[int, int]] = []
        for d in directions:
            for i in range(1, 8):
                p = get_piece_from_square(sx + i * d[0], sy + i * d[1], pieces)
                if p is None or p.color != self.color:
                    moves.append((sx + i * d[0], sy + i * d[1]))
                    if p is not None:
                        break
        return moves or None


class Bishop(Pieces):

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        super().__init__(x, y, color, sprite_path)

    def can_move(self, ex: int, ey: int, pieces: List[Pieces]) -> bool:
        """Return true if can move otherwise false"""
        sx, sy = self.get_square()
        moves = self.get_all_bishop_move(sx, sy, pieces)
        if moves is None:
            return False
        return (ex, ey) in moves

    def get_all_bishop_move(self, sx: int, sy: int, pieces: List[Pieces]) -> Union[List[Tuple[int, int]], None]:
        """Return a list of all bishop move that a bishop can do"""
        directions = ((1, 1), (-1, 1), (1, -1), (-1, -1))
        moves: List[Tuple[int, int]] = []
        for d in directions:
            for i in range(1, 8):
                p = get_piece_from_square(sx + i * d[0], sy + i * d[1], pieces)
                if p is None or p.color != self.color:
                    moves.append((sx + i * d[0], sy + i * d[1]))
                if p is not None:
                    break
        return moves


class Knight(Pieces):

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        super().__init__(x, y, color, sprite_path)

    def can_move(self, ex: int, ey: int, pieces: List[Pieces]) -> bool:
        """Return true if can move otherwise false"""
        sx, sy = self.get_square()
        moves = self.get_all_knight_move(sx, sy, pieces)
        if moves is None:
            return False
        return (ex, ey) in moves

    def get_all_knight_move(self, sx: int, sy: int, pieces: List[Pieces]) -> Union[List[Tuple[int, int]], None]:
        """Return a list of all knight move that a knight can do"""
        directions = ((1, 2), (1, -2), (-1, 2), (-1, -2),
                      (2, 1), (2, -1), (-2, 1), (-2, -1))
        moves: List[Tuple[int, int]] = []
        for d in directions:
            p = get_piece_from_square(sx + d[0], sy + d[1], pieces)
            if p is None or p.color != self.color:
                moves.append((sx + d[0], sy + d[1]))
        return moves or None


class Queen(Pieces):

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        super().__init__(x, y, color, sprite_path)

    def can_move(self, ex: int, ey: int, pieces: List[Pieces]) -> bool:
        """Return true if can move otherwise false"""
        sx, sy = self.get_square()
        moves = self.get_all_queen_move(sx, sy, pieces)
        if moves is None:
            return False
        return (ex, ey) in moves

    def get_all_queen_move(self, sx: int, sy: int, pieces: List[Pieces]) -> Union[List[Tuple[int, int]], None]:
        """Return a list of all queen move that a queen can do"""
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1))
        moves: List[Tuple[int, int]] = []
        for d in directions:
            for i in range(1, 8):
                p = get_piece_from_square(sx + i * d[0], sy + i * d[1], pieces)
                if p is None or p.color != self.color:
                    moves.append((sx + i * d[0], sy + i * d[1]))
                if p is not None:
                    break
        return moves or None


class King(Pieces):

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        super().__init__(x, y, color, sprite_path)

    def can_move(self, ex: int, ey: int, pieces: List[Pieces]) -> bool:
        """Return true if can move otherwise false"""
        sx, sy = self.get_square()
        moves = self.get_all_king_move(sx, sy, pieces)
        if moves is None:
            return False
        return (ex, ey) in moves

    def get_all_king_move(self, sx: int, sy: int, pieces: List[Pieces]) -> Union[List[Tuple[int, int]], None]:
        """Return a list of all king move that a king can do"""
        directions = ((1, 0), (-1, 0), (0, 1), (0, -1),
                      (1, 1), (-1, 1), (1, -1), (-1, -1))
        moves: List[Tuple[int, int]] = []
        for d in directions:
            ex = sx + d[0]
            ey = sy + d[1]
            p = get_piece_from_square(ex, ey, pieces)
            if (
                p is None
                or p.color != self.color
                and not (self.is_check(pieces, ex, ey))
            ) and self.is_valid_coordinate(ex, ey):
                moves.append((ex, ey))
        return moves or None

    def is_check(self, pieces: List[Any], sx: int = -1, sy: int = -1) -> bool:
        """Return true if in check otherwise false"""
        if sx == -1 and sy == -1:
            sx, sy = self.get_square()
        return any(
            p.color != self.color and p.can_move(sx, sy, pieces) for p in pieces
        )

    def is_checkmate(self, pieces: List[Any]) -> bool:
        """Return true if in checkmate otherwise false"""
        sx, sy = self.get_square()
        return self.get_all_king_move(sx, sy, pieces) is None and self.is_check(pieces)


# Functions to make pieces


def make_pawns() -> List[Pawn]:
    """Return list of pawns"""
    pawns: List[Pawn] = []
    for k in range(8):
        pawns.extend((
            Pawn(SQUARE_SIZE * k, SQUARE_SIZE * 6, WHITE,
                 f'{PIECE_PATH}white_pawn.png',),
            Pawn(SQUARE_SIZE * k, SQUARE_SIZE, BLACK,
                 f'{PIECE_PATH}black_pawn.png',),)
        )

    return pawns


def make_rooks() -> List[Rook]:
    """Return list of rooks"""
    rooks: List[Rook] = []
    for k in range(2):
        rooks.extend((
            Rook(SQUARE_SIZE * k * 7, SQUARE_SIZE * 7, WHITE,
                 f'{PIECE_PATH}white_rook.png',),
            Rook(SQUARE_SIZE * k * 7, SQUARE_SIZE * 0, BLACK,
                 f'{PIECE_PATH}black_rook.png',),)
        )

    return rooks


def make_bishops() -> List[Bishop]:
    """Return list of bishops"""
    bishops: List[Bishop] = []
    pos = [2, 5]
    for k in range(2):
        bishops.extend((
            Bishop(SQUARE_SIZE * pos[k], SQUARE_SIZE * 7, WHITE,
                   f'{PIECE_PATH}white_bishop.png',),
            Bishop(SQUARE_SIZE * pos[k], SQUARE_SIZE * 0, BLACK,
                   f'{PIECE_PATH}black_bishop.png',))
        )

    return bishops


def make_knights() -> List[Knight]:
    """Return list of knights"""
    knights: List[Knight] = []
    pos = [1, 6]
    for k in range(2):
        knights.extend((
            Knight(SQUARE_SIZE * pos[k], SQUARE_SIZE * 7, WHITE,
                   f'{PIECE_PATH}white_knight.png',),
            Knight(SQUARE_SIZE * pos[k], SQUARE_SIZE * 0, BLACK,
                   f'{PIECE_PATH}black_knight.png',))
        )

    return knights


def make_queens() -> List[Queen]:
    """Return list of queens"""
    return [
        Queen(
            SQUARE_SIZE * 3, SQUARE_SIZE * 7, WHITE,
            f'{PIECE_PATH}white_queen.png',
        ),
        Queen(
            SQUARE_SIZE * 3, SQUARE_SIZE * 0, BLACK,
            f'{PIECE_PATH}black_queen.png',
        ),
    ]


def make_king() -> List[King]:
    """Return list of kings"""
    return [
        King(
            SQUARE_SIZE * 4, SQUARE_SIZE * 7, WHITE,
            f'{PIECE_PATH}white_king.png',
        ),
        King(
            SQUARE_SIZE * 4, SQUARE_SIZE * 0, BLACK,
            f'{PIECE_PATH}black_king.png',
        ),
    ]


def get_kings_from_pieces(pieces: List[Pieces]) -> List[King]:
    """Return list of kings from pieces"""
    return [piece for piece in pieces if isinstance(piece, King)]


def make_pieces() -> List[Pieces]:
    """Return list of all pieces"""
    pawns = make_pawns()
    rooks = make_rooks()
    bishops = make_bishops()
    knights = make_knights()
    queens = make_queens()
    king = make_king()
    return list(chain(king, pawns, rooks, bishops, knights, queens))
