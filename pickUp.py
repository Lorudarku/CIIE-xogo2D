from personajes import *
POS1=0
POS2=1
class PickUp(MiSprite):
    def __init__(self,archivoImagen, archivoCoordenadas, numImagenes,rectangulo):
        
        MiSprite.__init__(self)
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()
        self.cooldown=0
        self.retardoAnimacion=30
        self.rect = rectangulo
        # Y lo situamos de forma global en esas coordenadas
        self.establecerPosicion((self.rect.left, self.rect.bottom))
        
        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        self.numPostura = 0;
        self.numImagenPostura = 0;
        cont = 0;
        self.coordenadasHoja = [];
        for linea in range(0, 2):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, numImagenes[linea]+1):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4
        
        self.retardoMovimiento = 0;
        self.actualizarPostura()
    
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

    def update(self, tiempo):
       
       self.actualizarPostura()
       MiSprite.update(self, tiempo)

       return
    
class Beer(PickUp):
    def __init__(self,rectangulo):
        PickUp.__init__(self,"beer.png", "beerCoord.txt", [8,1],rectangulo)
    
    def checkColisions(self,jugador):
        if pygame.sprite.collide_rect(self,jugador) :
            jugador.dashes+=1
            self.cooldown=100

    


    def update(self,jugador, tiempo):
        if self.cooldown>0:
            self.cooldown-=1
            self.numPostura=POS2
        else:
            self.numPostura=POS1
        self.checkColisions(jugador)
        PickUp.update(self,tiempo)
        return   
