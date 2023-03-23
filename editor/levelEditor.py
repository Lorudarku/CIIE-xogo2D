import pygame
import button
import csv

pygame.init()


clock = pygame.time.Clock()
FPS = 60

#ventana
SCREEN_WIDTH = 1200
SCREEN_HEIGTH = 720
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGTH))
pygame.display.set_caption('Level editor')


#variables
COLS = 25
MAX_ROWS = 16
TILE_SIZE = SCREEN_WIDTH // COLS
TILE_TYPES = 17
level = 0
current_tile = 0
scroll_up = False
scroll_down = False
scroll = 0
scroll_speed = 1

#colores
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#definir fuente
font = pygame.font.SysFont('Futura', 20)

#crear una lista de tiles
world_data = []
for col in range(MAX_ROWS):
    c = [-1] * COLS
    world_data.append(c)

#cargar imagenes
background = pygame.image.load('editor/img/background/bg.png').convert_alpha()
particles = pygame.image.load('editor/img/background/bg1.png').convert_alpha()

#almacenar tiles en una lista
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'editor/img/tile/{x}.png').convert_alpha()
    img =  pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('editor/img/save_btn.png').convert_alpha()
load_img = pygame.image.load('editor/img/load_btn.png').convert_alpha()

#texto en pantalla
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#dibujar background
def draw_bg():
    screen.fill(GREEN)
    heigth = background.get_height()
    for x in range(10):
        screen.blit(background, (0, (x * heigth) - scroll))
        screen.blit(particles, (0, (x * heigth) - scroll))

#dibujar los tiles
def draw_world():
    for y, col in enumerate(world_data):
        for x, tile in enumerate(col):
            if tile >= 0:
                screen.blit(img_list[tile],(x * TILE_SIZE, y * TILE_SIZE - scroll))

#dibujar cuadricula
def draw_grid():
    #lineas verticales
    for c in range(COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE, 0), (c * TILE_SIZE, SCREEN_HEIGTH))
    
    #lineas horizontales
    for c in range(MAX_ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE - scroll), (SCREEN_WIDTH, c * TILE_SIZE - scroll))

#crear botones
save_button = button.Button(SCREEN_WIDTH + SIDE_MARGIN - 250, SCREEN_HEIGTH - 75, save_img, 1)
load_button = button.Button(SCREEN_WIDTH + SIDE_MARGIN - 125, SCREEN_HEIGTH - 75, load_img, 1)
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = button.Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row +=1
        button_col = 0

run = True
while run:

    clock.tick(FPS)

    draw_bg()
    draw_grid()
    draw_world()
    draw_text(f'Level: {level}', font, WHITE, SCREEN_WIDTH + SIDE_MARGIN - 170, SCREEN_HEIGTH - 140)
    draw_text('RKEY o LKEY para cambiar nivel', font, WHITE, SCREEN_WIDTH + SIDE_MARGIN - 250, SCREEN_HEIGTH - 110)

    #save y load
    if save_button.draw(screen):
        #guardar nivel
        with open(f'niveles/level_data{level}.csv', 'w', newline='') as csvfile:
            write = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                write.writerow(row)
    if load_button.draw(screen):
        #cargar nivel
        #mover el scroll al inicio del nivel
        scroll = 0
        with open(f'niveles/level_data{level}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
                
    #escoger un tile
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    
    #destacar el tile seleccionado
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 2)

    #scroll
    if scroll_up == True and scroll > 0:
        scroll -= 2 * scroll_speed
    if scroll_down == True and scroll < (MAX_ROWS * TILE_SIZE) - SCREEN_HEIGTH:
        scroll += 2 * scroll_speed

    pos = pygame.mouse.get_pos()
    x = pos[0] // TILE_SIZE
    y = (pos[1] + scroll) // TILE_SIZE

    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGTH:
		#update tile value
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile         
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #teclas pulsadas
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                level += 1
            if event.key == pygame.K_LEFT and level > 0:
                level -= 1
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_DOWN:
                scroll_down = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()