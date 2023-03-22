
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
        self.decorado = Decorado('backgroundTest2.png',size=3)
        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group(self.jugador1)#lo de el grupo que tal que pin que pan, cargar, el trece
        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((550, 550))
        
        # Creamos las plataformas del decorado
        # La plataforma que conforma todo el suelo
        #plataformaSuelo = Plataforma(pygame.Rect(0, 550, 1200, 15))
        cerbeza1=Beer(pygame.Rect(800, 700, 6, 16))
        self.grupoPlataformas = pygame.sprite.Group()
        self.grupoEnemigos = pygame.sprite.Group()
        self.grupoMuros = pygame.sprite.Group()
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1 )
        self.grupoSprites = pygame.sprite.Group(  )
        self.grupoPickUps=pygame.sprite.Group( cerbeza1 )
        self.grupoSprites.add(cerbeza1)
        self.procesar_datos(datos)
        self.grupoSprites.add(self.jugador1)
        
    def procesar_datos(self, datos):
       for y, fila in enumerate(datos):
          for x, tile in enumerate(fila):
                if tile >= 0:
                    #tile_data = ()
                    if (tile >= 0 and tile <= 3) or (tile >= 5 and tile <= 8):
                        wall = Plataforma(x * TILE_SIZE, y * TILE_SIZE, f'{tile}.png')
                        self.grupoPlataformas.add(wall)
                        self.grupoSprites.add(wall)
                    if tile == 4:
                        wall = Plataforma(x * TILE_SIZE, y * TILE_SIZE, f'{tile}.png')
                        self.grupoMuros.add(wall)
                        self.grupoSprites.add(wall)
                    if tile >= 9 and tile <= 12:
                        pass
                        #decoracion = Decorado(f'{tile}.png') #tile_data)
                        #self.grupoDecorado.add(decoracion)
                    if tile == 13:
                        pass
                        
                    if tile == 14:
                        pass
                        # enemy = Jugador()
                        # self.grupoEnemigos.add(enemy)
                        # self.grupoSpritesDinamicos.add(enemy)
                        # self.grupoSprites.add(enemy)
                    if tile == 15:
                        pass
                        #item = Item()
                        #self.grupoItems.add(item)

    def update(self, tiempo):
        self.grupoSpritesDinamicos.update(self.grupoPlataformas, self.grupoMuros, tiempo)
        self.grupoPickUps.update(self.jugador1,tiempo)
        self.actualizarScroll(self.jugador1)
    
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        self.decorado.dibujar(pantalla)
        # self.grupoPlataformas.draw(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)
        # self.grupoPickUps.draw(pantalla)
    
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
   
      
    def actualizarScroll(self,jugador1):
        if jugador1.rect.center[1]<0:
            print("arriba")
            self.decorado.update("up")
            jugador1.establecerPosicion((jugador1.posicion[0],jugador1.posicion[1]+ALTO_PANTALLA-10))
        elif jugador1.rect.center[1]>ALTO_PANTALLA:
            print("abajo")
            self.decorado.update("down")
            jugador1.establecerPosicion((jugador1.posicion[0],jugador1.posicion[1]-ALTO_PANTALLA+10))

        #Si se cambio el scroll, hay que actualizar las posiciones de los sprites
        for sprite in self.grupoSprites:
            sprite.establecerPosicion((sprite.posicion[0],sprite.posicion[1]-self.decorado.rectSubimagen.top))

        

class Decorado:
    def __init__(self,backgroundName, size):
        self.imagen = GestorRecursos.CargarImagen(backgroundName, -1)
        self.imagen = pygame.transform.scale(self.imagen, ((ANCHO_PANTALLA, ALTO_PANTALLA*size)))

        self.rect = self.imagen.get_rect()
        self.rect.bottom = ALTO_PANTALLA*size
        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.top=ALTO_PANTALLA*(size-1)# El scroll vertical empieza en la posicion 1440 por defecto

    def update(self, dir):
        if dir=="up":
            self.rectSubimagen.bottom -= ALTO_PANTALLA
        elif dir=="down":
            self.rectSubimagen.bottom += ALTO_PANTALLA
    
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

        fase = Fase(self.director, "prueba.csv")
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
