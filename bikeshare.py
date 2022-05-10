import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:  # Loop to accept city
        try:
            city = input("Please enter which city you would like to investigate (New York City, Chicago, Washington): ").lower()
        except:
            print('Please enter a valid city!')
        if city != 'chicago' and city != 'new york city' and city != 'washington':
            print('Please enter a valid city!')
            continue
        else:
            break
            
    while True:  # Loop to accept month
        valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        try:
            month = input("Please enter which month you would like data from (January, February, ... , June, or All): ").lower()
        except:
            print('Please enter a valid month!')
        if month not in valid_months:
            print('Please enter a valid month!')
            continue
        else:
            break

    while True:  # Loop to accept day of week
        valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
        try:
            day = input("Please enter which day you would like data from (Monday, Tuesday, ... , Sunday, or All): ").lower()
        except:
            print('Please enter a valid day!')
        if day not in valid_days:
            print('Please enter a valid day!')
            continue
        else:
            break
            
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
    df = pd.read_csv("./OneDrive/Desktop/ClassPy/"+CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        #months = ['january', 'february', 'march', 'april', 'may', 'june']
        #month = months.index(month) + 1
    
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

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: ', common_month)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is: ', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    if common_hour >= 12:  #convert to AM/PM
        common_hour = str(common_hour - 12) + ' P.M.'
    else:
        common_hour = str(common_hour) + ' A.M.'
    print('The most common start hour is: ', common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is: ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common end station is: ', common_end_station)

    # display most frequent combination of start station and end station trip
    common_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print('The most common start-end combination is: ', common_combo[0], ' to ', common_combo[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_days = int(total_travel_time / 86400)
    total_hours = int(total_travel_time % 86400 / 3600)
    total_minutes = int(total_travel_time % 86400 % 3600 / 60)
    total_seconds = total_travel_time % 86400 % 3600 % 60
    print('The total travel time was: {} days, {} hours, {} minutes, and {} seconds.'.format(total_days, total_hours, total_minutes, total_seconds))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_days = int(mean_travel_time / 86400)
    mean_hours = int(mean_travel_time % 86400 / 3600)
    mean_minutes = int(mean_travel_time % 86400 % 3600 / 60)
    mean_seconds = mean_travel_time % 86400 % 3600 % 60
    print('The mean travel time was: {} days, {} hours, {} minutes, and {:.0f} seconds.'.format(mean_days, mean_hours, mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for index, user in enumerate(user_types.index.tolist()):
        print('Total number of', user, 'user type: ', user_types[index])

        
    if 'Gender' in df: #handle gender if not in data  
        # Display counts of gender
        print()
        genders = df['Gender'].value_counts(dropna=False)
        for index, gender in enumerate(genders.index.tolist()):
            if gender != 'Male' and gender != 'Female':
                print('Total number of unspecified gender: ', genders[index])     
            else:
                print('Total number of', gender, 'user type: ', genders[index])
    else:
        print('\nGender not provided for selected dataset.')

    if 'Birth Year' in df: # handle birth year if not in data
        # Display earliest, most recent, and most common birth year
        print()
        earliest_birth_year = int(df['Birth Year'].min())
        print('The earliest birth year was: ', earliest_birth_year)
        recent_birth_year = int(df['Birth Year'].max())
        print('The most recent birth year was: ', recent_birth_year)
        common_birth_year = int(df['Birth Year'].mode()[0])
        print('The most common birth year was: ', common_birth_year)
    else:
        print('\nBirth Year not provided for this dataset.')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def data_crawl(df): # display data upon request
    print(df.shape)
    while True: # loop to prompt user whether they would like to see data
        try:
            view_data = input("\nWould you like to view rows of individual trip data?  Enter Yes or No.").lower()
        except:
            print("Please enter either Yes or No.")
        if view_data != 'yes' and view_data != 'no':
            print("Please enter either Yes or No.")
            continue
        else:
            break
        
    while True: # loop to ask number of rows to view
        try:
            num_rows = int(input('How many rows would you like to view at a time? (1-100)'))
        except ValueError:
            print("Please enter an integer between 1 and 100.  (No strings allowed!)")
        if num_rows <= 0 or num_rows > 100:
            print('Please enter a positive integer.')
            continue
        else:
            break
        
    start = 0
    while view_data == 'yes':  #loop to continue if user wants more data
        if start >= df.shape[0]: # if statement to catch when all data has been displayed, and move to statistics
            print('\nYou have reached the end of the data.  Presenting statistics on selected dataset.')
            break
        else:      
            print(df.iloc[start:start+num_rows])
            start += num_rows
            while True:
                try:
                    view_data = input("\nDo you wish to view {} more lines?  Enter Yes or No.".format(num_rows)).lower()
                except:
                    print("Please enter either Yes or No.")
                if view_data != 'yes' and view_data != 'no':
                    print("Please enter either Yes or No.")
                    continue
                else:
                    break

    if start <= df.shape[0]:  #if statement to correctly display number of lines viewed
        print('\n{} total lines of data viewed.'.format(start))
    else:
        print('\n{} total lines of data viewed.'.format(df.shape[0]))
    print('-'*40)
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        data_crawl(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        while True:  # Loop to catch inputs other than yes/no
            try:
                restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            except:
                print('Please enter a valid city!')
            if restart != 'yes' and restart != 'no':
                print('Please enter a valid city!')
                continue
            else:
                break
        
        if restart == 'no':
            break


if __name__ == "__main__":
	main()