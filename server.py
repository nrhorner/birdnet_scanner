"""
This module gets the audio input from the remore RPi and streams it over WiFi

Adapted frrom https://gist.github.com/fopina/3cefaed1b2d2d79984ad7894aef39a68
"""

#!/usr/bin/env python3

import pyaudio
import socket
import select

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = RATE * 10

audio = pyaudio.PyAudio()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 4442))
serversocket.listen(5)


def callback(in_data, frame_count, time_info, status):
    for s in read_list[1:]:
        s.send(in_data)
    return (None, pyaudio.paContinue)


# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)
# stream.start_stream()

read_list = [serversocket]
print("recording...")

try:
    while True:
        readable, writable, errored = select.select(read_list, [], [])

        try:
            for s in readable:
                if s is serversocket:
                    (clientsocket, address) = serversocket.accept()
                    read_list.append(clientsocket)
                    print("Connection from", address)
                else:
                    data = s.recv(1024)
                    if not data:
                        read_list.remove(s)
        except ConnectionResetError:
            print('Connection reset')
except KeyboardInterrupt:
    pass


print("finished recording")

serversocket.close()
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()