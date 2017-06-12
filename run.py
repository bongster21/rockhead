"""
Find rockhead in India jobs
"""
import pandas as pd
import numpy as np

data = pd.read_csv(r'D:\Eric\Projects\Rockhead\python\Rockhead_RQD_UCS_20170609.csv', skiprows=2)

#print(list(Data))
df = pd.DataFrame(data, columns=['BH_ID', 'Top', 'Bot', 'Top.1', 'Bot.1', 'RQD', 'UCS (MPa).1', 'GEOL'])

df.columns = ['id', 'elv_top', 'elv_bot', 'dep_top', 'dep_bot', 'RQD', 'UCS', 'GEOL']
df = df.dropna(axis=0, how='all')
df.id = df.id.str.replace('?', '-')
df.RQD = pd.to_numeric(df.RQD, errors='coerce')
df.UCS = pd.to_numeric(df.UCS, errors='coerce')
soil = pd.Series(['I(B)','II(B)','III(B)','II/I(B)','I/II(B)','III/II(B)','II/III(B)','III/II/I(B)'])

def f(group):
    group.UCS = group.UCS.fillna(method='ffill')
    group.RQD = group.RQD.fillna(method='ffill')
    return group[(group.UCS > 22.0) & (group.RQD > 60.0) & (group.GEOL.isin(soil.values))].head(1)

gb = df.groupby(['id'], as_index=False)
print gb
#BH103 = gb.get_group('BH 103')
#BH103.UCS = BH103.UCS.fillna(method='ffill')
#group = BH103
#print group[(group.GEOL.isin(soil.values))]

gb = gb.apply(lambda group: f(group))

print(gb)

gb.to_csv('D:\Eric\Projects\Rockhead\python\out.csv', index=False)
