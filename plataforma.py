
from personajes import *
import pygame, sys, os
from pygame.locals import *

class Plataforma(MiSprite):
    def __init__(self,rectangulo,skin="rectangulo-semitransparente.png"):
        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self)
        # Rectangulo con las coordenadas en pantalla que ocupara
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        # En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
        self.image = GestorRecursos.CargarImagen(skin, -1)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        #pygame.Surface.blit(self.imagen,cubo,(0, 550))
    
