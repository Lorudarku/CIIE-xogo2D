import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *
from physics import *
import math

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4
ESPACIO=5
ESPACIOD=6
ESPACIOI=7
ESPACIOAR=8
ESPACIOAB=9
ESPACIODAR=10
ESPACIODAB=11
ESPACIOIAR=12
ESPACIOIAB=13
#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_AGACHADO = 2
SPRITE_SALTANDO = 3
SPRITE_CAYENDO = 4
SPRITE_APLASTADO = 5

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 1.4 # Pixeles por milisegundo
VELOCIDAD_MAXIMA_JUGADOR=15
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura

# updates que durará cada imagen del personaje
 
GRAVEDAD = 0.0003 # Píxeles / ms2


class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)

        self.speed = 0
        self.angle = 0
        
        self.maxJumpCount = 30
        self.jumpCount=0
        self.physics=Physics()
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollDecorado):
        self.scroll = scrollDecorado;
        (scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion;
        self.rect.left = posx - scrollx;
        self.rect.bottom = posy - scrolly;

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = math.sin(self.angle) * self.speed
        incrementoy = -math.cos(self.angle) * self.speed
        self.incrementarPosicion((incrementox, incrementoy))


####################################################################################
class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, walkSpeed, velocidadSalto, retardoAnimacion,maxSpeed):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);
        self.creativo=False
        # Se carga la hoja
        self.dashes=0
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = IZQUIERDA

        # Leemos las coordenadas de un archivo de texto
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 1;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, 6):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.numPostura = QUIETO

        # El rectangulo del Sprite
        self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

        # Las velocidades de caminar y salto
        self.walkSpeed = walkSpeed

        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion

        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    def add_gravity(self):
        self.angle, self.speed = self.physics.add_vectors(self.angle, self.speed, self.physics.gravity[0], self.physics.gravity[1])
  
        
    def saltar(self,direccion):
        print("salteeeeee")
            
        speed = (1.5 + ((self.jumpCount/5)**1.13))
        if direccion == "arriba":
            angle=0
        elif direccion == "derecha":
            angle= math.pi/3 * (1 - self.jumpCount / 45.5)
            speed += 0.9
        elif direccion == "izquierda":
            angle= -math.pi/3 * (1 - self.jumpCount / 45.5)
            speed += 0.9
        
        self.numPostura=SPRITE_SALTANDO
        self.jumpCount = 0
        
        return self.physics.add_vectors(self.angle, self.speed, angle, speed)
     
    def dash(self,direccion):
        print("dashieeeeee",direccion)
        speed = 10
        
        if direccion==ESPACIOAR:
            angle=0       
        
        elif direccion==ESPACIOAB:
            angle= math.pi
            
        elif direccion==ESPACIOD:
            angle= math.pi/2
            
        elif direccion==ESPACIOI:
            angle= -math.pi/2

        elif direccion==ESPACIODAR:
            angle= math.pi/4

        elif direccion==ESPACIODAB:
            angle= 3*math.pi/4

        elif direccion==ESPACIOIAR:
            angle= -math.pi/4

        elif direccion==ESPACIOIAB:
            angle= -3*math.pi/4
            
        return angle,speed

    def checarColisionAbajo(self, plataforma):
        #   DERECHA PLATAFORMA
        v1x=self.rect.bottomleft[0]-plataforma.rect.center[0]
        v1y=self.rect.bottomleft[1]-plataforma.rect.center[1]
        #diagonal derecha plataforma
        v2x=plataforma.rect.topright[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.topright[1]-plataforma.rect.center[1]
        
        #derecha negativa || izquierda positiva
        pendienteSelfL= math.atan(v1x/v1y) #por la derecha tiene que ser mayor
        pendientePlatL= math.atan(v2x/v2y)

        #   IZQUIERDA PLATAFORMA
        v1x=self.rect.bottomright[0]-plataforma.rect.center[0]
        v1y=self.rect.bottomright[1]-plataforma.rect.center[1]
        #diagonal izquierda plataforma
        v2x=plataforma.rect.topleft[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.topleft[1]-plataforma.rect.center[1]

        pendienteSelfR= math.atan(v1x/v1y) #por la derecha tiene que ser mayor
        pendientePlatR= math.atan(v2x/v2y)
        print("pendienteSelfR" ,pendienteSelfR)
        print("pendientePlatR" ,pendientePlatR)
        
        if (self.rect.bottom > plataforma.rect.top) and ( 
                (self.rect.left>plataforma.rect.left and self.rect.right<plataforma.rect.right)
                or (plataforma.rect.center[0]<self.rect.bottomleft[0] and pendienteSelfL>=pendientePlatL)
                or (plataforma.rect.center[0]>self.rect.bottomright[0] and pendienteSelfR<=pendientePlatR)
                ):
            return True
        else:        
            return False
        
    def checarColisionDerecha(self, plataforma):
        #   ARRIBA PLATAFORMA
        v1x=self.rect.bottomright[0]-plataforma.rect.center[0]
        v1y=self.rect.bottomright[1]-plataforma.rect.center[1]
        #diagonal derecha plataforma
        v2x=plataforma.rect.topleft[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.topleft[1]-plataforma.rect.center[1]
        
        #derecha negativa || izquierda positiva
        pendienteSelfL= math.atan(v1x/v1y) #por la derecha tiene que ser mayor
        pendientePlatL= math.atan(v2x/v2y)

        #   ABAJO PLATAFORMA
        v1x=self.rect.topright[0]-plataforma.rect.center[0]
        v1y=self.rect.topright[1]-plataforma.rect.center[1]
        #diagonal izquierda plataforma
        v2x=plataforma.rect.bottomleft[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.bottomleft[1]-plataforma.rect.center[1]

        pendienteSelfR= math.atan(v1x/v1y) #por la derecha tiene que ser mayor
        pendientePlatR= math.atan(v2x/v2y)
        print("pendientePlatR",pendientePlatR)
        print("pendienteSelfR",pendienteSelfR)
        
        if (self.rect.bottom > plataforma.rect.top) and ( 
                self.rect.left>plataforma.rect.left and self.rect.right<plataforma.rect.right
                or plataforma.rect.center[0]<self.rect.bottomleft[0] and pendienteSelfL>=pendientePlatL
                or plataforma.rect.center[0]>self.rect.bottomright[0] and pendienteSelfR<=pendientePlatR
                ):
            return True
        else:        
            return False
        
    #comprueba las colisiones del personaje devolviendo una tupla de cuatro booleanos (por las cuatro dirrecciones)
    def checkCollisions(self,grupoPlataformas):
        plataformas = pygame.sprite.spritecollide(self, grupoPlataformas)
        colisiones=(False,False,False,False) #([0]ABAJO, [1]ARRIBA, [2]DERECHA, [3]IZQUIERDA)
        if (plataformas != None):
            for plataforma in plataformas:
                self.rect.c
                if (self.checarColisionAbajo(plataforma)): #abajo
                    colisiones[0]=True
                elif (plataforma.rect.bottom>self.rect.top): #arriba
                    colisiones[1]=True
                elif (plataforma.rect.left>self.rect.right): #derecha
                    colisiones[2]=True
                elif (plataforma.rect.right>self.rect.left): #izquierda
                    colisiones[3]=True
            
        return colisiones
            
               
        
    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
        self.movimiento = movimiento

    def moveset(self,grupoPlataformas):
        angle=self.angle
        speed=self.speed
        # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
        #  Para ello, miramos si hay colision con alguna plataforma del grupo
        plataforma = pygame.sprite.spritecollideany(self, grupoPlataformas)
        
        #  Ademas, esa colision solo nos interesa cuando estamos cayendo
        #  y solo es efectiva cuando caemos encima, no de lado, es decir,
        #  cuando nuestra posicion inferior esta por encima de la parte de abajo de la plataforma
        if (plataforma != None)  and (self.checarColisionAbajo(plataforma)):
            print(self.checarColisionAbajo(plataforma))
            # Lo situamos con la parte de abajo un pixel colisionando con la plataforma
            #  para poder detectar cuando se cae de ella
            #self.establecerPosicion((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height+1))
            # self.checarColisionDerecha(plataforma)
            # Lo ponemos como quieto
            # Y estará quieto en el eje y
            speed=0

        if self.creativo!=True:
            if self.numPostura == SPRITE_SALTANDO or self.numPostura == SPRITE_CAYENDO:
                # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
                
                if self.movimiento in (ESPACIOD,ESPACIOI,ESPACIOAB,ESPACIOAR,ESPACIODAR,ESPACIODAB,ESPACIOIAR,ESPACIODAB) and self.dashes>0:
                    angle,speed=self.dash(self.movimiento)  
                self.movimiento = QUIETO  
            else:
                

                # Si vamos a la izquierda o a la derecha        
                if (self.movimiento == IZQUIERDA):
                    
                    self.mirando = self.movimiento
                    #si no está agachado AKA cargando el salto, se mueve
                    if not self.numPostura==SPRITE_AGACHADO:
                            angle=-math.pi/2
                            speed=self.walkSpeed
                    else :
                        angle,speed=self.saltar("izquierda")
                        self.numPostura =SPRITE_SALTANDO

                    # Si no estamos en el aire
                    if self.numPostura != SPRITE_SALTANDO:
                        # La postura actual sera estar caminando
                        self.numPostura = SPRITE_ANDANDO
                        # Ademas, si no estamos encima de ninguna plataforma, caeremos
                        if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                            self.numPostura = SPRITE_SALTANDO   

                elif (self.movimiento == DERECHA):
                    
                    self.mirando = self.movimiento
                    #si no está agachado AKA cargando el salto, se mueve
                    if not self.numPostura== SPRITE_AGACHADO:
                    # Esta mirando hacia ese lado
                        angle=math.pi/2
                        speed=self.walkSpeed
                    else:
                        angle,speed=self.saltar("derecha")
                        self.numPostura =SPRITE_SALTANDO

                    
                    # Si no estamos en el aire
                    if self.numPostura != SPRITE_SALTANDO:
                        # La postura actual sera estar caminando
                        self.numPostura = SPRITE_ANDANDO
                        # Ademas, si no estamos encima de ninguna plataforma, caeremos
                        if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                            self.numPostura = SPRITE_SALTANDO

                # Si queremos saltar
                #elif self.movimiento == ESPACIO or self.movimiento == ESPACIOD or self.movimiento == ESPACIOI:
                elif self.movimiento in (ESPACIO,ESPACIOD,ESPACIOI):
                    self.jumpCount += 1
                
                    
                    if self.numPostura != SPRITE_AGACHADO:
                        self.numPostura =SPRITE_AGACHADO

                    elif self.jumpCount>self.maxJumpCount:
                        if self.movimiento==ESPACIOD: 
                            self.mirando = self.movimiento
                            angle,speed=self.saltar("derecha")
                        elif self.movimiento==ESPACIOI:
                            self.mirando = self.movimiento
                            angle,speed=self.saltar("izquierda")
                        else:
                            self.establecerPosicion((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height-3))
                            angle,speed=self.saltar("arriba")
                    
                
            
                # Si no se ha pulsado ninguna tecla
            if self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
                if not self.numPostura == SPRITE_SALTANDO or (speed==0 and plataforma!=None):
                    self.numPostura = SPRITE_QUIETO

        else:
            if (self.movimiento == IZQUIERDA):  
                angle=-math.pi/2
                speed=5
            elif (self.movimiento == DERECHA):
                angle=math.pi/2
                speed=5
            elif (self.movimiento == ARRIBA): 
                angle=0
                speed=5
            elif (self.movimiento == ABAJO): 
                angle=math.pi
                speed=5
            elif (self.movimiento == QUIETO):
                speed=0               
        
        
        
        # Además, si estamos en el aire
        #if self.numPostura == SPRITE_SALTANDO:
        
        
        self.angle=angle
        
        self.speed=speed
            # Si no caemos en una plataforma, aplicamos el efecto de la gravedad


    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;
            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1
            self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

        
            #  Si no, si mira a la derecha, invertimos esa imagen
            if self.mirando == DERECHA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            elif self.mirando == IZQUIERDA:
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)


    def update(self, grupoPlataformas, tiempo):
        
        
        self.add_gravity()
        self.moveset(grupoPlataformas)
        
        self.actualizarPostura()
        # print(self.speed)
        
        if self.speed>VELOCIDAD_MAXIMA_JUGADOR: 
            self.speed=VELOCIDAD_MAXIMA_JUGADOR
        
        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite
        MiSprite.update(self, tiempo)
        
        return



# -------------------------------------------------
# Clase Jugador


# -------------------------------------------------
# Clase NoJugador

class NoJugador(Personaje):
    "El resto de personajes no jugadores"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    def mover_cpu(self, jugador1):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)
        return

