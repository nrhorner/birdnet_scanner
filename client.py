#!/usr/bin/env python
from pathlib import Path
import pyaudio
import socket
import sys
import time
import wave

PORT = 4442
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = RATE * 1000


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((sys.argv[1], PORT))
audio = pyaudio.PyAudio()


test_dir = Path('/home/neil/Desktop/birdnet')

stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)  # If you want to stream to speakers

chunk_nu = 0
play_audio = True
try:
    while True:
        data = s.recv(CHUNK)

        if play_audio:
            stream.write(data)
        else:
            # Only write wav files if there are less than a certain amount to be processed
            if len(list((test_dir.iterdir()))) > 5:
                print('Skipping audio. Too many unprocessed files')
                time.sleep(2)
                continue
            file_ = str(test_dir / f'bn_{chunk_nu}.wav')
            f = wave.open(file_, 'w')
            f.setnchannels(CHANNELS)
            f.setframerate(RATE)
            f.setsampwidth(audio.get_sample_size(FORMAT))
            f.writeframes(data)
            chunk_nu += 1

except KeyboardInterrupt:
    pass

print('Shutting down')
s.close()
stream.close()
audio.terminate()