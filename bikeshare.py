import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to explore? Chicago, New York or Washington?').title()
    cities = ['Chicago', 'New York', 'Washington']
    while True:
        try:
            cities.index(city)
            break
        except:
            city = input('Pls enter a valid city: Chicago, New York or Washington.')

    # get user input for month (all, january, february, ... , june)
    month = input('Which month would you like to explore? January, February, March, April, May, June? Enter All for no filter.').title()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
    while True:
        try:
            months.index(month)
            break
        except:
            month = input('Pls enter a valid month: January, February, March, April, May, June, All.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week would you like to explore? Enter All for no filter.').title()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
    while True:
        try:
            days.index(day)
            break
        except:
            day = input('Pls enter a valid weekday or enter All for no filter.')

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # use the index of the days list to get the corresponding int
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day = days.index(day)

        # filter by day of week to create the new dataframe
        df = df[df['day'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # use the months list to lookup month as a str
    months = ['January', 'February', 'March', 'April', 'May', 'June']

    # display the most common month
    popular_month_int = df['month'].mode()[0]
    popular_month = months[popular_month_int - 1]
    print('Most popular month is:', popular_month)

    # use the days list to lookup month as a str
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # display the most common day of week
    popular_day_int = df['day'].mode()[0]
    popular_day = days[popular_day_int]
    print('Most popular day is:', popular_day)

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most popular hour is:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station_count = df['Start Station'].value_counts()
    print('Most popular starting station is:', start_station_count.head(1))

    # display most commonly used end station
    end_station_count = df['End Station'].value_counts()
    print('Most popular ending station is:', end_station_count.head(1))

    # display most frequent combination of start station and end station trip
    df['Start + End'] = df['Start Station'] + ' to ' + df['End Station']
    start_end = df['Start + End'].value_counts()
    print('Most popular starting/ending station combination is:', start_end.head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print('Total travel time is:', int(total_travel))

    # display mean travel time
    average_travel = df['Trip Duration'].mean()
    print('Average travel time is:', int(average_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # display counts of user types
    user_count = df['User Type'].value_counts()
    print('Counts of each user type:', user_count)

    try:
        # display counts of gender for New York/Chicago
        gender_count = df['Gender'].value_counts()
        print('Counts of each gender:', gender_count)
    except:
        # error message dispalyed if Washington selected (no data)
        print('Counts of each gender:', 'No data for Washington')

    try:
        # display earliest, most recent, and most common year of birth for New York/Washington
        earliest_birth_year = df['Birth Year'].min()[0]
        most_recent__birth_year = df['Birth Year'].max()[0]
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Earliest birth year:', earliest_birth_year)
        print('Most recent birth year:', most_recent_birth_year)
        print('Most common birth year:', most_common_birth_year)
    except:
        # error message dispalyed if Washington selected (no data)
        print('Earliest birth year:', 'No data for Washington')
        print('Most recent birth year:', 'No data for Washington')
        print('Most common birth year:', 'No data for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # user prompt to view time statistics
        ts = input('Would you like to view data on time stats? Enter yes or no').lower()
        if ts == 'yes':
            time_stats(df)

        # user prompt to view station statistics
        ss = input('Would you like to view data on station stats? Enter yes or no').lower()
        if ss == 'yes':
            station_stats(df)

        # user prompt to view trip duration statistics
        tds = input('Would you like to view data on trip duration stats? Enter yes or no').lower()
        if tds == 'yes':
            trip_duration_stats(df)

        # user prompt to view user stats statistics
        us = input('Would you like to view data on user stats? Enter yes or no').lower()
        if us == 'yes':
            user_stats(df)

        # user prompt to view individual trip data
        i = 0
        raw = input("\nWould you like to see first 5 rows of raw data; type 'yes' or 'no'?\n").lower()

        while True:
            if raw == 'no':
                break
            print(df[i:i+5])
            raw = input('\nWould you like to see next rows of raw data?\n').lower()
            i += 5

        # user prompt to end/re-start application
        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
