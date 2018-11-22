Mentoring Stundenzettel
===================

This Python script checks timesheets created within the scope of the mentoring program conducted at FU Berlin for errors.


## Background
Mentors participating in the FU mentoring program have to write invoices. Each student must not work for more than a certain amount of time in a calendar week and a month. The present Python script automatizes the task of checking whether these criteria are fullfilled and creates an error file for each student.

## Installation and execution
Python 3.x is required. For an installation guide see: [Python Setup and Usage](https://docs.python.org/3/using/index.html)

Furthermore, you have to install [pandas](https://pandas.pydata.org/). For a tutorial on how to install packages in Python see: [Installing packages in Python](https://packaging.python.org/tutorials/installing-packages/)

## Procedure
### 1. Manual: Create a .csv file for each student
- Save the Excel files for each student as a .csv.
- Put all .csv files in the 'stundenzettel_csv' directory.

### 2. Run the Python script
Execute the Python script.

### 3. Manual: Check result files
Open the 'output' directory. The files created automatically for each student contain infos on whether the student worked more than the maximum amount of hours per week or month.

## In- and Output

### Input

#### CSV files generated from the Excel sheet

The files used as an input for the Python program have the following properties:

| Example | stundenzettel_csv/FUB_stundenzettel_Mustermann.csv |
|-----------------|-------------------|
| File format     | csv               |
| Content       | generated by saving the Excel form as .csv     |
| Separator  | ; |

### Output
#### Preprocessed files

| Example | preprocessing/studentData/Mustermann_Maximilian.csv|
|-----------------|-------------------------------|
| File name     | surname_firstname.csv                          |
| File format     | csv                           |
| First row       | column names (date;hours)                 |
| Following rows  | one row = date and the amount of hours worked |

#### Result files

| Example | output/Mustermann_Maximilian_result.csv|
|-----------------|-----|
| File format     | txt |
| Content    | Months and calendar weeks in which the max. number of hours worked was exceeded. |

## License
**Implementation:** Clarissa Elisabeth Staudt (TU Berlin & FU Berlin)

Distributed under GPLv3 License. See [LICENSE](license.md) for more information.