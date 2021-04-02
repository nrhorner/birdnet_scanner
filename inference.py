from pathlib import Path
import time
import datetime
import subprocess as sub
import sys
import yaml
import shutil
import threading

from birdnet_scanner import db_save


cfg_path = sys.argv[1]
with open(cfg_path, 'r') as fh:
    cfg = yaml.load(fh)

proj_dir = Path(cfg_path).parent
recording_dir = proj_dir / 'recordings'
recording_dir.mkdir(exist_ok=True)


inference_dir = proj_dir / 'bns_ids'
inference_dir.mkdir(exist_ok=True)
processed_wav_dir = proj_dir / 'processed_wavs'
processed_wav_dir.mkdir(exist_ok=True)

week = str(datetime.date.today().isocalendar()[1])

bnlite_root = Path(cfg['bnlite_root']).expanduser()
analyze_script = bnlite_root / 'analyze.py'


def copyfiles():
    """
    Copy any finished recordings from the Pi zero

    The order of --include and --excludes is significant
    """
    while True:
        print('copying files from listener')
        sub.call(['rsync',
                  '-av',
                  '--remove-source-files',
                  '--progress',
                  '--exclude', ".*",
                  '--include', "*.mp3",
                  '--exclude', "*",
                        f'pi@{cfg["recorder_ip"]}:/home/pi/bn/recordings/',  # TODO: Remove this hard coding
                  f'{recording_dir}'
                  ])
        time.sleep(5)


def run_birdnet():

    print('Starting file transfer on seperate thread')
    th = threading.Thread(target=copyfiles)
    th.start()

    print('Doing inference')
    while True:
        for i, file_ in enumerate(recording_dir.iterdir()):
            if not file_.is_file():
                continue
            if file_.name.startswith('.'):
                continue

            if i % 2 == 0: # 5
                print('saving to db')
                dbsave()

            print(f'Doing bird song id for {file_.name}')

            outfile = inference_dir / f'{file_.with_suffix("").name}.csv'
            sub.call(['python3', str(analyze_script),
                      '--i', file_,
                      '--o' , outfile,
                      '--lat', str(cfg['lat_long'][0]),
                      '--lon', str(cfg['lat_long'][1]),
                      '--week', week], cwd=str(bnlite_root))
            shutil.move(file_, processed_wav_dir / file_.name)


def dbsave():
    db_save.run(proj_dir, cfg['min_conf'])

run_birdnet()










