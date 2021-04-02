"""
This code will take the birdnet ids, parse and stick in the DB
"""
from pathlib import Path
import pandas as pd
import sqlalchemy
import shutil
from datetime import datetime

from typing import List

def parse_ids(id_dir: Path, confidence) -> pd.DataFrame:

    # Place to store_ids_before deleting in case soemthing goes wrong
    temp_id_dir = Path(str(id_dir) + '_processed')
    temp_id_dir.mkdir(exist_ok=True)

    dfs = []
    # id_dir = Path('/mnt/pi4/bn/bns_ids')
    for f in id_dir.iterdir():

        if f.is_dir():
            continue

        if not str(f).endswith('csv'):
            continue
        try:
            d = pd.read_csv(f, sep=';')
        except Exception:
            shutil.move(f, temp_id_dir / f.name)
            continue

        shutil.move(f, temp_id_dir / f.name)

        if len(d) == 0:
            continue

        try:
            d['time'] = f.with_suffix("").name
        except Exception:
            print(f'File name with error: {f}')

        d.time = pd.to_datetime(d.time, yearfirst=True)
        dfs.append(d)

    try:
        df = pd.concat(dfs)
    except (ValueError, UnboundLocalError):
        print('No ids to save')
        return
    df = df[df['Confidence'] > confidence]

    df.sort_values('Confidence', ascending=False, inplace=True)
    return df


def run(root: Path, conf) -> List[Path]:
    # TDOD: How to just add new rows rather then overwrite the table
    db_file = str(root / 'bn.db')

    engine = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)

    with engine.connect() as connection:
        id_root = root / 'bns_ids'
        df_ids = parse_ids(id_root, conf)
        if df_ids is not None:

            # save all ids to ids db
            df_ids.to_sql('ids', connection, if_exists='append')
            df_ids.to_csv(root / 'test.csv')


if __name__ == '__main__':
    import sys
    root_ = sys.argv[1]
    conf_ = sys.argv[2]

    run(Path(root_), float(conf_))
