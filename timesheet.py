import pandas as pd
import sys
import glob


# maximal amount of hours allowed in a month
max_hours_per_month = 2

# maximal amount of hours allowed in a calendar week
max_hours_per_week = 1


"""
Preprocess time sheets and extract all necessary information.
"""
def preprocessing():
    
    # get all timesheets
    timesheet_files = glob.glob("stundenzettel_csv/*.csv")
    
    for file in timesheet_files:
        preprocessed = "date;hours\n"
        try:
            with open(file, "r") as f:
                count = 0
                continue_lines = True
                name = file[18:]
                for line in f:
                    if "Summe der Einsatzzeiten" in line:
                        continue_lines = False
                    # extract student name
                    if count == 7:
                        name = extract_student_name(line)
                    # extract hours worked
                    if (count >= 14) and continue_lines:
                        l = str.split(line, ";")
                        if (len(l[1]) == 0) or (l[4] == "00:00:00"):
                            continue;
                        else:
                            new_string =  l[1] + ";" + l[4] + "\n"
                            preprocessed += new_string
                    count += 1
                
                path = "input/studentData/" + name + ".csv"
                write_to_file(path, preprocessed)
            
        except: 
            print("Error: Could not preprocess data.")
            sys.exit(1)


"""
Extract student name from line.
"""
def extract_student_name(line):
    
    l = str.split(line, ";")
    
    surname = l[1]
    # remove all whitespace characters
    surname = ''.join(surname.split())
    
    firstname = l[5]
    # remove all whitespace characters
    firstname = ''.join(firstname.split())
    
    return surname + "_" + firstname


"""
Calculate weekly sum of hours worked.
"""
def work_weekly(student, kw, kws):
    stud = student["date"].tolist()
    days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    for index, row in kw.iterrows():
        for day in days:
            # check if the current date is a date on which the student worked
            worked = [row[day] == s for s in stud]
            if any(worked):
                e = student.loc[student['date'] == row[day]]
                cal_week = row["Kalenderwoche"] + " " + str(row["Jahr"])
                datelist = e["hours"].tolist()
                minutes = int(datelist[0][-2:])/60
                hours = float(datelist[0][:-3]) + minutes
                # add worked hours to the calenderweek
                if cal_week in kws:
                    kws[cal_week] += float(hours)
                else:
                    kws[cal_week] = float(hours)
    return kws


"""
Calculate monthly sum of hours worked.
"""
def work_monthly(student):
    
    work_per_month = {}
    for index, row in student.iterrows():
        
        # extract month + year
        month = row["date"][3:5]
        year = row["date"][6:10]
        
        # extract hours worked
        minutes = int(str(row["hours"])[-2:])/60
        hours = int(str(row["hours"])[:-3]) + minutes
        
        # count all hours for a month
        if month+year in work_per_month:
            work_per_month[month + year] += hours
        else: 
            work_per_month[month + year] = hours
            
    return work_per_month


"""
Check whether the maximal amount of hours was exceeded for any calendar week.
"""
def max_hours_weekly(student, kw, errors):
    worked_weekly = dict()
    worked_weekly = work_weekly(student, kw, worked_weekly)
    
    error_max_hours_per_week = ""
    
    err_weeks = [el for el in worked_weekly if worked_weekly[el] > max_hours_per_week]
    error_max_hours_per_week = str.join("\n", err_weeks)
    
    errors += "Worked more than " + str(max_hours_per_week) + " hours in the following weeks:\n" + error_max_hours_per_week
    
    return errors


"""
Check whether the maximal amount of hours was exceeded for any month.
"""
def max_hours_monthly(student, errors):
    
    # calculates the sum for the worked hours in each month
    work_per_month = work_monthly(student)
    
    error_max_hours_per_month = ""
    
    for el in work_per_month:
        if work_per_month[el] > max_hours_per_month:
            el = el[:2] + "." + el[2:] + "\n"
            error_max_hours_per_month += el
       
    errors += "Worked more than " + str(max_hours_per_month) + " hours in the following months:\n" + error_max_hours_per_month
        
    return errors


"""
Write a given content to a new file.
"""
def write_to_file(path, content):
    try:
        with open(path, "w") as f:
            f.write(content)
    except:
        print("Error: Could not write the results to {}.".format(path))
        sys.exit(1)


def main():
    
    print("1) Data preprocessing")
    preprocessing()
    
    print("2) Calculating results")
    print("- Reading input files from input directory...")
    
    # read in calendar weeks
    kw = pd.read_csv('input/KW.csv', sep=";")

    # read in student data
    stud_path = "input/studentData/*.csv"
    txt_files = glob.glob(stud_path)
    
    print("  Found {} files in {} directory.".format(len(txt_files), stud_path[:-6]))
    print("- Processing...")
    
    for file in txt_files:
        student = pd.read_csv(file, sep=';', encoding='iso-8859-1')
        
        # check whether a student exceeded the max. amount of hours per month or calender week
        errors = ""
        errors = max_hours_monthly(student, errors)
        errors = max_hours_weekly(student, kw, errors)
        
        # write all errors to output file
        output_path = "output/" + file[18:-4] + "_result.txt"
        write_to_file(output_path, errors)
        
    print("\nDone! Results were written to the output directory.")


main()