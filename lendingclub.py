#!/usr/bin/env python
"""
Script for basic reporting of LendingClub account stats
leveraging the LendingClub API


"""

from __future__ import print_function


import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

import dateutil.parser
import datetime

from lendingclub_auth import __auth
from lendingclub_auth import _investorID as investorID



standard_header = {'Authorization': __auth,'Content-Type': 'application/json'}

# make an ordered list of all possible grades
GRADES = [
    'A1','A2','A3','A4','A5',
    'B1','B2','B3','B4','B5',
    'C1','C2','C3','C4','C5',
    'D1','D2','D3','D4','D5',
    'E1','E2','E3','E4','E5',
    'F1','F2','F3','F4','F5'
]




summary = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{id}/summary'.format(id=investorID), headers=standard_header)



notes_owned = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{id}/detailednotes'.format(id=investorID), headers=standard_header)

notes_list = json.loads(notes_owned.text)['myNotes']


# grade summary of all notes owned

grades = Counter([j.get('grade') for j in notes_list])
grades_sorted = sorted([(key,val) for key,val in grades.iteritems()], key=lambda x: x[0])



# get newly purchased loans
# i.e., last 72 hours
num_hours_prev = 72
yesterday = datetime.datetime.now() - datetime.timedelta(hours=num_hours_prev)
new_notes = filter(lambda x: dateutil.parser.parse(x.get('orderDate')).replace(tzinfo = None) > yesterday, notes_list)
print('New notes purchased in last {1} hours: {0}'.format(len(new_notes), num_hours_prev))








################ GENERATING BAR CHAR ################

# fill in values based on grades
bar_vals = [0] * len(GRADES)
for grade_held in grades_sorted:
    bar_vals[GRADES.index(grade_held[0])] = grade_held[1]

fig = plt.figure(figsize = (10,4))
bar_width = 1.5

bars = plt.bar(np.arange(len(GRADES)) * 2, bar_vals, width=bar_width)
plt.xticks(np.arange(len(GRADES)) * 2 + (bar_width / 2.0), GRADES)
plt.show()
