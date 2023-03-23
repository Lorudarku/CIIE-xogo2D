from personajes import *

VELOCIDAD_JUGADOR = 1.4 # Pixeles por milisegundo
VELOCIDAD_MAXIMA_JUGADOR=15
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5

SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1
SPRITE_AGACHADO = 2
SPRITE_SALTANDO = 3
SPRITE_CAYENDO = 4
SPRITE_APLASTADO = 5
SPRITE_POTA_D=6
SPRITE_POTA_U=7
SPRITE_POTA_UR=8
SPRITE_POTA_R=9
SPRITE_POTA_DR=10

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'drunkSpriteSheetMid.png','drunkCoord.txt', [2, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR,);
        #Personaje.__init__(self,'Jugador.png','coordJugador.txt', [6, 12, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);
        self.potaCount=0
        self.pota=False
        

    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, espacio):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        
        if teclasPulsadas[espacio] and teclasPulsadas[izquierda] and teclasPulsadas[arriba]:
            Personaje.mover(self,ESPACIOIAR)
        elif teclasPulsadas[espacio] and teclasPulsadas[izquierda] and teclasPulsadas[abajo]:
            Personaje.mover(self,ESPACIOIAB)
        elif teclasPulsadas[espacio] and teclasPulsadas[derecha] and teclasPulsadas[arriba]:
            Personaje.mover(self,ESPACIODAR)
        elif teclasPulsadas[espacio] and teclasPulsadas[derecha] and teclasPulsadas[abajo]:
            Personaje.mover(self,ESPACIODAB)
        elif teclasPulsadas[espacio] and teclasPulsadas[derecha]:
            Personaje.mover(self,ESPACIOD)
        elif teclasPulsadas[espacio] and teclasPulsadas[izquierda]:
            Personaje.mover(self,ESPACIOI)
        elif teclasPulsadas[espacio] and teclasPulsadas[abajo]:
            Personaje.mover(self,ESPACIOAB)
        elif teclasPulsadas[espacio] and teclasPulsadas[arriba]:
            Personaje.mover(self,ESPACIOAR)
        elif teclasPulsadas[espacio]:
            Personaje.mover(self,ESPACIO)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self,IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self,DERECHA)
        elif teclasPulsadas[abajo]:
            Personaje.mover(self,ABAJO)
        elif teclasPulsadas[arriba]:
            Personaje.mover(self,ARRIBA)
        else:
            Personaje.mover(self,QUIETO)
    
    def dash(self,direccion):
        
        speed = 10
        
        if direccion==ESPACIOAR:
            angle=0       
            self.numPostura=SPRITE_POTA_D

        elif direccion==ESPACIOAB:
            angle= math.pi
            self.numPostura=SPRITE_POTA_U
            
        elif direccion==ESPACIOD:
            angle= math.pi/2
            self.numPostura=SPRITE_POTA_R
            self.mirando=IZQUIERDA

        elif direccion==ESPACIOI:
            angle= -math.pi/2
            self.numPostura=SPRITE_POTA_R
            self.mirando=DERECHA


        elif direccion==ESPACIODAR:
            angle= math.pi/4
            self.numPostura=SPRITE_POTA_DR
            self.mirando=IZQUIERDA

        elif direccion==ESPACIODAB:
            angle= 3*math.pi/4
            self.numPostura=SPRITE_POTA_UR
            self.mirando=IZQUIERDA

        elif direccion==ESPACIOIAR:
            angle= -math.pi/4
            self.numPostura=SPRITE_POTA_DR
            self.mirando=DERECHA

        elif direccion==ESPACIOIAB:
            angle= -3*math.pi/4
            
            self.numPostura=SPRITE_POTA_UR
            self.mirando=DERECHA

        self.dashes-=1
        return angle,speed

    def cambiarPostura(self):
        if self.pota!=True:
            if self.estado==ESTADO_AIRE:
                self.numPostura=SPRITE_SALTANDO
            elif self.estado==ESTADO_ANDANDO:
                self.numPostura=SPRITE_ANDANDO
            elif self.estado==ESTADO_AGACHADO:
                self.numPostura=SPRITE_AGACHADO
            elif self.estado==ESTADO_QUIETO:
                self.numPostura=SPRITE_QUIETO

    def movesetDrunken(self,grupoPlataformas):
        if self.pota==True:
                if self.potaCount>0:
                    self.potaCount-=1
                else:
                    self.pota=False
                    self.estado=ESTADO_QUIETO
        elif self.estado==ESTADO_AIRE:
                # Si estamos en el aire y el personaje quiere saltar, ignoramos este movimiento
                if self.movimiento in (ESPACIOD,ESPACIOI,ESPACIOAB,ESPACIOAR,ESPACIODAR,ESPACIODAB,ESPACIOIAR,ESPACIODAB,ESPACIOIAB) and self.dashes>0:
                    self.angle,self.speed=self.dash(self.movimiento)
                    self.potaCount=40
                    self.pota=True
        else:
             self.moveset(grupoPlataformas)
        

    def update(self, grupoPlataformas, grupoMuros, tiempo):
        self.add_gravity()
        
        self.checkCollisionsWall(grupoMuros)
        self.checkCollisionsPlat(grupoPlataformas)
        self.movesetDrunken(grupoPlataformas)

        self.cambiarPostura()
        self.actualizarPostura()
        if self.speed>VELOCIDAD_MAXIMA_JUGADOR: 
            self.speed=VELOCIDAD_MAXIMA_JUGADOR
        MiSprite.update(self, tiempo)
        return

