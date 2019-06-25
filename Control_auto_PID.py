# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 16:10:27 2019

@author: Agustin
"""

from lantz.core.log import log_to_screen, DEBUG

log_to_screen(DEBUG)
from lantz.ino import INODriver, BoolFeat, QuantityFeat
import time
import matplotlib.pyplot as plt
import numpy as np

class ControlAuto(INODriver):
    velocidad = QuantityFeat('velocidad',getter=False)
    distancia = QuantityFeat('Distancia',setter=False)
    
with ControlAuto.via_packfile('ControlAuto.pack.yaml') as board: 
    for i in range(5):  #Iteración inicial del sensor de posición para determinar la posición inicial del acercamiento
        Dist = float(board.distancia)
        print(Dist)
        time.sleep(0.1)
    distancia_aux = float(board.distancia)
    ti = time.clock()
    tiempo =[]
    Dist = []
    Dist_teo=[]
    board.velocidad = 200 #Defino la velocidad inicial
    vel_min = 60 #Voltaje mínimo para que funcione el sistema
    distancia_frenado = 20 #distancia final de frenado
    distancia_inicio= 50 #Defino la distancia para comenzar la aproximación controlada
    a = 1 #Defino la aceleración para realizar la aproximación
    kp = 0.01
    p = 0
    ki = 1
    i = 0
    kd=1
    d=0
    while distancia_aux > distancia_frenado:
        if distancia_aux < distancia_inicio:
             error = distancia_aux-distancia_frenado
             
        
        distancia_aux = float(board.distancia)
        tiempo_aux = time.clock() - ti
        error = distancia_aux-distancia_teo(tiempo_aux)
        Dist.append(distancia_aux)
        tiempo.append(tiempo_aux)
        time.sleep(0.1)
    board.velocidad = 0
    print(distancia_aux)


def posicion_teo(t,xo,vo,a):
    return xo+vo*t+ 0.5*a*t**2



plt.plot(tiempo,Dist,'-o')
plt.xlabel('Tiempo(s)')
plt.ylabel('Distancia(cm)')
plt.show()
np.savetxt('salida_240_distancia_2',Dist)
np.savetxt('salida_240_tiempo_2',tiempo)
#    board.velocidad = int(0)
#    time.sleep(5)
    