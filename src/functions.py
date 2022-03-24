from .const import SQUARE_SIZE
from typing import Tuple, List, Union, Any


def get_square(x: int, y: int) -> Tuple[int, int]:
    """Return square at x, y from (0, 0) to (8, 8)."""
    return int(x/SQUARE_SIZE), int(y/SQUARE_SIZE)


def get_piece_from_square(x: int, y: int, pieces: List[Any]) -> Union[Any, None]:
    """Return Piece at square x, y"""
    for piece in pieces:
        if piece.get_square() == (x, y):
            return piece
