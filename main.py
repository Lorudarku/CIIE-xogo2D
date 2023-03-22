#!/usr/bin/env python
# -- coding: utf-8 --

# Importar modulos
import pygame
import director
from director import *
from fase import Menu
import escena
from escena import *



if __name__ == "__main__":

    # Inicializamos la libreria de pygame
    pygame.init()
    # Creamos el director
    director = Director()
    # Creamos la escena con la pantalla inicial
    escena = Menu(director)
    # Le decimos al director que apile esta escena
    director.apilarEscena(escena)
    # Y ejecutamos el juego
    director.ejecutar()
    # Cuando se termine la ejecución, finaliza la librería
    pygame.quit()