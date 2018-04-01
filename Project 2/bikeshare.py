import time
import pandas as pd

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
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input('Choose a city: Chicago, New York City, or Washington: ').lower() 
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Sorry, I did not understand your input.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Choose a month: January, February, March, April, May, June, or All: ').title() 
        if month in ['January','February','March','April','May','June','All']:
            break
        else:
            print('Sorry, I did not understand your input.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Choose a day of week: Monday, Tuesday, ..., Sunday, or All: ').title() 
        if day in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday',\
                    'Sunday','All']:
            break
        else:
            print('Sorry, I did not understnad your input.')

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
    df = pd.read_csv(CITY_DATA[city], parse_dates = ['Start Time', 'End Time'])
    
    if month != 'All':        
        df = df[df['Start Time'].dt.strftime('%B') == month]
        
    if day != 'All':
        
        df = df[df['Start Time'].dt.strftime('%A') == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    result = df['Start Time'].dt.strftime('%B').value_counts().head(1)
    print('The most common month is {}. Count: {}'.format(result.index[0],\
          result.values[0]))

    # display the most common day of week
    result = df['Start Time'].dt.strftime('%A').value_counts().head(1)
    print('The most common day of week is {}. Count: {}'.format(result.index[0],\
          result.values[0]))
    # display the most common start hour
    result = df['Start Time'].dt.strftime('%H').value_counts().head(1)
    print('The most common start hour is {}. Count: {}'.format(result.index[0],\
          result.values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    result = df['Start Station'].value_counts().head(1)
    print('The most commonly used start station is {}. Count: {}'.format(result.index[0],\
          result.values[0]))

    # display most commonly used end station
    result = df['End Station'].value_counts().head(1)
    print('The most commonly used end station is {}. Count: {}'.format(result.index[0],\
          result.values[0]))

    # display most frequent combination of start station and end station trip
    result = df.groupby('Start Station')['End Station'].value_counts()
    print('The most frequeny combination of start and end trip is {} to {}.\
          Count: {}'.format(result.argmax()[0], result.argmax()[1],result.max()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    df['Duration'] = df['End Time'] - df['Start Time']
    # display total travel time
    print('Total travle time: {}'.format(df['Duration'].sum()))

    # display mean travel time
    print('Total travle time: {}'.format(df['Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:')
    result = df['User Type'].value_counts()
    for i in range(result.shape[0]):
        print('{}: {}'.format(result.index[i], result.values[i]))
    print('')

    # Display counts of gender
    if 'Gender' in df.columns:
        print('Counts of gender:')
        result = df['Gender'].value_counts()
        for i in range(result.shape[0]):
            print('{}: {}'.format(result.index[i], result.values[i]))
    print('')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('Earliest birth year: {}'.format(int(df['Birth Year'].min())))
        
        print('Most recent birth year: {}'.format(int(df['Birth Year'].max())))
        
        result = df['Birth Year'].value_counts().head(1)
        print('Most common birth year is {}. Count: {}'.format(int(result.index[0]), result.values[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
