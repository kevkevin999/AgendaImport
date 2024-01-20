# Library for reading data from an Excel Spreadsheet
import xlrd

# Objective of this file: 
# Reads data from the Excel spreadsheet (agenda.xls)
# and populates our database with the data 

# (From README)
# 1. Open an Agenda excel file
agenda = xlrd.open_workbook("agenda.xls")

# 2. Design a SQLite Database table schema allowing to store agenda information
# Table 1: All SESSIONs (each session will have an id, date, time start/end, title, location, description)
# Table 2: All SUBSESSIONs (each subsession will have same columns as SESSIONs, but also which SESSION the subsession is a child of)
# Table 3: Speakers (each speaker will be assosciated with a SESSION id - for sessions this is just the id, 
# but for subsessions, this will be the session id of the parent - and an optional subsession id field and a session/subsession distinction). 

# 3. Parse the content of the excel file and store the content in the table you designed
# While parsing the excel file, keep a running count of the number of sessions counted (id)
# Each subsession's parent id is equal to the above number
