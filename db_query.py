import sqlalchemy
import pandas as pd

def top_ids() -> pd.DataFrame:
    """
    Just for testing
    Maybe add date range option
    """
    db_file = str('/home/neil/bn/bn.db')
    engine = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)

    sql = """SELECT COUNT(`index`) as count, `Common Name`
                FROM ids
                GROUP BY `Common Name`
                HAVING COUNT(`index`) > 5
                ORDER BY count  DESC;
                """

    with engine.connect() as con:
        x = pd.read_sql(sql, con)
        return x


def top_ids_last_24h() -> pd.DataFrame:
    # Theres no current recording so choose last active day for testing
    db_file = str('/home/neil/bn/bn.db')
    engine = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)

    start = '2021-03-08'
    end = '2021-03-09'

    sql = f"""SELECT COUNT(`index`) as count, `Common Name`
                    FROM ids
                    WHERE TIME > {start} AND time < {end}
                    GROUP BY `Common Name`
                    HAVING COUNT(`index`) > 5
                    ORDER BY count  DESC;
                    """

    with engine.connect() as con:
        x = pd.read_sql(sql, con)
        return x