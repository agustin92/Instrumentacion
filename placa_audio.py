# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 00:04:42 2019

@author: Agustin
"""

import pyaudio
import numpy as np
from matplotlib import pyplot as plt

class PlacaAudio():
    def __init__(self):
        self.p = pyaudio.PyAudio()
        
    def record(self,duracion,sr=44100,CHUNK=1024,FORMAT = pyaudio.paInt16, CHANNELS = 2):
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
        return np.fromstring(b''.join(frames),dtype=np.int16)
