# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 16:10:27 2019

@author: Agustin, Agostina y Christian
"""

from lantz.core.log import log_to_screen, DEBUG

log_to_screen(DEBUG)
from lantz.ino import INODriver, QuantityFeat
import time
import matplotlib.pyplot as plt
import numpy as np

class ControlAutoPID(INODriver):
    velocidad = QuantityFeat('velocidad',getter=False)
    distancia = QuantityFeat('Distancia',setter=False)

def posicion_teo(t,xo,vo,a):
    # Definimos la forma en la que queremos que el auto se mueva. En este caso,
    # un MRUV.
    return xo + (vo*t) + 0.5*a*t**2

def posicion_ini(xf,vo,a,vmin):
    
    return xf - (vo *(vmin-vo)) /a - 0.5 * ((vmin-vo) ** 2) /a
    
with ControlAutoPID.via_packfile('ControlAutoPID.pack.yaml') as board: 
    for i in range(5):  #Iteración inicial del sensor de posición para determinar la posición inicial del acercamiento
        dist = float(board.distancia)
        print("El rinamovil se encuentra a distancia %f de la pared.\n" % dist)
        time.sleep(0.1)
        
    distancia_aux = float(board.distancia)
    ti = time.clock()
    tiempo = []
    dist = []
    dist_teo = []
    
     ################# PARÁMETROS INICIALES DEL SISTEMA #################
    
    # Definimos la velocidad inicial del auto en pwm y en cm/seg.
    velocidad_ini = 180
    velocidad_ini_cms = - 38
    board.velocidad = velocidad_ini 
    # Definimos la aceleración a utilizar en la curva teórica a ajustar.
    a = 3
    vel_min = 65 # Voltaje pwm mínimo para que el auto se mueva
    distancia_frenado = 20 # distancia final de frenado [cm]
    
    # Definimos la distancia para comenzar la aproximación controlada
    distancia_inicio= posicion_ini(distancia_frenado,velocidad_ini_cms,a,-20) 
    
    # Parámetros del controlador PID
    kp = 2
    p = 0
    ki = 0.1
    i = 0
    kd = 1.5
    d = 0
    control = 0
    ti_ciclo = 0
    velocidad_aux = velocidad_ini
    pos_teo = []
    pos_exp = []
    tiempo_ciclo = []
    term_prop = []
    term_int = []
    term_diff = []
    control_d = False
    
    while distancia_aux > distancia_frenado:
        distancia_aux = float(board.distancia)
        print(distancia_aux)
        if distancia_aux < distancia_inicio:
            if control ==  0:
                ti_ciclo= time.clock()
                error_viejo = distancia_inicio - posicion_teo(0,distancia_inicio,velocidad_ini_cms,a)
                tiempo_viejo = 0
                control = 1
            tiempo_aux = time.clock() - ti_ciclo
            posicion_teo_calc = posicion_teo(tiempo_aux,distancia_inicio,velocidad_ini_cms,a)
            
            # A partir del error, calculamos los coeficientes PID para corregir.
            error = distancia_aux - posicion_teo_calc
            p = kp * error
            i += ki * error * tiempo_aux
            # Bypasseamos el primer cálculo del término derivativo.
            if control_d:
                d = kd * (error - error_viejo) / (tiempo_aux - tiempo_viejo)
                control_d= True
                
            error_viejo = error
            tiempo_viejo = tiempo_aux
            
            # Setteamos la nueva velocidad.
            velocidad_aux = int(velocidad_aux + p + i + d)
            #Ponemos una cota mínima de velocidad para que el auto se mueva.
            if velocidad_aux < vel_min:
                velocidad_aux = vel_min
            if velocidad_aux > 254:
                velocidad_aux = 254
            
            board.velocidad= velocidad_aux
            tiempo_ciclo.append(tiempo_aux)
            pos_teo.append(posicion_teo_calc)
            pos_exp.append(distancia_aux)
            
            term_prop.append(p)
            term_int.append(i)
            term_diff.append(d)
            
        time.sleep(0.02)
    board.velocidad = 0


plt.plot(tiempo_ciclo,pos_teo,'-ob')
plt.plot(tiempo_ciclo,pos_exp,'-or')
plt.xlabel('Tiempo(s)')
plt.ylabel('Distancia(cm)')
plt.savefig('Curva_buena_pos_teo_a_3_vini_-38_vmin_20_kp_2_ki_01_kd_1p5(p)_v2')
plt.show()
np.savetxt('pos_teo_a_3_vini_-38_vmin_20_kp_2_ki_01_kd_1p5(p)_v2.txt',pos_teo)
np.savetxt('pos_exp_a_3_vini_-38_vmin_20_kp_2_ki_01_kd_1p5(p)_v2.txt',pos_exp)
np.savetxt('tiempo_a_3_vini_-38_vmin_20_kp_2_ki_01_kd_1p5(p)_v2.txt',tiempo_ciclo)

fig2 = plt.figure()
plt.plot(tiempo_ciclo, term_prop, '-o', color='purple', label='Término proporcional')
plt.plot(tiempo_ciclo, term_int, '-o', color='blue', label='Término integral')
plt.plot(tiempo_ciclo, term_diff, '-o', color='orange', label='Término diferencial')

