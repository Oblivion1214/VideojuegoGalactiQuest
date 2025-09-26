import datetime
import sys
import pygame
import random
import re  # Importar módulo para expresiones regulares

from Menu import Menu
from VideoFondo import VideoFondo
from musica import Musica
from jugador import Prota
from enemigos import Enemigo, NaveAlienigena
from proyectiles import Bala
from item import Item
from JefeFinal import JefeFinal

# Musica del juego
musica = Musica()

# Icono del juego en ventana
pygame.display.set_caption("Galaxy Quest")
icono = pygame.image.load("media/Icono.ico")
pygame.display.set_icon(icono)

# Configuracion de la ventana
info = pygame.display.Info()
ANCHO = info.current_w - 200
ALTO = info.current_h - 200
VENTANA = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
FPS = 120
FUENTE = pygame.font.SysFont("Microsoft Himalaya", 70)

# Video de Fondo
video_fondo = VideoFondo("media/VideoFondo.mp4", ANCHO, ALTO)

# Variables de sonidos
sonidos = [musica.sonido_muerte, musica.sonido_hit, musica.sonido_pick, musica.sonido_disparo]

# Configuración del botón
boton_ancho = 150
boton_alto = 50
boton_x = ANCHO - boton_ancho - 10
boton_y = ALTO - boton_alto - 650
color_boton = (0, 0, 255)
texto_boton = FUENTE.render("Salir", True, "white")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)

# Fuentes
fuente_titulo = pygame.font.SysFont("Arial", 50)
fuente_texto = pygame.font.SysFont("Arial", 30)


def mostrar_instrucciones():
    instrucciones_activo = True
    fuente = pygame.font.SysFont("Microsoft Himalaya", 50)
    while instrucciones_activo:
        VENTANA.fill((0, 0, 0))  # Fondo negro para las instrucciones
        instrucciones_texto = fuente.render("Usa A y D para moverte, UP para disparar, ESC para pausar", True, "white")
        instrucciones_texto2 = fuente.render("Bajar volumen con 1 y subir volumen con 2", True, "white")
        volver_texto = fuente.render("Presiona cualquier tecla para volver", True, "white")

        # Centrar los textos en la pantalla
        VENTANA.blit(instrucciones_texto, (ANCHO // 2 - instrucciones_texto.get_width() // 2, ALTO // 3))
        VENTANA.blit(instrucciones_texto2, (ANCHO // 2 - instrucciones_texto2.get_width() // 2, ALTO // 4))
        VENTANA.blit(volver_texto, (ANCHO // 2 - volver_texto.get_width() // 2, ALTO // 2))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                instrucciones_activo = False  # Volver al menú.


def pausar_juego():
    pausado = True
    fuente_pausa = pygame.font.SysFont("Microsoft Himalaya", 100)
    texto_pausa = fuente_pausa.render("Pausa", True, "white")

    while pausado:
        musica.pausar_musica()
        # Dibuja el mensaje de pausa
        VENTANA.blit(texto_pausa,
                     (ANCHO // 2 - texto_pausa.get_width() // 2, ALTO // 2 - texto_pausa.get_height() // 2))
        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Presionar ESC de nuevo para reanudar
                    pausado = False  # Sale del bucle de pausa para reanudar el juego
                    musica.continuar_musica()

def mostrar_game_over(puntos):
    entrada_texto = ''
    ejecutando = True
    mensaje_error = ''  # Variable para almacenar el mensaje de error

    while ejecutando:
        VENTANA.fill(NEGRO)

        # Dibujar "Game Over" y otras instrucciones
        texto_game_over = fuente_titulo.render("Game Over", True, BLANCO)
        texto_game_over_rect = texto_game_over.get_rect(center=(800, 200))
        VENTANA.blit(texto_game_over, texto_game_over_rect)

        texto_instrucciones = fuente_texto.render("Introduce tu nombre:", True, BLANCO)
        texto_instrucciones_rect = texto_instrucciones.get_rect(center=(800, 300))
        VENTANA.blit(texto_instrucciones, texto_instrucciones_rect)

        # Mostrar el texto introducido
        texto_entrada = fuente_texto.render(entrada_texto, True, BLANCO)
        texto_entrada_rect = texto_entrada.get_rect(center=(800, 350))
        VENTANA.blit(texto_entrada, texto_entrada_rect)

        # Dibujar una línea debajo del texto introducido
        pygame.draw.line(VENTANA, BLANCO, (texto_entrada_rect.left, texto_entrada_rect.bottom + 5),
                        (texto_entrada_rect.right, texto_entrada_rect.bottom + 5), 2)

        # Mostrar mensaje de error si es necesario
        if mensaje_error:
            texto_error = fuente_texto.render(mensaje_error, True, ROJO)
            texto_error_rect = texto_error.get_rect(center=(800, 400))
            VENTANA.blit(texto_error, texto_error_rect)

        # Actualizar la pantalla
        pygame.display.flip()

        # Manejar eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                return None  # Salir sin guardar si se cierra la ventana
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if entrada_texto.strip() and len(entrada_texto) <= 8 and re.match("^[A-Za-z0-9]+$", entrada_texto):  # Verificar longitud y caracteres permitidos
                        # Guardar la puntuación en un archivo
                        with open('puntuaciones.txt', 'a') as archivo:
                            archivo.write(f"Player: {entrada_texto} || Puntos: {puntos} || Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        ejecutando = False  # Salir del bucle
                    else:
                        if not re.match("^[A-Za-z0-9]+$", entrada_texto):
                            mensaje_error = "Nombre no puede contener espacios ni caracteres especiales"
                        else:
                            mensaje_error = "Nombre demasiado largo (máx. 8 caracteres)"
                elif evento.key == pygame.K_BACKSPACE:
                    entrada_texto = entrada_texto[:-1]  # Borrar el último carácter
                    mensaje_error = ''  # Borrar mensaje de error
                else:
                    if len(entrada_texto) < 8:
                        if re.match("^[A-Za-z0-9]+$", evento.unicode):
                            entrada_texto += evento.unicode  # Agregar el carácter presionado
                            mensaje_error = ''  # Borrar mensaje de error
                        else:
                            mensaje_error = "Nombre no puede contener espacios ni caracteres especiales"
                    else:
                        mensaje_error = "Nombre demasiado largo (máx. 8 caracteres)"

    return entrada_texto


def mostrar_victoria(puntos):
    musica.detener_musica()
    musica.reproducir_musica_victoria()
    fuente = pygame.font.SysFont("Arial", 50)
    texto_victoria = fuente.render("¡Victoria!", True, "gold")
    texto_puntos = fuente.render(f"Puntos finales: {puntos}", True, "white")

    VENTANA.fill((0, 0, 0))
    VENTANA.blit(texto_victoria, (ANCHO // 2 - texto_victoria.get_width() // 2, ALTO // 3))
    VENTANA.blit(texto_puntos, (ANCHO // 2 - texto_puntos.get_width() // 2, ALTO // 2))

    pygame.display.update()
    pygame.time.wait(7000)  # Esperar 7 segundos antes de salir y mostrar el Game Over


menu = Menu(VENTANA, sonidos)

def ejecutar_juego():
    global ANCHO, ALTO, VENTANA

    jugando = True
    vida = 5
    puntos = 0
    nivel = 1  # Nivel inicial
    tiempo_pasado = 0
    tiempo_entre_enemigos = 600
    tiempo_pasado_item = 0
    tiempo_entre_items = 10000
    ultima_bala = 0
    tiempo_entre_balas = 600
    nivel_maximo = 11
    puntos_para_subir_de_nivel = 1750
    reloj = pygame.time.Clock()
    cubo = Prota(ANCHO / 2, ALTO - 80)
    enemigos = [Enemigo(ANCHO / 3, ALTO / 3)]
    naves_alienigenas = [] # Dentro del bucle principal del juego
    balas = []
    items = [Item(ANCHO / 2, 0)]
    jefe_final = []
    musica.reproducir_musica_fondo()

    def dibujar_boton():
        pygame.draw.rect(VENTANA, color_boton, (boton_x, boton_y, boton_ancho, boton_alto))
        VENTANA.blit(texto_boton, (boton_x + 30, boton_y))
        pygame.display.update()

    def crear_bala():
        nonlocal ultima_bala
        if pygame.time.get_ticks() - ultima_bala > tiempo_entre_balas:
            balas.append(Bala(cubo.rect.centerx, cubo.rect.centery))
            ultima_bala = pygame.time.get_ticks()
            musica.reproducir_disparo()

    def gestionar_teclas(tecla):
        if tecla[pygame.K_a]:
            if cubo.x >= 0:
                cubo.x -= cubo.velocidad
        if tecla[pygame.K_d]:
            if cubo.x + cubo.ancho <= ANCHO:
                cubo.x += cubo.velocidad
        if tecla[pygame.K_UP]:
            crear_bala()

    # Musica de niveles
    if 1 <= nivel < 6:
        tiempo_pasado = 125
    else:
        tiempo_pasado = 150

    while jugando and vida > 0:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jugando = False
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Si se presiona ESC, activa la pausa
                    pausar_juego()
                if evento.key == pygame.K_1:  # Disminuir volumen
                    menu.ajustar_volumen(-0.1)
                elif evento.key == pygame.K_2:  # Aumentar volumen
                    menu.ajustar_volumen(0.1)
            elif evento.type == pygame.VIDEORESIZE:
                ANCHO, ALTO = evento.w, evento.h
                VENTANA = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
                video_fondo.actualizar_tamano(ANCHO, ALTO)
        video_fondo.dibujar_video_fondo(VENTANA)
        video_fondo.actualizar_tamano(ANCHO, ALTO)
        tiempo_pasado += reloj.tick(FPS)
        tiempo_pasado_item += reloj.get_time()

        if tiempo_pasado > tiempo_entre_enemigos:
            enemigos.append(Enemigo(random.randint(0, ANCHO), -200))
            tiempo_pasado = 100

        if tiempo_pasado_item > tiempo_entre_items:
            items.append(Item(random.randint(0, ANCHO), -200))
            tiempo_pasado_item = 0

        # Incrementar el nivel según los puntos
        if puntos >= nivel * puntos_para_subir_de_nivel:
            nivel += 1
            puntos_para_subir_de_nivel *= 1.2  # Aumentar dificultad (más puntos para el siguiente nivel)

        if 3 <= nivel <= 4:
            if len(naves_alienigenas) == 0:  # Crear la nave solo si no existe
                naves_alienigenas.append(NaveAlienigena(ANCHO // 2, 50, 50, ANCHO - 50))
                naves_alienigenas.append(NaveAlienigena(2 * ANCHO // 3, 50, 50, ANCHO - 50))

        # Si el nivel es 5, elimina enemigos2
        if nivel == 5:
            naves_alienigenas = []

        # Cambia enemigos2 por una lista de naves alienígenas
        if 6 <= nivel <= 8:
            if len(naves_alienigenas) == 0:  # Solo crear las naves si no existen
                naves_alienigenas.append(NaveAlienigena(ANCHO // 3, 50, 50, ANCHO - 50))
                naves_alienigenas.append(NaveAlienigena(2 * ANCHO // 3, 50, 50, ANCHO - 50))
                naves_alienigenas.append(NaveAlienigena(2 * ANCHO // 4, 50, 50, ANCHO - 50))

        # Si el nivel es mayor a 8, eliminar las naves alienígenas
        if nivel == 9:
            naves_alienigenas = []

        for nave in naves_alienigenas[:]:  # Iterar sobre una copia para eliminar elementos
            nave.movimiento()
            nave.disparar()
            nave.dibujar(VENTANA)

            for bala in balas:
                if nave.rect.colliderect(bala.rect):  # Colisión con las balas del jugador
                    nave.vida -= 1
                    balas.remove(bala)
                    if nave.vida <= 0:
                        musica.reproducir_hit()
                        naves_alienigenas.remove(nave)  # Eliminar la nave destruida
                        puntos += 500  # Añadir puntos al eliminar la nave

            # Colisiones de balas de la nave con el jugador
            for proyectil in nave.proyectiles:
                if cubo.rect.colliderect(proyectil.rect):
                    vida -= 1
                    musica.reproducir_hit()
                    nave.proyectiles.remove(proyectil)

        if nivel == 10:
            if len(jefe_final) == 0:  # Crear la nave solo si no existe
                jefe_final.append(JefeFinal(ANCHO // 2, 50, 50, ANCHO - 50))
                musica.reproducir_musica_jefe()
            for jefe in jefe_final[:]:  # Iterar sobre una copia para eliminar elementos
                jefe.dibujar(VENTANA)
                jefe.movimiento()
                jefe.disparar()
                jefe.invocar_enemigos(naves_alienigenas)
                jefe.dibujar_barra_vida(VENTANA)  # Dibuja la barra de vida

                for bala in balas:
                    if jefe.rect.colliderect(bala.rect):
                        jefe.vida -= 1
                        balas.remove(bala)
                        if jefe.vida <= 0:
                            musica.reproducir_hit()
                            jefe_final.remove(jefe) # Eliminar la nave destruida
                            puntos += 100000  # Añadir puntos al eliminar la nave

                # Colisiones de proyectiles del jefe con el jugador
                for proyectil in jefe.proyectiles:
                    if cubo.rect.colliderect(proyectil.rect):
                        musica.reproducir_hit()
                        vida -= 1
                        jefe.proyectiles.remove(proyectil)


        if nivel == nivel_maximo:
            mostrar_victoria(puntos)  # Mostrar pantalla de victoria
            jugando = False

        eventos = pygame.event.get()
        teclas = pygame.key.get_pressed()

        texto_vida = FUENTE.render(f"Vidas: {vida}", True, "white")
        texto_puntos = FUENTE.render(f"Puntos: {puntos}", True, "white")
        texto_nivel = FUENTE.render(f"Nivel: {nivel}", True, "white")  # Mostrar el nivel actual

        gestionar_teclas(teclas)

        for evento in eventos:
            if evento.type == pygame.QUIT:
                jugando = False
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.VIDEORESIZE:
                ANCHO, ALTO = evento.w, evento.h
                VENTANA = pygame.display.set_mode((ANCHO, ALTO), pygame.RESIZABLE)
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_x <= evento.pos[0] <= boton_x + boton_ancho and boton_y <= evento.pos[
                    1] <= boton_y + boton_alto:
                    jugando = False

        cubo.dibujar(VENTANA)

        for enemigo in enemigos:
            enemigo.dibujar(VENTANA)
            enemigo.movimiento()
            if pygame.Rect.colliderect(cubo.rect, enemigo.rect):
                vida -= 1
                enemigos.remove(enemigo)
            if enemigo.y > ALTO:
                puntos += 100
                enemigos.remove(enemigo)
            for bala in balas:
                if pygame.Rect.colliderect(bala.rect, enemigo.rect):
                    enemigo.vida -= 1
                    balas.remove(bala)
            if enemigo.vida <= 0:
                musica.reproducir_hit()
                enemigos.remove(enemigo)
                puntos += 200
            if nivel == 10:
                enemigos.remove(enemigo)

        for bala in balas:
            bala.dibujar(VENTANA)
            bala.movimiento()
            if bala.y < 0:
                balas.remove(bala)

        for item in items:
            item.dibujar(VENTANA)
            item.movimiento()
            if pygame.Rect.colliderect(item.rect, cubo.rect):
                musica.reproducir_pick()
                items.remove(item)
                if item.tipo == 1:
                    tiempo_entre_balas -= 30
                    if tiempo_entre_balas < 300:
                        tiempo_entre_balas = 300
                elif item.tipo == 2:
                    cubo.velocidad += 0.3
                    if cubo.velocidad > 5:
                        cubo.velocidad = 5
            if item.y > ALTO:
                items.remove(item)

        VENTANA.blit(texto_vida, (20, 80))
        VENTANA.blit(texto_puntos, (20, 20))
        VENTANA.blit(texto_nivel, (20, 140))  # Mostrar el nivel en la pantalla
        dibujar_boton()

        pygame.display.update()

    musica.detener_musica()
    musica.reproducir_muerte()
    musica.reproducir_musica_fin()

    mostrar_game_over(puntos)


# Bucle principal del menú
while True:
    musica.reproducir_musica_menu()
    ventana_menu = Menu(VENTANA, sonidos)
    opcion = ventana_menu.mostrar()
    if opcion == "Jugar":
        ejecutar_juego()
        pygame.display.update()
    elif opcion == "Instrucciones":
        mostrar_instrucciones()
        pygame.display.update()
    elif opcion == "Puntuaciones":
        menu.mostrar_scores()
        pygame.display.update()
    elif opcion == "Salir":
        pygame.quit()
        sys.exit()
