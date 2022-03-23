from .const import WHITE, BLACK
import pygame as pg
import sys


class Pieces:

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        if (x < 0 or y < 0 or color not in [WHITE, BLACK]):
            sys.exit("Wrong cordinate or bad color value.")
        self.color = color
        self.pos = {"x": x, "y": y}
        self.sprite = pg.image.load(sprite_path)

    def display(self, window: pg.surface.Surface):
        """Display the pieces on the surface window"""
        print("ok")
        window.blit(self.sprite, (self.pos["x"], self.pos["y"]))


class Pawn(Pieces):

    def __init__(self, x: int, y: int, color: int, sprite_path: str):
        super().__init__(x, y, color, sprite_path)
