# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 19:42:18 2019

@author: Agustin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:20:10 2019

@author: Agustin
"""


from lantz.core.log import log_to_screen, DEBUG

log_to_screen(DEBUG)
from lantz.ino import INODriver, BoolFeat, QuantityFeat
import time
import matplotlib.pyplot as plt
import numpy as np

class ControlArduino(INODriver):
    rampa = QuantityFeat('Voltaje',getter=False)
    senal = QuantityFeat('senal',setter=False)
    
with ControlArduino.via_packfile('ControlArduino.pack.yaml') as board:
    setpoint = 500
    i = 0
    j = 0
    volt= []
    board.rampa = 0
    time.sleep(2)
    kp= 0.3
    p=0
    while p < 255 and j<300:
        aux = float(board.senal)
        error = (setpoint - aux)
        p = p + int(kp*error)
        board.rampa = p
        volt.append(aux)
        j = j +1 
        print(p)
#        print(board.rampa)
#        print(aux)
plt.plot(volt)
plt.xlabel('Iteracion')
plt.ylabel('Voltaje (mV)')
plt.show()  
    
npvolt = np.array(volt)
np.savetxt('C:/Users/Agustin/Documents/Instrumentacion/Clase 10/control_P_500mV_setpoint_kp05.txt',npvolt)  