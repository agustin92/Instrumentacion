import visa
import numpy as np
import time
import pyaudio
import wave


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
            
            
            
            
rm = visa.ResourceManager('@py')
data = rm.list_resources()
generador = TekGen(rm, 0)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100 #  number of samples of audio carried per second
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "agus.wav"

# Abrimos una instancia de pyaudio?
p = pyaudio.PyAudio()

#Abrimos una stream

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()