#!/usr/bin/env python
# encoding: utf-8

## Module infomation ###
# Python (3.4.4)
# numpy (1.10.2)
# PyAudio (0.2.9)
# matplotlib (1.5.1)
# All 32bit edition
########################

import numpy as np
import pyaudio

import matplotlib.pyplot as plt

import requests

url = 'http://127.0.0.1:5001/robot/incline?angles='



def normalize(v):
    norm = np.linalg.norm(v, ord=1)
    if norm == 0:
        norm = np.finfo(v.dtype).eps
    return v / norm


class SpectrumAnalyzer:
    FORMAT = pyaudio.paFloat32
    CHANNELS = 1
    RATE = 16000
    CHUNK = 4096
    START = 0
    N = 3

    wave_x = 0
    wave_y = 0
    spec_x = 0
    spec_y = 0
    data = []

    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=self.FORMAT,
                                   channels=self.CHANNELS,
                                   rate=self.RATE,
                                   input=True,
                                   output=False,
                                   frames_per_buffer=self.CHUNK)
        # Main loop
        self.loop()

    def loop(self):
        try:
            while True:
                self.data = self.audioinput()
                self.fft()
                self.graphplot()

        except KeyboardInterrupt:
            self.pa.close()

        print("End...")

    def audioinput(self):
        ret = self.stream.read(self.CHUNK)
        ret = np.fromstring(ret, np.float32)
        return ret

    def fft(self):
        self.wave_x = range(self.START, self.START + self.N)
        self.wave_y = self.data[self.START:self.START + self.N]
        self.spec_x = np.fft.fftfreq(self.N, d=1.0 / self.RATE)
        y = np.fft.fft(self.data[self.START:self.START + self.N])
        self.spec_y = [np.sqrt(c.real ** 2 + c.imag ** 2) * 100.0 for c in y]

    def graphplot(self):
        plt.clf()
        # wave
        plt.subplot(311)
        plt.plot(self.wave_x, self.wave_y)
        # print("wave:" + str(self.wave_x) + "," + str(self.wave_y))
        norm = 100.0 * np.linalg.norm(self.wave_y)
        print("Norm:" + str(norm))
        plt.axis([self.START, self.START + self.N, -0.5, 0.5])
        plt.xlabel("time [sample]")
        plt.ylabel("amplitude")
        # Spectrum
        plt.subplot(312)
        plt.plot(self.spec_x, self.spec_y, marker='o', linestyle='-')
        plt.axis([0, self.RATE / 2, 0, 50])
        plt.xlabel("frequency [Hz]")
        plt.ylabel("amplitude spectrum")
        # print("freq:" + str(self.spec_x) + "," + str(self.spec_y))
        dir = normalize(np.array(self.spec_y))
        print("Normalized vector" + str(dir))

        result_vec = np.append(dir, norm)

        result_url_string = url + ','.join(map(str, result_vec))
        print("Result URL:" + result_url_string)
        response = requests.put(result_url_string)
        print("Response:" + str(response))
        # Pause
        plt.pause(.01)


if __name__ == "__main__":
    spec = SpectrumAnalyzer()
