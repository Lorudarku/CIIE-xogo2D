# -*- encoding: utf-8 -*-

import pygame
import pyganim
from pygame.locals import *
from escena import *
from gestorRecursos import *
from fase import Fase
from math import *
# -------------------------------------------------
# Clase abstracta ElementoGUI

class ElementoGUI:
    def __init__(self, pantalla, rectangulo):
        self.pantalla = pantalla
        self.rect = rectangulo

    def establecerPosicion(self, posicion):
        (posicionx, posiciony) = posicion
        self.rect.left = posicionx
        self.rect.bottom = posiciony

    def posicionEnElemento(self, posicion_mouse):
        (posicionx, posiciony) = posicion_mouse
        if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
            return True
        else:
            return False

    def dibujar(self):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
    def accion(self):
        raise NotImplemented("Tiene que implementar el metodo accion.")



# -------------------------------------------------
# Clase reactive button
class ReactiveButton(ElementoGUI):
    '''
    def __init__(self, pantalla, font, base_color, hovering_color, imagen, texto, posicion ):
        self.imagen=GestorRecursos.CargarImagen(imagen)
        self.base_color = base_color #Color base del boton
        self.hovering_color = hovering_color #Color del boton cuando el raton pasa por encima
        self.font = font #Fuente del texto del boton
         #Posicion y del boton
        # Se llama al método de la clase padre con el rectángulo que ocupa 
        ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
        self.establecerPosicion(posicion)
        
        self.text_input = texto #Texto del boton
        self.text = self.font.render(self.text_input, True, self.base_color)  #Texto del boton
        ElementoGUI.__init__(self, pantalla, self.text.get_rect())
        self.establecerPosicion(posicion)
    '''
    def __init__(self, image, pos, text_input, font, base_color, hovering_color, pantalla):
        self.base_color = base_color #Color base del boton
        self.hovering_color = hovering_color #Color del boton cuando el raton pasa por encima
        
        self.image = GestorRecursos.CargarImagen(image) #Imagen del boton
        self.rect = self.image.get_rect(center=pos) #Rectangulo del boton

        self.font = font #Fuente del texto del boton
        self.text_input = text_input #Texto del boton
        self.text = self.font.render(self.text_input, True, self.base_color)  #Texto del boton
        self.text_rect = self.text.get_rect(center=pos) #Rectangulo del texto del boton

        ElementoGUI.__init__(self, pantalla, self.rect)


    #Cambia el color del boton cuando el raton pasa por encima
    def change_color(self, mouse_pos):
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
    
    #Actualiza la ventana
    def dibujar(self, pantalla): 
        if self.image is not None:
            pantalla.blit(self.image, self.rect)
        pantalla.blit(self.text, self.text_rect)

##### BOTONES PANTALLA INICIO #####
class ReactiveButtonJugar(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        ReactiveButton.__init__(self, "rectangulo-semitransparente.png",
            (600, 250),"Jugar",fuente,"#d7fcd4","Green",pantalla)
    
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class ReactiveButtonOpciones(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (600, 400),"Opciones",fuente,"#d7fcd4","Green",pantalla)
    
    def accion(self):
        self.pantalla.menu.mostrarPantallaOpciones()

class ReactiveButtonSalir(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (600, 550),"Salir",fuente,"#ffddda","Red",pantalla)
        
    def accion(self):
        self.pantalla.menu.salirPrograma()

##### BOTONES PANTALLA OPCIONES #####
class ReactiveButtonVolver(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 20)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (80, 30),"Volver",fuente,"#fff5b9","Yellow",pantalla)
        #Reescalamos la imagen y el rectangulo
        self.image = pygame.transform.scale(self.image, (130,40))
        self.rect = self.image.get_rect(center=(80, 30))
        
    def accion(self):
        self.pantalla.menu.mostrarPantallaInicial()

class ReactiveButtonMusicaMas(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (700, 250),">",fuente,"#abdbff","Blue",pantalla)
        #Reescalamos la imagen y el rectangulo
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect(center=(700, 250))
        
    def accion(self):
        self.pantalla.menu.subirVolumen()
        
class ReactiveButtonMusicaMenos(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (600, 250),"<",fuente,"#abdbff","Blue",pantalla)
        #Reescalamos la imagen y el rectangulo
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect(center=(600, 250))
        
    def accion(self):
        self.pantalla.menu.bajarVolumen()

# -------------------------------------------------
# Clase texto plano
""" class Text(ElementoGUI):
    def __init__(self, pos, text_input, font, base_color):
        self.x_pos = pos[0] #Posicion x del texto
        self.y_pos = pos[1] #Posicion y del texto
        self.font = font #Fuente del texto del boton
        self.base_color = base_color #Color base del boton
        self.text_input = text_input #Texto del boton
        self.text = self.font.render(self.text_input, True, self.base_color)  #Texto del boton
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos)) #Rectangulo del texto del boton
        
    #Actualiza la ventana
    def dibujar(self, ventana): 
        ventana.blit(self.text, self.text_rect)

class MenuText(Text):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 100)
        Text.__init__(self, (600, 100), "Menu", fuente, (255,255,255)) """

class Text(ElementoGUI):
    def __init__(self, pantalla, text, pos):
        self.text= text
        self.text_rect=text.get_rect(center=pos)
        ElementoGUI.__init__(self, pantalla, self.text_rect)
        
    #Actualiza la ventana
    def dibujar(self, pantalla): 
        pantalla.blit(self.text, self.text_rect)

#### Texto plano del menu inicial ####
class MenuText(Text):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 100)
        self.text = fuente.render("Menu", True, (255,255,255))
        Text.__init__(self, pantalla, self.text, (600,80))

#### Texto plano de la pantalla de opciones ####
class OpcionesText(Text):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 80)
        self.text = fuente.render("Opciones", True, (255,255,255))
        Text.__init__(self, pantalla, self.text, (550,80))

class MusicaText(Text):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        self.text = fuente.render("Musica", True, "#6fc1ff")
        Text.__init__(self, pantalla, self.text, (430,250))


class MedidorMusica(Text):
    def __init__(self, pantalla, medidor):
        #Convertrimos el valor del medidor a string
        medidor = str(floor(medidor))
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        self.text = fuente.render(medidor, True, "Orange")
        Text.__init__(self, pantalla, self.text, (650,250))

    def actualizar(self, medidor):
        #Convertrimos el valor del medidor a string
        medidor = str(floor(medidor))
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        self.text = fuente.render(medidor, True, "Orange")
        Text.__init__(self, self.pantalla, self.text, (650,250))

# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self, menu, nombreImagen1, nombreImagen2 = None):
        self.menu = menu
        self.es_animacion = False #Variable que indica si la imagen es un gif
        #Comprobamos si nombreImagen es una imagen o un gif
        if nombreImagen1[-3:] == "gif":
            self.imagen = GestorRecursos.CargarAnimacion(nombreImagen1)
            self.es_animacion = True
        # Si no, se carga la imagen de fondo
        else:
            self.es_animacion = False
            self.imagen = GestorRecursos.CargarImagen(nombreImagen1)
            self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))

        # Si se ha pasado una segunda imagen, se carga
        if nombreImagen2 != None:
            self.imagen2 = GestorRecursos.CargarImagen(nombreImagen2)
            self.imagen2 = pygame.transform.scale(self.imagen2, (ANCHO_PANTALLA, ALTO_PANTALLA))

        # Se tiene una lista de elementos GUI
        self.elementosGUI = []
        # Se tiene una lista de elementos de texto
        self.textList = []
        # Se tiene una lista de animaciones
        self.animaciones = []


    def dibujar(self, pantalla):
        #Si la imagen es un gif, se dibuja la animación
        if self.es_animacion:
            self.imagen.blit(pantalla, (0,0))
        #Si no, dibujamos la imagen de fondo
        else:
            pantalla.blit(self.imagen, self.imagen.get_rect())

        #Si existe imagen2, se dibuja
        if hasattr(self, "imagen2"):
            pantalla.blit(self.imagen2, self.imagen2.get_rect())
        
        # Después las animaciones
        for animacion in self.animaciones:
            animacion.dibujar(pantalla)
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)
        # Después los textos
        for texto in self.textList:
            texto.dibujar(pantalla)

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            MOUSE_POS = pygame.mouse.get_pos()
            if evento.type == MOUSEBUTTONDOWN:
                self.elementoClicado = None
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        self.elementoClicado = elemento
            if evento.type == MOUSEBUTTONUP:
                for elemento in self.elementosGUI:
                    if elemento.posicionEnElemento(evento.pos):
                        if (elemento == self.elementoClicado):
                            elemento.accion()
            for elemento in self.elementosGUI:
               elemento.change_color(MOUSE_POS)

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, menu):
        #Cargamos la musica inicial
        GestorRecursos.CargarSonido("Cry_Thunder_8bit.mp3",True)
        pygame.mixer.music.set_volume(0) #volumen inicial
        pygame.mixer.music.play()

        PantallaGUI.__init__(self, menu, 'fondoMenu.png')
        #PantallaGUI.__init__(self, menu, 'fondoMenu.gif')
        # Creamos los botones y los metemos en la lista
        botonJugar = ReactiveButtonJugar(self)
        botonOpciones = ReactiveButtonOpciones(self)
        botonSalir = ReactiveButtonSalir(self)
        textoMenu = MenuText(self)
    
        self.textList.append(textoMenu)
        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonOpciones)
        self.elementosGUI.append(botonSalir)
      
        
class PantallaOpcionesGUI(PantallaGUI):
    def __init__(self, menu):
        #Cargamos encima de la pantalla actual el fondo de opciones
        PantallaGUI.__init__(self, menu, 'fondoMenu.png', 'rectangulo-semitransparente.png')
        #PantallaGUI.__init__(self, menu, 'fondoMenu.gif', 'rectangulo-semitransparente.png')
  
        # Creamos los botones y los metemos en la lista
        botonVolver = ReactiveButtonVolver(self)
        botonMusicaMenos = ReactiveButtonMusicaMenos(self)
        botonMusicaMas = ReactiveButtonMusicaMas(self)
        self.elementosGUI.append(botonVolver)
        self.elementosGUI.append(botonMusicaMenos)
        self.elementosGUI.append(botonMusicaMas)
        # Creamos el texto y lo metemos en la lista
        textoOpciones = OpcionesText(self)
        textoMusica = MusicaText(self)
        medidorMusica = MedidorMusica(self, pygame.mixer.music.get_volume())
        self.textList.append(textoOpciones)
        self.textList.append(textoMusica)    
        self.textList.append(medidorMusica)
               
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
        self.auxBool = True
        self.listaPantallas.append(PantallaOpcionesGUI(self)) #1
        # En que pantalla estamos actualmente
        self.mostrarPantallaInicial()

    def update(self, *args):
        return

    def eventos(self, lista_eventos):
        # Se mira si se quiere salir de esta escena
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == KEYDOWN: #Si se pulsa una tecla
                if evento.key == K_ESCAPE: #Si es la tecla escape
                    self.salirPrograma()
            elif evento.type == pygame.QUIT: #Si se pulsa la X de la ventana
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

    def mostrarPantallaOpciones(self):
        self.pantallaActual = 1

    def mostrarPantallaInicial(self):
        if self.auxBool:
            self.subirVolumen()
            self.auxBool = False
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
