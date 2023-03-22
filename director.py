# -*- encoding: utf-8 -*-

# Modulos
import pygame
import sys
#import escena
from escena import *
from pygame.locals import *


class Director():
    @classmethod
    def __init__(cls):
        # Inicializamos la pantalla y el modo grafico
        cls.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Drunken-Jumper")    #Drunk King
        # Pila de escenas
        cls.pila = []
        # Flag que nos indica cuando quieren salir de la escena
        cls.salir_escena = False
        # Reloj
        cls.reloj = pygame.time.Clock()

    @classmethod
    def bucle(cls, escena):

        cls.salir_escena = False

        # Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()
        
        # El bucle del juego, las acciones que se realicen se harán en cada escena
        while not cls.salir_escena:

            # Sincronizar el juego a 60 fps
            tiempo_pasado = cls.reloj.tick(60)
            
            # Pasamos los eventos a la escena
            escena.eventos(pygame.event.get())

            # Actualiza la escena
            escena.update(tiempo_pasado)

            # Se dibuja en pantalla
            escena.dibujar(cls.screen)
            pygame.display.flip()

    @classmethod
    def ejecutar(cls):

        # Mientras haya escenas en la pila, ejecutaremos la de arriba
        while (len(cls.pila)>0):

            # Se coge la escena a ejecutar como la que este en la cima de la pila
            escena = cls.pila[len(cls.pila)-1]

            # Ejecutamos el bucle de eventos hasta que termine la escena
            cls.bucle(escena)

    @classmethod
    def salirEscena(cls):
        # Indicamos en el flag que se quiere salir de la escena
        cls.salir_escena = True
        # Eliminamos la escena actual de la pila (si la hay)
        if (len(cls.pila)>0):
            cls.pila.pop()

    @classmethod
    def salirPrograma(cls):
        # Vaciamos la lista de escenas pendientes
        cls.pila = []
        cls.salir_escena = True

    @classmethod
    def cambiarEscena(cls, escena):
        cls.salirEscena()
        # Ponemos la escena pasada en la cima de la pila
        cls.pila.append(escena)

    @classmethod
    def apilarEscena(cls, escena):
        cls.salir_escena = True
        # Ponemos la escena pasada en la cima de la pila
        #  (por encima de la actual)
        cls.pila.append(escena)

