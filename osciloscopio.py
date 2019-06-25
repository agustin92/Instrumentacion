import visa
import numpy as np
from matplotlib import pyplot as plt
# Inicializamos el Resource Manager de visa. En el caso de pyvisa-py, se coloca
# el '@py'. Sino, con NiVisa, va vacío.

rm = visa.ResourceManager()



class Osciloscopio:
    
    def __init__(self,rm,num):
		# Toma como parámetros para abrir el canal de comunicación el ResourceManager 
        #y el número de equipo dentro de la lista de instrumentos
        data = rm.list_resources() # Guarda la información de la lista de instrumentos
        self.inst = rm.open_resource('{}'.format(data[num])) 
        self.parameters = None 
        
    def identity(self):
        #Devuelve el nombre del instrumento según el fabricante.
        name = self.inst.query("*IDN?")
        print("Name of this device: {}".format(name))
    
    def get_parameters(self):
        # Toma los parámetros necesarios para escalar la señal del osciloscopio
        if self.parameters is None:
            self.parameters = self.inst.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

    
    def curva(self):
        # 
        self.get_parameters()
        xze, xin, yze, ymu, yoff = self.parameters
        data = self.inst.query_ascii_values("CURV?",container=np.array)
        tiempo = xze + np.arange(len(data)) * xin
        data = (data-yoff)* ymu + yoff
        return tiempo, data



		