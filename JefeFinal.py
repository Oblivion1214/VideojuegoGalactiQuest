import pygame
import random
from enemigos import NaveAlienigena
from proyectiles import Bala

class JefeFinal:
    def __init__(self, x, y, limite_izquierdo, limite_derecho):
        self.x = x
        self.y = y
        self.ancho = 200
        self.alto = 150
        self.velocidad = 1
        self.direccion = 1  # 1 para derecha, -1 para izquierda
        self.limite_izquierdo = limite_izquierdo
        self.limite_derecho = limite_derecho
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        try:
            self.imagen = pygame.image.load('media/NaveAlienigena.PNG')  # Reemplaza con la imagen del jefe
            self.imagen = pygame.transform.scale(self.imagen, (self.ancho, self.alto))
        except pygame.error as e:
            print(f"Error al cargar imagen del jefe: {e}")
            self.imagen = None  # Asignar None o una imagen de respaldo en caso de error
        self.vida = 50  # Vida actual
        self.vida_maxima = 50  # Vida máxima
        self.proyectiles = []  # Proyectiles disparados por el jefe
        self.invocar_cooldown = 0  # Controla la invocación de enemigos adicionales

    def dibujar(self, ventana):
        # Actualizar el rectángulo para seguir la posición del jefe
        self.rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        if self.imagen:
            ventana.blit(self.imagen, (self.x, self.y))

        # Dibujar los proyectiles disparados
        for bala in self.proyectiles:
            bala.dibujar(ventana)

    def dibujar_barra_vida(self, ventana):
        barra_ancho = self.ancho
        barra_alto = 15
        barra_x = self.x
        barra_y = self.y - barra_alto - 5
        porcentaje_vida = self.vida / self.vida_maxima

        # Dibujar fondo con degradado de rojo a negro
        for i in range(barra_ancho):
            intensidad = int(255 * (1 - i / barra_ancho))
            pygame.draw.line(ventana, (intensidad, 0, 0), (barra_x + i, barra_y), (barra_x + i, barra_y + barra_alto))

        # Dibujar vida restante (verde)
        barra_vida_rect = pygame.Rect(barra_x, barra_y, barra_ancho * porcentaje_vida, barra_alto)
        pygame.draw.rect(ventana, (0, 255, 0), barra_vida_rect)

        # Agregar borde negro
        borde_rect = pygame.Rect(barra_x - 1, barra_y - 1, barra_ancho + 2, barra_alto + 2)
        pygame.draw.rect(ventana, (0, 0, 0), borde_rect, 1)

        # Dibujar texto con el porcentaje de vida restante
        fuente = pygame.font.SysFont('arial', 15)  # Fuente predeterminada de pygame
        texto_vida = fuente.render(f"{int(porcentaje_vida * 100)}%", True, (0, 0, 0))  # Texto negro
        texto_x = barra_x + barra_ancho // 2 - texto_vida.get_width() // 2
        texto_y = barra_y + barra_alto // 2 - texto_vida.get_height() // 2
        ventana.blit(texto_vida, (texto_x, texto_y))

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
        # Disparar múltiples proyectiles en diferentes direcciones
        if random.randint(0, 100) < 1:  # Probabilidad de disparar (1% por frame)
            # Dispara tres proyectiles con diferentes posiciones iniciales
            posiciones = [self.x + 50, self.x + self.ancho // 2, self.x + self.ancho - 50]
            for pos in posiciones:
                nueva_bala = Bala(pos, self.y + self.alto)
                nueva_bala.color = "orange"  # Diferenciar las balas del jefe
                nueva_bala.velocidad = -5
                self.proyectiles.append(nueva_bala)

    def invocar_enemigos(self, lista_enemigos):
        # Invocar enemigos adicionales cada cierto tiempo
        if self.invocar_cooldown == 0:
            for _ in range(4):  # Invoca cuatro naves alienígenas
                try:
                    # Generar posición X dentro de los límites
                    posicion_x = random.randint(self.limite_izquierdo, self.limite_derecho - 60)

                    # Crear la nave alienígena
                    nueva_nave_alienigena = NaveAlienigena(
                        posicion_x, self.y + self.alto + 20,
                        self.limite_izquierdo, self.limite_derecho
                    )

                    # Agregar la nave a la lista de enemigos
                    lista_enemigos.append(nueva_nave_alienigena)
                except Exception as e:
                    print(f"Error al crear nave alienígena: {e}")

            # Reiniciar el cooldown para el próximo spawn
            self.invocar_cooldown = 2400  # Tiempo para el próximo spawn (ajustar según el FPS)
        else:
            # Reducir el cooldown
            self.invocar_cooldown -= 1
