import sounddevice as sd
from scipy.io.wavfile import write
import sys
from pathlib import Path
import time
import shutil
from datetime import datetime
import yaml
from pydub import AudioSegment

FREE_SPACE_LIMIT_MB = 100 # If less than 100mb remaining, don't record any more samples

cfg_path = sys.argv[1]
with open(cfg_path, 'r') as fh:
    cfg = yaml.load(fh)

sample_rate = cfg['sample_rate']

proj_dir = Path(cfg_path).parent
recording_dir = proj_dir / 'recordings'
recording_dir.mkdir(exist_ok=True, parents=True)


while True:
    myrecording = sd.rec(int(cfg['recording_length'] * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Wait until recording is finished
    fname = recording_dir / str(datetime.now())

    # Save with .tmp extension so. Rsync does not pick it up until it's fully written and it has a sound file extension
    tmp = fname.with_suffix('.tmp')

    # Could not get direct to mp3 working, so save to wav first
    # Write wav
    write(tmp, sample_rate, myrecording)  # Save as WAV file

    # to mp3
    seg = AudioSegment.from_wav(tmp)
    tmp.unlink()
    seg.export(tmp, format="mp3", bitrate="320k", codec='libmp3lame')
    shutil.move(tmp, fname.with_suffix('.mp3'))

    if shutil.disk_usage(proj_dir).free / 1e+6 <= FREE_SPACE_LIMIT_MB:
        print(f'Less than {FREE_SPACE_LIMIT_MB} disk space available. Waiting for space to free up')
        time.sleep(5)


