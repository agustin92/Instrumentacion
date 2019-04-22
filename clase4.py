from lantz import MessageBasedDriver 
from lantz import Feat, Action
import numpy as np
import time
from pylab import *

# MessageBasedDriver toma como argumento, el resource name.
# Del generador de funciones, es 'USB0::1689::838::C034167::0::INSTR'

gen = 'USB0::1689::838::C034167::0::INSTR'
osc = 'USB0::1689::867::C065087::0::INSTR'

class TekGen(MessageBasedDriver):
    
    DEFAULTS = {'COMMON': {'write_termination': '\n','read_termination': '\n'}}
    
    @Feat()
    def identity(self):
        return self.query('*IDN?')
    
    @Feat()
    def amplitude(self):
        return float(self.query('SOUR1:VOLT:AMPL?'))
    
    @amplitude.setter
    def amplitude(self, volts, channel=1):
        self.write("SOUR{}:VOLT:AMPL {}".format(channel, volts))
        
    def frequency_set(self, hertz, channel=1):
        self.write("SOUR{}:FREQ:FIX {}".format(channel, hertz))
        
    def waveform_shape(self, shape = 'SIN', channel = 1):
        # Formas posibles: SIN, SQU, PULS, RAMP
        # PRNoise, DC|SINC|GAUSsian|LORentz|ERISe|EDECay|
        # HAVersine
        self.write('SOUR{}:FUNC:SHAPE {}'.format(channel, shape))
    
        

class TekOsc(MessageBasedDriver):
    
    @Feat()
    def identity(self): 
        return self.query('*IDN?')
    
    # Tomamos estas tres siguientes funciones del 
    # https://github.com/lantzproject/lantz-drivers/blob/master/lantz/drivers/
    # tektronix/tds1012.py para probar
    # el osciloscopio porque arrojaba timeout hasta haciendo un identity.
    # Lametablemente, no funcionó.
    
    @Action()
    def acquire_parameters(self):
        """ Acquire parameters of the osciloscope.
            It is intended for adjusting the values obtained in acquire_curve
        """
        values = 'XZE?;XIN?;PT_OF?;YZE?;YMU?;YOF?;'
        answer = self.query('WFMP:{}'.format(values))
        parameters = {}
        for v, j in zip(values.split('?;'),answer.split(';')):
            parameters[v] = float(j)
        return parameters
    
    @Action()
    def data_setup(self):
        """ Sets the way data is going to be encoded for sending. 
        """
        self.send('DAT:ENC ASCI;WID 2')
    
    @Action()
    def acquire_curve(self,start=1,stop=2500):
        """ Gets data from the oscilloscope. It accepts setting the start and 
            stop points of the acquisition (by default the entire range).
        """
        parameters = self.acquire_parameters()
        self.data_setup() 
        self.send('DAT:STAR {}'.format(start))
        self.send('DAT:STOP {}'.format(stop))
        data = self.query('CURV?')
        data = data.split(',')
        data = np.array(list(map(float,data)))
        ydata = (data - parameters['YOF']) * parameters['YMU']\
                + parameters['YZE']
        xdata = np.arange(len(data))*parameters['XIN'] + parameters['XZE']
        return list(xdata), list(ydata)
    
    
    # Definimos un getter y un setter usando los feats:
    @Feat()
    def timebase(self):
        return float(self.query('HOR:MAIN:SCA?'))

    @timebase.setter
    def set_timebase(self, value):
        return self.write('HOR:MAIN:SCA {}'.format(value))
    
##
inst1 = TekGen(gen)
inst2 = TekOsc(osc)

inst2 = TekOsc('USB0::1689::872::C017059::0::INSTR')

# Inicializamos los dos instrumentos
inst1.initialize()
inst2.initialize()

# Armamos un programa que cambie la frecuencia del gen, y que el osciloscopio 
# la levante.

ion()

freq_ini = 10
freq_fin = 20
steps = 10
i = -1

freqs = np.arange(freq_ini, freq_fin, steps)

x, y = inst2.acquire_curve()

for frecuencia in freqs:
    i += 1
    inst1.frequency_set(frecuencia)
    time.sleep(2)
    pantallax, pantallay = inst2.acquire_curve()
    
    if i == 0:
        line1, = plot(pantallax, pantallay, color='orange')
        draw()
    else:
        line1.set_xdata(pantallax)
        line1.set_ydata(pantallay)
        draw()
        

# Finalizamos los dos instrumentos
inst1.finalize()
inst2.finalize()

