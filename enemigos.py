from personajes import *


class Rata(NoJugador):
    "El enemigo 'Sniper'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'ratAndBat.png','rat_coord.txt', [10, 10, 10], 1.4, 0,  5);
        
        

    def checkCollisionsWall(self,grupoMuros):
        
        muros = pygame.sprite.spritecollide(self, grupoMuros,False)
        if (muros != None):
            for muro in muros:
                if (self.checarColisionDerecha(muro)): #derecha
                    self.movimiento=IZQUIERDA
                    
            
                elif (self.checarColisionIzquierda(muro)): #izquierda
                    self.movimiento=DERECHA
    
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self,grupoPlataformas,grupoMuros):
       
        plataformas = pygame.sprite.spritecollide(self, grupoPlataformas,False)
        
        if plataformas.__len__()==1:
            
            if self.movimiento==DERECHA and self.rect.right>plataformas[0].rect.right:
                self.speed=self.walkSpeed
                self.angle=-math.pi/2
            elif self.movimiento==IZQUIERDA and self.rect.left<plataformas[0].rect.left:
                self.speed=self.walkSpeed
                self.angle=math.pi/2
        else:
            self.speed=self.walkSpeed
            self.angle=-math.pi/2
        
            
        # Movemos solo a los enemigos que esten en la pantalla
        
    def update(self, grupoPlataformas, grupoMuros, tiempo):
        self.add_gravity()
        self.actualizarPostura()
        self.checkCollisionsWall(grupoMuros)
        self.checkCollisionsPlat(grupoPlataformas)
        
        
        MiSprite.update(self, tiempo)
        return 
            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano


