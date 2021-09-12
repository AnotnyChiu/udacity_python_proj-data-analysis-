import time
import calendar
import pandas as pd
import numpy as np
import os
from termcolor import colored
import matplotlib.pyplot as plt
from scipy import stats

#avoid somtime can't find csv file problem

current_dir = os.curdir

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_filters(file_dict):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_verify = True
    city_list = [x for x in file_dict.keys()]
    while(city_verify):
        city_input = input('Please choose which city\'s data you would like to analyze: {} \nInput Here:'.format(city_list)).lower()
        if city_input not in file_dict.keys():
            print('Seems like your input is invalid, please try again!\n')
        else:
            city = city_input
            print(colored('Your choose: {} \n'.format(city),'yellow'))
            city_verify = False

    # get user input for month (all, january, february, ... , june)
    month_verify = True
    while(month_verify):
        try:
            month_input = int(input('Please choose the month to analyze(Please type number, for January please type \'1\'), or type \'0\' to not do the filtering \nInput Here:'))
        except :
            print('Seems like your input is invalid, please try again!')
        else:
            if month_input not in range(13):
                print('Seems like your input is out of range. Please type a number from 0 to 12\n')
            elif month_input == 0:
                month = 'all'
                
                print(colored('Your choose: Skip month filtering \n','yellow'))
                month_verify = False
            else:
                month = calendar.month_name[month_input]
                print(colored('Your choose: {} \n'.format(month),'yellow'))
                month_verify = False

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_verify = True
    while(day_verify):
        try:
            day_input = int(input('Please choose the weekday to analyze(Please type number, for Monday please type \'1\'), or type \'0\' to not do the filtering \nInput Here:'))
        except:
            print('Seems like your input is invalid, please try again!\n')
        else:
            if day_input not in range(8):
               print('Seems like your input is out of range. Please type a number from 0 to 7\n')
            elif day_input == 0:
                day = 'all'
                print(colored('Your choose: Skip weekday filtering \n','yellow'))
                day_verify = False
            else:
                day = calendar.day_name[day_input-1] #is zero base
                print(colored('Your choose: {} \n'.format(day),'yellow'))
                day_verify = False

    print('-'*40)

    #get user input to choose whether eliminating rows with nan inside.
    nan_verify = True
    while(nan_verify):
        try:
            nan_input = input('Please choose whether eliminating rows with nan inside(Please type \'y\' for yes and \'n\' for no \nInput Here:').lower()
        except:
            print('Seems like your input is invalid, please try again!\n')
        else:
            if nan_input == 'y':
                nan_check = 'yes'
                print(colored('Your choose: Eliminating rows that has nan value. \n','yellow'))
                nan_verify = False
            else:
                nan_check = 'no'
                print(colored('Your choose: Keep the data as original.','yellow'))
                nan_verify = False

    print('-'*40)

    return city, month, day, nan_check

def load_data(city, month, day,nan_check):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #get data from csv
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] =  pd.to_datetime(df['Start Time'])

    #region : filter data
    df['Month'] = df['Start Time'].dt.month_name() #not in zero base
    df['Weekday'] = df['Start Time'].dt.day_name() ##keep this method in mind!

    if month != 'all':
        df = df[df['Month'] == month.title()]
    if day != 'all':
        df = df[df['Weekday'] == day.title()]
    
    if nan_check == 'yes':
        df.dropna(axis=0,inplace=True);

    ##avoid all datas being eliminated
    if df.size == 0:
        return df
    '''
    note: way to do both at the same time:
    df = df[(df['Month'] == month.title()) & (df['Weekday'] == day.title())]
    * use & rather than and / use | rather than or
    '''
    #endregion

    #region : display data
    print_more = True
    line_count = 0
    while(print_more):
        if line_count + 5 > len(df.index):
            print(df.tail(len(df.index)-line_count))
            print('{} ~ {} rows of total {} rows of data\n'.format(line_count+1,len(df.index),len(df.index)))
            print('--- Already reached the bottom ---\n')
        else:
            print(df[line_count:line_count+5])
            data_notice = '{} ~ {} rows of total {} rows of data\n'.format(line_count+1,line_count+5,len(df.index))
            print(colored(data_notice,'yellow'))
            print('Current 5 rows of data are as above. Please type \'y\' if you want to continue checking the next five rows, or type \'n\' to see analysis of travel frequency.')
        
        input_verify = True
        while(input_verify):
            answer = input('Input here:').lower()
            if answer == 'y':
                line_count += 5
                input_verify = False
            elif answer == 'n':
                print_more = False
                input_verify = False
            else:
               print('Seems like your input is invalid, please try again! (type \'y\' or \'n\')\n')
    #endregion
    
    return df

#get_statis: get the most frequent rentals, the count of rentals and percentage depends on different factors, then return colored string
def get_statis(df,column):
    most_common = colored(df[column].mode().values[0],'green')
    rental_counts = df[column].value_counts().iloc[0]
    percentage = round((rental_counts/len(df.index))*100)
    rental_counts = colored(str(rental_counts),'red')
    percentage = colored(str(percentage),'red')
    return most_common,rental_counts,percentage

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print(colored('\nCalculating The Most Frequent Times of Travel...\n','yellow'))
    start_time = time.time()

    # display the most common month
    most_common_month, rental_counts, percentage = get_statis(df,'Month')
    print('The month has the most rentals is {}, has {} rentals. ({}% of all rentals)'.format(most_common_month,rental_counts,percentage))

    # display the most common day of week
    most_common_day, rental_counts, percentage = get_statis(df,'Weekday')
    print('The weekday has the most rentals is {}, has {} rentals. ({}% of all rentals)'.format(most_common_day,rental_counts,percentage))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    most_common_hour, rental_counts, percentage = get_statis(df,'Hour')
    print('The most common start hour is at {}:00, has {} rentals. ({}% of all rentals)'.format(most_common_hour,rental_counts,percentage))

    print("\nThis took %s seconds." % (time.time() - start_time))
    input("\nPress any key to see analysis of the most popular stations and trip")
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print(colored('\nCalculating The Most Popular Stations and Trip...\n','yellow'))
    start_time = time.time()

    # display most commonly used start station
    station_count = df['Start Station'].nunique() #nunique can get the count of unique items
    most_common_start, rental_counts, percentage = get_statis(df,'Start Station')
    print('The most commonly used start station is \'{}\', total {} times used. ({}% of all rentals out of {} stations)'.format(most_common_start,rental_counts,percentage,station_count))

    # display most commonly used end station
    most_common_end, rental_counts,percentage = get_statis(df,'End Station')
    print('The most commonly used end station is \'{}\', total {} times used. ({}% of all rentals out of {} stations)'.format(most_common_end,rental_counts,percentage,station_count))

    # display most frequent combination of start station and end station trip
    df['Station_comb'] = df['Start Station'] + '/to/' + df['End Station']
    sta_comb, rental_counts, percentage = get_statis(df,'Station_comb')
    sta_comb = sta_comb.split('/to/')
    print('The most frequent combination of start station and end station trip is from \'{}\' to \'{}\''.format(sta_comb[0],sta_comb[1]))
    print('Has a total of {} times'.format(rental_counts))

    print("\nThis took %s seconds." % (time.time() - start_time))
    input("\nPress any key to see analysis of total and average trip duration")
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print(colored('\nCalculating Trip Duration...\n','yellow'))
    start_time = time.time()

    # display total travel time
    travel_sum = df['Trip Duration'].sum()
    print('Total travel time is {} seconds'.format(colored(str(travel_sum),'red')))

    # display mean travel time
    travel_mean = df['Trip Duration'].mean()
    print('Mean of travel time is {} seconds'.format(colored(str(travel_mean),'red')))

    print("\nThis took %s seconds." % (time.time() - start_time))

    

    input("\nPress any key to see sum of trip duration in all cities through out all months (Analysis will be shown in graph)")
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print(colored('\nCalculating User Stats...\n','yellow'))
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The counts of user types are as below:\n')
    print(colored(user_types,'green') + '\n')

    # Display counts of gender
    gender_counts = df['Gender'].value_counts()
    print('The counts of genders are as below:\n')
    print(colored(gender_counts,'green') + '\n')

    # Display earliest, most recent, and most common year of birth
    earliest = str(int(df['Birth Year'].min()))
    latest = str(int(df['Birth Year'].max()))
    common = str(int(df['Birth Year'].mode()))
    print('The earliest year of birth is {}'.format(colored(earliest,'red')))
    print('The most recent year of birth is {}'.format(colored(latest,'red')))
    print('The most common year of birth is {}'.format(colored(common,'red')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print(colored('End of analysis','yellow'))
    print('-'*40)

#region : extra quesiton
''' 
Extra Question (loop through all cities)
Q: Find out whether season affect the total rental duration (Show it in a line graph)
'''
def eliminate_outliers(df):
    z_scores = stats.zscore(df)
    #take absolute values
    z_scores = np.abs(z_scores)
    filter_entries = (z_scores<3).all(axis=1)
    return df[filter_entries]

def general_report_on_month(city_dict):
    #retrieve all data and combine
    df_dict = {}
    for city,file in city_dict.items():
        city_df = pd.read_csv(file)
        city_df.dropna(axis=0,inplace=True)
        city_df['Start Time'] =  pd.to_datetime(city_df['Start Time'])
        city_df['Month_in_num'] = city_df['Start Time'].dt.month
        #convert duration to hours
        city_df['Trip Duration'] = city_df['Trip Duration']/3600
        city_df = city_df.loc[:,['Trip Duration','Month_in_num']]
        city_df = eliminate_outliers(city_df)
        ## set as_index to false: let the column still be as a column, not change it to row index. For that we can still retrive it.
        city_df = city_df.groupby(['Month_in_num'],as_index=False).sum()
        df_dict[city] = city_df
        
    #combine all cities
    df_dict['integrated'] = pd.concat(df_dict.values(),axis=0,ignore_index=True)

    #region : try making graph
    ##calculate correation
    corr = df_dict['integrated']['Month_in_num'].corr(df_dict['integrated']['Trip Duration'],method='pearson').round(3)
    corr_status = ""
    if abs(corr)>=0.7:
        corr_status += 'Strong'
    elif abs(corr)>=0.3:
        corr_status += 'Medium'
    elif abs(corr)>=0.1:
        corr_status += 'Weak'
    else:
        corr_status += 'No or negligible correation'
    if abs(corr)>=0.1 and corr>0:
        corr_status += ' Positive'
    elif abs(corr)>=0.1 and corr<0:
        corr_status += ' Negative'
        
    #group by for integrated again to create readable graph
    df_dict['integrated'] = df_dict['integrated'].groupby(['Month_in_num'],as_index=False).sum()

    plt.figure(figsize=(12,10))
    plt.style.use('ggplot')
    plt.title('Rental duration through out Months \nCorrelation Coefficient: {} ({})'.format(corr,corr_status))
    plt.xlabel('Months')
    plt.ylabel('Sum of rental duration in hours')
    city_list = [x for x in df_dict.keys()]
    
    for city,df in df_dict.items():
        plt.plot(df['Month_in_num'],df['Trip Duration'])
        month_arr = np.array(df['Month_in_num'])
        duration_arr = np.array(df['Trip Duration'])
        for i in range(len(month_arr)):
            plt.annotate(text='{} Hours'.format(round(duration_arr[i])),xy=(month_arr[i],duration_arr[i]))
    
    #legend should be put after the graph creation
    plt.legend(city_list)
    plt.show()
    #endregion
    input("\nPress any key to see analysis on bikeshare users")
    print('-'*40)
#endregion

def main():
    retry = True
    while retry:
        df_verify = True
        while(df_verify):
            city, month, day, nan_check = get_filters(CITY_DATA)
            df = load_data(city, month, day, nan_check)
            ##avoid all datas being eliminated
            if df.size == 0:
                print(colored('Find no matched results caused empty dataframe. Please try again','red'))
            else:
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                general_report_on_month(CITY_DATA)
                user_stats(df)
                df_verify = False
                restart = input('\nWould you like to restart? Enter \'y\' for yes or \'n\' for no.\n')
                if restart.lower() != 'y':
                    retry = False


if __name__ == "__main__":
	main()
