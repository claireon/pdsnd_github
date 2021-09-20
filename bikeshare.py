import time
import pandas as pd
import numpy as np
from IPython.display import display

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
MONTHS = {'jan': 'january', 'feb': 'february', 'mar': 'march',
          'apr': 'april', 'may': 'may', 'jun': 'june'}
DAYS = {'mon': 'monday', 'tue': 'tuesday', 'wed': 'wednesday',
        'thu': 'thursday', 'fri': 'friday', 'sat': 'saturday', 'sun': 'sunday'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('.'*40)
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # user input for city (chicago, new york city, washington)
    while True:
        city = input(
            '\nWhich city\'s data will you like to explore? Chicago, New York City, or Washington?\n').lower()

        if city in CITY_DATA:
            confirmation = input(
                '\nYou have opted to view data for {}. If this was an error, enter no to restart, else enter yes to continue.\n'.format(city.title())).lower()
            if confirmation == 'yes':
                break
        else:
            print(
                'Sorry, we do not have that data, type a city name from the 3 options provided.\n')

    # user input for month (all, january, february, ... , june)
    while True:
        month = input(
            '\nWhat month will you like to explore? (Enter Jan for January, Feb for February, etc.)\nIf you don\'t want to filter by month, enter all.\n').lower()

        if month in MONTHS:
            month = MONTHS[month]
            break
        elif month == 'all':
            break
        else:
            print('\nOops! That\'s not in the options\n')

    # user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            '\nWould you like to see data for a particular day of the week?\nIf yes, enter the day. (Enter Mon for Monday, Tue for Tuesday, etc.) If no, just type all.\n').lower()

        if day in DAYS:
            day = DAYS[day]
            break
        elif day == 'all':
            break
        else:
            print('\nOops! That\'s not in the options\n')

    if month != 'all' or day != 'all':
        print('\nYou have chosen to explore US bikeshare data for \ncity: {}, month: {}, day: {}'.format(
            city, month, day).title())

    print('-'*40)
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
    df['City'] = city.title()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # the most common month
    if np.count_nonzero(df['month'].unique()) > 1:
        most_traveled_month = df['month'].mode()[0]
        print('The month with the most trips is', most_traveled_month)

    # the most common day of week
    if np.count_nonzero(df['day_of_week'].unique()) > 1:
        most_traveled_day = df['day_of_week'].mode()[0]
        print('The day of the week with the most trips is', most_traveled_day)

    # the most common start hour
    start_hour_pdseries = df['Start Time'].dt.hour
    most_traveled_hour = start_hour_pdseries.mode()[0]

    # to determine time of day based on the time in 12-hour time format
    if 0 <= most_traveled_hour < 12:
        time_of_day = 'AM'
    elif most_traveled_hour == 12:
        time_of_day = 'Noon'
    else:
        time_of_day = 'PM'

    # converting to 12-hour time format
    if most_traveled_hour > 12:
        print('The most common trip start hour is {}{}'.format(
            most_traveled_hour-12, time_of_day))
    else:
        print('The most common trip start hour is {}{}'.format(
            most_traveled_hour, time_of_day))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print('Most trips start at {} Station'.format(most_start_station))

    # display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print('Most trips end at {} Station'.format(most_end_station))

    # display most frequent combination of start station and end station trip
    df['journey_routes'] = df['Start Station'] + ' and ' + df['End Station']
    most_station_combination = df['journey_routes'].mode()[0]
    print('The most frequent station trips are between', most_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = ((df['Trip Duration'].sum())/60).round(1)
    print('The total travel time is {:,} minutes, which is approximately {:,} hours'.format(
        total_travel_time, (total_travel_time/60).round(1)))

    # display mean travel time
    mean_travel_time = ((df['Trip Duration'].mean())/60).round(1)
    print('The average travel time is {:,} minutes.'.format(
        mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby('User Type')['User Type'].count()
    print('These are the user counts by type, \n{}'.format(
        user_types.to_string(header=False)))
    print()

    # Display counts of gender
    if np.any(df['City'] != 'Washington'):
        gender_count = df.groupby('Gender')['Gender'].count()
        print('These are the user counts by gender, \n{}'.format(
            gender_count.to_string(header=False)))
        print()

        # Display earliest, most recent, and most common year of birth
        print('The earliest year of birth is:', int(df['Birth Year'].min()))
        print('The most recent year of birth is:',
              int(df['Birth Year'].max()))
        print('The most common year of birth is:',
              int(df['Birth Year'].mode()[0]))
    else:
        print('Please note that no data exists for gender and year of birth for Washington')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df, city):
    """ 
    Asks user whether or not to display some raw data.

    Displays five rows of raw data at a time.
    Will continue to display 5 more rows at a time as long as the user specifies 'yes'.
    """
    # get user's choice to view raw data
    row = 0
    while True:
        choice = input(
            '\nWill you like to view some of the raw data for {}? (Enter yes/no)\n'.format(city)).lower()

        if choice != 'yes':
            break
        else:
            while row < df.size:
                display(df.iloc[row: row+5])
                row += 5
                view_more = input(
                    '\n Will you like to view 5 more rows? (Enter yes/no)').lower()
                if view_more != 'yes':
                    break
        break

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
