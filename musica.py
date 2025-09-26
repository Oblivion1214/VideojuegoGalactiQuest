import pygame

class Musica:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        # Cargar sonidos
        try:
            self.sonido_disparo = pygame.mixer.Sound('media/retro-laser-1-236669.mp3')
            self.sonido_hit = pygame.mixer.Sound('media/video-game-hit-noise-001-135821.mp3')
            self.sonido_pick = pygame.mixer.Sound('media/coin-upaif-14631.mp3')
            self.sonido_muerte = pygame.mixer.Sound('media/videogame-death-sound-43894.mp3')
        except pygame.error as e:
            print(f"Error al cargar sonidos: {e}")

        # Configurar volumen de los sonidos
        self.sonido_disparo.set_volume(0.3)
        self.sonido_hit.set_volume(0.2)
        self.sonido_pick.set_volume(0.3)
        self.sonido_muerte.set_volume(0.3)

    def reproducir_musica_fondo(self):
        try:
            pygame.mixer.music.load('media/cancionMain.mp3')
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error al cargar música de fondo: {e}")

    def reproducir_musica_fondo2(self):
        try:
            pygame.mixer.music.load('media/area6.mp3')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error al cargar música de fondo: {e}")

    def reproducir_musica_menu(self):
        try:
            pygame.mixer.music.load('media/CancionMenu.mp3')
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error al cargar música del menú: {e}")

    def reproducir_musica_victoria(self):
        try:
            pygame.mixer.music.load('media/Victory.mp3')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error al cargar música de victoria: {e}")

    def reproducir_musica_jefe(self):
        try:
            pygame.mixer.music.load('media/game-boss-fiight.mp3')
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error al cargar música del jefe: {e}")

    def continuar_musica(self):
        pygame.mixer.music.unpause()

    def pausar_musica(self):
        pygame.mixer.music.pause()

    def detener_musica(self):
        pygame.mixer.music.stop()

    def reproducir_musica_fin(self):
        try:
            pygame.mixer.music.load('media/GameOver.mp3')
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"Error al cargar música de fin del juego: {e}")

    def reproducir_disparo(self):
        self.sonido_disparo.play()

    def reproducir_hit(self):
        self.sonido_hit.play()

    def reproducir_pick(self):
        self.sonido_pick.play()

    def reproducir_muerte(self):
        self.sonido_muerte.play()
