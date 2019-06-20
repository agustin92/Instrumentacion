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
    setpoint = 1000
    i = 0
    j = 0
    volt= []
    board.rampa = 0
    time.sleep(2)
    kp= 0.04
    ki= 0.02
    kd= 0.002
    p=0
    i=0
    d=0
    ti = time.clock()
    lasterror= 0
    while p < 255 and j<300:
        aux = float(board.senal)
        error = (setpoint - aux)
        tf = time.clock()
        deltat = tf-ti
        p = p + int(kp*error)
        i = i + int(ki*error*deltat)
        d = d + int(kd*(error-lasterror)/deltat)
        board.rampa = p + i 
        volt.append(aux)
        ti = tf
        lasterror= error
        j = j +1 
        print(p)
#        time.sleep(0.5)
#        print(board.rampa)
#        print(aux)
plt.plot(volt)
plt.xlabel('Iteracion')
plt.ylabel('Voltaje (mV)')
plt.show()  
    
npvolt = np.array(volt)
np.savetxt('C:/Users/Agustin/Documents/Instrumentacion/Clase 11/control_PID_1000mV_setpoint_kp004_ki002_kd0002_p200.txt',npvolt)  