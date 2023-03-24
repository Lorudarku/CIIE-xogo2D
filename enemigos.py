from personajes import *
import random
SPRITE_QUIETO1 = 0
SPRITE_QUIETO2 = 1
SPRITE_ANDANDO = 2

BAT_VOLANDO=0
BAT_FLIP=1

class Rata(NoJugador):
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'ratAndBat.png','rat_coord.txt', [10, 10, 10], 1.4,   5,False)
        self.idlecount=0
        Personaje.mover(self,IZQUIERDA)
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
    def mover_cpu(self,grupoPlataformas,grupoMuros,jugador):
       
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
        
            
    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
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
        self.moveset(grupoPlataformas)

        self.cambiarPostura()
        self.actualizarPostura()
        
        MiSprite.update(self, tiempo)
        return 
            # Por ejemplo, intentara acercarse al jugador mas cercano en el eje x
            # Miramos cual es el jugador mas cercano


class Bat(NoJugador):
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'ratAndBat.png','bat_coord.txt', [10, 10], 1.4,  5, True)
        self.numPostura=SPRITE_QUIETO1
        self.angle=random.uniform(0, 2*math.pi)
        self.speed=3
        self.cooldown=100
        self.flipcount=random.randint(50, 200)
    
    def changeDir(self):
        if self.cooldown==0:
            self.numPostura=BAT_FLIP
            self.speed=0
            if self.flipcount==0:
                self.angle=random.uniform(0, 2*math.pi)
                self.speed=3
                self.cooldown=random.randint(50, 1000)
                self.flipcount=random.randint(50, 200)
                self.numPostura=BAT_VOLANDO
            else:
                self.flipcount-=1
        else:
            self.cooldown-=1




    
    
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self,grupoPlataformas,grupoMuros,jugador):
        if self.rect.left<0 or self.rect.right>ANCHO_PANTALLA or self.rect.bottom>ALTO_PANTALLA or self.rect.top<0:
            self.angle=-self.angle
        if self.rect.bottom>ALTO_PANTALLA or self.rect.top<0:
            self.angle+=math.pi
        self.changeDir()
        
            
    def actualizarPostura(self):
        self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0
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
        
        self.actualizarPostura()
        
        MiSprite.update(self, tiempo)
        return 

class WhiteBat(NoJugador):
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'ratAndBat.png','whiteBat_coord.txt', [10, 10], 1.4,  5, True);
        self.numPostura=BAT_VOLANDO
        self.angle=random.uniform(0, 2*math.pi)
        self.speed=3
        self.cooldown=100
        self.flipcount=random.randint(50, 200)
    
    def changeDir(self,jugador):
        #primero calculamos el vector del murcielago al jugador
        vector_union=(self.rect.center[0]-jugador.rect.center[0],self.rect.center[1]-jugador.rect.center[1])
        
        #luego el angulo del mismo, aplicando trigonometria 
        # pitagoras para la longitud del vector, y arcoseno de la componente x partida por esta para el angulo final
     

        angulo=math.asin(Personaje.div(self,vector_union[0],math.sqrt(math.pow(vector_union[0],2)+math.pow(vector_union[1],2))))
        angulo+=math.pi
        if self.cooldown==0:
            self.numPostura=BAT_FLIP
            self.speed=0
            if self.flipcount==0:
                self.angle=angulo
                self.speed=3
                self.cooldown=random.randint(50, 1000)
                self.flipcount=random.randint(50, 200)
                self.numPostura=BAT_VOLANDO
            else:
                self.flipcount-=1
        else:
            self.cooldown-=1




    
    
    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self,grupoPlataformas,grupoMuros,jugador):
        if self.rect.left<0 or self.rect.right>ANCHO_PANTALLA or self.rect.bottom>ALTO_PANTALLA or self.rect.top<0:
            self.angle=-self.angle
        if self.rect.bottom>ALTO_PANTALLA or self.rect.top<0:
            self.angle+=math.pi
        self.changeDir(jugador)
        
            
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
        
        self.actualizarPostura()
        
        MiSprite.update(self, tiempo)
        return 


