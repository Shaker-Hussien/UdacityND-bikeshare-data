import sys
import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


# region get city

def get_city():
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = ['Chicago', 'New York City', 'Washington']

    while True:
        city = input('''\nEnter the city you want to explore data for:
a)Chicago
b)New York City
c)Washington

Select Option : ''').title()

        if city not in cities:
            print(
                '\nSorry, Your Selection is incorrect ,Please Choose one from the available options')
        else:
            return city

# endregion

# region get month


def get_month():
    # get user input for month (all, january, february, ... , june)
    months = ['All', 'January', 'February', 'March', 'April', 'May', 'June']

    while True:
        month = input('''\nEnter the month you want to explore data for:
1)All
2)January
3)February
4)March
5)April
6)May
7)June

Select Option : ''').title()

        if month not in months:
            print(
                '\nSorry, Your Selection is incorrect ,Please Choose one from the available options')
        else:
            return month

# endregion

# region get day


def get_day():
    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['All', 'Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
            'Friday']

    while True:
        day = input('''\nEnter the day you want to explore data for:
1)All
2)Saturday
3)Sunday
4)Monday
5)Tuesday
6)Wednesday
7)Thursday
8)Friday
Select Option : ''').title()

        if day not in days:
            print(
                '\nSorry, Your Selection is incorrect ,Please Choose one from the available options')
        else:
            return day


# endregion

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = get_city()

    # get user input for month (all, january, february, ... , june)
    month = get_month()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = get_day()

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
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']

        # filter by month to create the new dataframe
        df = df[df['month'] == months.index(month.lower())+1]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print(f'The Most Common Month is {months[ df["month"].mode()[0] - 1 ]}')

    # display the most common day of week
    print(f'The Most Common Day of Week is {df["day_of_week"].mode()[0]}')

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    print(f'The Most Common Start Hour is {df["hour"].mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print(
        f'The Most Commonly Used Start Station is {df["Start Station"].mode()[0]}')

    # display most commonly used end station
    print(
        f'The Most Commonly Used End Station is {df["End Station"].mode()[0]}')

    # display most frequent combination of start station and end station trip
    print(
        f'The Most Frequent Combination of Start Station and End Station trip is {(df["Start Station"] + " and "+ df["End Station"]).mode()[0]}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df["Trip Duration"].sum()
    total_travel_minutes, total_travel_seconds = divmod(total_travel_time, 60)
    total_travel_hours, total_travel_minutes = divmod(total_travel_minutes, 60)
    total_travel_days, total_travel_hours = divmod(total_travel_hours, 24)

    print(
        f'Total Travel Time for All Trips is {total_travel_days} days, {total_travel_hours} hours, {total_travel_minutes} minutes and {total_travel_seconds} seconds')

    # display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    mean_travel_minutes, mean_travel_seconds = divmod(mean_travel_time, 60)
    mean_travel_hours, mean_travel_minutes = divmod(mean_travel_minutes, 60)
    print(
        f'Average Travel Time is {mean_travel_hours} hour, {mean_travel_minutes} minutes and {mean_travel_seconds} seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(f'Counts of User Types are: \n{df["User Type"].value_counts()}\n')

    if "Gender" in df.columns:
        # Display counts of gender
        print(f'Counts of Gender are: \n{df["Gender"].value_counts()}\n')

    if "Birth Year" in df.columns:
        # Display earliest, most recent, and most common year of birth
        print(
            f'Earliest Year of Birth is {df["Birth Year"].min().astype(int)}')
        print(
            f'Most Recent Year of Birth is {df["Birth Year"].max().astype(int)}')
        print(
            f'Most Common Year of Birth is {df["Birth Year"].mode()[0].astype(int)}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(city):
    """Displays the raw data if requested by user, the raw data should be returned 5 rows at a time."""

    print('\nExploring Raw Data ...\n')
    show_data = input(
        f'Do you want to see sample(5 rows) of raw data for {city} ? (yes/no)\nSelect Option: ').lower()
    if show_data == 'yes':
        for sample in pd.read_csv(CITY_DATA[city.lower()], chunksize=5):
            print(sample)

            if input(f'Do you want to see another sample(5 rows) of raw data for {city} ? (yes/no)\nSelect Option: ').lower() == 'no':
                break

    print('-'*40)

def main():
    while True:
        try:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            show_raw_data(city)

            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() != 'yes':
                print('\nThank you\n')
                break

        except KeyboardInterrupt:
            if input('\nDo you want to exit? (yes/no)\nSelect Option: ').lower() == 'yes':
                sys.exit('\nThank you\n')
            continue

        except Exception as e:
            print(f'\nSorry , An Error happened while processing the data\n')
            if input('\nWould you like to restart? (yes/no)\n').lower() == 'no':
                sys.exit('\nThank you\n')
            continue


if __name__ == "__main__":
    main()
