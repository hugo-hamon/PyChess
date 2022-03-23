from .const import BOARD_PATH
import pygame as pg


class Board:

    def __init__(self, path: str = BOARD_PATH) -> None:
        self.sprite = pg.image.load(path)

    def display(self, window: pg.surface.Surface):
        """Display the board on the surface window"""
        window.blit(self.sprite, (0, 0))
