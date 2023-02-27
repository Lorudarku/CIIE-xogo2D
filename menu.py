################################################################################
#####                            Menu del juego                           ######
################################################################################

import pygame
import sys
from button import Button
from pygame.locals import *

#Inicializamos pygame
pygame.init()

#Creamos la VENTANA
VENTANA = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Menu")

#Cargamos el gif de fondo y lo escalamos a la VENTANA
gif = pygame.image.load("fondoMenu1.gif")
BACK_GROUND = pygame.transform.scale(gif, (1200, 720))


#Establecemos el temporizador para controlar el gif
clock = pygame.time.Clock()


def get_font(size): #Devuelve Press-Start-2P en el tamaño que le indiquemos
    return pygame.font.Font("Press-Start-2P.ttf", size)

def jugar(): #VENTANA de jugar
    pygame.display.set_caption("jugar")

    while True:

        PLAY_MOUSE_POS = pygame.mouse.get_pos() #Posicion del raton

        VENTANA.fill("black")

        PLAY_TEXT = get_font(25).render("Esta es la VENTANA de juego", True, 
                                         (255, 255, 255)) #Texto del juego
        PLAY_RECT = PLAY_TEXT.get_rect(center=(600, 100)) #Rectangulo del texto del juego
        VENTANA.blit(PLAY_TEXT, PLAY_RECT) #Ponemos el texto del juego

        PLAY_BACK_BUTTON = Button(image=None, pos=(640, 460), text_input="BACK",
            font=get_font(75), base_color="White", hovering_color="Green") #Boton de volver

        PLAY_BACK_BUTTON.change_color(PLAY_MOUSE_POS)
        PLAY_BACK_BUTTON.update(VENTANA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK_BUTTON.check_click(PLAY_MOUSE_POS):
                    main_menu()
        
        pygame.display.update()

def opciones(): #VENTANA de opciones
    pygame.display.set_caption("Opciones")

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos() #Posicion del raton

        VENTANA.fill("white")

        OPTIONS_TEXT = get_font(25).render("Esta es la VENTANA de opciones", True, (0, 0, 0)) #Texto de las opciones
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 100)) #Rectangulo del texto de las opciones
        
        VENTANA.blit(OPTIONS_TEXT, OPTIONS_RECT) #Ponemos el texto de las opciones

        OPTIONS_BACK_BUTTON = Button(image=None, pos=(640, 460), text_input="BACK",
            font=get_font(75), base_color="Black", hovering_color="Green") #Boton de volver

        OPTIONS_BACK_BUTTON.change_color(OPTIONS_MOUSE_POS)
        OPTIONS_BACK_BUTTON.update(VENTANA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK_BUTTON.check_click(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu(): #VENTANA del menu principal
    pygame.display.set_caption("Menu")

    while True:
        #Ponemos nuestro gif de fondo
        VENTANA.blit(BACK_GROUND, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos() #Posicion del raton

        MENU_TEXT = get_font(100).render("Menu", True, (255, 255, 255)) #Texto del menu
        MENU_RECT = MENU_TEXT.get_rect(center=(600, 100)) #Rectangulo del texto del menu

        PLAY_BUTTON = Button(image=None, pos=(640, 250), text_input="Jugar",
            font=get_font(25), base_color="#d7fcd4", hovering_color="White") #Boton de jugar
        OPTIONS_BUTTON = Button(image=None, pos=(640, 400), text_input="Opciones",
            font=get_font(25), base_color="#d7fcd4", hovering_color="White") #Boton de opciones
        EXIT_BUTTON = Button(image=None, pos=(640, 550), text_input="Salir",
            font=get_font(25), base_color="#d7fcd4", hovering_color="White") #Boton de salir

        VENTANA.blit(MENU_TEXT, MENU_RECT) #Ponemos el texto del menu

        for button in (PLAY_BUTTON, OPTIONS_BUTTON, EXIT_BUTTON): #Ponemos los botones
            button.change_color(MENU_MOUSE_POS)
            button.update(VENTANA)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_click(MENU_MOUSE_POS):
                    jugar()
                if OPTIONS_BUTTON.check_click(MENU_MOUSE_POS):
                    opciones()
                if EXIT_BUTTON.check_click(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(60) #Controlamos el gif

main_menu()