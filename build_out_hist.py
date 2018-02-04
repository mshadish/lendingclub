# -*- coding: utf-8 -*-
"""
This script takes all of the historical note data
(stored in a SQLite database)
and transforms into a daily summary of how many notes are:
- in default
- late
- in-grace period

Output is currently dumped into a separate SQLite table, called NOTES_PLOTS
"""
import datetime
import time
import sqlite3
import pandas as pd

SQLITE_PATH = 'lendingclub.db'
SECONDS_IN_YEAR = 31536000
THREE_YRS_AGO_SQLITE = time.time() - (3 * SECONDS_IN_YEAR)
THREE_YRS_AGO = datetime.datetime.fromtimestamp(THREE_YRS_AGO_SQLITE)


sqlite_con = sqlite3.connect(SQLITE_PATH)


#convertDate = lambda indate: datetime.datetime.fromtimestamp(indate / 1000.0)

def convertDate(indate):
    a = datetime.datetime.fromtimestamp(indate / 1000.0)
    a_str = a.strftime('%m/%d/%y')
    return datetime.datetime.strptime(a_str, '%m/%d/%y')



print 'First step: transform any data that has come in'
print '    Read from SQLite database'
df = pd.read_sql('select * from notes_hist where issue_date / 1000 > {0}'.format(THREE_YRS_AGO_SQLITE),
                 sqlite_con)

# get the min date
df['status_date'] = df['status_date'].apply(convertDate)
df['crawl_date'] = df['crawl_date'].apply(convertDate)
df['issue_date'] = df['issue_date'].apply(convertDate)



# compute rankings
df['ranking'] = df.groupby('id')['status_date'].rank(ascending=False)


mindate = df['issue_date'].min()
today = datetime.datetime.strptime(datetime.datetime.now().strftime('%m/%d/%y'), '%m/%d/%y')
datediff = (today - mindate).days

date_range = [today - datetime.timedelta(days=d) for d in range(datediff+1)]

print '    Populate each day'
outlist = []
# for each date, get a subset and compute metrics
for date in date_range:
    subdf = df[df['status_date'] <= date]
    if len(subdf) == 0:
        continue
    subdf = subdf.ix[subdf.groupby('id')['ranking'].idxmin()]
    # with this subset, compute all relevant metrics
    
    counts = subdf.groupby('status')['id'].count().reset_index()
    counts = counts.rename(columns={'id': 'num_notes'})
    # filter out in funding, in review
    counts = counts[counts['status'].apply(lambda x: x not in ['In Funding','In Review'])]
    total_notes = counts['num_notes'].sum()
    
    current_or_paid_df = counts[counts['status'].apply(lambda y: y not in ['Charged Off'] and 'late' not in y.lower())]
    current_or_paid = current_or_paid_df['num_notes'].sum()
    
    
    defaulted_df = counts[counts['status'].apply(lambda z: z in ['Charged Off','Default'])]
    defaulted = defaulted_df['num_notes'].sum()
    
    
    late_or_default_df = counts[counts['status'].apply(lambda a: a in ['Charged Off','Default'] or 'late' in a.lower())]
    late_or_default = late_or_default_df['num_notes'].sum()
    
    
    # include grace period
    anything_bad_df = counts[counts['status'].apply(lambda b: b in ['Charged Off','Default','In Grace Period'] or 'late' in b.lower())]
    anything_bad = anything_bad_df['num_notes'].sum()
    
    
    default_ratio = defaulted / float(total_notes)
    late_ratio = late_or_default / float(total_notes)
    include_grace_ratio = anything_bad / float(total_notes)

    outlist.append({'date': date, 'default': default_ratio,
                    'default/late': late_ratio,
                    'default/late/grace': include_grace_ratio,
                    'total notes': total_notes})






outdf = pd.DataFrame(outlist)




outdf['date'] = outdf['date'].apply(lambda x: int(x.strftime('%s')) * 1000)
# assert ordering
outdf = outdf[['date','default','default/late','default/late/grace','total notes']]
cursor = sqlite_con.cursor()
for elem in outdf.to_dict('split')['data']:
    cursor.execute('insert or ignore into notes_plots (day, defaultrate, default_late_rate, default_late_grace_rate, total_notes) VALUES (?,?,?,?,?)', tuple(elem))
cursor.close()
# commit changes
sqlite_con.commit()




# read the full dataset from the tables
print 'Reading full dataset for plotting...'
full_summary = pd.read_sql('''
select
    date(day / 1000, 'unixepoch') as date,
    defaultrate,
    default_late_rate - defaultrate as laterate,
    default_late_grace_rate - default_late_rate as gracerate
from
    notes_plots
order by day
''', sqlite_con)
# write out to csv
print '...and dump to CSV'
# rename the columns to easier-to-read representations
full_summary = full_summary.rename(columns={'defaultrate': 'Default',
                                            'laterate': 'Late',
                                            'gracerate': 'In Grace Period'})
full_summary.to_csv('data.csv', index=False)


sqlite_con.close()
