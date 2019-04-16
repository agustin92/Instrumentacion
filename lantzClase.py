import numpy as np

from lantz import Feat
from lantz import Action
from lantz.errors import InvalidCommand
from lantz.messagebased import MessageBasedDriver



class TDS1002b(MessageBasedDriver):

    MANUFACTURER_ID = '0x689'
    MODEL_CODE = '0x363'

    DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}
                           
    @Feat(read_once=True)
    def idn(self):
        return self.query('*IDN?')
        
    @Feat()
    def horizontal_division(self):
        """ Horizontal time base. 
        """
        return float(self.query('HOR:MAIN:SCA?'))
    
    @horizontal_division.setter
    def horizontal_division(self,value):
        """ Sets the horizontal time base. 
        """
        return float(self.send('HOR:MAIN:SCA {}'.format(value)))

    @Action()
    def acquire_parameters(self):
        """ Acquire parameters of the osciloscope.
            It is intended for adjusting the values obtained in acquire_curve
        """
        values = 'XZE?;XIN?;PT_OF?;YZE?;YMU?;YOF?;'
        answer = self.Resources.query('WFMP:{}'.format(values))
        parameters = {}
        for v, j in zip(values.split('?;'),answer.split(';')):
            parameters[v] = float(j)
        return parameters
    
    @Action()
    def data_setup(self):
        """ Sets the way data is going to be encoded for sending. 
        """
        self.send('DAT:ENC ASCI;WID 2') #ASCII is the least efficient way, but
# couldn't make the binary mode to work

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
        

if __name__ == '__main__':
    with TDS1002b('USB0::1689::867::C065087::0::INSTR') as inst:
        print('The identification of this instrument is : ' + inst.idn)
        print (inst.horizontal_division)
        #x,y = inst.acquire_curve
     



        
