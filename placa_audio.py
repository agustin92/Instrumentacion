# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 00:04:42 2019

@author: Agustin
"""
import visa

import time
import pyaudio
import numpy as np
import wave 
from matplotlib import pyplot as plt

class PlacaAudio():
    def __init__(self):
        self.p = pyaudio.PyAudio()
        
    #Funcion para saber cuantos dispositivos de audio hay en la placa    
    def info_devices(self):
        info = self.p.get_host_api_info_by_index(0)
        numdevices = info.get('deviceCount')

        for i in range (0,numdevices):
            if self.p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                print ("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0,i).get('name'))

            if self.p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                print ("Output Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0,i).get('name'))

        devinfo = self.p.get_device_info_by_index(1)
        print ("Selected device is ",devinfo.get('name'))
        
        
    def record(self,duracion,sr=44100,CHUNK=1024,FORMAT = pyaudio.paInt16, CHANNELS = 2):
        # Tengo dos canales
        self.stream = self.p.open(format=FORMAT, 
                                  channels=CHANNELS, 
                                  rate=sr, 
                                  input=True, 
                                  frames_per_buffer=CHUNK)
        print("* recording")

        frames = []

        for i in range(0, int(sr / CHUNK * duracion)):
            self.data = self.stream.read(CHUNK)
            frames.append(self.data)
        
        print("* done recording")
        
        self.stream.stop_stream()
        self.stream.close()
        tiempo = np.arange(0,duracion,1/40960)
        return tiempo, np.fromstring(b''.join(frames),dtype=np.int16)
    
    def play_sin(self, frec, duration=2, volume=0.5, sr=44100):
        length = sr*duration
        seno = (np.sin(2*np.pi*np.arange(length)*frec/sr)).astype(np.float32)
        self.stream = self.p.open(format=pyaudio.paFloat32,channels=1,rate=sr,output=True)
        self.stream.write(volume*seno)
    


        
    def sweep_sin(self, fi, ff, step, duration=3, volume =0.5):
        frecs = np.linspace(fi,ff,step)
        for i in frecs:
            self.play_sin(i,duration, volume)
            print(i)
    
    def ch_separator(self,data):
        ch1=[]
        ch2=[]
        i=0
        for elemento in data:
            if i%2==0:
                ch1.append(elemento)
            else:
                ch2.append(elemento)
            i += 1
        return ch1,ch2
                



#Control del osciloscopio      
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

class Osciloscopio:
    
    def __init__(self,rm,num):
        data = rm.list_resources()
        self.inst = rm.open_resource('{}'.format(data[num]))
        self.parameters = None
        
    def identity(self):
        #Devuelve el nombre del instrumento según el fabricante.
        name = self.inst.query("*IDN?")
        print("Name of this device: {}".format(name))
    
    def get_parameters(self):
        self.parameters = self.inst.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')
        
#        if self.parameters is None:
#            self.parameters = self.inst.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

    
    def curva(self):
        self.get_parameters()
        xze, xin, yze, ymu, yoff = self.parameters
        data = self.inst.query_ascii_values("CURV?",container=np.array)
        tiempo = xze + np.arange(len(data)) * xin
        data = (data-yoff)* ymu + yoff
        return tiempo, data


def input_placa(gen, placa,freq_inicial, freq_final, step, stop = 1, channel = 1):
        # Hace un barrido de frecuencias desde freq_inicial hasta freq_final
        # con un step. Entre cada cambio de frecuencia dejamos 1 segundo de
        # stop.
        frecuencias = np.arange(freq_inicial, freq_final, step)
        salida = []
        for elemento in frecuencias:
            gen.set_freq(elemento)
            salida.extend(placa.record(0.05, CHANNELS=1)[1])
            time.sleep(stop)
        
        return salida

rm = visa.ResourceManager()
data = rm.list_resources()

#%%
      

plt.xlabel('Tiempo (s)')
plt.ylabel('Voltaje (mV)')  
plt.plot(vd[50:],v2[50:],'-')


#%%

tiempo,data = p.record(0.1,CHANNELS = 2,sr=192000)
ch1,ch2 = p.ch_separator(data)
plt.plot(ch1,'.-')
plt.plot(ch2,'.-')

ch1 = np.array(ch1)
ch2 = np.array(ch2)

#plt.grid()
plt.plot(data,'.-')