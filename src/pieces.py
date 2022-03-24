from .const import WHITE, BLACK, PIECE_MARGIN, SQUARE_SIZE
from .functions import get_square, get_piece_from_square
from typing import Tuple, Union, Any
import pygame as pg
import sys


def abs(x: Union[float, int]):
    return x if x >= 0 else x * -1


class Pieces:

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        if (x < 0 or y < 0 or color not in [WHITE, BLACK]):
            sys.exit("Wrong cordinate or bad color value.")
        self.color = color
        self.pos = {"x": x, "y": y}
        self.sprite = pg.image.load(sprite_path)
        self.play = False

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


class Pawn(Pieces):

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        super().__init__(x, y, color, sprite_path)

    def can_move(self, ex: int, ey: int, pieces: Any) -> bool:
        """Return true if can move otherwise false"""
        sx, sy = self.get_square()
        if sx == ex and sy == ey:
            return False
        if sx != ex:
            return self.__can_move_horizontally(sx, sy, ex, ey, pieces)
        return self.__can_move_vertically(sx, sy, ey, pieces)

    def __can_move_vertically(self, sx: int, sy: int, ey: int, pieces: Any) -> bool:
        """Return true if can move vertically"""
        c = (self.color == BLACK) - (self.color == WHITE)
        d = abs(sy - ey)
        # Check distance
        if d > 2 or (sy - ey) * c > 0:
            return False
        # check if piece on next square
        p1 = get_piece_from_square(sx, sy + c, pieces)
        if p1 != None:
            return False
        # Check if piece on second square
        if d == 2:
            p2 = get_piece_from_square(sx, sy + 2 * c, pieces)
            if p2 != None or self.play:
                return False
        return True

    def __can_move_horizontally(self, sx: int, sy: int, ex: int, ey: int, pieces: Any) -> bool:
        """Return true if can move horizontally"""
        c = (self.color == BLACK) - (self.color == WHITE)
        p1 = get_piece_from_square(sx - 1, sy + c, pieces)
        p2 = get_piece_from_square(sx + 1, sy + c, pieces)
        if sx - 1 == ex and sy + c == ey:
            if p1 != None:
                return True
        if sx + 1 == ex and sy + c == ey:
            if p2 != None:
                return True

        return False
