import pygame
import random

class Laberinto:
    """
    Clase para generar, dibujar y gestionar la lógica del laberinto.
    """
    def __init__(self, tamano_celda=40, ancho=800, alto=600):
        self.tamano_celda = tamano_celda
        self.ancho = ancho
        self.alto = alto
        self.num_celdas_x = ancho // tamano_celda
        self.num_celdas_y = alto // tamano_celda
        self.grid = self.generar_laberinto_dfs()

    def generar_laberinto_dfs(self):
        """
        Genera un laberinto usando el algoritmo de Búsqueda en Profundidad (DFS).
        """
        grid = [[{'pared_derecha': True, 'pared_abajo': True, 'visitado': False}
                 for _ in range(self.num_celdas_x)]
                for _ in range(self.num_celdas_y)]

        stack = [(0, 0)]
        grid[0][0]['visitado'] = True

        while stack:
            actual_x, actual_y = stack[-1]
            vecinos = []

            # Vecino de arriba
            if actual_y > 0 and not grid[actual_y - 1][actual_x]['visitado']:
                vecinos.append((actual_x, actual_y - 1, 'arriba'))
            # Vecino de abajo
            if actual_y < self.num_celdas_y - 1 and not grid[actual_y + 1][actual_x]['visitado']:
                vecinos.append((actual_x, actual_y + 1, 'abajo'))
            # Vecino de la izquierda
            if actual_x > 0 and not grid[actual_y][actual_x - 1]['visitado']:
                vecinos.append((actual_x - 1, actual_y, 'izquierda'))
            # Vecino de la derecha
            if actual_x < self.num_celdas_x - 1 and not grid[actual_y][actual_x + 1]['visitado']:
                vecinos.append((actual_x + 1, actual_y, 'derecha'))

            if vecinos:
                next_x, next_y, direccion = random.choice(vecinos)
                if direccion == 'arriba':
                    grid[actual_y - 1][actual_x]['pared_abajo'] = False
                elif direccion == 'abajo':
                    grid[actual_y][actual_x]['pared_abajo'] = False
                elif direccion == 'izquierda':
                    grid[actual_y][actual_x - 1]['pared_derecha'] = False
                elif direccion == 'derecha':
                    grid[actual_y][actual_x]['pared_derecha'] = False

                grid[next_y][next_x]['visitado'] = True
                stack.append((next_x, next_y))
            else:
                stack.pop()

        return grid

    def dibujar(self, pantalla):
        """
        Dibuja el laberinto en la pantalla de Pygame.
        """
        for y in range(self.num_celdas_y):
            for x in range(self.num_celdas_x):
                # Coordenadas de la celda
                top_left_x = x * self.tamano_celda
                top_left_y = y * self.tamano_celda

                # Dibujar paredes
                if self.grid[y][x]['pared_derecha']:
                    pygame.draw.line(pantalla, (255, 255, 255), (top_left_x + self.tamano_celda, top_left_y),
                                     (top_left_x + self.tamano_celda, top_left_y + self.tamano_celda))
                if self.grid[y][x]['pared_abajo']:
                    pygame.draw.line(pantalla, (255, 255, 255), (top_left_x, top_left_y + self.tamano_celda),
                                     (top_left_x + self.tamano_celda, top_left_y + self.tamano_celda))

        # Dibujar bordes externos
        pygame.draw.line(pantalla, (255, 255, 255), (0, 0), (self.ancho, 0))
        pygame.draw.line(pantalla, (255, 255, 255), (0, 0), (0, self.alto))

    def es_valido(self, x, y):
        """
        Verifica si una posición (x, y) está dentro de los límites del laberinto.
        """
        return 0 <= x < self.ancho and 0 <= y < self.alto

    def colision_pared(self, x, y, radio):
        """
        Verifica si un círculo colisiona con alguna pared del laberinto.
        """
        # Calcular la celda en la que se encuentra el agente
        celda_x = int(x // self.tamano_celda)
        celda_y = int(y // self.tamano_celda)

        # Si el agente está fuera de los límites, hay colisión
        if not (0 <= celda_x < self.num_celdas_x and 0 <= celda_y < self.num_celdas_y):
            return True

        # Puntos de la celda actual
        pared_abajo_y = (celda_y + 1) * self.tamano_celda
        pared_derecha_x = (celda_x + 1) * self.tamano_celda
        pared_arriba_y = celda_y * self.tamano_celda
        pared_izquierda_x = celda_x * self.tamano_celda

        # Colisión con la pared de arriba
        if self.grid[celda_y][celda_x]['pared_abajo'] and y + radio >= pared_abajo_y:
            return True
        if self.grid[celda_y][celda_x]['pared_derecha'] and x + radio >= pared_derecha_x:
            return True
        if celda_x > 0 and self.grid[celda_y][celda_x - 1]['pared_derecha'] and x - radio <= pared_izquierda_x:
            return True
        if celda_y > 0 and self.grid[celda_y - 1][celda_x]['pared_abajo'] and y - radio <= pared_arriba_y:
            return True

        # Verificación de bordes del laberinto
        if x - radio <= 0 or x + radio >= self.ancho or y - radio <= 0 or y + radio >= self.alto:
            return True

        return False

    def obtener_posicion_meta(self):
        """
        Devuelve las coordenadas de la meta.
        """
        meta_x = (self.num_celdas_x - 1) * self.tamano_celda + self.tamano_celda // 2
        meta_y = (self.num_celdas_y - 1) * self.tamano_celda + self.tamano_celda // 2
        return meta_x, meta_y