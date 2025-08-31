# Laberinto con IA (NEAT)

Este proyecto es una demostración del poder de la neuroevolución aplicada a la resolución de problemas. Un agente (representado por un círculo) aprende a navegar y resolver un laberinto generado proceduralmente, utilizando el algoritmo **NEAT (NeuroEvolution of Augmenting Topologies)**.

El objetivo principal es mostrar cómo una red neuronal puede evolucionar de forma autónoma para encontrar la solución a un problema sin necesidad de programación explícita de reglas.

## ⚙️ Tecnologías

- **Python**: El lenguaje de programación principal.
- **Pygame**: Utilizado para la creación de la interfaz gráfica del laberinto y la visualización del agente.
- **NEAT (neat-python)**: La biblioteca que implementa el algoritmo de neuroevolución, permitiendo el entrenamiento de las redes neuronales.

## 🎮 En qué Consiste el Juego

El juego visualiza en tiempo real el proceso de entrenamiento de la IA.

- **El Laberinto**: Se genera de forma aleatoria en cada nueva generación de entrenamiento.
- **Los Agentes**: Una población de pequeños círculos que representan las redes neuronales en evolución. Cada agente intenta resolver el laberinto.
- **La Meta**: El cuadrado verde al final del laberinto. El objetivo de los agentes es llegar a ella.
- **El Fitness**: El "rendimiento" de cada agente se mide por su "fitness". Cuanto más cerca llegue a la meta y más tiempo permanezca activo, mayor será su fitness.
- **La Evolución**: Al final de cada generación, los agentes con el mayor fitness son seleccionados para "reproducirse" (mutar y cruzarse), pasando sus características a la siguiente generación. Este ciclo se repite hasta que un agente logra resolver el laberinto.

## 📁 Estructura del Proyecto

El código está organizado en varios archivos para facilitar su comprensión y mantenimiento:

-   `main.py`: El punto de entrada del programa. Inicializa Pygame, carga la configuración de NEAT y gestiona el bucle principal de entrenamiento y visualización.
-   `laberinto.py`: Contiene la clase `Laberinto` responsable de generar el laberinto de forma procedural, dibujarlo en pantalla y gestionar la lógica de colisiones con las paredes.
-   `agente.py`: Define la clase `Agente`, que representa a cada individuo en la población de la IA. Gestiona el movimiento del agente, sus "sensores" para interactuar con el entorno y el cálculo de su fitness.
-   `config_neat.txt`: El archivo de configuración crucial para NEAT. Aquí se definen todos los parámetros del algoritmo genético, como el tamaño de la población, las tasas de mutación y los criterios de aptitud.
-   `requirements.txt`: Lista de todas las dependencias de Python necesarias para ejecutar el proyecto.

## 🚀 Cómo Instalar y Ejecutar

Para poner en marcha el proyecto, se recomienda usar un entorno virtual de Python.

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/nicorl/Laberinto-NEAT.git](https://github.com/nicorl/Laberinto-NEAT.git)
    cd nombre-del-repo
    ```

2.  **Crear y activar el entorno virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # En Linux/macOS
    # O en Windows: venv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Ejecutar el programa:**
    ```bash
    python main.py
    ```

## 🧠 Explicación Técnica

El núcleo del proyecto reside en la interacción entre los archivos `agente.py` y `neat-python`.

-   **Entradas de la Red Neuronal**: El agente percibe su entorno a través de **8 sensores**. Cada sensor mide la distancia a la pared más cercana en una dirección específica (0°, 45°, 90°, etc.). Estos 8 valores son la entrada (`num_inputs = 8`) para la red neuronal del agente.
-   **Salidas de la Red Neuronal**: La red neuronal produce 4 valores (`num_outputs = 4`), uno para cada dirección de movimiento: arriba, abajo, izquierda y derecha. El agente se mueve en la dirección con el valor de salida más alto.
-   **Función de Fitness**: El fitness de un genoma (la red neuronal del agente) se calcula como `1000 - distancia_a_meta`. Esto significa que cuanto más cerca del objetivo esté el agente, mayor será su puntuación de aptitud. Si un agente logra alcanzar la meta, se le otorga un bonus de fitness para priorizar su genoma en la siguiente ronda de selección.

Este enfoque permite que la IA aprenda a evitar obstáculos y a optimizar su camino hacia la meta de manera completamente autónoma, sin programación de reglas de navegación.
