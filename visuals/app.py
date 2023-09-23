import streamlit as st
import pandas as pd


CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    st.write('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington).
    city = st.selectbox('Select the city to analyze:', list(CITY_DATA.keys()))

    # Get user input for month (All, January, February..., june).
    month = st.selectbox('Select the month to filter by:', ['all'] + MONTHS)

    # Get user input for day of the week (all, monday, tuesday, ..., sunday).
    day = st.selectbox('Select the day of the week to filter by:', ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])

    return city, month, day

def load_data(city, month, day):
    # data file for the selected city.
    file_name = CITY_DATA[city]
    df = pd.read_csv(file_name)

    # Converting the 'Start Time' column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month and day of the week from the 'Start Time' column.
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # Apply filters based on user input for month and day, considering no filters as well.
    if month != 'all':
        # Filter by month if valid month is specified.
        month_num = MONTHS.index(month) + 1
        df = df[df['Month'] == month_num]

    if day != 'all':
        # Filter by day of the week if a day is specified.
        df = df[df['Day of Week'] == day.title()]

    return df

def time_stats(df):
    st.header('Time Statistics')

    if not df.empty:
        # Calculate and display the most common month.
        common_month = df['Month'].mode()[0]
        month_name = MONTHS[common_month - 1].capitalize()
        st.write(f"The most common month for bike rides is: {month_name}")

        # Calculate and display the most common day of the week.
        common_day = df['Day of Week'].mode()[0]
        st.write(f"The most common day of the week for bike rides is: {common_day}")

        # Calculate and display the most common start hour.
        df['Hour'] = df['Start Time'].dt.hour
        common_hour = df['Hour'].mode()[0]
        st.write(f"The most common start hour for bike rides is: {common_hour}:00")
    else:
        st.write("No data available for the selected filters.")

def station_stats(df):
    st.header('Station Statistics')

    if not df.empty:
        # Most commonly used start station,
        common_start_station = df['Start Station'].mode()[0]
        common_start_station_count = df['Start Station'].value_counts().max()
        st.write(f"The most commonly used start station is: {common_start_station}")
        st.write(f"Count: {common_start_station_count}")

        # Most commonly used end station 
        common_end_station = df['End Station'].mode()[0]
        common_end_station_count = df['End Station'].value_counts().max()
        st.write(f"The most commonly used end station is: {common_end_station}")
        st.write(f"Count: {common_end_station_count}")

        # Most frequent trip combination of start station and end station trip with count
        df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
        common_trip = df['Trip'].mode()[0]
        common_trip_count = df['Trip'].value_counts().max()
        st.write(f"The most frequent combination of start station and end station trip is: {common_trip}")
        st.write(f"Count: {common_trip_count}")
    else:
        st.write("No data available for the selected filters.")

def trip_duration_stats(df):
    st.header('Trip Duration Statistics')

    if not df.empty:
        # Total travel time.
        total_travel_time = df['Trip Duration'].sum()
        st.write(f"The Total travel time for all trips: {total_travel_time} seconds")

        # AVG travel time.
        mean_travel_time = df['Trip Duration'].mean()
        st.write(f"The Mean travel time for trips: {mean_travel_time:.2f} seconds")
    else:
        st.write("No data available for the selected filters.")

def user_stats(df):
    st.header('User Statistics')

    if not df.empty:
        # Display counts of user types.
        user_types_counts = df['User Type'].value_counts()
        st.write("User Types:")
        st.write(user_types_counts)

        # Check if 'Gender' column exists in the DF.
        if 'Gender' in df.columns:
            # Display counts if 'Gender' column is available
            gender_counts = df['Gender'].value_counts()
            st.write("Gender:")
            st.write(gender_counts)
        else:
            st.write("Gender data not available for this city.")

        # Check if 'Birth Year' column exists in the DF.
        if 'Birth Year' in df.columns:
            # Filter out rows with none/NAN birth year data.
            df_valid_birth_years = df[pd.notna(df['Birth Year'])]

            if not df_valid_birth_years.empty:
                # Earliest, most recent, n most common year of birth.
                earliest_birth_year = int(df_valid_birth_years['Birth Year'].min())
                most_recent_birth_year = int(df_valid_birth_years['Birth Year'].max())
                common_birth_year = int(df_valid_birth_years['Birth Year'].mode()[0])
                st.write(f"Earliest Birth Year: {earliest_birth_year}")
                st.write(f"Most Recent Birth Year: {most_recent_birth_year}")
                st.write(f"Most Common Birth Year: {common_birth_year}")
            else:
                st.write("No valid birth year data available for this city.")
        else:
            st.write("Birth year data not available for this city.")

def main():
    st.title('Bikeshare Data Analysis')
    
    # Get user input for city, month, and day
    city, month, day = get_filters()
    
    # Load data based on user selections
    df = load_data(city, month, day)

    # Display options for analysis
    analysis_option = st.selectbox(
        'Select analysis option:',
        ('Time Statistics', 'Station Statistics', 'Trip Duration Statistics', 'User Statistics')
    )

    if analysis_option == 'Time Statistics':
        time_stats(df)

    elif analysis_option == 'Station Statistics':
        station_stats(df)

    elif analysis_option == 'Trip Duration Statistics':
        trip_duration_stats(df)

    elif analysis_option == 'User Statistics':
        user_stats(df)

if __name__ == "__main__":
    main()
