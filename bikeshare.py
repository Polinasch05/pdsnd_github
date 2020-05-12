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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # TO DO: get user input for month (all, january, february, ... , june) 
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    
    print('\nHello! Let\'s explore some US bikeshare data!')
    
    city = input("\nWould you like to see data for New York City, Chicago or Washington?\n").lower()
    while city not in ('chicago', 'new york city', 'washington'):
        city = input("City is name is invalid! Please input another name: ").lower()
        
        
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("\nWhich month would you like to filter by? January, February, March, April, May, June or type 'all' if you do not have any preference?\n").lower()
    while month not in ('january', 'february', 'march', 'april', 'may', 'june', 'all'):
        month = input("Sorry, there must be a typo. Please try again.").lower() 
        
        
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("\nAre you looking for a particular day? If so, kindly enter the day as follows: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or type 'all' if you do not have any preference.\n").lower() 
    while day not in ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all'):
        day = input("Sorry, there must be a typo. Please try again.").lower() 

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

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
        

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)   
    
    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Common Day:', popular_day)     
    
    # TO DO: display the most common start 
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Common Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most common start station is: {} ".format(df['Start Station'].mode().values[0]))

    # TO DO: display most commonly used end station
    print("The most common end station is: {} ".format(df['End Station'].mode().values[0]))

    # TO DO: display most frequent combination of start station and end station trip
    frequent_stations = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('Most frequent start and end station: ', frequent_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = sum(df['Trip Duration'])
    print('Total travel time:', total_travel_time/86400, " Days")


    # TO DO: display mean travel time

    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time/60, " Minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("Here are the counts of different user types:")
    print(df['User Type'].value_counts())

    # TO DO: Display counts of gender
    if city != 'washington':
        gender_types = df['Gender'].value_counts()
        print('\nGender Types:\n', gender_types)

    # TO DO: Display earliest, most recent, and most common year of birth
    
    try:
        earliest_year = df['Birth Year'].min()
        print('\nEarliest Year:', earliest_year)
    except KeyError:
        print('There is no data to display')
    
    try:
        most_recent_year = df['Birth Year'].max()
        print('\nMost Recent Year:', most_recent_year)
    except KeyError:
        print('There is no data to display')

    try:
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Year:', most_common_year)
    except KeyError:
        print('There is no data to display')

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
#show raw data
def display_data(df):
    start_loc = 0
    end_loc = 5
  
    display_question = input("Do you want to see the raw data?: ").lower()
    if display_question == 'yes':
        while end_loc <= df.shape[0] - 1:
            print(df.iloc[start_loc:end_loc,:])
            start_loc += 5
            end_loc += 5
            
            end_display = input("Do you want to see more 5 lines of raw data?: ").lower()
            if end_display == 'no':
                break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
