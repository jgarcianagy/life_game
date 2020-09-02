import pygame
import numpy as np
import time

# Creamos la pantalla del juego.
pygame.init()

width, height = 1000, 1000
screen = pygame.display.set_mode((height, width))

# Establecemos color de fondo casi negro
bg = 25, 25, 25

# Pintamos el fondo con el color que elegimos
screen.fill(bg)

# Cantidad de celdas
nxC, nyC = 25,25
# Dimensión de celdas
dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas. Vivas = 1; Muertas = 0
gameState = np.zeros((nxC, nyC))

# Automata palo
# gameState[5, 3] = 1
# gameState[5, 4] = 1
# gameState[5, 5] = 1

# Autómata movil
gameState[21,21] = 1
gameState[22,22] = 1
gameState[22,23] = 1
gameState[21,23] = 1
gameState[20,23] = 1

# Control de la ejecución del juego

pauseExect = False

# Bucle de ejecución continua.
while True:

    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    # Registramos eventos de teclado y mouse
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect

        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouseClick[2]


    for y in range(0, nxC):
        for x in range(0, nyC):

            if not pauseExect:

                # Calculamos el número de vecinos cercanos.
                n_neigh = gameState[(x - 1)% nxC, (y - 1) % nyC] + \
                          gameState[(x)    % nxC, (y - 1) % nyC] + \
                          gameState[(x + 1)% nxC, (y - 1) % nyC] + \
                          gameState[(x - 1)% nxC, (y)     % nyC] + \
                          gameState[(x + 1)% nxC, (y)     % nyC] + \
                          gameState[(x - 1)% nxC, (y + 1) % nyC] + \
                          gameState[(x)    % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1)% nxC, (y + 1) % nyC]

            # Regla 1: una celula muerta con exactamente 3 vecinas vivas revive.
                if gameState[x,y] == 0 and n_neigh == 3:
                    newGameState[x,y] = 1


            # regla 2: una celula viva con menos de 2 o mas de 3 vecinas viva, muere
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x,y] = 0

        # Construimos los poligonos de las celdas.
            poly = [((x)   * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x)   * dimCW, (y+1) * dimCH)]

        # Dibujamos la celda para cada par de x e y.
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128), poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado del juego
    gameState = np.copy(newGameState)

    pygame.display.flip()
