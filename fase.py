
# -*- coding: utf-8 -*-
import pygame, escena
from escena import *
from personajes import *
from plataforma import Plataforma
from pygame.locals import *
from drunken import *
from menew import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------


# Los bordes de la pantalla para hacer scroll horizontal

# -------------------------------------------------
# Clase Fase
class Fase(Escena):
    def __init__(self, director):
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
            # Si se pulsa una tecla
            if evento.type == pygame.KEYDOWN:
                #Si es la tecla ESCAPE
                if evento.key == K_ESCAPE:
                    # Se muestra la pantalla de pausa
                    self.director.apilarEscena(MenuPausa(self.director))
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
        fase = Fase(self.director)
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
                #Si se pulsa una tecla
                if evento.type == pygame.KEYDOWN:
                    #Si esa tecla es ESC
                    if evento.key == pygame.K_ESCAPE:
                        #Si estamos en el menu
                        if self.pantallaActual == 0:
                            #Se sale del programa
                            self.director.salirPrograma()
                        #Si estamos en las opciones
                        if self.pantallaActual == 1:
                            #Se vuelve al menu
                            self.mostrarPantallaPausa()
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