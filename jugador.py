import pygame

class Prota:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.velocidad = 4
        self.color = "green"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        try:
            self.imagen = pygame.image.load('media/avion.png')
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        except pygame.error as e:
            print(f"Error al cargar imagen del avión: {e}")
            self.imagen = None

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        if self.imagen:
            ventana.blit(self.imagen, (self.x, self.y))
