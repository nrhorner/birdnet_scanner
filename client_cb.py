#!/usr/bin/env python
from pathlib import Path
import pyaudio
import socket
import sys
import time
import wave
## This does not work at the moment
PORT = 4442
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 44100 * 50


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], PORT))
audio = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    print('fc', frame_count)
    data = s.recv(CHUNK)
    print(data)
    return (data, pyaudio.paContinue)

# test_dir = Path('/home/neil/Desktop/birdnet')


#
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK,
                    stream_callback=callback)  # If you want to stream to speakers


# Callback method
stream.start_stream()
while stream.is_active():
    print('test')
    time.sleep(0.1)

stream.stop_stream()
stream.close()

audio.terminate()
