import time
import pandas as pd
import numpy as np

# a dictionary CITY_DATA is created to store data for all the three cities in key-value pairs
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# a function get_filters is created that interacts with user input. allows user to input their choices of data they want to see
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # first allow user to input a city name
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    # the while loop keeps looping as long as invalid city name is entered. breaks out of loop once valid name is input
    # .lower() also helps with making input non-case sensitivee
    while True:
        cities = ['chicago', 'new york city', 'washington']
        city = input('Would you like to see data for chicago, new york city or washington? Choose one city.\n').lower()
        if city in cities:
            print('You entered', city)
            break
        else:
            print('\nInvalid city name entered. Please try again\n')

    # now user must choose a specific month or all the months
    # get user input for month (all, january, february, ... , june)
    while True:
        month_list =['all','january', 'february', 'march', 'april', 'may', 'june']
        month =input('\nEnter a month for which to display data. Enter month from January to June or All to display data for all months\n').lower()
        if month in month_list:
            print('You entered {}'.format(month))
            break
        else:
            print('\nInvalid month name entered. Please try again')

    # now user must choose a specific day or all days
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        day = input('\nEnter a day for which to display data. Enter a day from Monday to Sunday or All to display data for all days\n').lower()
        if day in day_list:
            print('You entered {}'.format(day))
            break
        else:
            print('Invalid day name entered. Please try again')

    print('-'*40)
    # this returns valid city, month, day inputs of user
    return city, month, day 

# so we started by storing all the data in CITY_DATA dictionary
# then interacted with user who inputed filters for data they want to see
# now, based on those filters of city, month, day, that got returned above, we load that data they want to see
# the load_data funtion below takes those valid filters as its arguments
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
    # first load csv data for city chosen from CITY_DATA dictionary
    # load the csv file of the specific chosen city into a dataframe df
    df = pd.read_csv(CITY_DATA[city])
    #csv file has start time coloumn, so convert it to date time so you can extract things like month, days, hours, minutes
    # our start time dataframe simply becomes a start time dataframe that has been converted to datatime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # now extract the month and day of the week from converted start time
    df['month'] = df['Start Time'].dt.month
    df['week_day'] = df['Start Time'].dt.day_name()

    # now we have extracted the relevant parametrs month and day of week, we can filter to get data wanted by the user
    # first filter by the month. only filter if user chose a specific month. that is , if they did not enter all
    if month != 'all':
        # use inex of the month_list to get th corresponding integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
        # now actually do the month filtering to create a new data frame
        # date frame is made of data frame where dataframe is equal to month
        df = df[df['month'] == month]

    # now filter by the days of the week if user did not input all but entered a specific day
    # then create a new data frame for the day's data
    if day != 'all':
        df = df[df['week_day'] == day.title()]
    # function returns the dataframe with relevant columns based on filtering by month and day
    return df

# now that the user has  input city, month, day choices, and we have filtered and extracted date time parameters
# the time_stats function below compues the month, day, hour stats
def time_stats(df):
    """Displays statistics on the most frequent times of travel. """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    # we can only display most common month if user has chosen all instead of a specific month
    # the mode is used to find the most common paramters
    #if month == 'all':
    most_common_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    most_common_month = months[most_common_month - 1]
    print('The most common month is', most_common_month)

    # display the most common day of week
    # also, can only display most common day if user chose all
    #if day == 'all':
    most_common_day = df['week_day'].mode()[0]
    print('The most common day day of week is {}'.format(most_common_day))

    # display the most common start hour
    # since hour is not explicitly input like month and day. have to extract it first from the start time column
    df['Start Hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['Start Hour'].mode()[0]
    print('The most common start hour is {}:00 hours'.format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# function displaying statistics about stations
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('The most common start station is {}'.format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most common end station is', most_common_end_station)

    # display most frequent combination of start station and end station trip
    # trick is to combine the start station and end station columns using str.cat and create a new column for the result named start_end
    # then apply usual mode on start_end  to find most common
    df['Start_End'] = df['Start Station'].str.cat(df['End Station'], sep = 'to')
    most_common_combination = df['Start_End'].mode()[0]
    print('The most frequent station combunation is {}'.format(most_common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# function displaying trip duration statistics
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time using sum method
    # then find the duration in terms of seconds, minutes, also hour, minutes
    total_travel_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_travel_duration, 60)
    hour, minute = divmod(minute, 60)
    print('The total travel time is {} hour(s) {} minute(s) {} second(s)'.format(hour,minute,second))

    # display mean travel time using the mean function
    # the find the duration average in terms of minutes and secons
    # now, if the minutes are above an hour, display in hours
    average_travel_duration = round(df['Trip Duration'].mean())
    mins, secs = divmod(average_travel_duration, 60)
    # if the minutes are above 60, we are in hours
    if mins > 60:
        hrs, mins = divmod(mins,60)
        print('The average travel duration is {} hour(s) {} minute(s) {} second(s)'.format(hrs, mins, secs))
    else:
        print('The average travel duration is {} minute(s) {} second(s)'.format(mins, secs))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# functon to calculate the statistics about users
def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        param1 (df): The data frame you wish to work with.
    Returns:
        None."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types using value_counts which counts unique values
    user_type_count = df['User Type'].value_counts()
    print('The user type count is\n', user_type_count)

    # Display counts of gender
    # but now not all csv files may have the gender coloum, in fact only chicago and new york have
    # hence use try clausesss
    try:
        gender_count = df['Gender'].value_counts()
        print('\nThe count of different gender types is\n', gender_count)
        print(' ')
    except:
        print('The file does not contain a gender information')

    # Display earliest, most recent, and most common year of birth
    # also use the try clause as not all csv files contain the birth month colunm
    # in fact only chicago and new york have birth mobth column
    try:
        earliest_year_of_birth = int(df['Birth Year'].min())
        print('\nThe earliest year of birth is {}'.format(earliest_year_of_birth))
        most_recent_birth_year = int(df['Birth Year'].max())
        print('The most recent year of birth is {}'.format(most_recent_birth_year))
        most_common_birth_year = int(df['Birth Year'].mode()[0])
        print('The most common year of birth is {}'.format(most_common_birth_year))
    except:
        print('The file does not contain a birth year information')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# defining a function that asks ther user if they want to
# displays 5 rows of data, showing all available columns for the chosen csv file
# and then keeping asking the user if they want to view further data
def display_data(df):
    user_answer_list = ['yes', 'no']
    counter = 0
    answer =input('Do you want to display 5 entries of data? Choose yes or no\n').lower()
    if answer in user_answer_list:
        if answer == 'yes':
            print('You have entered {}'.format(answer))
            print(df.head())
        elif answer not in user_answer_list:
                print('Invalid input. Please try again')
    # keep asking user to view more 5 raw data 
    # use while loop, meaning as long as the anser is yes, keep asking further
    while answer == 'yes':
        print('Do you want to display 5 more rows of data? Choose yes or no\n')
        counter = counter +5 
        answer = input().lower()
        if answer == 'yes':
            print('You have entered {}'.format(answer))
            print(df[counter:counter+5])
        elif answer == 'no':
            print('You have entered {} program preparing to terminate...'.format(answer))
        elif answer not in user_answer_list:
            print('Invalid answer entered')
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
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        
if __name__ == "__main__":
	main()
