import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
width = 800
height = 600

# Tamaño inicial del grifo de salida (porcentaje del tamaño del grifo)
orificio_size = 10

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

# Función para crear un botón
def create_button(rect, color, text, font, action):
    button = {
        "rect": rect,
        "color": color,
        "text": text,
        "font": font,
        "action": action
    }
    return button

# Función para dibujar un botón en la pantalla
def draw_button(button):
    pygame.draw.rect(screen, button["color"], button["rect"])
    text_surface = button["font"].render(button["text"], True, BLACK)
    text_rect = text_surface.get_rect(center=button["rect"].center)
    screen.blit(text_surface, text_rect)

# Función para cambiar el tamaño del grifo de salida y la velocidad de vaciado
def change_orificio_size(increment):
    global orificio_size, empty_speed
    orificio_size += increment
    orificio_size = max(0, min(100, orificio_size))  # Limitar el tamaño del grifo entre 0 y 100
    empty_speed = orificio_size / 10  # Ajustar la velocidad de vaciado según el tamaño del grifo

# Botones
font = pygame.font.SysFont(None, 24)

button_width_increase = create_button(pygame.Rect(10, 80, 100, 50), RED, "+", font, lambda: change_orificio_size(10))
button_width_decrease = create_button(pygame.Rect(10, 140, 100, 50), RED, "-", font, lambda: change_orificio_size(-10))


class Particle:
    def __init__(self, x, y, speed, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = random.randint(1, 5)
        self.color = color

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

# Fuente de texto
font = pygame.font.Font(None, 24)

start_time = 0.0

# Bucle principal del juego
running = True
while running:
    elapsed_time = pygame.time.get_ticks() / 1000.0 - start_time
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic izquierdo
                pos = pygame.mouse.get_pos()
                if button_width_increase["rect"].collidepoint(pos):
                    button_width_increase["action"]()
                elif button_width_decrease["rect"].collidepoint(pos):
                    button_width_decrease["action"]()

    # Incrementar el nivel del líquido automáticamente
    if liquid_level < 100.0:
        liquid_level += fill_speed / 100.0  # Dividir por 100 para ajustar el porcentaje a la escala de 0 a 1
        liquid_level = min(100.0, liquid_level)  # Limitar el nivel de líquido a 100

    if start_time is 0.0 and liquid_level >= 100.0:        
        start_time = pygame.time.get_ticks() / 1000.0  # Obtener el tiempo actual en segundos


    # Crear nuevas partículas para simular el chorro de agua
    if random.random() < empty_speed / 100.0:
        particle_x = random.uniform(orificio_x, orificio_x + orificio_width)
        particle_y = tank_y + tank_height
        particle_speed = random.uniform(1, 5)
        particle_color = BLUE  # Color rojo para el chorro de agua
        particle = Particle(particle_x, particle_y, particle_speed, particle_color)
        particles.append(particle)

    # Decrementar el nivel del líquido si el tanque no está vacío
    if liquid_level > 0.0:
        liquid_level -= empty_speed / 100.0  # Dividir por 100 para ajustar el porcentaje a la escala de 0 a 1
        liquid_level = max(0.0, liquid_level)  # Limitar el nivel de líquido a 0

    # Eliminar partículas fuera de la pantalla
    particles = [particle for particle in particles if particle.y > 0]

    # Crear nuevas partículas para simular el chorro de agua
    if random.random() < empty_speed / 100.0:
        particle_x = random.uniform(orificio_x, orificio_x + orificio_width)
        particle_y = tank_y + tank_height
        particle_speed = random.uniform(1, 5)
        particle = Particle(particle_x, particle_y, particle_speed, BLUE)  # Cambiar el color a rojo para el chorro de agua
        particles.append(particle)
    # Renderizar elementos gráficos
    screen.fill(WHITE)

    # Dibujar los botones
    draw_button(button_width_increase)
    draw_button(button_width_decrease)

    # Dibujar el tanque
    pygame.draw.rect(screen, BLUE, (tank_x, tank_y + tank_height - tank_height * liquid_level / 100.0, tank_width, tank_height * liquid_level / 100.0))

    # Dibujar el contorno del tanque
    pygame.draw.rect(screen, BLUE, (tank_x, tank_y, tank_width, tank_height), 2)

    # Dibujar el grifo de entrada
    grifo_width = tank_width * grifo_size / 100.0
    grifo_x = tank_x + (tank_width - grifo_width) / 2.0
    pygame.draw.rect(screen, BLUE, (grifo_x, tank_y, grifo_width, 10))

    # Dibujar el orificio de salida
    orificio_width = grifo_width * orificio_size / 100.0
    orificio_x = grifo_x + (grifo_width - orificio_width) / 2.0
    pygame.draw.rect(screen, BLUE, (orificio_x, tank_y + tank_height, orificio_width, 10))

    # Dibujar partículas
    for particle in particles:
        particle.update()
        particle.draw()

    # Mostrar la velocidad de llenado actual y las instrucciones
    speed_text = font.render("Velocidad de llenado: {}% por segundo".format(fill_speed), True, BLACK)
    instructions_text = font.render("Presiona UP para acelerar, DOWN para ralentizar, R para reiniciar", True, BLACK)
    screen.blit(speed_text, (10, 10))
    screen.blit(instructions_text, (10, 40))

   # Mostrar las variables en pantalla
    liquid_level_text = font.render("Nivel de llenado: {}%".format(round(liquid_level, 2)), True, BLACK)
    grifo_size_text = font.render("Tamaño del grifo: {}%".format(grifo_size), True, BLACK)
    orificio_size_text = font.render("Tamaño del orificio: {}%".format(orificio_size), True, BLACK)
    elapsed_time_text = font.render("Tiempo transcurrido: {:.2f} segundos".format(elapsed_time), True, BLACK)
    screen.blit(elapsed_time_text, (10, 160))

    # Ajustar las coordenadas x para alinear a la derecha
    liquid_level_x = width - liquid_level_text.get_width() - 10
    grifo_size_x = width - grifo_size_text.get_width() - 10
    orificio_size_x = width - orificio_size_text.get_width() - 10

    # Renderizar las variables en pantalla
    screen.blit(liquid_level_text, (liquid_level_x, 70))
    screen.blit(grifo_size_text, (grifo_size_x, 100))
    screen.blit(orificio_size_text, (orificio_size_x, 130))

    # Actualizar la pantalla
    pygame.display.flip()
# Salir del juego
pygame.quit()
