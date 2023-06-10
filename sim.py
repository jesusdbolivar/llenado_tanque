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

# Coordenadas del tanque
tank_x = width // 4
tank_y = height // 4

# Dimensiones del tanque
tank_width = width // 2
tank_height = height // 2

# Nivel de líquido actual (porcentaje)
liquid_level = 50

# Velocidad de cambio del nivel de líquido
fill_speed = 5

# Bucle principal del juego
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                liquid_level += fill_speed
                if liquid_level > 100:
                    liquid_level = 100
            elif event.key == pygame.K_DOWN:
                liquid_level -= fill_speed
                if liquid_level < 0:
                    liquid_level = 0

    # Renderizar elementos gráficos
    screen.fill(WHITE)

    # Calcular la altura del líquido en función del nivel actual
    liquid_height = tank_height * liquid_level / 100

    # Dibujar el tanque
    pygame.draw.rect(screen, BLUE, (tank_x, tank_y + tank_height - liquid_height, tank_width, liquid_height))

    # Dibujar el contorno del tanque
    pygame.draw.rect(screen, BLUE, (tank_x, tank_y, tank_width, tank_height), 2)

    # Actualizar la pantalla
    pygame.display.flip()

# Salir del juego
pygame.quit()
