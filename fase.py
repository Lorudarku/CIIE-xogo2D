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

#img_list = []
#for x in range(TILE_TYPES):
#    img = GestorRecursos.CargarImagen(f'{x}.png')
#    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
#    img_list.append(img)

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
        #self.decorado = Decorado()
        #self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group()

        # Ponemos a los jugadores en sus posiciones iniciales
        #self.jugador1.establecerPosicion((200, 400))
        
        # Creamos las plataformas del decorado
        # La plataforma que conforma todo el suelo
        #plataformaSuelo = Plataforma(pygame.Rect(0, 550, 1200, 15))
        self.grupoPlataformas = pygame.sprite.Group()
        self.grupoSpritesDinamicos = pygame.sprite.Group()
        self.grupoSprites = pygame.sprite.Group()
        self.grupoEnemigos = pygame.sprite.Group()

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
    
    def procesar_datos(self, datos):
       for y, fila in enumerate(datos):
          for x, tile in enumerate(fila):
                if tile >= 0 and tile <= 8:
                    wall = Plataforma()
                    self.grupoPlataformas.add(wall)
                if tile >= 9 and tile <= 12:
                    decoracion = Decorado()
                    self.grupoDecorado.add(decoracion)
                if tile == 13:
                    player = Jugador()
                    self.grupoEnemigos.add(player)
                    self.grupoSpritesDinamicos.add(player)
                    self.grupoSprites.add(player)
                if tile == 14:
                    enemy = Jugador()
                    self.grupoEnemigos.add(enemy)
                    self.grupoSpritesDinamicos.add(enemy)
                    self.grupoSprites.add(enemy)
                if tile == 15:
                    pass
                    #item = Item()
                    #self.grupoItems.add(item)
                    
       
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
