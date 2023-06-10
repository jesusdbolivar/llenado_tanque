import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
width = 800
height = 600

# Crear la ventana
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Juego del llenado y vaciado de un tanque rectangular")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Coordenadas del tanque
tank_x = width // 4
tank_y = height // 4

# Dimensiones del tanque
tank_width = width // 2
tank_height = height // 2

# Nivel de líquido actual (porcentaje)
liquid_level = 0.0

# Velocidad de llenado del tanque (porcentaje por segundo)
fill_speed = 1.0

# Velocidad de vaciado del tanque (porcentaje por segundo)
empty_speed = 0.5

# Tamaño del grifo de entrada (porcentaje del ancho del tanque)
grifo_size = 10

# Tamaño del orificio de salida (porcentaje del tamaño del grifo)
orificio_size = 10

# Partículas
particles = []

class Particle:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = random.randint(1, 5)
        self.color = BLUE

    def update(self):
        self.y -= self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Fuente de texto
font = pygame.font.Font(None, 24)

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Controles para acelerar o ralentizar el llenado del agua
            if event.key == pygame.K_UP:
                fill_speed += 0.5
            elif event.key == pygame.K_DOWN:
                fill_speed = max(fill_speed - 0.5, 0)
            elif event.key == pygame.K_r:
                # Reiniciar el juego
                liquid_level = 0.0
                fill_speed = 1.0
                particles = []

    # Incrementar el nivel del líquido automáticamente
    if liquid_level < 100.0:
        liquid_level += fill_speed / 100.0  # Dividir por 100 para ajustar el porcentaje a la escala de 0 a 1
        liquid_level = min(100.0, liquid_level)  # Limitar el nivel de líquido a 100

        # Crear nuevas partículas
        if random.random() < fill_speed / 100.0:
            particle_x = random.uniform(tank_x, tank_x + tank_width)
            particle_y = tank_y + tank_height
            particle_speed = random.uniform(1, 5)
            particle = Particle(particle_x, particle_y, particle_speed)
            particles.append(particle)

    # Eliminar partículas fuera de la pantalla
    particles = [particle for particle in particles if particle.y > 0]

    # Renderizar elementos gráficos
    screen.fill(WHITE)

    # Dibujar el tanque
    pygame.draw.rect(screen, BLUE, (tank_x, tank_y + tank_height - tank_height * liquid_level / 100.0, tank_width, tank_height * liquid_level / 100.0))

    # Dibujar el contorno del tanque
    pygame.draw.rect(screen, BLUE, (tank_x, tank_y, tank_width, tank_height), 2)

    # Dibujar el grifo de entrada
    grifo_width = tank_width * grifo_size / 100.0
    grifo_x = tank_x + (tank_width - grifo_width) / 2.0
    pygame.draw.rect(screen, RED, (grifo_x, tank_y, grifo_width, 10))

    # Dibujar el orificio de salida
    orificio_width = grifo_width * orificio_size / 100.0
    orificio_x = grifo_x + (grifo_width - orificio_width) / 2.0
    pygame.draw.rect(screen, BLACK, (orificio_x, tank_y, orificio_width, 10))

    # Dibujar partículas
    for particle in particles:
        particle.update()
        particle.draw()

    # Mostrar la velocidad de llenado actual y las instrucciones
    speed_text = font.render("Velocidad de llenado: {}% por segundo".format(fill_speed), True, BLACK)
    instructions_text = font.render("Presiona UP para acelerar, DOWN para ralentizar, R para reiniciar", True, BLACK)
    screen.blit(speed_text, (10, 10))
    screen.blit(instructions_text, (10, 40))

    # Actualizar la pantalla
    pygame.display.flip()

# Salir del juego
pygame.quit()
