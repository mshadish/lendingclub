# -*- coding: utf-8 -*-
"""
Plotting script
takes note summary data from the SQLite table NOTES_PLOTS
and plots it as a Stacked Line chart

Future work:
	want to plot as a Stacked Area chart, preferably in D3.js
"""
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import datetime


SQLITE_PATH = 'lendingclub.db'
PLOT_PATH = 'lendingclub_default.png'
sqlite_con = sqlite3.connect(SQLITE_PATH)


def convertDate(indate):
    a = datetime.datetime.fromtimestamp(indate / 1000.0)
    a_str = a.strftime('%m/%d/%y')
    return datetime.datetime.strptime(a_str, '%m/%d/%y')


datapoints = pd.read_sql('select * from notes_plots', sqlite_con)

datapoints = datapoints.sort_values('day')

fig = plt.figure()
plt.plot(datapoints['day'].apply(convertDate), datapoints['defaultrate'])
plt.plot(datapoints['day'].apply(convertDate), datapoints['default_late_rate'])
plt.plot(datapoints['day'].apply(convertDate), datapoints['default_late_grace_rate'])
plt.gcf().autofmt_xdate()
plt.legend(loc='upper left')


plt.savefig(PLOT_PATH)
