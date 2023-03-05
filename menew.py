# -*- encoding: utf-8 -*-

import pygame
import pyganim
from pygame.locals import *
from escena import *
from gestorRecursos import *
from fase import Fase
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
        self.image = GestorRecursos.CargarImagen(image) #Imagen del boton
        self.pantalla=pantalla
        self.x_pos = pos[0] #Posicion x del boton
        self.y_pos = pos[1] #Posicion y del boton
        self.font = font #Fuente del texto del boton
        self.base_color = base_color #Color base del boton
        self.hovering_color = hovering_color #Color del boton cuando el raton pasa por encima
        self.text_input = text_input #Texto del boton
        self.text = self.font.render(self.text_input, True, self.base_color)  #Texto del boton
        if self.image is None: #Si no hay imagen, la imagen sera el texto
            self.image = self.text 
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos)) #Rectangulo del boton
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos)) #Rectangulo del texto del boton

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

class ReactiveButtonJugar(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        '''
        ReactiveButton.__init__(self, pantalla=pantalla, font=fuente, base_color="#d7fcd4", hovering_color="Green", imagen="rectangulo-semitransparente.png", 
        texto="Jugar", posicion=(600, 250))
        '''
        ReactiveButton.__init__(self, image="rectangulo-semitransparente.png", pos=(600, 250), text_input="Jugar", font=fuente, base_color="#d7fcd4", hovering_color="Green", pantalla=pantalla)
    
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class ReactiveButtonOpciones(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        
        """ ReactiveButton.__init__(self, pantalla=pantalla, font=fuente, base_color="#d7fcd4", hovering_color="Green", imagen="rectangulo-semitransparente.png", 
        texto="Opciones", posicion=(600, 400)) """
        
        ReactiveButton.__init__(self, image="rectangulo-semitransparente.png", pos=(600, 400), text_input="Opciones", font=fuente, base_color="#d7fcd4", hovering_color="Green", pantalla=pantalla)
    
    def accion(self):
        #################################PROVISIONAL,CAMBIAR A ESCENA OPCIONES###############################################
        self.pantalla.menu.ejecutarJuego()

class ReactiveButtonSalir(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        
        """ ReactiveButton.__init__(self, pantalla=pantalla, font=fuente, base_color="#d7fcd4", hovering_color="Green", imagen="rectangulo-semitransparente.png", 
        texto="Salir", posicion=(600, 550)) """
        ReactiveButton.__init__(self, image="rectangulo-semitransparente.png", pos=(600, 550), text_input="Salir", font=fuente, base_color="#d7fcd4", hovering_color="Green", pantalla=pantalla)
        
    def accion(self):
        self.pantalla.menu.salirPrograma()
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

class MenuText(Text):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 100)
        self.text = fuente.render("Menu", True, (255,255,255))
        Text.__init__(self, pantalla, self.text, (600,80))

        
# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
    def __init__(self, menu, nombreImagen):
        self.menu = menu
        # Se carga la imagen de fondo
        self.imagen = GestorRecursos.CargarImagen(nombreImagen)
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        # Se tiene una lista de elementos GUI
        self.elementosGUI = []
        # Se tiene una lista de elementos de texto
        self.textList = []
        # Se tiene una lista de animaciones
        self.animaciones = []


    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        # Después las animaciones
        for animacion in self.animaciones:
            animacion.dibujar(pantalla)
        # Después los botones
        for elemento in self.elementosGUI:
            elemento.dibujar(pantalla)
        # Después los textos
        for texto in self.textList:
            texto.dibujar(pantalla)

class PantallaInicialGUI(PantallaGUI):
    def __init__(self, menu):
        PantallaGUI.__init__(self, menu, 'fondoMenu1.gif')
        # Creamos los botones y los metemos en la lista
        botonJugar = ReactiveButtonJugar(self)
        botonOpciones = ReactiveButtonOpciones(self)
        botonSalir = ReactiveButtonSalir(self)
        textoMenu = MenuText(self)
    
        self.textList.append(textoMenu)
        self.elementosGUI.append(botonJugar)
        self.elementosGUI.append(botonOpciones)
        self.elementosGUI.append(botonSalir)
        # Creamos el texto y lo metemos en la lista
      
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
            # if evento.type == MOUSEMOTION:
            for elemento in self.elementosGUI:
               elemento.change_color(MOUSE_POS)

        """ for elemento in self.elementosGUI:
            elemento.changecolor(MOUSE_POS)
            elemento.changecolor(pygame.mouse.get_pos()) """
               
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
        self.listaPantallas.append(PantallaInicialGUI(self))
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

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...
