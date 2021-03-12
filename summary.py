from pathlib import Path


import pandas as pd

id_dir = Path('/home/neil/bns_ids')

dfs = []
for f in id_dir.iterdir():
    dfs.append(pd.read_csv(f, sep='\t'))

df = pd.concat(dfs)
df = df[df['Confidence'] > 0.99]

df.sort_values('Confidence', ascending=False, inplace=True)
df.rename(columns={'Begin File': 'time'}, inplace=True)
df.time = df.time.map(lambda x: x.strip('.wav'))
df.time = pd.to_datetime(df.time, yearfirst=True)
df.set_index('time', drop=True, inplace=True)
# Keep todays id only
df = df.loc['2021-03-09':'2021-03-10']
df.to_csv('/home/neil/test.csv')

# unique = pd.unique(df['Common Name'])[['Rank']]
gb = df.groupby('Common Name').count()
gb = gb.rename(columns={'Rank': 'count'})[['count']]
gb.sort_values('count', inplace=True, ascending=False)
gb.to_csv('/home/neil/uique_ids.csv')

