# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
import pyganim, PIL


# -------------------------------------------------
# Clase GestorRecursos

# En este caso se implementa como una clase vacía, solo con métodos de clase
class GestorRecursos(object):
    recursos = {}

    @classmethod
    def CargarAnimacion(cls, nombre, colorkey=None):
        #gifMenu = pyganim.PygAnimation('Menu/fondoMenu.gif')
        #gifMenu.play()
        #Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            #Se devuelve ese recurso
            return cls.recursos[nombre]
        #Si no ha sido cargado anteriormente
        else:
            #Se carga la animación indicando la carpeta en la que está
            fullname = os.path.join('imagenes', nombre)
            try:
                gif = pyganim.PygAnimation(fullname)
                gif.play()
            except pygame.error:
                print ('Cannot load animation:', fullname)
                raise SystemExit
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = gif.get_at((0,0))
                gif.set_colorkey(colorkey, RLEACCEL)
            #Se almacena en el diccionario de recursos
            cls.recursos[nombre] = gif
            return gif
            
    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join('imagenes', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error:
                print ('Cannot load image:', fullname)
                raise SystemExit
            # Para evitar convertir la transparencia
            if (nombre!="rectangulo-semitransparente.png"):
                imagen = imagen.convert()
                
            if colorkey is not None:
                if colorkey == -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join('imagenes', nombre)
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos

##################### YO! PREGUNTA AL PRFE SI GESTIONAR ESTE RECURSO #############################################################
    @classmethod
    def CargarFuenteTexto(cls,nombre,size): #Devuelve Press-Start-2P en el tamaño que le indiquemos     
        fullname = os.path.join('imagenes', nombre)
        return pygame.font.Font(fullname, size)
    
    @classmethod
    def CargarSonido(cls, nombre, esMusica):
     #Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            try:
                if (esMusica):
                    sound = pygame.mixer.music.load("sonidos/musica/" + nombre)    
                else:
                    sound = pygame.mixer.Sound("sonidos/" + nombre)
            except pygame.error:
                print ('Cannot load sound:', nombre)
                raise SystemExit
            # Se almacena
            cls.recursos[nombre] = sound
            # Se devuelve
            return sound
