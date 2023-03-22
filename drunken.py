from personajes import *

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'drunkSpriteSheetMid.png','drunkCoord.txt', [2, 3, 1, 3, 3, 1, 3, 3, 3, 3, 3], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR,VELOCIDAD_MAXIMA_JUGADOR);
        #Personaje.__init__(self,'Jugador.png','coordJugador.txt', [6, 12, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);


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

