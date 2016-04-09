#!/usr/bin/env python
"""
Script for basic reporting of LendingClub account stats
leveraging the LendingClub API
"""

from __future__ import print_function


import json
import requests
from collections import Counter

import dateutil.parser
import datetime

from lendingclub_auth import __auth
from lendingclub_auth import _investorID as investorID



standard_header = {'Authorization': __auth,'Content-Type': 'application/json'}




summary = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{id}/summary'.format(id=investorID), headers=standard_header)



notes_owned = requests.get('https://api.lendingclub.com/api/investor/v1/accounts/{id}/detailednotes'.format(id=investorID), headers=standard_header)

notes_list = json.loads(notes_owned.text)['myNotes']


# grade summary of all notes owned
grades = Counter([j.get('grade') for j in notes_list])
grades_sorted = sorted([(key,val) for key,val in grades.iteritems()], key=lambda x: x[0])
for grade in grades_sorted:
	print(grade)


# get newly purchased loans
# i.e., last 24 hours
yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
new_notes = filter(lambda x: dateutil.parser.parse(x.get('orderDate')).replace(tzinfo = None) > yesterday, notes_list)
print('New notes purchased in last 24 hours: {0}'.format(len(new_notes)))
