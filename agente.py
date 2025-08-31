import pygame
import math

class Agente:
    """
    Clase para el agente (cerebro) que navega por el laberinto.
    """
    def __init__(self, x, y, radio, color, laberinto):
        self.x = x
        self.y = y
        self.radio = radio
        self.color = color
        self.velocidad = 5
        self.laberinto = laberinto
        self.fitness = 0
        self.ha_ganado = False

    def dibujar(self, pantalla):
        """
        Dibuja el agente en la pantalla.
        """
        pygame.draw.circle(pantalla, self.color, (int(self.x), int(self.y)), self.radio)

    def mover(self, movimientos):
        """
        Mueve al agente basándose en las salidas de la red neuronal.
        """
        # La red neuronal devuelve un array de 4 valores (arriba, abajo, izquierda, derecha)
        # Tomamos el movimiento con el valor más alto.
        movimiento = movimientos.index(max(movimientos))

        nueva_x = self.x
        nueva_y = self.y

        if movimiento == 0:  # Arriba
            nueva_y -= self.velocidad
        elif movimiento == 1:  # Abajo
            nueva_y += self.velocidad
        elif movimiento == 2:  # Izquierda
            nueva_x -= self.velocidad
        elif movimiento == 3:  # Derecha
            nueva_x += self.velocidad

        # Comprobar colisión antes de mover
        if not self.laberinto.colision_pared(nueva_x, nueva_y, self.radio):
            self.x = nueva_x
            self.y = nueva_y

    def obtener_sensores(self):
        """
        Devuelve las entradas para la red neuronal (sensores).
        Los sensores detectan la distancia a las paredes en 8 direcciones.
        """
        sensores = []
        direcciones = [0, 45, 90, 135, 180, 225, 270, 315]  # En grados

        for angulo in direcciones:
            distancia = 0
            punto_x = self.x
            punto_y = self.y
            while self.laberinto.es_valido(punto_x, punto_y):
                if self.laberinto.colision_pared(punto_x, punto_y, 0):
                    break
                
                punto_x += math.cos(math.radians(angulo))
                punto_y += math.sin(math.radians(angulo))
                distancia += 1

            sensores.append(distancia)
        return sensores

    def ha_llegado_a_la_meta(self, meta_x, meta_y):
        """
        Verifica si el agente ha llegado a la meta.
        """
        distancia = math.sqrt((self.x - meta_x)**2 + (self.y - meta_y)**2)
        if distancia < self.radio:
            self.ha_ganado = True
            return True
        return False