import __init__
from init_project import *
#
import pandas as pd

yy = '09'
ifpath = opath.join(dpath['analysis'], 'decision-ap-20%s.csv' % yy)
df = pd.read_csv(ifpath)

df['sumQnum']

df['joinQ'] = df.apply(lambda row: row[''], axis=1)