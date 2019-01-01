import time as tm
import pandas as pd
import numpy as np

from datetime import date
from datetime import time
from datetime import datetime
import statistics
import calendar

#######################################
#note 1/1/2019 - Austin to be added 3Q 2019


#######################################

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}
months = (
    'all', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november',
    'december')
days = ('all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

#######################################

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # referenced global variable info (https://www.programiz.com/python-programming/global-local-nonlocal-variables)

    global city, month, day
    city, month, day = "", "", ""

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = str(input('Please enter city to analyze: '))
    while not city in CITY_DATA:
        city = str(input("Please select a city value from chicago, new york city, washington: "))

    # get user input for month (all, january, february, ... , june)

    month = str(input('Please enter month or all: '))
    while not month in months:
        month = str(input("Please specify a month (e.g., january) or all: "))

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day = str(input('Please specify a day of the week or all: '))
    while not day in days:
        day = str(input("Please specify a day of the week (e.g., monday) or all: "))

    print('-' * 40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA.get(city))

    df['Start Date'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Date'].dt.month
    df['weekday'] = df['Start Date'].dt.weekday
    df['Start Hour'] = df['Start Date'].dt.hour

    ############################################
    ## filter by month

    if month == 'january':
        df = df[df.month == 1]
    elif month == 'february':
        df = df[df.month == 2]
    elif month == 'march':
        df = df[df.month == 3]
    elif month == 'april':
        df = df[df.month == 4]
    elif month == 'may':
        df = df[df.month == 5]
    elif month == 'june':
        df = df[df.month == 6]
    elif month == 'july':
        df = df[df.month == 7]
    elif month == 'august':
        df = df[df.month == 8]
    elif month == 'september':
        df = df[df.month == 9]
    elif month == 'october':
        df = df[df.month == 10]
    elif month == 'november':
        df = df[df.month == 11]
    elif month == 'december':
        df = df[df.month == 12]
    # when ALL is selected
    # no restriction needed

    ############################################
    ## filter by day

    if day == 'monday':
        df = df[df.weekday == 0]
    elif day == 'tuesday':
        df = df[df.weekday == 1]
    elif day == 'wednesday':
        df = df[df.weekday == 2]
    elif day == 'thursday':
        df = df[df.weekday == 3]
    elif day == 'friday':
        df = df[df.weekday == 4]
    elif day == 'saturday':
        df = df[df.weekday == 5]
    elif day == 'sunday':
        df = df[df.weekday == 6]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = tm.time()

    # display the most common month
    # referenced calendar.month_name from (https://stackoverflow.com/questions/6557553/get-month-name-from-number)

    month_count = sum(df.month)
    count = df['month'].value_counts()
    max_month_count = count.max()
    max_month_df = df.mode()
    #max_month_int = int(max_month_df.iloc[0, 10])
    max_month = df['month'].value_counts().idxmax()
    max_month_desc = calendar.month_name[max_month]

    print("the most frequent month is " + str(max_month_desc))

    # display the most common day of week

    max_weekday = df['weekday'].value_counts().idxmax()
    max_weekday_desc = calendar.day_name[max_weekday]

    print("the most frequent weekday is " + str(max_weekday_desc))

    # display the most common start hour


    max_start_hour = df['Start Hour'].value_counts().idxmax()

    if max_start_hour < 12:
        max_start_hour_desc = str(max_start_hour) + "AM"
    else:
        max_start_hour -= 12
        max_start_hour_desc = str(max_start_hour) + "PM"

    print("the most common start time is " + max_start_hour_desc)

    print("\nThis took %s seconds." % (tm.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = tm.time()

    # display most commonly used start station

    max_start_station = df['Start Station'].value_counts().idxmax()
    print("the most commonly used start station is " + str(max_start_station))

    # display most commonly used end station

    max_end_station = df['End Station'].value_counts().idxmax()
    print("the most commonly used end station is " + str(max_end_station))

    # display most frequent combination of start station and end station trip
    # referenced groupby information from (https://stackoverflow.com/questions/38933071/
    # group-by-two-columns-and-count-the-occurrences-of-each-combination-in-pandas)

    count_combos = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index[0]
    print("the most frequent combination of Start and End Stations is: " + str(count_combos))

    print("\nThis took %s seconds." % (tm.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = tm.time()

    # display total travel time

    total_time = df['Trip Duration'].sum()
    print('\nThe total trip duration was ' + str(total_time).format() + ' seconds')

    # display mean travel time

    mean_time = df['Trip Duration'].mean()  #
    print('\nThe mean trip duration was ' + str(mean_time).format() + ' seconds')

    print("\nThis took %s seconds." % (tm.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')

    start_time = tm.time()

    # Display counts of user types
    # (referenced example code https://chrisalbon.com/python/data_wrangling/pandas_list_unique_values_in_column/)

    distinct_user_types = df['User Type'].unique()

    print('The unique user types represented are ' + str(distinct_user_types) + '\n')

    # Display counts of gender

    ct_gender = df['Gender'].value_counts()

    print('The passenger count by gender is: \n')
    print(ct_gender)

    # Display earliest, most recent, and most common year of birth

    earliest_birth_year = df['Birth Year'].min()
    latest_birth_year = df['Birth Year'].max()
    mode_birth_year = df['Birth Year'].mode()

    print('The earliest passenger birth year is ' + str(earliest_birth_year) + '\n')
    print('The latest earliest passenger birth year is ' + str(latest_birth_year) + '\n')
    print('The most common passenger birth year is ' + str(mode_birth_year) + '\n')

    print("\nThis took %s seconds." % (tm.time() - start_time))
    print('-'*40)


def main():
    while True:
        get_filters()

        #print(city + month+ day)

        df = load_data(city, month, day)
        #
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        #
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
