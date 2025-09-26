import random
import pygame


class Item:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 30
        self.alto = 30
        self.velocidad = 2
        self.tipo = random.randint(1, 2)
        self.color = "black"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)

        try:
            if self.tipo == 1:
                self.imagen = pygame.image.load('media/item1.png')
            elif self.tipo == 2:
                self.imagen = pygame.image.load('media/item2.png')

            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
            # self.imagen = pygame.transform.rotate(self.imagen,180)
        except pygame.error as e:
            print(f"Error al cargar imagen del item: {e}")
            self.imagen = None

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        if self.imagen:
            ventana.blit(self.imagen, (self.x, self.y))

    def movimiento(self):
        self.y += self.velocidad
