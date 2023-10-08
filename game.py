import pygame
import random
import math
import tkinter as tk
from tkinter import simpledialog

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Proyectiles")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

Fondo_principal= (236, 239, 244)
Botones= (136, 192, 208)
Texto= (46, 52, 64)
Destacado= (191, 97, 106)


ancho_jugador = 20
alto_jugador = 50

posicion_jugador1 = (50, HEIGHT // 2 - 25)
posicion_jugador2 = (WIDTH - 70, HEIGHT // 2 - 25)

posicion_obstacle = abs(posicion_jugador1[0] - posicion_jugador2[0])/2 + 70


inicio_linea_suelo = (0 + 15, posicion_jugador1[1] + alto_jugador)
fin_linea_suelo = (WIDTH -15 , posicion_jugador1[1] + alto_jugador)


# Jugadores
player1 = pygame.Rect(posicion_jugador1[0], posicion_jugador1[1], ancho_jugador, alto_jugador)
player2 = pygame.Rect(posicion_jugador2[0], posicion_jugador2[1], ancho_jugador, alto_jugador)

# Obstáculo (por defecto, no hay obstáculo)
obstacle = None

# Viento (por defecto, no hay viento)
wind = None
wind_direction = 0  # 0 para viento hacia la izquierda, 1 para viento hacia la derecha

# Función para calcular la trayectoria del proyectil
def calcular_trayectoria(angle, v0, wind_speed, player_rect):
    g = 2  # Gravedad simulada
    t = 0
    x0, y0 = player_rect.centerx, player_rect.centery
    radianes = math.radians(angle)
    vx0 = v0 * math.cos(radianes)
    vy0 = -v0 * math.sin(radianes)
    ax = 0.0  # Aceleración horizontal debido al viento

    if wind_direction == 0:
        ax = -wind_speed
    elif wind_direction == 1:
        ax = wind_speed

    while True:
        pygame.time.delay(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        x = x0 + vx0 * t + 0.5 * ax * t ** 2
        y = y0 + vy0 * t + 0.5 * g * t ** 2
        t += 0.1
        pygame.draw.circle(screen, BLACK, (int(x), int(y)), 5)

        # Verificar colisión con el otro jugador
        if player_rect == player1 and player2.collidepoint(x, y):
            return "Player 1"
        elif player_rect == player2 and player1.collidepoint(x, y):
            return "Player 2"

        # Verificar colisión con el obstáculo
        if obstacle and obstacle.collidepoint(x, y):
            return None  # Colisión con el obstáculo, juego sigue

        # Verificar colisión con los límites de la pantalla
        if x < 0 or x > WIDTH:
            return None  # Fuera de pantalla, juego sigue
        
        # Verificar colisión con el suelo
        if colision_circulo_linea((x, y), 5, inicio_linea_suelo, fin_linea_suelo):
            return None

        pygame.display.update()

# Función para que el jugador ingrese los parámetros
def ingresar_parametros(player_name):
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter

    angle = simpledialog.askfloat("Ángulo", f"{player_name}, ingresa el ángulo de lanzamiento (en grados):")
    v0 = simpledialog.askfloat("Velocidad Inicial", f"{player_name}, ingresa la rapidez inicial del lanzamiento:") 
    #angle = float(input(f"{player_name}, ingresa el ángulo de lanzamiento (en grados): "))
    #v0 = float(input(f"{player_name}, ingresa la rapidez inicial del lanzamiento: "))
    if player_name=="Player 2":
        angle=180-angle
    root.destroy()
    return angle, v0


def colision_circulo_linea(centro_circulo, radio_circulo, inicio_linea, fin_linea):
    # Línea representada desde inicio_linea hasta fin_linea
    # Círculo representado por centro_circulo y radio_circulo

    # Calcula la distancia del centro del círculo a la línea
    dx = fin_linea[0] - inicio_linea[0]
    dy = fin_linea[1] - inicio_linea[1]

    longitud_cuadrada = dx*dx + dy*dy

    # Verifica si la longitud de la línea es cero (para evitar división por cero)
    if longitud_cuadrada == 0:
        return False

    # Calcula el t que minimiza la distancia.
    t = ((centro_circulo[0] - inicio_linea[0]) * dx + (centro_circulo[1] - inicio_linea[1]) * dy) / longitud_cuadrada

    # Encuentra el punto más cercano en la línea al centro del círculo
    if t < 0:
        punto_mas_cercano = inicio_linea
    elif t > 1:
        punto_mas_cercano = fin_linea
    else:
        punto_mas_cercano = (inicio_linea[0] + t * dx, inicio_linea[1] + t * dy)

    # Calcula la distancia entre el centro del círculo y este punto más cercano
    distancia_cuadrada = (centro_circulo[0] - punto_mas_cercano[0])**2 + (centro_circulo[1] - punto_mas_cercano[1])**2

    # Si la distancia es menor que el radio del círculo, están colisionando
    return distancia_cuadrada < radio_circulo**2



# Preguntar al jugador si desea insertar un obstáculo y especificar la dificultad
while True:
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    obstaculo_input = simpledialog.askstring("Obstaculo","¿Deseas insertar un obstáculo? (yes/no): ")

    #obstaculo_input = input("¿Deseas insertar un obstáculo? (yes/no): ").lower()
    if obstaculo_input == "yes":
        dificultad_obstaculo = simpledialog.askstring("Dificultad","Selecciona la dificultad del obstáculo (none/easy/medium/hard): ")
        #dificultad_obstaculo = input("Selecciona la dificultad del obstáculo (none/easy/medium/hard): ").lower()
        if dificultad_obstaculo == "easy":
            alto = random.randint(100, 130)
            obstacle = pygame.Rect(posicion_obstacle, inicio_linea_suelo[1] - alto, ancho_jugador, alto)
        elif dificultad_obstaculo == "medium":
            alto = random.randint(120, 150)
            obstacle = pygame.Rect(posicion_obstacle, inicio_linea_suelo[1] - alto, ancho_jugador, alto)
        elif dificultad_obstaculo == "hard":
            alto = random.randint(130, 200)
            obstacle = pygame.Rect(posicion_obstacle, inicio_linea_suelo[1] - alto, ancho_jugador, alto)
        break
    elif obstaculo_input == "no":
        break
    root.destroy()


# Bucle principal del juego
running = True
en_juego = True
while running:
    turno = "Player 1"
    # Preguntar al jugador si hay viento y especificar la magnitud y dificultad
    while True:
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter

        viento_input = simpledialog.askstring("Viento","¿Hay viento? (yes/no): ")
        #viento_input = input("¿Hay viento? (yes/no): ").lower()
        if viento_input == "yes":
            dificultad_viento = simpledialog.askstring("Dificultad","Selecciona la dificultad del viento (none/easy/medium/hard): ")
            #dificultad_viento = input("Selecciona la dificultad del viento (none/easy/medium/hard): ").lower()
            if dificultad_viento != "none":
                wind = dificultad_viento
                wind_direction = random.randint(0, 1)  # Aleatoriamente hacia izquierda o derecha
            break
        elif viento_input == "no":
            break
        root.destroy()

    while en_juego:
        screen.fill(Fondo_principal)
        #screen.fill(WHITE)
        pygame.draw.rect(screen, Botones, player1)
        pygame.draw.rect(screen, Destacado, player2)
        pygame.draw.line(screen, (255, 0, 0), inicio_linea_suelo, fin_linea_suelo, 5)

        # Dibuja el obstáculo si está presente
        if obstacle:
            pygame.draw.rect(screen, BLACK, obstacle)

        # Dibuja el viento si está presente
        if wind:
            wind_str = "WIND: " + wind 
            font = pygame.font.Font(None, 36)
            #text = font.render(wind_str, True, RED)

            text = font.render(wind_str, True, Texto)
            text_rect = text.get_rect(center=(WIDTH // 2, 20))
            screen.blit(text, text_rect)

        # Turno del jugador 1 (lanzamiento de izquierda a derecha)
        pygame.display.set_caption("Turno de Player 1")
        # input("Presiona Enter para lanzar el proyectil...")
        angle, v0 = ingresar_parametros("Player 1")
        wind_speed = 1 if wind else 0
        if wind:
            if wind_direction==1:
                direct="-->"
            if wind_direction==0:
                direct="<--"
            wind_str = direct
            font = pygame.font.Font(None, 36)
            #text = font.render(wind_str, True, BLACK)
            text = font.render(wind_str, True, Texto)
            text_rect = text.get_rect(center=(WIDTH // 2, 50))
            screen.blit(text, text_rect)
        resultado = calcular_trayectoria(angle, v0, wind_speed, player1)
        if resultado == "Player 1":
            print("¡Player 1 gana!")
            en_juego = False
            break

        # Turno del jugador 2 (lanzamiento de derecha a izquierda)
        pygame.display.set_caption("Turno de Player 2")
        # input("Presiona Enter para lanzar el proyectil...")
        angle, v0 = ingresar_parametros("Player 2")
        wind_speed = 1 if wind else 0
        resultado = calcular_trayectoria(angle, v0, wind_speed, player2)
        if resultado == "Player 2":
            print("¡Player 2 gana!")
            en_juego = False
            break
    response = tk.messagebox.askyesno("decea continuar","¿Desea continuar jugando?")

    if response==False:
        running=False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
