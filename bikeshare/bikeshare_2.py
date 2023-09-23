#!/usr/bin/env python3


import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington).
    while True:
        city = input('Enter the name of the city (Chicago, New York City, Washington): ').lower()
        if city in CITY_DATA:
            break
        else:
            print('You have entere an Invalid city name. Please enter one of the provided city names.')
    
    # Get user input for month (All, January, February..., june).
    while True:
        month = input('Enter the name of the month From This List (All, January, February, March, April, May, June): ').lower()
        if month in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
            break
        else:
            print('You have entered an Invalid Month. Please enter a valid month or "all" for no filter.')
    
    # Get user input for day of the week (all, monday, tuesday, ..., sunday).
    while True:
        day = input('Enter the name of the day of the week fom this list (all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday): ').lower()
        if day in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            break
        else:
            print('Invalid day of the week. Please enter a valid day or "all" for no filter.')
    
    print('-'*40)
    return city, month, day




def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "" for no month filter
        (str) day - name of the day of the week to filter by, or "" for no day filter

    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # data file for the selected city.
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)

    # Converting the 'Start Time' column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month and day of the week from the 'Start Time' column.
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Defining a list of valid month names for filtering.
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june']

    # Apply filters based on user input for month and day, considering no filters as well.
    if month.lower() != 'all' and month.lower() in valid_months:
        # Filter by month if valid month is specified.
        month_num = valid_months.index(month.lower()) + 1
        df = df[df['Month'] == month_num]


    if day.lower() != 'all':
        # Filter by day of the week if a day is specified.
        df = df[df['Day of Week'] == day.title()]

    
    #print(df.head(5))

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if not df.empty:
        # Calculate and display the most common month.
        common_month = df['Month'].mode()[0]
        month_name = MONTHS[common_month - 1].capitalize()
        print(f"The most common month for bike rides is: {month_name}")

        # Calculate and display the most common day of the week.
        common_day = df['Day of Week'].mode()[0]
        print(f"The most common day of the week for bike rides is: {common_day}")

        # Calculate and display the most common start hour.
        df['Hour'] = df['Start Time'].dt.hour
        common_hour = df['Hour'].mode()[0]
        print(f"The most common start hour for bike rides is: {common_hour}:00")
    else:
        print("No data available for the selected filters.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)




def station_stats(df):
    """Displays statistics on the most popular stations and trips."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if not df.empty:
        # Most commonly used start station,
        common_start_station = df['Start Station'].mode()[0]
        common_start_station_count = df['Start Station'].value_counts().max()
        print(f"The most commonly used start station is: {common_start_station}")
        print(f"Count: {common_start_station_count}")

        # Most commonly used end station 
        common_end_station = df['End Station'].mode()[0]
        common_end_station_count = df['End Station'].value_counts().max()
        print(f"The most commonly used end station is: {common_end_station}")
        print(f"Count: {common_end_station_count}")

        # Most frequent trip combination of start station and end station trip with count
        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        common_trip = df['Trip'].mode()[0]
        common_trip_count = df['Trip'].value_counts().max()
        print(f"The most frequent combination of start station and end station trip is: {common_trip}")
        print(f"Count: {common_trip_count}")
    else:
        print("No data available for the selected filters.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)





def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Total travel time.
    total_travel_time = df['Trip Duration'].sum()
    print(f"The Total travel time for all trips: {total_travel_time} seconds")

    # AVG travel time.
    mean_travel_time = df['Trip Duration'].mean()
    print(f"The Mean travel time for trips: {mean_travel_time:.2f} seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    user_types_counts = df['User Type'].value_counts()
    for user_type, count in user_types_counts.items():
        print(f"{user_type}: {count}")

    # Check if 'Gender' column exists in the DF.
    if 'Gender' in df.columns:
        # Display counts if 'Gender' column is available
        gender_counts = df['Gender'].value_counts()
        for gender, count in gender_counts.items():
            print(f"{gender}: {count}")
    else:
        print("Gender data not available for this city.")

    # Check if 'Birth Year' column exists in the DF.
    if 'Birth Year' in df.columns:
        # Filter out rows with none/NAN birth year data.
        df_valid_birth_years = df[pd.notna(df['Birth Year'])]

        if not df_valid_birth_years.empty:
            # Earliest, most recent, n most common year of birth.
            earliest_birth_year = int(df_valid_birth_years['Birth Year'].min())
            most_recent_birth_year = int(df_valid_birth_years['Birth Year'].max())
            common_birth_year = int(df_valid_birth_years['Birth Year'].mode()[0])
            print(f"Earliest Birth Year: {earliest_birth_year}")
            print(f"Most Recent Birth Year: {most_recent_birth_year}")
            print(f"Most Common Birth Year: {common_birth_year}")
        else:
            print("No valid birth year data available for this city.")
    else:
        print("Birth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    """
    Displays individual trip data in increments of 5 rows as requested by the user.

    Args:
        df (DataFrame): Pandas DataFrame containing the bike-sharing data.
    """
    start_loc = 0
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()

    while view_data == 'yes':
        end_loc = start_loc + 5
        print(df.iloc[start_loc:end_loc])
        
        start_loc += 5

        view_data = input('Do you wish to continue? Enter yes or no: ').lower()

        if view_data != 'yes':
            break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw_data = input('\nWould you like to view individual trip data? Enter yes or no: ').lower()
        if display_raw_data == 'yes':
            display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
