class Button():
    # Inicializa el boton
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image #Imagen del boton
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

    # Cambia el color del boton cuando el raton pasa por encima
    def change_color(self, mouse_pos):
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
    
    # Actualiza la ventana
    def update(self, ventana): 
        if self.image is not None:
            ventana.blit(self.image, self.rect)
        ventana.blit(self.text, self.text_rect) 

    # Comprueba si el boton ha sido pulsado
    def check_click(self, mouse_pos):
        if mouse_pos[0] in range(self.rect.left, self.rect.right) and mouse_pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        else:
            return False