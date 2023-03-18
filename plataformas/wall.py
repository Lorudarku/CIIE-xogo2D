
from plataformas.plataformas import *
import pygame, sys, os
from pygame.locals import *
from gestorRecursos import *

class Wall(Plataformas):
    def __init__(self, x, y):
        Plataformas.__init__(self)
        wall_image = GestorRecursos.CargarImagen('wall.png',-1)
        self.image = wall_image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.establecerPosicion((self.rect.left, self.rect.bottom))