#!/usr/bin/env python


"""spans several different calendars, calculates the days between 2 dates, the standard python tutorial for introduction"""


def is_leap_year(year):

    if year >= -45 and year <= -9 and year%3 == 0:
        return True

    if year >= 8 and year <= 1582 and year%4 == 0:
        return True

    if year > 1582 and year%4 == 0:
        if year%400 == 0:
            return True
        elif year%100 == 0:
            return False
        else:
            return True

    return False

def add_leap_day_birth(birth_month, birth_year):

    if is_leap_year(birth_year) == True:
        if birth_month != 1 and birth_month != 2:
            return True

    return False


def add_leap_day_this(this_month, this_year, birthday):

    if is_leap_year(this_year) == True:
        if this_month == 1 or (this_month == 2 and birthday != 29):
            return True

    return False






def age_in_days(birth_month, birthday, birth_year, this_month, today, this_year):

    leap_year_correction = 0

    if add_leap_day_this(this_month,this_year,birthday) == True:
        leap_year_correction = leap_year_correction + 1

    if add_leap_day_birth(birth_month,birth_year) == True:
        leap_year_correction = leap_year_correction + 1

    leap_years = 0

    days_in_month = [31,28,31,30,31,30,31,31,30,31,30,31]

    year_difference = this_year - birth_year - 1

    #adjusts difference in years because the year after 1 BC is 1 AD
    if birth_year < 0:
        year_difference = this_year - birth_year - 1

    month_days_birth_year = 0

    January_string = 'January'

    if birth_month == 1:
        month_days_birth_year = 0

    if birth_month == 2:
        month_days_birth_year = 31

    if birth_month == 3:
        month_days_birth_year = 59

    if birth_month == 4:
        month_days_birth_year = 90

    if birth_month == 5:
        month_days_birth_year = 120

    if birth_month == 6:
        month_days_birth_year = 151

    if birth_month == 7:
        month_days_birth_year = 181

    if birth_month == 8:
        month_days_birth_year = 212

    if birth_month == 9:
        month_days_birth_year = 242

    if birth_month == 10:
        month_days_birth_year = 273

    if birth_month == 11:
        month_days_birth_year = 303

    if birth_month == 12:
        month_days_birth_year = 334

    days_from_start_of_year_birth_year = month_days_birth_year + birthday

    if this_month == 1:
        month_days_this_year = 0

    if this_month == 2:
        month_days_this_year = 31

    if this_month == 3:
        month_days_this_year = 59

    if this_month == 4:
        month_days_this_year = 90

    if this_month == 5:
        month_days_this_year = 120

    if this_month == 6:
        month_days_this_year = 151

    if this_month == 7:
        month_days_this_year = 181

    if this_month == 8:
        month_days_this_year = 212

    if this_month == 9:
        month_days_this_year = 242

    if this_month == 10:
        month_days_this_year = 273

    if this_month == 11:
        month_days_this_year = 303

    if this_month == 12:
        month_days_this_year = 334

    days_from_start_of_year_this_year = month_days_this_year + today

    #protects against bad years

    if birth_year == 0 or this_year == 0:
        return 'There is no year 0, the year after 1 BC is 1 AD.'

    if birth_year > this_year:
        return 'Please enter the correct years...the birthday cannot be in the future!!!'

    if birth_year == this_year and days_from_start_of_year_birth_year > days_from_start_of_year_this_year:
        return 'Please enter the correct years...the birthday cannot be in the future!!!'

    #finds how many leap years are within the span for Gregorian only

    #The year Gregorian calendar starts = 1582

    GregorianStart = 1582

    if birth_year >= GregorianStart:


        test_birth_year = birth_year

        while True:
            if test_birth_year > this_year:
                break

            birth_year_by_four = test_birth_year % 4
            birth_year_by_hundred = test_birth_year % 100
            birth_year_by_fourhundred = test_birth_year % 400

            if birth_year_by_four == 0 and birth_year_by_hundred != 0:
                leap_years = leap_years + 1
            if birth_year_by_hundred == 0 and birth_year_by_fourhundred == 0:
                leap_years = leap_years + 1

            test_birth_year = test_birth_year + 1

#changes leap year pattern to only Julian calendar

    if birth_year < GregorianStart and this_year < GregorianStart:



        #tests for BC leap year values...up to 9 BC, leap years were divisible by 3...leap years came back in 8 AD, divisible by 4 now

        test_birth_year = birth_year

        #if birth year is before the first leap year, sets the test to start with the first leap year

        if birth_year < -45:
            test_birth_year = -45

        #if statement nested within the condition of "birth_year < GregorianStart" in line 179, so
        #another entire code block isn't needed. if the birth year is before 1582, it may be before
        #1 AD, it may not



            while True:
                if test_birth_year > this_year:
                    break

            #since leap years were discontinued until 8 AD, sets test year to 8 AD...if it skips past
            #'this year', it'll break the loop

                if test_birth_year > -8:
                    test_birth_year = 7

                birth_year_by_three = test_birth_year % 3

                if birth_year_by_three == 0:
                    leap_years = leap_years + 1

                test_birth_year = test_birth_year + 1

        while True:
            if test_birth_year > this_year:
                break

            birth_year_by_four = test_birth_year % 4

            if birth_year_by_four == 0:
                leap_years = leap_years + 1


            test_birth_year = test_birth_year + 1

#changes leap year patterm to split Julian and Gregorian calendars

    if birth_year < GregorianStart and birth_year >= 0 and this_year >= GregorianStart:



        test_birth_year = birth_year

        if birth_year < 8:
            while True:
                if test_birth_year > this_year:
                    break

                if test_birth_year > -8:
                    test_birth_year = 7

                birth_year_by_three = test_birth_year % 3

                if birth_year_by_three == 0:
                    leap_years = leap_years + 1

                test_birth_year = test_birth_year + 1

        while True:

            #since birthyear was already said to be in julian calendar

            birth_year_by_four = test_birth_year % 4

            if birth_year_by_four == 0:
                leap_years = leap_years + 1

            test_birth_year = test_birth_year + 1

            if test_birth_year == GregorianStart:
                if test_birth_year > this_year:
                    break

                #since thisyear was stated in Gregorian calendar

                birth_year_by_four = test_birth_year % 4
                birth_year_by_hundred = test_birth_year % 100
                birth_year_by_fourhundred = test_birth_year % 400

                if birth_year_by_four == 0 and birth_year_by_hundred != 0:
                    leap_years = leap_years + 1
                if birth_year_by_hundred == 0 and birth_year_by_fourhundred == 0:
                    leap_years = leap_years + 1

                test_birth_year = test_birth_year + 1


    #final equation

    age_in_dayz = (year_difference * 365) + days_from_start_of_year_this_year - days_from_start_of_year_birth_year + leap_years - leap_year_correction

    #Silly input prevention

    check_birth_year_by_three = birth_year % 3

    check_birth_year_by_four = birth_year % 4
    check_birth_year_by_hundred = birth_year % 100
    check_birth_year_by_fourhundred = birth_year % 400

    leap_year_check_birth_year = False


    if check_birth_year_by_four == 0 and check_birth_year_by_hundred != 0:
        leap_year_check_birth_year = True
    if check_birth_year_by_hundred == 0 and check_birth_year_by_fourhundred == 0:
        leap_year_check_birth_year = True


    check_this_year_by_four = this_year % 4
    check_this_year_by_hundred = this_year % 100
    check_this_year_by_fourhundred = this_year % 400

    leap_year_check_this_year = False

    if check_this_year_by_four == 0 and check_this_year_by_hundred != 0:
        leap_year_check_this_year = True
    if check_this_year_by_hundred == 0 and check_this_year_by_fourhundred == 0:
        leap_year_check_this_year = True

    messages = []
    if birth_month == 1 and birthday > 31:
        messages.append('January only has 31 days, goofball!')
    if this_month == 1 and today > 31:
        messages.append('January only has 31 days, goofball!')

    if is_leap_year(birth_year) == True:
        if this_month == 2 and today > 29:
            messages.append('February only has 29 days in a leap year, goofball!')
    if is_leap_year(birth_year) == False:
        if this_month == 2 and today > 28:
            messages.append('February only has 29 days in a leap year, goofball!')

    if birth_month == 3 and birthday > 31:
        messages.append('March only has 31 days, goofball!')
    if this_month == 3 and today > 31:
        messages.append('March only has 31 days, goofball!')
    if birth_month == 4 and birthday > 30:
        messages.append('April only has 30 days, goofball!')
    if this_month == 4 and today > 30:
        messages.append('April only has 30 days, goofball!')
    if birth_month == 5 and birthday > 31:
        messages.append('May only has 31 days, goofball!')
    if this_month == 5 and today > 31:
        messages.append('May only has 31 days, goofball!')
    if birth_month == 6 and birthday > 30:
        messages.append('June only has 30 days, goofball!')
    if this_month == 6 and today > 30:
        messages.append('June only has 30 days, goofball!')
    if birth_month == 7 and birthday > 31:
        messages.append('July only has 31 days, goofball!')
    if this_month == 7 and today > 31:
        messages.append('July only has 31 days, goofball!')
    if birth_month == 8 and birthday > 31:
        messages.append('August only has 31 days, goofball!')
    if this_month == 8 and today > 31:
        messages.append('August only has 31 days, goofball!')
    if birth_month == 9 and birthday > 30:
        messages.append('September only has 30 days, goofball!')
    if this_month == 9 and today > 30:
        messages.append('September only has 30 days, goofball!')
    if birth_month == 10 and birthday > 31:
        messages.append('October only has 31 days, goofball!')
    if this_month == 10 and today > 31:
        messages.append('October only has 31 days, goofball!')
    if birth_month == 11 and birthday > 30:
        messages.append('November only has 30 days, goofball!')
    if this_month == 11 and today > 30:
        messages.append('November only has 30 days, goofball!')
    if birth_month == 12 and birthday > 31:
        messages.append('December only has 31 days, goofball!')
    if this_month == 12 and today > 31:
        messages.append('December only has 31 days, goofball!')


    if len(messages) == 2:
        if messages[0] == messages[1]:
            return messages[0]

    else:
        for s in messages:
            return s




        return age_in_dayz



#input birthday first: 1, 23, 1987, then today: 1, 29, 2014...in that format

print age_in_days(3, 29, 1955, 3, 29, 1988)
