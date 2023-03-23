from personajes import *


class Rata(NoJugador):
    "El enemigo 'Sniper'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'ratAndBat.png','rat_coord.txt', [10, 10, 10], 1.8,  5);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1, jugador2):

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano
            if abs(jugador1.posicion[0]-self.posicion[0])<abs(jugador2.posicion[0]-self.posicion[0]):
                jugadorMasCercano = jugador1
            else:
                jugadorMasCercano = jugador2
            # Y nos movemos andando hacia el
            if jugadorMasCercano.posicion[0]<self.posicion[0]:
                Personaje.mover(self,IZQUIERDA)
            else:
                Personaje.mover(self,DERECHA)

        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO)

