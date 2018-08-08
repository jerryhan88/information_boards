import h_hypothesisTest
from __path_organizer import *
#
import pandas as pd

yy = '09'
ifpath = opath.join(dpath['analysis'], 'decision-ap-20%s.csv' % yy)
df = pd.read_csv(ifpath)

df['sumQnum']

df['joinQ'] = df.apply(lambda row: row[''], axis=1)