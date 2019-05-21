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


data = []

with nidaqmx.Task() as task:
     task.ai_channels.add_ai_voltage_chan("Dev1/ai1",terminal_config = TerminalConfiguration.RSE)
     task.timing.cfg_samp_clk_timing(rate= 20000,samps_per_chan=5000)
     data = task.read(number_of_samples_per_channel=2000)

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

