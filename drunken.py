from personajes import *

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'drunkSpriteSheet.png','drunkCoord.txt', [1, 3, 1, 1, 1, 1], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR,VELOCIDAD_MAXIMA_JUGADOR);
        #Personaje.__init__(self,'Jugador.png','coordJugador.txt', [6, 12, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR);


    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha, espacio):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        if teclasPulsadas[espacio]:
            Personaje.mover(self,ESPACIO)
        elif teclasPulsadas[izquierda]:
            Personaje.mover(self,IZQUIERDA)
        elif teclasPulsadas[derecha]:
            Personaje.mover(self,DERECHA)
        else:
            Personaje.mover(self,QUIETO)

