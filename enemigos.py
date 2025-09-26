import pygame
import random
from proyectiles import Bala

class Enemigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ancho = 50
        self.alto = 50
        self.velocidad = 1.5
        self.color = "red"
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        try:
            self.imagen = pygame.image.load('media/asteroide.png')
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        except pygame.error as e:
            print(f"Error al cargar imagen de asteroide: {e}")
            self.imagen = None
        self.vida = 2

    def dibujar(self, ventana):
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        if self.imagen:
            ventana.blit(self.imagen, (self.x, self.y))

    def movimiento(self):
        self.y += self.velocidad

class NaveAlienigena:
    def __init__(self, x, y, limite_izquierdo, limite_derecho):
        self.x = x
        self.y = y
        self.ancho = 60
        self.alto = 40
        self.velocidad = 1.4
        self.direccion = 1  # 1 para derecha, -1 para izquierda
        self.color = "green"
        self.limite_izquierdo = limite_izquierdo
        self.limite_derecho = limite_derecho
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        try:
            self.imagen = pygame.image.load('media/NaveAlienigena.png')  # Reemplaza con la imagen que quieras
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        except pygame.error as e:
            print(f"Error al cargar imagen de nave alienígena: {e}")
            self.imagen = None
        self.vida = 3
        self.proyectiles = []  # Lista para las balas disparadas

    def dibujar(self, ventana):
        # Actualizar el rectángulo para seguir la posición de la nave
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        if self.imagen:
            ventana.blit(self.imagen, (self.x, self.y))

        # Dibujar los proyectiles disparados
        for bala in self.proyectiles:
            bala.dibujar(ventana)

    def movimiento(self):
        # Movimiento horizontal de izquierda a derecha
        self.x += self.velocidad * self.direccion

        # Cambiar de dirección al alcanzar los límites
        if self.x <= self.limite_izquierdo or self.x + self.ancho >= self.limite_derecho:
            self.direccion *= -1

        # Movimiento de los proyectiles
        for bala in self.proyectiles:
            bala.movimiento()

        # Eliminar proyectiles que han salido de la pantalla
        self.proyectiles = [bala for bala in self.proyectiles if bala.y + bala.alto > 0]

    def disparar(self):
        # Probabilidad de disparar un proyectil
        if random.randint(0, 100) < 0.02:  # 0.2% de probabilidad por cada frame
            nueva_bala = Bala(self.x + self.ancho // 2 - 10, self.y + self.alto)
            nueva_bala.color = "green"  # Diferenciar las balas enemigas
            nueva_bala.velocidad = -7  # Las balas se mueven hacia abajo
            self.proyectiles.append(nueva_bala)
