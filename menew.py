# -*- encoding: utf-8 -*-

import pygame
import pyganim
from pygame.locals import *
from escena import *
from gestorRecursos import *
from math import *
from random import randint
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
            (ANCHO_PANTALLA/2, ALTO_PANTALLA/2.88),"Jugar",fuente,"#d7fcd4","Green",pantalla)
    
    def accion(self):
        self.pantalla.menu.ejecutarJuego()

class ReactiveButtonOpciones(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (ANCHO_PANTALLA/2, ALTO_PANTALLA/1.8),"Opciones",fuente,"#d7fcd4","Green",pantalla)
    
    def accion(self):
        self.pantalla.menu.mostrarPantallaOpciones(False)

class ReactiveButtonSalir(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (ANCHO_PANTALLA/2, ALTO_PANTALLA/1.31),"Salir",fuente,"#ffddda","Red",pantalla)
        
    def accion(self):
        self.pantalla.menu.salirPrograma()

##### BOTONES PANTALLA OPCIONES #####
class ReactiveButtonVolver(ReactiveButton):
    def __init__(self, pantalla, ingame=False):
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
            (750, 350),">",fuente,"#abdbff","Blue",pantalla)
        #Reescalamos la imagen y el rectangulo
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect(center=(750, 350))
        
    def accion(self):
        self.pantalla.menu.subirVolumen()
        
class ReactiveButtonMusicaMenos(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (650, 350),"<",fuente,"#abdbff","Blue",pantalla)
        #Reescalamos la imagen y el rectangulo
        self.image = pygame.transform.scale(self.image, (40,40))
        self.rect = self.image.get_rect(center=(650, 350))
        
    def accion(self):
        self.pantalla.menu.bajarVolumen()

class ReactiveButtonContinuar(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 35)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (600, 250),"Continuar",fuente,"#d7fcd4","Green",pantalla)
        #Reescalamos la imagen y el rectangulo
        self.image = pygame.transform.scale(self.image, (380,80))
        self.rect = self.image.get_rect(center=(600, 250))
        
    def accion(self):
            self.pantalla.menu.volverAJugar()

class ReactiveButtonVolverMenu(ReactiveButton):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 35)
        ReactiveButton.__init__(self,"rectangulo-semitransparente.png",
            (600, 450),"Volver al menu",fuente,"#fff5b9","Yellow",pantalla)
        #Reescalamos la imagen y el rectangulo
        self.image = pygame.transform.scale(self.image, (500,80))
        self.rect = self.image.get_rect(center=(600, 450))
        
    def accion(self):
        self.pantalla.menu.volverMenu()

# -------------------------------------------------
# Clase texto plano
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
        Text.__init__(self, pantalla, self.text, (600,80))

class MusicaText(Text):
    def __init__(self, pantalla):
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        self.text = fuente.render("Musica", True, "#6fc1ff")
        Text.__init__(self, pantalla, self.text, (480,350))


class MedidorMusica(Text):
    def __init__(self, pantalla, medidor):
        #Convertrimos el valor del medidor a string
        medidor = str(round(medidor*10,0))
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        self.text = fuente.render(medidor[0], True, "Orange")
        Text.__init__(self, pantalla, self.text, (700,350))

    def actualizar(self, medidor):
        #Convertrimos el valor del medidor a string
        medidor = str(floor(medidor))
        fuente = GestorRecursos.CargarFuenteTexto("Press-Start-2P.ttf", 40)
        self.text = fuente.render(medidor, True, "Orange")
        Text.__init__(self, self.pantalla, self.text, (700,350))

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
        #Creamos un array de strings con los nombres de las canciones
        canciones = ["Cry_Thunder_8bit.mp3", "Fury_Of_The_Storm_8bit.mp3", "Through_The_Fire_And_Flames_8bit.mp3"]
        #Escogemos un numero aleatorio entre 0 y 2
        numeroCancion = randint(0,2)
        #Cargamos la musica inicial
        GestorRecursos.CargarSonido(canciones[numeroCancion],True)
        pygame.mixer.music.set_volume(round(0.1,1)) #volumen inicial
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
      
#Pantalla de opciones desde el menu principal     
class PantallaOpcionesGUI(PantallaGUI):
    def __init__(self, menu):
        #Cargamos encima de la pantalla actual el fondo de opciones
        PantallaGUI.__init__(self, menu, 'fondoMenu.png', 'rectangulo-semitransparente.png') #Se carga el fondo del menu y despues el rectangulo semitransparente
        #PantallaGUI.__init__(self, menu, 'fondoMenu.gif', 'rectangulo-semitransparente.png')
        

        # Creamos los botones y los metemos en la lista
        botonVolver = ReactiveButtonVolver(self, False)
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
               
#Pantalla de opciones desde el juego
class PantallaPausaGUI(PantallaGUI):
    def __init__(self, menu):
        #Cargamos encima de la pantalla actual el fondo de opciones
        PantallaGUI.__init__(self, menu, 'fondoPausa.png', 'rectangulo-semitransparente.png') #No se carga el fondo del menu por encima
        # Creamos los botones y los metemos en la lista
        botonContinuar = ReactiveButtonContinuar(self)
        botonVolverMenu = ReactiveButtonVolverMenu(self)
        botonMusicaMas = ReactiveButtonMusicaMas(self)
        botonMusicaMenos = ReactiveButtonMusicaMenos(self)
        self.elementosGUI.append(botonContinuar)
        self.elementosGUI.append(botonVolverMenu)
        self.elementosGUI.append(botonMusicaMas)
        self.elementosGUI.append(botonMusicaMenos)

        # Creamos el texto y lo metemos en la lista
        textoOpciones = OpcionesText(self)
        textoMusica = MusicaText(self)
        medidorMusica = MedidorMusica(self, pygame.mixer.music.get_volume())
        self.textList.append(textoOpciones)
        self.textList.append(textoMusica)    
        self.textList.append(medidorMusica)
