from personajes import *
import random
SPRITE_QUIETO1 = 0
SPRITE_QUIETO2 = 1
SPRITE_ANDANDO = 2

class Rata(NoJugador):
    "El enemigo 'Sniper'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'ratAndBat.png','rat_coord.txt', [10, 10, 10], 1.4, 0,  5);
        self.idlecount=0
        self.ultimoMovimiento=IZQUIERDA
        self.idlecooldown=100
        self.idletimer=50
        
    def cambiarPostura(self):
        if self.estado==ESTADO_ANDANDO:
            self.numPostura=SPRITE_ANDANDO
            self.idlecount=0
        elif self.estado==ESTADO_QUIETO:
            if self.idlecount==0:
                self.numPostura = random.choice((SPRITE_QUIETO1,SPRITE_QUIETO2))
                self.idlecount=50
            else: 
                self.idlecount-=1
    

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
        if self.idlecooldown<=0 :
                self.idletimer=50

        if self.idletimer>0:
            Personaje.mover(self,QUIETO)
            self.idlecooldown=random.randint(50, 1000)
            self.idletimer-=1
        else:
            Personaje.mover(self,self.ultimoMovimiento)
        self.idlecooldown-=1    
            
            
        if plataformas.__len__()==1:
            if self.movimiento==DERECHA and self.rect.right>plataformas[0].rect.right:
                Personaje.mover(self,IZQUIERDA)
                self.ultimoMovimiento=IZQUIERDA
            elif self.movimiento==IZQUIERDA and self.rect.left<plataformas[0].rect.left:
                Personaje.mover(self,DERECHA)
                self.ultimoMovimiento=DERECHA
        
        print(self.idlecooldown)
        print(self.idletimer)
            
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
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)    
            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            elif self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            
        # Movemos solo a los enemigos que esten en la pantalla
        
    def update(self, grupoPlataformas, grupoMuros, tiempo):
        self.add_gravity()
        
        self.checkCollisionsWall(grupoMuros)
        self.checkCollisionsPlat(grupoPlataformas)
        Personaje.moveset(self,grupoPlataformas)

        self.cambiarPostura()
        self.actualizarPostura()
        
        MiSprite.update(self, tiempo)
        return 
            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano


class Bat(NoJugador):
    "El enemigo 'Sniper'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'ratAndBat.png','rat_coord.txt', [10, 10, 10], 1.4, 0,  5);
        self.idlecount=0
        self.ultimoMovimiento=IZQUIERDA
        self.idlecooldown=100
        self.idletimer=50
        
    def cambiarPostura(self):
        if self.estado==ESTADO_ANDANDO:
            self.numPostura=SPRITE_ANDANDO
            self.idlecount=0
        elif self.estado==ESTADO_QUIETO:
            if self.idlecount==0:
                self.numPostura = random.choice((SPRITE_QUIETO1,SPRITE_QUIETO2))
                self.idlecount=50
            else: 
                self.idlecount-=1
    

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
        if self.idlecooldown<=0 :
                self.idletimer=50

        if self.idletimer>0:
            Personaje.mover(self,QUIETO)
            self.idlecooldown=random.randint(50, 1000)
            self.idletimer-=1
        else:
            Personaje.mover(self,self.ultimoMovimiento)
        self.idlecooldown-=1    
            
            
        if plataformas.__len__()==1:
            if self.movimiento==DERECHA and self.rect.right>plataformas[0].rect.right:
                Personaje.mover(self,IZQUIERDA)
                self.ultimoMovimiento=IZQUIERDA
            elif self.movimiento==IZQUIERDA and self.rect.left<plataformas[0].rect.left:
                Personaje.mover(self,DERECHA)
                self.ultimoMovimiento=DERECHA
        
        print(self.idlecooldown)
        print(self.idletimer)
            
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
                self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)    
            # Si esta mirando a la izquiera, cogemos la porcion de la hoja
            elif self.mirando == IZQUIERDA:
                self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
            
        # Movemos solo a los enemigos que esten en la pantalla
        
    def update(self, grupoPlataformas, grupoMuros, tiempo):
        self.add_gravity()
        
        self.checkCollisionsWall(grupoMuros)
        self.checkCollisionsPlat(grupoPlataformas)
        Personaje.moveset(self,grupoPlataformas)

        self.cambiarPostura()
        self.actualizarPostura()
        
        MiSprite.update(self, tiempo)
        return 



