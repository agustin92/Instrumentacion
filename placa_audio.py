# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 00:04:42 2019

@author: Agustin
"""

import pyaudio
import numpy as np
import wave 
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
    
    def play_sin(self, frec, duration=2, volume=0.5, sr=44100):
        length = sr*duration
        seno = (np.sin(2*np.pi*np.arange(length)*frec/sr)).astype(np.float32)
        self.stream = self.p.open(format=pyaudio.paFloat32,channels=1,rate=sr,output=True)
        self.stream.write(volume*seno)
        
    def sweep_sin(self, fi, ff, step, duration=3, volume =0.5):
        frecs = np.linspace(fi,ff,step)
        for i in frecs:
            self.play_sin(i,duration, volume)
        
