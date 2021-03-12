from pathlib import Path
import time

outdir = Path.home() / 'bns_recordings'
outdir.mkdir(exist_ok=True)

BN_DIR = '/home/neil/git/BirdNET'

inference_dir = Path.home() / 'bns_ids'
inference_dir.mkdir(exist_ok=True)

import subprocess as sub

SERVER = '192.168.0.52'

while True:
    print('copying files from listener')
    sub.call(['rsync',
              '-av',
              '--remove-source-files',
              '--include', '*.wav',
              f'pi@{SERVER}:/home/pi/bns_recordings/',
              '/home/neil/bns_recordings'
              ])
    if len(list(outdir.iterdir())) > 0:
        print('Doing bird song id')

        sub.call(['python3', '/home/neil/git/BirdNET/analyze.py',
                  '--i', outdir,
                  '--o' , inference_dir], cwd=BN_DIR)

        # Now remove files
        print('removing local files')
        for f in outdir.iterdir():
            f.unlink()

    else:
        time.sleep(10)
        continue




