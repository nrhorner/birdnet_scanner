import sounddevice as sd
from scipy.io.wavfile import write
import sys
from pathlib import Path
import time


MAX_FILE_BACKLOG = 10
from datetime import datetime
RECORDING_TIME = 15
SAMPLE_RATE = 44100

outdir = Path.home() / 'bns_recordings'
outdir.mkdir(exist_ok=True)


while True:
    myrecording = sd.rec(int(RECORDING_TIME * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1)
    sd.wait()  # Wait until recording is finished
    fname = outdir / f'{str(datetime.now())}.wav'
    write(fname, SAMPLE_RATE, myrecording)  # Save as WAV file

    if len(list(outdir.iterdir())) > MAX_FILE_BACKLOG:
        print('Max file backlog reached. Waiting')
        time.sleep(5)



