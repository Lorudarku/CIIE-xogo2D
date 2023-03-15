# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from plataforma import Plataforma
from pygame.locals import *
from drunken import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
COLUMNAS = 25
FILAS = 15
TILE_SIZE = escena.ALTO_PANTALLA // COLUMNAS
TILE_TYPES = 16
nivel = 0

# Los bordes de la pantalla para hacer scroll vertical

img_list = []
for x in range(TILE_TYPES):
    img = GestorRecursos.CargarImagen(f'{nivel}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# -------------------------------------------------
# Clase Fase

class Fase(Escena):
    def __init__(self, director, archivoFase):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)
        datos = GestorRecursos.CargarArchivoFase(archivoFase)
        # Creamos el decorado y el fondo
        self.decorado = Decorado()
        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group( self.jugador1)

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((200, 400))
        
        # Creamos las plataformas del decorado
        # La plataforma que conforma todo el suelo
        plataformaSuelo = Plataforma(pygame.Rect(0, 550, 1200, 15))
        self.grupoPlataformas = pygame.sprite.Group( plataformaSuelo)
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1 )
        self.grupoSprites = pygame.sprite.Group( self.jugador1 )

    def update(self, tiempo):

        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
       
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.decorado.dibujar(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)
    
    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)
       
class Decorado:
    def __init__(self):
        self.imagen = GestorRecursos.CargarImagen('backgroundTest.png', -1)
        cubo=GestorRecursos.CargarImagen("rectangulo-semitransparente.png", -1)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.Surface.blit(self.imagen,cubo,(0, 550, 1200, 15))
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto

    def update(self, scrollx):
        self.rectSubimagen.left = scrollx

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

class Nivel():
    def __init__(self):
        self.obstacultos = []
    
    def procesar_datos(self, datos):
        for y, fila in enumerate(datos):
            for x, tile in enumerate(fila):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    