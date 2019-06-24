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
    for i in range(5):
        Dist = float(board.distancia)
        print(Dist)
        time.sleep(0.1)
    distancia_aux = float(board.distancia)
    ti = time.clock()
    tiempo =[]
    Dist = []
    while distancia_aux > 30:
        board.velocidad = 240
        distancia_aux = float(board.distancia)
        Dist.append(distancia_aux)
        tiempo.append(time.clock() - ti)
        time.sleep(0.1)
    board.velocidad = 0
    print(distancia_aux)

plt.plot(tiempo,Dist,'-o')
plt.xlabel('Tiempo(s)')
plt.ylabel('Distancia(cm)')
plt.show()
np.savetxt('salida_240_distancia_2',Dist)
np.savetxt('salida_240_tiempo_2',tiempo)
#    board.velocidad = int(0)
#    time.sleep(5)
    