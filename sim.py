import pygame
import math

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

# Coordenadas del tanque
tank_x = width // 4
tank_y = height // 4

# Dimensiones del tanque
tank_width = width // 2
tank_height = height // 2

# Nivel de líquido actual (porcentaje)
liquid_level = 0

# Velocidad de llenado del tanque (porcentaje por segundo)
fill_speed = 10

# Velocidad de vaciado del tanque (porcentaje por segundo)
empty_speed = 5

# Tamaño del grifo de salida (porcentaje del ancho del tanque)
grifo_size = 20

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Incrementar el nivel del líquido automáticamente
    if liquid_level < 100:
        liquid_level += fill_speed * 0.01  # 0.01 para ajustar el porcentaje a la escala de 0 a 1
        liquid_level = min(100, liquid_level)  # Limitar el nivel de líquido a 100

    # Decrementar el nivel del líquido si el tanque no está vacío
    if liquid_level > 0:
        empty_rate = empty_speed * grifo_size / 100  # Cálculo de la velocidad de vaciado en base al tamaño del grifo
        liquid_level -= empty_rate * 0.01  # 0.01 para ajustar el porcentaje a la escala de 0 a 1
        liquid_level = max(0, liquid_level)  # Limitar el nivel de líquido a 0

    # Renderizar elementos gráficos
    screen.fill(WHITE)

    # Dibujar el tanque
    pygame.draw.rect(screen, BLUE, (tank_x, tank_y + tank_height - tank_height * liquid_level / 100, tank_width, tank_height * liquid_level / 100))

    # Dibujar el contorno del tanque
    pygame.draw.rect(screen, BLUE, (tank_x, tank_y, tank_width, tank_height), 2)

    # Dibujar el grifo de salida
    grifo_width = tank_width * grifo_size / 100
    grifo_x = tank_x + (tank_width - grifo_width) / 2
    pygame.draw.rect(screen, RED, (grifo_x, tank_y, grifo_width, 10))

    # Actualizar la pantalla
    pygame.display.flip()

# Salir del juego
pygame.quit()
