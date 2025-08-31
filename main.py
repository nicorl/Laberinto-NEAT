import pygame
import neat
import os
import sys
import math # <-- CAMBIO: Importado para el cálculo de distancia
from laberinto import Laberinto
from agente import Agente

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
PANTALLA = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Solucionador de Laberinto con NEAT")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

# Variables globales
generacion = 0
reloj = pygame.time.Clock()
FPS = 60

def evaluar_genomas(genomas, config):
    """
    Función de evaluación de fitness para NEAT.
    Esta función se ejecuta para cada generación.
    """
    global generacion
    generacion += 1

    # Crear un nuevo laberinto para cada generación para evitar sobreajuste
    laberinto = Laberinto(ancho=ANCHO_PANTALLA, alto=ALTO_PANTALLA)
    meta_x, meta_y = laberinto.obtener_posicion_meta()
    pos_inicial_x = laberinto.tamano_celda // 2
    pos_inicial_y = laberinto.tamano_celda // 2

    # Configuración de la simulación
    agentes = []
    redes = []
    ge = []

    for _, g in genomas:
        red = neat.nn.FeedForwardNetwork.create(g, config)
        redes.append(red)
        agente = Agente(x=pos_inicial_x, y=pos_inicial_y,
                        radio=laberinto.tamano_celda // 4, color=AZUL, laberinto=laberinto)
        agentes.append(agente)
        g.fitness = 0  # Iniciar fitness en 0
        ge.append(g)

    # <-- CAMBIO: Lógica de tiempo y pasos
    max_pasos = 750  # Número máximo de movimientos antes de que un agente sea descalificado
    pasos_actuales = 0

    ejecutando = True
    while ejecutando and len(agentes) > 0:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        PANTALLA.fill(NEGRO)
        laberinto.dibujar(PANTALLA)
        pygame.draw.circle(PANTALLA, VERDE, (int(meta_x), int(meta_y)), laberinto.tamano_celda // 4)

        # <-- CAMBIO: Bucle a través de los agentes al revés para poder eliminarlos de forma segura
        for i in range(len(agentes) - 1, -1, -1):
            agente = agentes[i]
            
            # Obtener entradas y mover agente
            entradas = agente.obtener_sensores()
            salidas = redes[i].activate(entradas)
            agente.mover(salidas)

            # Calcular distancia a la meta
            distancia_a_meta = math.sqrt((agente.x - meta_x)**2 + (agente.y - meta_y)**2)
            
            # Asignar fitness: premiar la cercanía a la meta
            # La distancia inicial máxima sirve como referencia
            distancia_inicial = math.sqrt((pos_inicial_x - meta_x)**2 + (pos_inicial_y - meta_y)**2)
            ge[i].fitness = (distancia_inicial - distancia_a_meta) * 2 # Premiar el progreso

            # Comprobar si ha ganado o se ha quedado sin tiempo
            if agente.ha_llegado_a_la_meta(meta_x, meta_y):
                ge[i].fitness += 1000  # Gran bonus por ganar
                print(f"¡Agente ha ganado en la generación {generacion}!")
                agentes.pop(i)
                redes.pop(i)
                ge.pop(i)
            elif pasos_actuales > max_pasos:
                # Penalización por no llegar (opcional, pero útil)
                ge[i].fitness -= 100
                agentes.pop(i)
                redes.pop(i)
                ge.pop(i)

        # Dibujar todos los agentes que quedan
        for agente in agentes:
            agente.dibujar(PANTALLA)
        
        # Incrementar pasos
        pasos_actuales += 1

        # Si no quedan agentes, terminar la generación
        if len(agentes) == 0:
            ejecutando = False

        # Mostrar estadísticas
        fuente = pygame.font.Font(None, 24)
        texto_gen = fuente.render(f"Generación: {generacion}", True, BLANCO)
        texto_vivos = fuente.render(f"Vivos: {len(agentes)}", True, BLANCO)
        texto_pasos = fuente.render(f"Pasos: {pasos_actuales}/{max_pasos}", True, BLANCO)
        PANTALLA.blit(texto_gen, (10, 10))
        PANTALLA.blit(texto_vivos, (10, 30))
        PANTALLA.blit(texto_pasos, (10, 50))

        pygame.display.flip()
        reloj.tick(FPS)


def run(config_path):
    """
    Función principal para configurar y ejecutar NEAT.
    """
    # <-- CAMBIO: Carga de la configuración integrada aquí
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    # Crear la población
    p = neat.Population(config)
    
    # Añadir reportadores para ver las estadísticas en la consola
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Ejecutar el algoritmo NEAT por hasta 100 generaciones
    ganador = p.run(evaluar_genomas, 100)

    print('\nMejor genoma encontrado:\n{!s}'.format(ganador))

if __name__ == "__main__":
    # Determinar la ruta al archivo de configuración
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config_neat.txt')
    
    # Comprobar si el archivo de configuración existe
    if not os.path.exists(config_path):
        print(f"Error: No se encuentra el archivo 'config_neat.txt' en la ruta {config_path}")
        sys.exit(1)

    run(config_path)