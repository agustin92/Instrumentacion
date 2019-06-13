# -*- coding: utf-8 -*-
"""
Created on Tue May 21 16:56:28 2019

@author: Agustin
"""
import nidaqmx
import matplotlib.pyplot as plt
import numpy as np
import time
from nidaqmx.constants import TerminalConfiguration
from nidaqmx.constants import AcquisitionType
from nidaqmx.constants import READ_ALL_AVAILABLE
import visa

data = []

with nidaqmx.Task() as task:
     task.ai_channels.add_ai_voltage_chan("Dev2/ai1",terminal_config = TerminalConfiguration.DIFFERENTIAL)
     task.timing.cfg_samp_clk_timing(rate= 250000,sample_mode= AcquisitionType.CONTINUOUS)
     data = task.read(number_of_samples_per_channel= 1000000)

plt.plot(data)


#%%
data=[]
with nidaqmx.Task() as task:
     task.ai_channels.add_ai_voltage_chan("Dev2/ai1",terminal_config = TerminalConfiguration.DIFFERENTIAL)
     task.timing.cfg_samp_clk_timing(rate= 20000,sample_mode= AcquisitionType.CONTINUOUS)
     for i in range(10):
         data.extend(task.read(number_of_samples_per_channel= 1000))
         time.sleep(1)

plt.plot(data)


#samps_per_chan= 100000,
#number_of_samples_per_channel= 0000
#%%

rm = visa.ResourceManager()
data = rm.list_resources()

class TekGen:
    
    # Me defino un template para los generadores de funciones de tektronix.
    # Para crear un generador, se necesita proveer el resource manager,
    # y la posición que ocupa el instrumento en la lista de list.resources().
    
    def __init__(self, rm, num):
        # Si el generador de funciones responde, se escucha un beep al inicia_
        # lizarlo.
        data = rm.list_resources()
        self.inst = rm.open_resource('{}'.format(data[num]))
        self.inst.write('SYSTEM:BEEPER:IMM')        
        
    def identity(self):
        print(self.inst.query('*IDN?'))
    
    def set_freq(self, hertz):
        self.inst.write("SOUR1:FREQ:FIX {}".format(hertz))
        
    def set_amp(self, volts):
        self.inst.write("SOUR1:VOLT:AMPL {}".format(volts))
    
    def waveform_shape(self, channel = 1, shape = 'SIN'):
        # Formas posibles: SIN, SQU, PULS, RAMP
        # PRNoise, DC|SINC|GAUSsian|LORentz|ERISe|EDECay|
        # HAVersine
        self.inst.write('SOUR{}:FUNC:SHAPE {}'.format(channel, shape))
        
    def waveform_phase(self, radians, channel = 1):
        self.inst.write('SOUR{}:PHAS {})'.format(channel, radians))
    
    def freq_sweep(self, freq_inicial, freq_final, step, stop = 1, channel = 1):
        # Hace un barrido de frecuencias desde freq_inicial hasta freq_final
        # con un step. Entre cada cambio de frecuencia dejamos 1 segundo de
        # stop.
        frecuencias = np.arange(freq_inicial, freq_final, step)
        for elemento in frecuencias:
            self.inst.write('SOUR{}:FREQ:FIX {}'.format(channel, elemento))
            time.sleep(stop)




#%%

todos=[]     

plt.plot(data,'.-')
plt.plot(data[1],'.-r')
plt.plot(data[2],'.-g')
plt.grid()
for i in range(2000):
    todos.append(data[0][i])
    todos.append(data[1][i])
    todos.append(data[2][i])


plt.plot(todos,'.-',color='orange')

nidaqmx.constants.TerminalConfiguration.NRSE

