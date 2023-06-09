"""
Module that validates the flight school's records.

This is the primary module that does all of the work. It loads the files, loops through
the lessons, and searches for any takeoffs that violate insurance requirements.

Technically, we could have put many of these functions in __main__.py.  That is the
main module of this application anyway.  However, for testing purposes we want all
functions in modules and we only want script code in the file __main__.py

Author: Saroj Bono
Date: 05/03/2023
"""
import utils
import tests
import os.path
import violations

# Uncomment for the extra credit
import endorsements
import inspections


def discover_violations(directory,output):
    """
    Searches the dataset directory for any flight lessons the violation regulations.
    
    This function will call list_weather_violations() to get the list of weather violations.
    If list_endorsment_violations (optional) is completed, it will call that too, as
    well as list_inspection_violations.  It will concatenate all of these 2d lists
    into a single 2d list of violations (so a flight may be listed more than once for
    each of the three types of violations).
    
    If the parameter output is not None, it will create the CSV file with name output
    and write the 2d list of violations to this file.  This CSV file should have the
    following header:
    
        STUDENT,AIRPLANE,INSTRUCTOR,TAKEOFF,LANDING,FILED,AREA,REASON
    
    Regardless of whether output is None, this function will print out the number of
    violations, as follows:
    
        '23 violations found.'
    
    If no violations are found, it will say
    
        'No violations found.'
    
    Parameter directory: The directory of files to audit
    Precondition: directory is the name of a directory containing the files 'daycycle.json',
    'weather.json', 'minimums.csv', 'students.csv', 'teachers.csv', 'lessons.csv',
    'fleet.csv', and 'repairs.csv'.
    
    Parameter output: The CSV file to store the results
    Precondition: output is None or a string that is a valid file name
    """
    # Implement this functiondef discover_violations(directory, output):
    lessons = utils.read_csv(os.path.join(directory, 'lessons.csv'))
    students = utils.read_csv(os.path.join(directory, 'students.csv'))
    weather = utils.read_json(os.path.join(directory, 'weather.json'))
    minimums = utils.read_csv(os.path.join(directory, 'minimums.csv'))
    daytimes = utils.read_json(os.path.join(directory, 'daycycle.json'))

    # Call list_weather_violations() to get the list of weather violations
    weather_violations = violations.list_weather_violations(directory)

    # Concatenate all violation lists (add endorsement_violations and inspection_violations if applicable)
    all_violations = weather_violations

    # Write the 2D list of violations to a CSV file if output is not None
    header = ['STUDENT', 'AIRPLANE', 'INSTRUCTOR', 'TAKEOFF', 'LANDING', 'FILED', 'AREA', 'REASON']
    if output is not None:
        
        utils.write_csv( [header] + all_violations,output)
    else:
        utils.write_csv( [header] + all_violations,'output.csv')


    # Print the number of violations found
    num_violations = len(all_violations)
    if num_violations == 0:
        print('No violations found.')
    else:
        if num_violations==1:
            print(f'{num_violations} violation found.')
        else:
            print(f'{num_violations} violations found.')




def execute(args):
    """
    Executes the application or prints an error message if executed incorrectly.
    
    The arguments to the application (EXCLUDING the application name) are provided to
    the list args. This list should contain either 1 or 2 elements.  If there is one
    element, it should be the name of the data set folder or the value '--test'.  If
    there are two elements, the first should be the data set folder and the second
    should be the name of a CSV file (for output of the results).
    
    If the user calls this script incorrectly (with the wrong number of arguments), this
    function prints:
    
        Usage: python auditor dataset [output.csv]
    
    This function does not do much error checking beyond counting the number of arguments.
    
    Parameter args: The command line arguments for the application (minus the application name)
    Precondition: args is a list of strings
    """
    # Implement thiunction
    
 
    if len(args) == 1:
        directory = args[0]
        if args[0]=='--test':
            tests.test_all()
        else:
            discover_violations(directory, None)
    elif len(args) == 2:
        directory = args[0]
        output_file = args[1]
        if args[1]=='--test' or args[0]=='--test':
            print("Usage: python auditor dataset [output.csv]")
 
        else:
            discover_violations(directory, output_file)
    else:
        print("Usage: python auditor dataset [output.csv]")

