from pathlib import Path
import time
import datetime
import subprocess as sub
import sys
import yaml


cfg_path = sys.argv[1]
with open(cfg_path, 'r') as fh:
    cfg = yaml.load(fh)

proj_dir = Path(cfg_path).parent
recording_dir = proj_dir / 'recordings'
recording_dir.mkdir(exist_ok=True)


inference_dir = proj_dir / 'bns_ids'
inference_dir.mkdir(exist_ok=True)

week = str(datetime.date.today().isocalendar()[1])

bnlite_root = Path(cfg['bnlite_root']).expanduser()
analyze_script = bnlite_root / 'analyze.py'


def copyfiles():

    print('copying files from listener')
    sub.call(['rsync',
              '-av',
              '--remove-source-files',
              '--include', '*.wav',
              f'pi@{cfg["recorder_ip"]}:/home/pi/bn/recordings',  # TODO: Remove this hard coding
              f'{recording_dir}'
              ])


def run_birdnet():

    for file_ in recording_dir.iterdir():
        print(f'Doing bird song id for {file_.name}')

        outfile = inference_dir / f'{file_.name}.csv'
        sub.call(['python3', str(analyze_script),
                  '--i', file_,
                  '--o' , outfile,
                  '--lat', str(cfg['lat_long'][0]),
                  '--lon', str(cfg['lat_long'][1]),
                  '--week', week], cwd=str(bnlite_root))

        # # Now remove files
        # print('removing local files')
        # for f in outdir.iterdir():
        #     f.unlink()

while True:
    copyfiles()
    run_birdnet()
    time.sleep(30)








