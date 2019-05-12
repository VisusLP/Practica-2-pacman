AGENTE AUTOMÁTICO PACMAN
========================

APRENDIZAJE POR REFUERZO
========================

# Introducción


En esta práctica, vamos a crear un agente de aprendizaje automático a traves de aprendizaje por refuerzo.
El agente resultante será evaluado usando diversas técnicas, y se redactarán las conclusiones obtenidas.

## Ejecución

La ejecucion básica de la práctica se hace de la siguiente forma:
```
$python busters.py -p QLearningAgent
```
A este comando se le pueden añadir los siguientes argumentos:
**-g** -> *Establece el agente usado por los fantasmas* - *Default = StaticGhosts*

**-l** -> *Selecciona el mapa usado en la partida* - *Default = oneHunt*

**-k** -> *Selecciona el número de fantasmas que aparecerán (Nunca mayor que el número de fantasmas definidos en el mapa)* - *Default = 4*

**-n** -> *Define el número de partidas que se jugarán con los parámetros establecidos* - *Default = 1*

**-x** -> *Define el número de partidas de entrenamiento, las cuales no tendrán interfaz gráfica* - *Default = 0*

**-e** -> *Define el valor de la variable epsilon* - *Default = 0.5*

**-r** -> *Define el valor de la variable alpha (Learning Rate)* - *Default = 0.3*

**-d** -> *Define el valor de la variable discount* - *Default = 0.8*

**-q** -> *Desactiva el uso de la interfaz gráfica* - *Default = False*

## Entrenamiento

Para entrenar el agente, se utilizarán los mapas designados para esta tarea

* [labAA1.lay](layouts/labAA1.lay)
* [labAA2.lay](layouts/labAA2.lay)
* [labAA3.lay](layouts/labAA3.lay)
* [labAA4.lay](layouts/labAA4.lay)
* [labAA5.lay](layouts/labAA5.lay)

La secuencia de comandos utilizada para un entrenamiento básico completo sera la siguiente:
```
$python busters.py -p QLearningAgent -k 1 -l labAA1 -n 10 -x 10 &&
$python busters.py -p QLearningAgent -k 2 -l labAA2 -n 10 -x 10 &&
$python busters.py -p QLearningAgent -k 3 -l labAA3 -n 10 -x 10 &&
$python busters.py -p QLearningAgent -k 3 -l labAA4 -n 10 -x 10 &&
$python busters.py -p QLearningAgent -k 3 -l labAA5 -n 10 -x 10
```
En caso de querer hacer un entrenamiento intensivo, se ejecutarán más episodios de entrenamiento: (RECOMENDADO!)
```
$python busters.py -p QLearningAgent -k 1 -l labAA1 -n 100 -x 100 &&
$python busters.py -p QLearningAgent -k 2 -l labAA2 -n 100 -x 100 &&
$python busters.py -p QLearningAgent -k 3 -l labAA3 -n 100 -x 100 &&
$python busters.py -p QLearningAgent -k 3 -l labAA4 -n 100 -x 100 &&
$python busters.py -p QLearningAgent -k 3 -l labAA5 -n 100 -x 100
```

## Evaluación de resultados

Tras realizar el entrenamiendo deseado, se podrá evaluar el agente. Para ello, se ejecutará el mapa deseado un número grande de veces, para obtener una media más sólida.
Se hará uso de los argumentos -e y -r para eliminar movimientos aleatorios y evitar que siga aprendiendo el agente.
```
$python busters.py -p QLearningAgent -l originalClassic -n 100 -r 0 -e 0 -q
```
Al acabar, se mostrarán en pantalla las estadísticas de la partida.

## Scripts

Los scripts utilizados se encuentran en la carpeta [Scripts](Scripts) por temas de organización. No obstante, es necesario extraer a la carpeta raíz todo script que quiera ser ejecutado

Algunos scripts se han dejado en la carpeta raíz para permitir un fácil acceso a la ejecución del programa.