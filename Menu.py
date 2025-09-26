import pygame
import sys
import cv2

class Menu:
    def __init__(self, ventana, sonidos):
        self.ventana = ventana
        self.ancho, self.alto = ventana.get_size()
        self.fuente = pygame.font.SysFont("Microsoft Himalaya", 80)
        self.opciones = ["Jugar", "Instrucciones", "Puntuaciones", "Salir"]  # Añade "Scores"
        self.opcion_seleccionada = 0
        self.rects = []  # Para almacenar los rectángulos de las opciones

        self.video_cap = cv2.VideoCapture('media/VideoMenu.mp4')
        self.sonidos = sonidos  # Lista de objetos de sonido

    def ajustar_volumen(self, cambio):
        # Ajustar el volumen de la música
        volumen_actual = pygame.mixer.music.get_volume()
        volumen_actual = max(0.0, min(1.0, volumen_actual + cambio))
        pygame.mixer.music.set_volume(volumen_actual)

        # Ajustar el volumen de los efectos de sonido
        for sonido in self.sonidos:
            volumen_sonido = sonido.get_volume()
            volumen_sonido = max(0.0, min(1.0, volumen_sonido + cambio))
            sonido.set_volume(volumen_sonido)

        print(f"Volumen: {volumen_actual:.1f}")

    def dibujar_menu(self):
        # Reproducir el video de fondo
        ret, frame = self.video_cap.read()
        if not ret:
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reiniciar el video si ha terminado
            ret, frame = self.video_cap.read()

        frame = cv2.resize(frame, (self.ancho, self.alto))  # Redimensionar el video al tamaño de la ventana
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convertir de BGR a RGB
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Convertir a una superficie de Pygame

        self.ventana.blit(frame_surface, (0, 0))  # Dibujar el video en la ventana

        # Dibujar el título y las opciones del menú
        self.rects = []  # Reiniciar rectángulos en cada dibujo
        titulo = self.fuente.render("Galactic Quest", True, "white")
        titulo_rect = titulo.get_rect(center=(self.ancho // 2, self.alto // 4))
        self.ventana.blit(titulo, titulo_rect)

        for i, opcion in enumerate(self.opciones):
            color = (255, 255, 255) if i == self.opcion_seleccionada else (100, 100, 100)
            texto = self.fuente.render(opcion, True, color)
            texto_rect = texto.get_rect(center=(self.ancho // 2, self.alto // 2 - 50 + i * 100))
            self.ventana.blit(texto, texto_rect)
            self.rects.append(texto_rect)  # Guardar rectángulos

        pygame.display.update()

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.VIDEORESIZE:
                self.ancho, self.alto = evento.w, evento.h
                self.ventana = pygame.display.set_mode((self.ancho, self.alto), pygame.RESIZABLE)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                elif evento.key == pygame.K_DOWN:
                    self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                elif evento.key == pygame.K_RETURN:
                    return self.opciones[self.opcion_seleccionada]
                elif evento.key == pygame.K_1:  # Disminuir volumen
                    self.ajustar_volumen(-0.1)
                elif evento.key == pygame.K_2:  # Aumentar volumen
                    self.ajustar_volumen(0.1)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                for i, rect in enumerate(self.rects):
                    if rect.collidepoint(evento.pos):
                        return self.opciones[i]
        return None

    def mostrar(self):
        seleccion = None
        while not seleccion:
            self.dibujar_menu()
            seleccion = self.manejar_eventos()
        return seleccion


    def mostrar_scores(self):
        # Cargar la imagen de fondo
        fondo = pygame.image.load('media/escenario1.jpg')

        # Leer el archivo de puntuaciones
        try:
            with open('puntuaciones.txt', 'r') as archivo:
                lineas = archivo.readlines()
        except FileNotFoundError:
            lineas = ["No hay puntuaciones guardadas."]

        fuente_texto = pygame.font.SysFont("Arial", 30)
        desplazamiento = 0  # Variable para manejar el desplazamiento
        max_desplazamiento = max(0, len(lineas) * 40 - (self.alto - 200))  # Desplazamiento máximo

        ejecutando = True
        while ejecutando:
            # Redimensionar la imagen de fondo según el tamaño de la ventana
            fondo_rescalado = pygame.transform.scale(fondo, (self.ancho, self.alto))
            self.ventana.blit(fondo_rescalado, (0, 0))  # Dibujar la imagen de fondo rescalada
            titulo = self.fuente.render("Puntuaciones", True, "white")
            titulo_rect = titulo.get_rect(center=(self.ancho // 2, 50))
            self.ventana.blit(titulo, titulo_rect)

            # Columnas del encabezado
            encabezados = ["Nombre", "Puntuación", "Fecha"]
            posiciones = [100, self.ancho // 2 - 100, self.ancho - 500]
            for i, encabezado in enumerate(encabezados):
                texto_encabezado = fuente_texto.render(encabezado, True, "white")
                x_pos = posiciones[i]
                self.ventana.blit(texto_encabezado, (x_pos, 120))

            # Dibujar una línea divisoria para separar el título de las puntuaciones
            pygame.draw.line(self.ventana, "white", (50, 150), (self.ancho - 50, 150), 2)

            # Mostrar cada línea de puntuación con el desplazamiento aplicado
            for i, linea in enumerate(lineas):
                y_pos = 180 + i * 50 - desplazamiento  # Ajustar el espaciado vertical
                if 180 <= y_pos <= self.alto - 50:  # Solo mostrar las líneas que caben en pantalla
                    partes = linea.strip().split(' || ')
                    for j, parte in enumerate(partes):
                        texto = fuente_texto.render(parte, True, "white")
                        x_pos = posiciones[j]
                        self.ventana.blit(texto, (x_pos, y_pos))

            pygame.display.update()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:  # Presionar Esc para regresar al menú
                        ejecutando = False
                    elif evento.key == pygame.K_DOWN:  # Desplazar hacia abajo
                        desplazamiento = min(desplazamiento + 50, max_desplazamiento)  # Ajustar el desplazamiento
                    elif evento.key == pygame.K_UP:  # Desplazar hacia arriba
                        desplazamiento = max(desplazamiento - 50, 0)  # Ajustar el desplazamiento
                elif evento.type == pygame.VIDEORESIZE:
                    # Actualizar el tamaño de la ventana
                    self.ancho, self.alto = evento.w, evento.h
                    self.ventana = pygame.display.set_mode((self.ancho, self.alto), pygame.RESIZABLE)
                elif evento.type == pygame.MOUSEWHEEL:  # Desplazar con el scroll del mouse
                    if evento.y > 0:  # Scroll hacia arriba
                        desplazamiento = max(desplazamiento - 50, 0)  # Ajustar el desplazamiento
                    elif evento.y < 0:  # Scroll hacia abajo
                        desplazamiento = min(desplazamiento + 50, max_desplazamiento)  # Ajustar el desplazamiento