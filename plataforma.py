
from personajes import *
import pygame, sys, os, escena
from pygame.locals import *
from escena import *


class Plataforma(MiSprite):
    def __init__(self, x, y, skin="rectangulo-semitransparente.png"):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        
        # Y lo situamos de forma global en esas coordenadas
        
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = GestorRecursos.CargarImagen(skin, -1)
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        #self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.establecerPosicion((x, y))
        #pygame.Surface.blit(self.imagen,cubo,(0, 550))