"""
This code will take the birdnet ids, parse and stick in the DB
"""
from pathlib import Path
import pandas as pd
import sqlalchemy
from datetime import datetime


def parse_ids(id_dir: Path) -> pd.DataFrame:

    dfs = []

    for f in id_dir.iterdir():
        dfs.append(pd.read_csv(f, sep='\t'))

    df = pd.concat(dfs)
    df = df[df['Confidence'] > 0.99]

    df.sort_values('Confidence', ascending=False, inplace=True)
    df.rename(columns={'Begin File': 'time'}, inplace=True)
    df.time = df.time.map(lambda x: x.strip('.wav'))
    df.time = pd.to_datetime(df.time, yearfirst=True)
    # df.set_index('time', drop=True, inplace=True)

    return df


def run(root: Path):
    # TDOD: How to just add new rows rather then overwrite the table
    db_file = str(root / 'bn.db')

    engine = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)

    with engine.connect() as connection:
        id_file = root / 'bns_ids'
        df_ids = parse_ids(id_file)

        # save all ids to ids db
        df_ids.to_sql('ids', connection, if_exists='replace')
        df_ids.to_csv(root / 'test.csv')




# def test_time():
#     db  = '/home/neil/bn/bn.db'
#     csv = '/home/neil/bn/test.csv'
#
#
#     start = datetime.now()
#     df = pd.read_csv(csv)
#     end = datetime.now()
#     elapsed = end = start
#     print(elapsed.microsecond)
#
#     start = datetime.now()
#     engine = sqlalchemy.create_engine(f'sqlite:///{db}', echo=True)
#     sqlite_connection = engine.connect()
#     df = pd.read_sql('SELECT * FROM ids;', sqlite_connection)
#     end = datetime.now()
#     elapsed = end = start
#     print(elapsed.microsecond)




if __name__ == '__main__':
    bn_dir = Path('~/bn').expanduser()
    run(bn_dir)

    # test_time()