# AgenteExploradorConAlgoritmoGenetico
Este proyecto es una implementación de un algoritmo genético en un juego de agente
explorador con vecindad de Von Neumann.

El juego consiste en que se tiene un agente en un mapa de 10 x 10 casillas de las cuales
algunas contienen un tesoro, las demás pueden estar vacías o ser un muro (límite del mapa).

Los agentes pueden realizar las siguientes tareas: moverse hacia arriba, a la derecha, a la
izquierda o hacia abajo, levantar marca, hacer nada o hacer cualquiera de los 4 primeros
movimientos.

Las puntuaciones de cada agente se obtienen de la siguiente manera:
1. Si se levanta en una casilla donde no hay un tesoro, pierde 3 puntos.
2. Si intenta salir del mundo, pierde 1 punto.
3. Si levanta una marca (en casilla marcada) obtiene 10 puntos.

El entorno de cada agente se rige por Norte, Sur, Este y Oeste.

Gracias al algoritmo genético, los agentes podrán evolucionar de tal manera que puedan
obtener la mayor puntuación posible.

El programa se hizo en el lenguaje de Python y se utilizó la librería de Pygame para poder
visualizar el juego.
