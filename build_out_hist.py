# -*- coding: utf-8 -*-
"""
This script takes all of the historical note data
(stored in a SQLite database)
and transforms into a daily summary of how many notes are:
- in default
- late
- in-grace period

Output is currently dumped into a separate SQLite table NOTES_PLOTS
as well as a CSV data file

Steps
1) Read in from SQLite database notes from the last 3 years

2) Compute daily summaries

3) Update the database table NOTES_PLOTS

4) Write out summary to CSV for plotting
"""
# imports
import datetime
import time
import sqlite3
import pandas as pd


# define the path to the local SQLite database as a constant
SQLITE_PATH = 'lendingclub.db'

# define a few other constants around date management in SQLite
SECONDS_IN_YEAR = 31536000
THREE_YRS_AGO_SQLITE = time.time() - (3 * SECONDS_IN_YEAR)
THREE_YRS_AGO = datetime.datetime.fromtimestamp(THREE_YRS_AGO_SQLITE)





def convertDate(indate):
    """ Helper function to convert a POSIX timestampe to a datetime """
    a = datetime.datetime.fromtimestamp(indate / 1000.0)
    a_str = a.strftime('%m/%d/%y')
    return datetime.datetime.strptime(a_str, '%m/%d/%y').date()






# main implementation
if __name__ == '__main__':
    
    # connect to the SQLite database using the path defined
    sqlite_con = sqlite3.connect(SQLITE_PATH)






    ###########################################################################
    # STEP 1
    # Read in all notes data and perform conversions
    print 'First step: transform any data that has come in'
    print '    Read from SQLite database'
    # define the qry against the historical notes tables
    qry = 'select * from notes_hist where issue_date / 1000 > {0}'
    # note: formatting for a query can be prone to SQL injection
    # this isn't a huge concern since the constant is defined by us directly
    qry = qry.format(THREE_YRS_AGO_SQLITE)
    # run the query against the database
    df = pd.read_sql(qry, sqlite_con)
    
    # perform date conversions
    df['status_date'] = df['status_date'].apply(convertDate)
    df['crawl_date'] = df['crawl_date'].apply(convertDate)
    df['issue_date'] = df['issue_date'].apply(convertDate)
    ###########################################################################







    ###########################################################################
    # STEP 2
    # Compute daily summaries of distributions of note statuses
    # among Default, Late, or In-Grace Period
    #
    # Methodology: we'll take the most recent status for a note
    # and carry it forward for every subsequent day
    # until a new status for a note is found
    # when comuting summary metrics for any given day
    # 
    # We'll leverage pandas built-in fill methods for speed
    # and to avoid iterating over each date
    print 'Second step: compute daily summaries'
    # identify the range of dates we should iterate over
    # get the first date
    mindate = df['issue_date'].min()
    # get today's date
    today = datetime.datetime.today().date()
    # and compute the number of days we need to iterate over
    datediff = (today - mindate).days
    # with this difference, build out the list of exact days to iterate over
    date_range = [today-datetime.timedelta(days=d) for d in range(datediff+1)]
    
    ###
    # determine when each note started showing data on status
    # which will tell us from which point we can start forward-filling data
    # for each note
    note_minimums = df.groupby('id')['status_date'].min().to_dict()
    # expand each note out so there is a date for every day
    # after the note started showing status
    #
    # need this as a flat list
    all_possible_dates = [ (loan_id, dateval) \
                            # iterate over every possible day
                            for dateval in date_range \
                            # and every loan
                            for loan_id in note_minimums \
                            # but only expand with dates after
                            # the note started showing a status
                            if dateval >= note_minimums[loan_id]]
    # convert this into a dataframe
    all_possible_df = pd.DataFrame(all_possible_dates,
                                   columns=['id', 'status_date'])
    
    # fill in every possible date with note status data
    # if we have it for a given day
    data_expanded = pd.merge(all_possible_df, df, how='left',
                             on=['id','status_date'])
    # use a forward-fill
    # i.e., we'll take the last observed note status
    # and carry it forward for the next date
    # first, need to sort...
    data_expanded = data_expanded.sort_values(['id','status_date'],
                                              ascending=[True,True])
    # ...and once sorted, we can apply the forward-fill interpolation
    data_interpolate = data_expanded.fillna(method='ffill')
    
    # once note status has been interpolated, compute daily metrics
    # obtain a count of note status by day
    daily_summary = data_interpolate.groupby(['status_date','status'])['id'].\
        count().reset_index()
    # filter out notes that are In Review or Issued
    # these won't add to the total count of notes
    review_filter = lambda x: x not in ['In Review','Issued']
    daily_summary = daily_summary[daily_summary['status'].apply(review_filter)]
    # pivot out of from normal form s.t. each column represents a note status
    daily_summary_pivot = daily_summary.pivot(index='status_date',
                                              columns='status', values='id')
    # fill in any empty columns with 0's
    daily_summary_pivot = daily_summary_pivot.fillna(0)


    # now we're set up to start computing summary stats by day
    # compute a daily total count
    daily_summary_pivot['total notes'] = daily_summary_pivot.apply(sum, axis=1)
    # compute several bad loan status rates
    # default rate
    daily_summary_pivot['default'] = daily_summary_pivot.\
        apply(lambda x: (x['Charged Off'] + x['Default']) / float(x['total notes']), axis=1)
    # rate of loans that are late by 4 months
    daily_summary_pivot['late'] = daily_summary_pivot.\
        apply(lambda x: (x['Late (16-30 days)'] + x['Late (31-120 days)']) / float(x['total notes']), axis=1)
    # rate of loans that are in their grace period (late by 2 weeks)
    daily_summary_pivot['grace'] = daily_summary_pivot.\
        apply(lambda x: x['In Grace Period'] / float(x['total notes']), axis=1)
    
    # the database schema was previously set up to store precompuated rates
    # i.e., rates that combine different numbers
    # with the thought of building a stacked area/line chart
    # we'll want to move away from this in the future
    # and just store the raw loan rates
    daily_summary_pivot['default/late'] = daily_summary_pivot['default'] + daily_summary_pivot['late']
    daily_summary_pivot['default/late/grace'] = daily_summary_pivot['default/late'] + daily_summary_pivot['grace']


    # compute the date that will go into the SQLite database
    daily_summary_pivot['date'] = daily_summary_pivot.index.\
        map(lambda x: int(x.strftime('%s')) * 1000)
    ###########################################################################










    ###########################################################################
    # STEP 3
    # Insert into the database where we don't have any data for a given day
    #
    # Note: we're inserting into the NOTES_PLOTS table
    # which is keyed on day

    # define the column ordering of our data so we can use an INSERT statement    
    column_ordering = ['date', 'default', 'default/late', 'default/late/grace',
                       'total notes']
    # break each day out into a list of lists
    daily_values = [ [elem[col] for col in column_ordering] \
                        for elem in daily_summary_pivot.to_dict('records')]
    
    # define the cursor to perform the SQL insertions
    cursor = sqlite_con.cursor()
    # and loop through our daily values, inserting line-by-line
    # future work -- leverage some insert-many functionality
    insert_stmt = '''
        insert or replace into notes_plots
        (day, defaultrate, default_late_rate, default_late_grace_rate,
        total_notes)
        VALUES (?,?,?,?,?)
    '''
    for day_values in daily_values:
        cursor.execute(insert_stmt, tuple(day_values))
    # clean-up our connection to the SQL database
    cursor.close()
    sqlite_con.commit()
    sqlite_con.close()
    ###########################################################################











    ###########################################################################
    # STEP 4
    # Write out the data that we just updated the database with
    # which we'll use to plot
    #
    # Future -- we'll want to drive our visualizations directly off of the DB
    # currently driving visualization off of CSV
    # for simplicity of hosting off github.io
    # minor formatting
    out_csv = daily_summary_pivot.rename(columns={'default': 'Default',
                                                  'late': 'Late',
                                                  'grace': 'In Grace Period'})
    out_csv['date'] = out_csv.index
    out_csv = out_csv[['date','Default','Late','In Grace Period']]
    # and write out
    out_csv.to_csv('data.csv', index=False)
    ###########################################################################
