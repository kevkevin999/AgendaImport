#!/usr/bin/python

# For reading command line argments
import sys
# Library for reading data from an Excel Spreadsheet
import xlrd


# Objective of this file: 
# Reads data from the Excel spreadsheet (agenda.xls)
# and populates our database with the data 

# (From README)
# 1. Open an Agenda excel file
if (len(sys.argv) > 1):
    agenda = xlrd.open_workbook(sys.argv[1])
    print('Worksheet opened!')
else:
    print('Minimum 1 argement expected')
    sys.exit()


# 2. Design a SQLite Database table schema allowing to store agenda information
# Table 1: All SESSIONs (each session will have an id, date, time start/end, title, location, description)
# Table 2: All SUBSESSIONs (each subsession will have same columns as SESSIONs, but also which SESSION the subsession is a child of)
# Table 3: Speakers (each speaker will be assosciated with a SESSION id - for sessions this is just the id, 
# but for subsessions, this will be the session id of the parent - and an optional subsession id field and a session/subsession distinction). 

# from db_table import db_table
# users = db_table("session", {   "id": "integer PRIMARY KEY", 
#                                 "date" : "date", 
#                                 "time_start" : "text",
#                                 "time_end" : "text",
#                                 "title" : "text",
#                                 "location" : "text",
#                                 "description" : "text",  })

# users = db_table("subsession", {"id": "integer PRIMARY KEY",
#                                 "parent_id" : "integer", 
#                                 "date": "date", 
#                                 "time_start": "text",
#                                 "time_end": "text",
#                                 "title" : "text",
#                                 "location" : "text",
#                                 "description" : "text",  })

# users = db_table("speaker", {   "name": "text", 
#                                 "session" : "boolean", # true = session, false = subsession 
#                                 "session_id" : "integer",
#                                 "parent_id": "integer", # optional field 
#                                 })

# 3. Parse the content of the excel file and store the content in the table you designed
# While parsing the excel file, keep a running count of the number of sessions counted (id)
# Each subsession's parent id is equal to the above number

# Open the 'Agenda' sheet
sh = agenda.sheet_by_index(0)
for row in range (14, sh.nrows):
    values = []
    for col in range (sh.ncols): 
        values.append(sh.cell(row, col).value)
    print (','.join(values))
print

