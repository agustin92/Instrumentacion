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

class ControlAutoPID(INODriver):
    velocidad = QuantityFeat('velocidad',getter=False)
    distancia = QuantityFeat('Distancia',setter=False)
 


def posicion_teo(t,xo,vo,a):
    return xo+vo*t+ 0.5*a*t**2

def posicion_ini(xf,vo,a,vmin):
    return xf-(vo*(vmin-vo))/a- 0.5*((vmin-vo)**2)/a
    
with ControlAutoPID.via_packfile('ControlAutoPID.pack.yaml') as board: 
    for i in range(5):  #Iteración inicial del sensor de posición para determinar la posición inicial del acercamiento
        Dist = float(board.distancia)
        print(Dist)
        time.sleep(0.1)
    distancia_aux = float(board.distancia)
    ti = time.clock()
    tiempo =[]
    Dist = []
    Dist_teo=[]
    velocidad_ini= 180
    velocidad_ini_cms=-38
    board.velocidad = velocidad_ini #Defino la velocidad inicial
    a = 3
    #Defino la aceleración para realizar la aproximación
    vel_min = 65 #Voltaje mínimo para que funcione el sistema
    distancia_frenado = 20 #distancia final de frenado
    distancia_inicio= posicion_ini(distancia_frenado,velocidad_ini_cms,a,-20) #Defino la distancia para comenzar la aproximación controlada
    kp = 2
    p = 0
    ki = 0.1
    i = 0
    kd=1.5
    d=0
    control=0
    ti_ciclo=0
    velocidad_aux = velocidad_ini
    pos_teo =[]
    pos_exp=[]
    tiempo_ciclo=[]
    pos_total=[]
    tiempo_total=[]
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
            if control_d:
                d = kd * (error - error_viejo) / (tiempo_aux - tiempo_viejo)
            error_viejo = error
            control_d= True
            tiempo_viejo = tiempo_aux
            # Setteamos la nueva velocidad.
            velocidad_aux = int(velocidad_aux + p + i + d)
            #Ponemos una cota mínima de velocidad para que el auto se mueva.
            if velocidad_aux < vel_min:
                velocidad_aux = vel_min
            if velocidad_aux>254:
                velocidad_aux=254
            
            
            
            
#            if control ==0:
#                ti_ciclo= time.clock()
#                control = 1
#            tiempo_aux= time.clock()-ti_ciclo
#            posicion_teo_calc = posicion_teo(tiempo_aux,distancia_inicio,velocidad_ini_cms,a)
#            error = distancia_aux-posicion_teo_calc
#            print(posicion_teo_calc)
#            print(distancia_aux)
#            print(error)
#            p = kp*error
#            velocidad_aux= int(velocidad_aux + p)
#            if velocidad_aux <vel_min:
#                velocidad_aux=vel_min
            board.velocidad= velocidad_aux
            tiempo_ciclo.append(tiempo_aux)
            pos_teo.append(posicion_teo_calc)
            pos_exp.append(distancia_aux)
            
        print("termino proporcional {}".format(p))
        print("termino integral {}".format(i))
        print("termino derivativo {}".format(d))
        tiempo_aux = time.clock() - ti
        tiempo_total.append(tiempo_aux)
        pos_total.append(distancia_aux)
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
#    board.velocidad = int(0)
#    time.sleep(5)
    