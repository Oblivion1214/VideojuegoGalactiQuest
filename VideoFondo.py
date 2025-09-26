import cv2
import pygame

class VideoFondo:
    def __init__(self, ruta_video, ancho, alto):
        self.cap = cv2.VideoCapture(ruta_video)
        self.ancho = ancho
        self.alto = alto
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, ancho)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, alto)

    def dibujar_video_fondo(self, ventana):
        ret, frame = self.cap.read()
        if not ret:  # Si el video terminó, reiniciar la lectura del video
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reiniciar el video al primer fotograma
            ret, frame = self.cap.read()  # Volver a leer el primer fotograma

        if ret:
            # Convertir la imagen de BGR (OpenCV) a RGB (Pygame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = pygame.surfarray.make_surface(frame)  # Convertir el frame a una superficie de Pygame
            frame = pygame.transform.scale(frame, (self.ancho, self.alto))  # Ajustar al tamaño de la ventana
            ventana.blit(frame, (0, 0))  # Mostrar el fondo en la ventana

    def actualizar_tamano(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto