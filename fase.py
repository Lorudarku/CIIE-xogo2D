
# -*- coding: utf-8 -*-
import pygame, escena
from escena import *
from personajes import *
from plataforma import Plataforma
from pygame.locals import *
from drunken import *
from menew import *
from pickUp import *
import csv
import numpy as np

# -------------------------------------------------
# -------------------------------------------------
# Constantes
nivel = 0

# Los bordes de la pantalla para hacer scroll vertical
'''
img_list = []
for x in range(TILE_TYPES):
    img = GestorRecursos.CargarImagen(f'{x}.png')
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)
'''
# -------------------------------------------------
# -------------------------------------------------
COLS = 25
ROWS = 15

# Los bordes de la pantalla para hacer scroll horizontal

# -------------------------------------------------
# Clase Fase
class Fase(Escena):
    def __init__(self, director,archivoFase):
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
        #print(datos)
        # Creamos el decorado y el fondo
        # self.decorado = Decorado(decorado)
        self.decorado = Decorado()
        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)#lo de el grupo que tal que pin que pan, cargar, el trece
        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((550, 550))
        
        # Creamos las plataformas del decorado
        # La plataforma que conforma todo el suelo
        #plataformaSuelo = Plataforma(pygame.Rect(0, 550, 1200, 15))
        cerbeza1=Beer(pygame.Rect(300, 450, 6, 16))
        self.grupoPlataformas = pygame.sprite.Group()
        self.grupoEnemigos = pygame.sprite.Group()
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1 )
        self.grupoSprites = pygame.sprite.Group( self.jugador1 )
        self.grupoPickUps=pygame.sprite.Group( cerbeza1 )
        self.procesar_datos(datos)

        
        
        

    def procesar_datos(self, datos):
       for y, fila in enumerate(datos):
          for x, tile in enumerate(fila):
                if tile >= 0:
                    #tile_data = ()
                    if tile >= 0 and tile <= 8:
                        wall = Plataforma(x * TILE_SIZE, y * TILE_SIZE, f'{tile}.png')
                        self.grupoPlataformas.add(wall)
                    if tile >= 9 and tile <= 12:
                        pass
                        decoracion = Decorado(f'{tile}.png') #tile_data)
                        self.grupoDecorado.add(decoracion)
                    if tile == 13:
                        pass
                        jugador1 = Jugador()
                        self.grupoEnemigos.add(jugador1)
                        self.grupoSpritesDinamicos.add(jugador1)
                        self.grupoSprites.add(jugador1)
                    if tile == 14:
                        pass
                        enemy = Jugador()
                        self.grupoEnemigos.add(enemy)
                        self.grupoSpritesDinamicos.add(enemy)
                        self.grupoSprites.add(enemy)
                    if tile == 15:
                        pass
                        #item = Item()
                        #self.grupoItems.add(item)

        
        
    def update(self, tiempo):
        self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
        self.grupoPickUps.update(self.jugador1,tiempo)
    
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.decorado.dibujar(pantalla)
        self.grupoPlataformas.draw(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)
        self.grupoPickUps.draw(pantalla)
    
    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()
            # Si se pulsa una tecla
            if evento.type == pygame.KEYDOWN:
                #Si es la tecla ESCAPE
                if evento.key == K_ESCAPE:
                    # Se muestra la pantalla de pausa
                    self.director.apilarEscena(MenuPausa(self.director))
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE)
   
      
       

class Decorado:
    def __init__(self,nombre='backgroundTest.png'):
        self.imagen = GestorRecursos.CargarImagen(nombre, -1)
        #cubo=GestorRecursos.CargarImagen("rectangulo-semitransparente.png", -1)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        #pygame.Surface.blit(self.imagen,cubo,(0, 550))
        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
    def update(self, scrollx):
        self.rectSubimagen.left = scrollx
    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

# -------------------------------------------------
# Clase Menu, la escena en sí
class Menu(Escena):

    def __init__(self, director):
        # Llamamos al constructor de la clase padre
        Escena.__init__(self, director)
        # Creamos la lista de pantallas
        self.listaPantallas = []
        # Creamos las pantallas que vamos a tener
        #   y las metemos en la lista
        self.listaPantallas.append(PantallaInicialGUI(self)) #0
        self.listaPantallas.append(PantallaOpcionesGUI(self)) #1
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director 
            if evento.type == pygame.QUIT: #Si se pulsa la X de la ventana
                self.director.salirPrograma()
        # Se pasa la lista de eventos a la pantalla actual
        self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

    def dibujar(self, pantalla):
        self.listaPantallas[self.pantallaActual].dibujar(pantalla)

    #--------------------------------------
    # Metodos propios del menu

    def salirPrograma(self):
        self.director.salirPrograma()

    def ejecutarJuego(self):    

        fase = Fase(self.director, "level_data0.csv")
        self.director.apilarEscena(fase)

    def mostrarPantallaOpciones(self, ingame=False):
        if ingame:
            self.pantallaActual = 2
        else:
            self.pantallaActual = 1

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0
    
    def subirVolumen(self):
        volumen = pygame.mixer.music.get_volume() + 0.1
        #redondeamos el volumen a 1 decimal
        volumen = round(volumen,1)
        if volumen >= 1:
            volumen = 1
        pygame.mixer.music.set_volume(volumen)
        self.listaPantallas[1].textList[2].actualizar(volumen*10)

    def bajarVolumen(self):
        volumen = pygame.mixer.music.get_volume() - 0.1
        #redondeamos el volumen a 1 decimal
        volumen = round(volumen,1)
        if volumen <= 0:
            volumen = 0
        pygame.mixer.music.set_volume(volumen)
        self.listaPantallas[1].textList[2].actualizar(volumen*10)

class MenuPausa(Escena):
    
        def __init__(self, director):
            # Llamamos al constructor de la clase padre
            Escena.__init__(self, director)
            # Creamos la lista de pantallas
            self.listaPantallas = []
            # Creamos las pantallas que vamos a tener
            #   y las metemos en la lista
            self.listaPantallas.append(PantallaPausaGUI(self)) #0
            # En que pantalla estamos actualmente
            self.mostrarPantallaOpcionesPausa()
    
        def update(self, *args):
            return
    
        def eventos(self, lista_eventos):
            # Se mira si se quiere salir de esta escena
            for evento in lista_eventos:
                # Si se quiere salir, se le indica al director 
                if evento.type == pygame.QUIT: #Si se pulsa la X de la ventana
                    self.director.salirPrograma()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == K_ESCAPE:
                        self.director.salirEscena()
            # Se pasa la lista de eventos a la pantalla actual
            self.listaPantallas[self.pantallaActual].eventos(lista_eventos)
    
        def dibujar(self, pantalla):
            self.listaPantallas[self.pantallaActual].dibujar(pantalla)
    
        #--------------------------------------
        # Metodos propios del menu de pausa
    
        def salirPrograma(self):
            self.director.salirPrograma()
    
        def mostrarPantallaOpcionesPausa(self, ingame=False):
            self.pantallaActual = 0

        def volverAJugar(self):
            self.director.salirEscena()

        def volverMenu(self):
            #Miramos el tamaño de la pila y desapilamos hasta que quede solo 1 elemento
            while len(self.director.pila) > 0:    
                self.director.salirEscena()
            #Creamos una nueva escena y la apilamos
            menu = Menu(self.director)
            self.director.apilarEscena(menu)

        def subirVolumen(self):
            volumen = pygame.mixer.music.get_volume() + 0.1
            #redondeamos el volumen a 1 decimal
            volumen = round(volumen,1)
            if volumen >= 1:
                volumen = 1
            pygame.mixer.music.set_volume(volumen)
            self.listaPantallas[0].textList[2].actualizar(volumen*10)

        def bajarVolumen(self):
            volumen = pygame.mixer.music.get_volume() - 0.1
            #redondeamos el volumen a 1 decimal
            volumen = round(volumen,1)
            if volumen <= 0:
                volumen = 0
            pygame.mixer.music.set_volume(volumen)
            self.listaPantallas[0].textList[2].actualizar(volumen*10)
