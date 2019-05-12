AGENTE AUTOMÁTICO PACMAN
========================

APRENDIZAJE POR REFUERZO
========================

# Introducción


En esta práctica, vamos a crear un agente de aprendizaje automático a traves de aprendizaje por refuerzo.
El agente resultante será evaluado usando diversas técnicas, y se redactarán las conclusiones obtenidas.

##Ejecución

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