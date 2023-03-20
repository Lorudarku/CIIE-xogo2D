# -*- encoding: utf-8 -*-
import pygame

ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 720
COLUMNAS = 25
FILAS = 16
TILE_SIZE = ANCHO_PANTALLA // COLUMNAS
TILE_TYPES = 16

# -------------------------------------------------
# Clase Escena con lo metodos abstractos

class Escena:

    def __init__(self, director):
        self.director = director
 #   si solo vamos a tener escenas de pygame se inicializa aqui la biblioteca
        # pygame.init()

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def eventos(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def dibujar(self, pantalla):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")


#   en caso de crear mas tipos de escenas esta heredan de escena