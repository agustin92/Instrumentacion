import visa

# Inicializamos el Resource Manager de visa. En el caso de pyvisa-py, se coloca
# el '@py'. Sino, con NiVisa, va vacío.

rm = visa.ResourceManager('@py')

#inst.query("SOUR1:FREQ:FIX 1")


class Tek:

    def __init__(self, rm, num):
        data = rm.list_resources()
        self.inst = rm.open_resource('{}'.format(data[num]))
        
    def identity(self):
        #Devuelve el nombre del instrumento según el fabricante.
        name = self.inst.query("*IDN?")
        print("Name of this device: {}".format(name))
        
    def set_freq(self, value):
        # Settea la frecuencia (en Hz) del instrumento.
        self.inst.query("SOUR1:FREQ:FIX {}".format(value))
        
    def set_amp(self, value):
        #Settea la amplitud (en V) del instrumento.
        self.inst.query("SOUR1:VOLT:AMPL {}".format(value))
    

# Inicializamos el instrumento num = 0 en la lista (si tenemos uno solo 
# conectado, es trivial)      
        
gen = Tek(rm, 0)

# Si quisiéramos poner la frecuencia del instrumento en 40hz:
gen.set_freq(40)
   
    