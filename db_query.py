import sqlalchemy
import pandas as pd
from datetime import datetime, timedelta


def top_ids(db_file=None) -> pd.DataFrame:
    """
    Just for testing
    Maybe add date range option
    """
    if not db_file:
        db_file = str('/home/neil/bn/bn.db')
    engine = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)

    sql = """SELECT COUNT(`index`) as count, `Common Name`
                FROM ids
                GROUP BY `Common Name`
                ORDER BY count  DESC;
                """

    with engine.connect() as con:
        x = pd.read_sql(sql, con)
        return x


def top_ids_last_24h(db_file=None) -> pd.DataFrame:
    # Theres no current recording so choose last active day for testing
    if not db_file:
        db_file = str('/home/neil/bn/bn.db')
    engine = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)

    start = datetime.now() - timedelta(days = 1)
    end = datetime.now()

    sql = f"""SELECT COUNT(`index`) as count, `Common Name`, max(time)
                    FROM ids
                    WHERE time BETWEEN '{start}' AND '{end}'
                    GROUP BY `Common Name`
                    ORDER BY count  DESC;
                    """

    with engine.connect() as con:
        x = pd.read_sql(sql, con)
        x.rename(columns={'max(time)': 'last seen'}, inplace=True)
        x['last seen'] = x['last seen'].astype('datetime64[s]')
        x.sort_values('last seen', ascending=False, inplace=True)
        return x

if __name__ == '__main__':
    x = top_ids_last_24h('/mnt/pi4/bn/bn.db')
    print(x)