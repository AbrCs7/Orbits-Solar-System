import pygame
import math
import random

# Inicialização do Pygame
pygame.init()

# Definições da janela para Full HD
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Órbitas dos Planetas")

# Cores
black = (0, 0, 0)
yellow = (255, 255, 0)  # Sol
asteroid_gray = (105, 105, 105)  # Asteroides cinza
colors = {
    "Mercury": (169, 169, 169),  # Mercúrio cinza
    "Venus": (173, 216, 230),  # Vênus azul claro
    "Earth": (0, 0, 255),  # Terra azul
    "Mars": (255, 0, 0),  # Marte vermelho
    "Jupiter": (139, 69, 19),  # Júpiter marrom
    "Saturn": (210, 180, 140),  # Saturno bege
    "Uranus": (0, 255, 255),  # Urano ciano
    "Neptune": (0, 0, 128)  # Netuno azul escuro
}

# Dados aproximados das órbitas dos planetas (raios médios em UA - Unidades Astronômicas)
# Distâncias aproximadas do Sol aos planetas em UA
distances = {
    "Mercury": 0.39,
    "Venus": 0.72,
    "Earth": 1.0,
    "Mars": 1.52,
    "Jupiter": 5.2,
    "Saturn": 9.58,
    "Uranus": 19.18,
    "Neptune": 30.07
}

# Velocidades orbitais relativas
speeds = {
    "Mercury": 4.74,
    "Venus": 3.5,
    "Earth": 2.98,
    "Mars": 2.41,
    "Jupiter": 1.31,
    "Saturn": 0.97,
    "Uranus": 0.68,
    "Neptune": 0.54
}


# Função para converter unidades astronômicas para pixels
def au_to_pixels(distance):
    # Considerando 1 UA = 25 pixels para melhor ajuste na tela
    return distance * 25


# Função para desenhar os planetas
def draw_planet(name, distance, color, angle):
    if name == "Jupiter":
        radius = 12
    elif name in ["Saturn", "Uranus"]:
        radius = 10
    elif name in ["Venus", "Earth", "Mars"]:
        radius = 8
    else:
        radius = 6  # Para Mercúrio e Netuno

    distance_px = au_to_pixels(distance)  # Converter distância de UA para pixels
    x = width // 2 + distance_px * math.cos(math.radians(angle))
    y = height // 2 + distance_px * math.sin(math.radians(angle))
    pygame.draw.circle(screen, color, (int(x), int(y)), radius)

    # Desenhar anéis de Saturno
    if name == "Saturn":
        pygame.draw.ellipse(screen, (192, 192, 192), (int(x) - 20, int(y) - 5, 40, 10), 2)
        pygame.draw.ellipse(screen, (192, 192, 192), (int(x) - 25, int(y) - 7, 50, 14), 1)

        # Desenhar continentes da Terra
        if name == "Earth":
            draw_continents()

    # Função para desenhar os continentes da Terra
    def draw_continents():
        continents = [
            [(0.1, 0.2), (0.3, 0.1), (0.5, 0.25), (0.35, 0.4), (0.2, 0.3)],  # Exemplo de continente 1
            [(0.6, 0.3), (0.8, 0.25), (0.75, 0.45), (0.65, 0.5)]  # Exemplo de continente 2
            # Adicione mais continentes conforme desejado
        ]

        for continent in continents:
            points = [(int(width // 2 + x * width * 0.4), int(height // 2 + y * height * 0.4)) for x, y in continent]
            pygame.draw.polygon(screen, (34, 139, 34), points)


# Inicialização dos ângulos para cada planeta
angles = {planet: 0 for planet in distances}


# Função para gerar as posições dos asteroides
def generate_asteroid_belt():
    asteroids = []
    # Cinturão de asteroides entre 2.1 e 3.3 UA aproximadamente
    inner_belt = 2.1
    outer_belt = 3.3
    num_asteroids = 200

    for _ in range(num_asteroids):
        distance = random.uniform(inner_belt, outer_belt)
        angle = random.uniform(0, 360)
        distance_px = au_to_pixels(distance)
        speed = random.uniform(0.1, 0.5)  # Velocidade de rotação lenta e variável
        asteroids.append({"distance": distance, "angle": angle, "speed": speed})

    return asteroids


# Gerar as posições dos asteroides uma vez
asteroids = generate_asteroid_belt()

# Loop principal
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(black)  # Preencher o fundo da tela com preto

    # Desenhar o Sol
    pygame.draw.circle(screen, yellow, (width // 2, height // 2), 10)

    # Desenhar órbitas
    for planet, distance in distances.items():
        distance_px = au_to_pixels(distance)
        pygame.draw.circle(screen, colors[planet], (width // 2, height // 2), int(distance_px), 1)

    # Desenhar planetas
    for planet, distance in distances.items():
        draw_planet(planet, distance, colors[planet], angles[planet])
        angles[planet] += speeds[planet]  # Atualizar ângulo baseado na velocidade orbital

    # Desenhar cinturão de asteroides
    for asteroid in asteroids:
        distance_px = au_to_pixels(asteroid["distance"])
        x = width // 2 + distance_px * math.cos(math.radians(asteroid["angle"]))
        y = height // 2 + distance_px * math.sin(math.radians(asteroid["angle"]))
        pygame.draw.circle(screen, asteroid_gray, (int(x), int(y)), 2)
        asteroid["angle"] += asteroid["speed"]  # Atualizar ângulo do asteroide

    pygame.display.flip()
    clock.tick(60)  # Limitar a taxa de quadros a 60 por segundo

# Finalizar o Pygame
pygame.quit()
