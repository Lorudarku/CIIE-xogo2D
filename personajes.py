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
ESTADO_QUIETO = 0
ESTADO_ANDANDO = 1
ESTADO_AGACHADO = 2
ESTADO_AIRE = 3





# Velocidades de los distintos personajes
 # updates que durará cada imagen del personaje
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
        
        
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] 
        self.rect.bottom = self.posicion[1] 

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
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, walkSpeed, velocidadSalto, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);
        self.creativo=True
        self.maxJumpCount = 33
        self.jumpCount=0
        self.physics=Physics()
        self.estado=ESTADO_QUIETO


        # Se carga la hoja
        self.potaCount=0
        self.dashes=0
        self.hoja = GestorRecursos.CargarImagen(archivoImagen)
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
        for linea in range(0, numImagenes.__len__()):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;

        # En que postura esta inicialmente
        self.estado = ESTADO_QUIETO

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
        
            
        speed = (1.5 + ((self.jumpCount/5)**1.13))
        if direccion == "arriba":
            angle=0
        elif direccion == "derecha":
            angle= math.pi/3 * (1 - self.jumpCount / 45.5)
            speed += 0.9
        elif direccion == "izquierda":
            angle= -math.pi/3 * (1 - self.jumpCount / 45.5)
            speed += 0.9
        
        self.estado=ESTADO_AIRE
        self.jumpCount = 0
        
        return self.physics.add_vectors(self.angle, self.speed, angle, speed)
     
    
    def div(self,n, d):
        return n / d if d else 0

    def checarColisionAbajo(self, plataforma):
        #   DERECHA PLATAFORMA
        v1x=self.rect.bottomleft[0]+5-plataforma.rect.center[0]
        v1y=self.rect.bottomleft[1]+5-plataforma.rect.center[1]
        
        #diagonal derecha plataforma
        v2x=plataforma.rect.topright[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.topright[1]-plataforma.rect.center[1]
        
        #derecha negativa || izquierda positiva
        pendienteSelfL= math.atan(self.div(v1x,v1y)) #por la derecha tiene que ser mayor
        pendientePlatL= math.atan(self.div(v2x,v2y))

        #   IZQUIERDA PLATAFORMA
        v1x=self.rect.bottomright[0]-5-plataforma.rect.center[0]
        v1y=self.rect.bottomright[1]-5-plataforma.rect.center[1]
        #diagonal izquierda plataforma
        v2x=plataforma.rect.topleft[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.topleft[1]-plataforma.rect.center[1]

        pendienteSelfR= math.atan(self.div(v1x,v1y)) #por la derecha tiene que ser mayor
        pendientePlatR= math.atan(self.div(v2x,v2y))
        
        if (self.rect.bottom > plataforma.rect.top > self.rect.top) and ( 
                (self.rect.left>plataforma.rect.left<plataforma.rect.right)
                or self.rect.left>plataforma.rect.left<plataforma.rect.right
                or (plataforma.rect.center[0]<self.rect.bottomleft[0]<plataforma.rect.right and pendienteSelfL>=pendientePlatL)
                or (plataforma.rect.center[0]>self.rect.bottomright[0]>plataforma.rect.left and pendienteSelfR<=pendientePlatR)
                )and(
                    (math.pi/2<self.angle<3*math.pi/2) or (-math.pi/2>self.angle>-3*math.pi/2)
                ):
            return True
        else:        
            return False
    
    def checarColisionArriba(self, plataforma):
        #   DERECHA PLATAFORMA
        v1x=self.rect.topleft[0]-plataforma.rect.center[0]
        v1y=self.rect.topleft[1]-plataforma.rect.center[1]
        
        #diagonal derecha plataforma
        v2x=plataforma.rect.bottomright[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.bottomright[1]-plataforma.rect.center[1]
        
        #derecha negativa || izquierda positiva
        pendienteSelfL= math.atan(self.div(v1x,v1y)) #por la derecha tiene que ser mayor
        pendientePlatL= math.atan(self.div(v2x,v2y))

        #   IZQUIERDA PLATAFORMA
        v1x=self.rect.topright[0]-plataforma.rect.center[0]
        v1y=self.rect.topright[1]-plataforma.rect.center[1]
        #diagonal izquierda plataforma
        v2x=plataforma.rect.bottomleft[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.bottomleft[1]-plataforma.rect.center[1]

        pendienteSelfR= math.atan(self.div(v1x,v1y)) #por la derecha tiene que ser mayor
        pendientePlatR= math.atan(self.div(v2x,v2y))
        
        if (self.rect.top < plataforma.rect.bottom < self.rect.bottom) and ( 
                (self.rect.left>plataforma.rect.left and self.rect.right<plataforma.rect.right)
                or (plataforma.rect.center[0]<self.rect.topleft[0]<plataforma.rect.right and pendienteSelfL>=pendientePlatL)
                or (plataforma.rect.center[0]>self.rect.topright[0]>plataforma.rect.left and pendienteSelfR<=pendientePlatR)
                )and(
                    (-math.pi/2<self.angle<math.pi/2) or (3*math.pi/2>self.angle>5*math.pi/2)
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
        pendienteSelfL= math.atan(self.div(v1x,v1y)) #por la derecha tiene que ser mayor
        pendientePlatL= math.atan(self.div(v2x,v2y))

        #   ABAJO PLATAFORMA
        v1x=self.rect.topright[0]-plataforma.rect.center[0]
        v1y=self.rect.topright[1]-plataforma.rect.center[1]
        #diagonal izquierda plataforma
        v2x=plataforma.rect.bottomleft[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.bottomleft[1]-plataforma.rect.center[1]

        pendienteSelfR= math.atan(self.div(v1x,v1y)) #por la derecha tiene que ser mayor
        pendientePlatR= math.atan(self.div(v2x,v2y))
        
        
        if (self.rect.right > plataforma.rect.left > self.rect.left 
                and (plataforma.rect.top <= self.rect.top and self.rect.bottom < plataforma.rect.bottom 
                    or plataforma.rect.center[1] >  self.rect.bottomright[1] > plataforma.rect.top and pendienteSelfL>=pendientePlatL
                    or plataforma.rect.center[1] < self.rect.topright[1] < plataforma.rect.bottom and pendienteSelfR<=pendientePlatR
                ) and(
                    (0<self.angle<math.pi) or (-math.pi>self.angle>-2*math.pi)
                )
                
            ) :
            return True
        else:        
            return False
        

    def checarColisionIzquierda(self, plataforma):
        #   ARRIBA PLATAFORMA
        v1x=self.rect.bottomleft[0]-plataforma.rect.center[0]
        v1y=self.rect.bottomleft[1]-plataforma.rect.center[1]
        #diagonal izquierda plataforma
        v2x=plataforma.rect.topright[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.topright[1]-plataforma.rect.center[1]
        
        #izquierda negativa || derecha positiva
        pendienteSelfL= math.atan(self.div(v1x,v1y)) #por la derecha tiene que ser mayor
        pendientePlatL= math.atan(self.div(v2x,v2y))

        #   ABAJO PLATAFORMA
        v1x=self.rect.topleft[0]-plataforma.rect.center[0]
        v1y=self.rect.topleft[1]-plataforma.rect.center[1]
        #diagonal izquierda plataforma
        v2x=plataforma.rect.bottomright[0]-plataforma.rect.center[0]
        v2y=plataforma.rect.bottomright[1]-plataforma.rect.center[1]

        pendienteSelfR= math.atan(self.div(v1x,v1y)) #por la derecha tiene que ser mayor
        pendientePlatR= math.atan(self.div(v2x,v2y))
        
        
        if (self.rect.left < plataforma.rect.right < self.rect.right 
                and (plataforma.rect.top <= self.rect.top and self.rect.bottom < plataforma.rect.bottom 
                    or plataforma.rect.center[1] >  self.rect.bottomleft[1] > plataforma.rect.top and pendienteSelfL<=pendientePlatL
                    or plataforma.rect.center[1] < self.rect.topleft[1] < plataforma.rect.bottom and pendienteSelfR>=pendientePlatR
                )and(
                    (math.pi<self.angle<2*math.pi) or (0>self.angle>-math.pi)
                ) 
                
            ) :
            return True
        else:        
            return False
        
    #comprueba las colisiones del personaje devolviendo una tupla de cuatro booleanos (por las cuatro dirrecciones)
    def checkCollisionsPlat(self,grupoPlataformas):
        plataformas = pygame.sprite.spritecollide(self, grupoPlataformas,False)
        if (plataformas != None):
            for plataforma in plataformas:
                if (self.checarColisionAbajo(plataforma)): #abajo
                    self.establecerPosicion((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height+1))
                    if self.estado==ESTADO_AIRE:
                        self.estado=ESTADO_QUIETO
                    self.speed=0
                    self.dashes=0
                elif (self.checarColisionArriba(plataforma)): #arriba
                    
                    self.establecerPosicion((self.posicion[0], plataforma.posicion[1]+self.rect.height-1))
                    
                elif (self.checarColisionDerecha(plataforma)): #derecha
                    if self.estado==ESTADO_AIRE:
                        self.angle=-self.angle
                    else:
                        self.establecerPosicion(( self.posicion[0]-2,self.posicion[1]))
            
                elif (self.checarColisionIzquierda(plataforma)): #izquierda
                    if self.estado==ESTADO_AIRE:
                        self.angle=-self.angle
                    else:
                        self.establecerPosicion(( self.posicion[0]+plataforma.rect.width-1,self.posicion[1]))
            
    def checkCollisionsWall(self,grupoMuros):
        
        muros = pygame.sprite.spritecollide(self, grupoMuros,False)
        if (muros != None):
            for muro in muros:
                if (self.checarColisionDerecha(muro)): #derecha
                    
                    if self.estado==ESTADO_AIRE:
                        self.angle=-self.angle
                    else:
                        self.establecerPosicion(( self.posicion[0]-1,self.posicion[1]))
            
                elif (self.checarColisionIzquierda(muro)): #izquierda
                    if self.estado==ESTADO_AIRE:
                        self.angle=-self.angle
                    else:
                        
                    
                        self.establecerPosicion(( self.posicion[0]+2,self.posicion[1]))
                    
            
               
        
    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento):
        self.movimiento = movimiento

    def moveset(self,grupoPlataformas):
        angle=self.angle
        speed=self.speed
        # Miramos a ver si hay que parar de caer: si hemos llegado a una plataforma
        #  Para ello, miramos si hay colision con alguna plataforma del grupo
        
        #plataforma = pygame.sprite.spritecollide(self, grupoPlataformas)
        
        

        if self.creativo!=True:
            
            # Si vamos a la izquierda o a la derecha        
            if (self.movimiento == IZQUIERDA):
                
                self.mirando = self.movimiento
                #si no está agachado AKA cargando el salto, se mueve
                if not self.estado==ESTADO_AGACHADO:
                        angle=-math.pi/2
                        speed=self.walkSpeed
                        
                else :
                    angle,speed=self.saltar("izquierda")
                    self.estado=ESTADO_AIRE

                # Si no estamos en el aire
                if self.estado!=ESTADO_AIRE:
                    # La postura actual sera estar caminando
                    self.estado=ESTADO_ANDANDO
                    # Ademas, si no estamos encima de ninguna plataforma, caeremos
                    if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                        print(pygame.sprite.spritecollideany(self, grupoPlataformas))
                    
                        self.estado=ESTADO_AIRE  

            elif (self.movimiento == DERECHA):
                
                self.mirando = self.movimiento
                #si no está agachado AKA cargando el salto, se mueve
                if not self.estado==ESTADO_AGACHADO:
                # Esta mirando hacia ese lado
                    angle=math.pi/2
                    speed=self.walkSpeed
                else:
                    angle,speed=self.saltar("derecha")
                    self.estado=ESTADO_AIRE

                
                # Si no estamos en el aire
                if self.estado!=ESTADO_AIRE:
                    # La postura actual sera estar caminando
                    self.estado=ESTADO_ANDANDO
                    # Ademas, si no estamos encima de ninguna plataforma, caeremos
                    if pygame.sprite.spritecollideany(self, grupoPlataformas) == None:
                        self.estado=ESTADO_AIRE  

            # Si queremos saltar
            #elif self.movimiento == ESPACIO or self.movimiento == ESPACIOD or self.movimiento == ESPACIOI:
            elif self.movimiento in (ESPACIO,ESPACIOD,ESPACIOI):
                self.jumpCount += 1
            
                
                if self.estado!=ESTADO_AGACHADO:
                    self.estado=ESTADO_AGACHADO

                elif self.jumpCount>self.maxJumpCount:
                    if self.movimiento==ESPACIOD: 
                        self.mirando = self.movimiento
                        angle,speed=self.saltar("derecha")
                    elif self.movimiento==ESPACIOI:
                        self.mirando = IZQUIERDA
                        angle,speed=self.saltar("izquierda")
                    else:
                        angle,speed=self.saltar("arriba")
                
                
            
                # Si no se ha pulsado ninguna tecla
            if self.movimiento == QUIETO:
            # Si no estamos saltando, la postura actual será estar quieto
                if not self.estado==ESTADO_AIRE:
                    if self.estado==ESTADO_AGACHADO:
                        angle,speed=self.saltar("arriba")
                    else:
                        self.estado=ESTADO_QUIETO

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


    def update(self, grupoPlataformas,grupoMuros, tiempo):
        
        #El update lo hacen las subcalses


        # print(self.speed)
        
        
        
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
    def mover_cpu(self, grupoPlataformas,grupoMuros):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)
        return

