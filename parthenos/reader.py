#!/usr/bin/python

import re
import pandas as pd

#path = "/home/slavat/parthenos/matrix.xlsx"
df = pd.read_excel(path, header = 1)
d = df[df['POLICY'] == 'ADS - Archaeology Data Service']
data = d.transpose()
print data.to_json()
