"""
Module providing utility functions for this project.

These functions are general purpose utilities used by other modules in this project.
Some of these functions were exercises in early course modules and should be copied
over into this file.

The preconditions for many of these functions are quite messy.  While this makes writing 
the functions simpler (because the preconditions ensure we have less to worry about), 
enforcing these preconditions can be quite hard. That is why it is not necessary to 
enforce any of the preconditions in this module.

Author: Saroj Bono
Date: 04/23/2023
"""
import csv
import json
import datetime

def read_csv(filename):
    """
    Returns the contents read from the CSV file filename.
    
    This function reads the contents of the file filename and returns the contents as
    a 2-dimensional list. Each element of the list is a row, with the first row being
    the header. Cells in each row are all interpreted as strings; it is up to the 
    programmer to interpret this data, since CSV files contain no type information.
    
    Parameter filename: The file to read
    Precondition: filename is a string, referring to a file that exists, and that file 
    is a valid CSV file
    """
    
    list1=[]
    file=open(filename)
    reader=csv.reader(file)
    for row in reader:
        list1.append(row)
    file.close()
    return list1



from datetime import datetime

def write_csv(data,filename):
    """
    Writes the given data out as a CSV file filename.
    
    To be a proper CSV file, data must be a 2-dimensional list with the first row 
    containing only strings.  All other rows may be any Python value.  Dates are
    converted using ISO formatting. All other objects are converted to their string
    representation.
    
    Parameter data: The Python value to encode as a CSV file
    Precondition: data is a  2-dimensional list of strings
    
    Parameter filename: The file to read
    Precondition: filename is a string representing a path to a file with extension
    .csv or .CSV.  The file may or may not exist.
    """
    # Implement this function

    def convert_to_iso_format(date_str):
        try:
            date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            iso_format_str = date_obj.date().isoformat()
            return iso_format_str
        except ValueError:
            return date_str

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            new_row = []
            for col in row:
                col = convert_to_iso_format(col)
                new_row.append(col)
            writer.writerow(new_row)




def read_json(filename):
    """
    Returns the contents read from the JSON file filename.
    
    This function reads the contents of the file filename, and will use the json module
    to covert these contents in to a Python data value.  This value will either be a
    a dictionary or a list. 
    
    Parameter filename: The file to read
    Precondition: filename is a string, referring to a file that exists, and that file 
    is a valid JSON file
    """
    
    file=open(filename,'r')
    text=file.read()
    json1=json.loads(text)
    file.close()
    return json1

from dateutil.parser import parse   
import pytz

def str_to_time(timestamp,tzsource=None):
    """
    Returns the datetime object for the given timestamp (or None if timestamp is 
    invalid).
    
    This function should just use the parse function in dateutil.parser to
    convert the timestamp to a datetime object.  If it is not a valid date (so
    the parser crashes), this function should return None.
    
    If the timestamp has a time zone, then it should keep that time zone even if
    the value for tzsource is not None.  Otherwise, if timestamp has no time zone 
    and tzsource is not None, then this function will use tzsource to assign 
    a time zone to the new datetime object.
    
    The value for tzsource can be None, a string, or a datetime object.  If it 
    is a string, it will be the name of a time zone, and it should localize the 
    timestamp.  If it is another datetime, then the datetime object created from 
    timestamp should get the same time zone as tzsource.
    
    Parameter timestamp: The time stamp to convert
    Precondition: timestamp is a string
    
    Parameter tzsource: The time zone to use (OPTIONAL)
    Precondition: tzsource is either None, a string naming a valid time zone,
    or a datetime object.
    """
    # HINT: Use the code from the previous exercise and add time zone handling.
    # Use localize if tzsource is a string
    
    try:
        dt = parse(timestamp)
    except Exception as e:
        #print('except',e)
        return None
    if dt.tzinfo is None and tzsource is not None:
        if isinstance(tzsource, str):
            tz_obj = pytz.timezone(tzsource)
            if tz_obj is not None:
                dt = tz_obj.localize(dt)
        elif isinstance(tzsource, datetime.datetime):
            dt = dt.replace(tzinfo=tzsource.tzinfo)

        
    
    return dt
import datetime 


def daytime(time,daycycle):
    """
    Returns true if the time takes place during the day.
    
    A time is during the day if it is after sunrise but before sunset, as
    indicated by the daycycle dicitionary.
    
    A daycycle dictionary has keys for several years (as int).  The value for
    each year is also a dictionary, taking strings of the form 'mm-dd'.  The
    value for that key is a THIRD dictionary, with two keys "sunrise" and
    "sunset".  The value for each of those two keys is a string in 24-hour
    time format.
    
    For example, here is what part of a daycycle dictionary might look like:
    
        "2015": {
            "01-01": {
                "sunrise": "07:35",
                "sunset":  "16:44"
            },
            "01-02": {
                "sunrise": "07:36",
                "sunset":  "16:45"
            },
            ...
        }
    
    In addition, the daycycle dictionary has a key 'timezone' that expresses the
    timezone as a string. This function uses that timezone when constructing
    datetime objects from this set.  If the time parameter does not have a timezone,
    we assume that it is in the same timezone as the daycycle dictionary
    
    Parameter time: The time to check
    Precondition: time is a datetime object
    
    Parameter daycycle: The daycycle dictionary
    Precondition: daycycle is a valid daycycle dictionary, as described above
    """
    # HINT: Use the code from the previous exercise to get sunset AND sunrise
    # Add a timezone to time if one is missing (the one from the daycycle)
    
    # Add a timezone to time if one is missing (the one from the daycycle)

    if time is None or daycycle is None:
        return None
    if 'timezone' not in daycycle:
        daycycle['timezone'] = 'UTC'
    
    year = str(time.year)
    if year not in daycycle:
        return None

    month_day = time.strftime("%m-%d")
    if month_day not in daycycle[year]:
        return None

    sunrise_str = daycycle[year][month_day]["sunrise"]
    sunset_str = daycycle[year][month_day]["sunset"]

    timezone = pytz.timezone(daycycle["timezone"])

    if time.tzinfo is None:
        time = timezone.localize(time)

    sunrise_time = timezone.localize(datetime.datetime.strptime(year + "-" + month_day + "T" + sunrise_str, "%Y-%m-%dT%H:%M"))

    # Add one minute to the sunrise_time to account for the test case requirement
    #sunrise_time += datetime.timedelta(minutes=1)
    sunset_time = timezone.localize(datetime.datetime.strptime(year + "-" + month_day + "T" + sunset_str, "%Y-%m-%dT%H:%M"))


    return sunrise_time <time < sunset_time



def get_for_id(id,table):
    """
    Returns (a copy of) a row of the table with the given id.
    
    Table is a two-dimensional list where the first element of each row is an identifier
    (string).  This function searches table for the row with the matching identifier and
    returns a COPY of that row. If there is no match, this function returns None.
    
    This function is useful for extract rows from a table of pilots, a table of instructors,
    or even a table of planes.
    
    Parameter id: The id of the student or instructor
    Precondition: id is a string
    
    Parameter table: The 2-dimensional table of data
    Precondition: table is a non-empty 2-dimension list of strings
    """
    # Implement this

    #iterate through the rows
    for row in table:
        # Check if the id is in the row
        if id in row:
            # If found
            return row.copy()
    # If not found
    return None