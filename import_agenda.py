#!/usr/bin/python

# For reading command line argments
import sys
# Library for reading data from an Excel Spreadsheet
import xlrd
from db_table import db_table

# Read stdin and handle stdin input arguments
if (len(sys.argv) > 1):
    try:  
        agenda = xlrd.open_workbook(sys.argv[1])
    except FileNotFoundError:
        print("Invalid File Input")
        sys.exit()
else:
    print('Exactly 1 argument expected')
    sys.exit()

# Set up SQLite Database table schemas
sessions = db_table("sessions", { 
    "id": "integer PRIMARY KEY", 
    "date": "text", 
    "time_start": "text", 
    "time_end": "text", 
    "title": "text", 
    "location": "text", 
    "description": "text",
    "speaker" : "text",
})

subsessions = db_table("subsessions", {
    "id": "integer PRIMARY KEY",
    "parent_id" : "integer", 
    "date": "text", 
    "time_start": "text",
    "time_end": "text",
    "title" : "text",
    "location" : "text",
    "description" : "text",  
    "speaker" : "text",
})

speakers = db_table("speaker", {   
    "name": "text", 
    "session" : "boolean", # true = session, false = subsession 
    "session_id" : "integer",
})


# Open the first sheet of the agenda (this file will only parse the first sheet)
sh = agenda.sheet_by_index(0)
session_id = -1 # Assume the first row is NOT a subsession
subsession_id = -1

# For each row starting from row 16
for row in range (15, sh.nrows):
    # Add data to the correct table
    if (sh.cell(row, 3).value.strip() == 'Session'):
        session_id = row
        sessions.insert({   
            "id" : str(row), 
            "date" : sh.cell(row, 0).value.strip(),
            "time_start" : sh.cell(row, 1).value.strip(),
            "time_end" : sh.cell(row, 2).value.strip(),
            "title" : "%s" % (sh.cell(row, 4).value.replace("'", "''").strip()),
            "location" : "%s" % (sh.cell(row, 5).value.replace("'", "''").strip()),
            "description" : "%s" % (sh.cell(row, 6).value.replace("'", "''").strip()),
            "speaker" : "%s" % (sh.cell(row, 7).value.replace("'", "''").strip()),        
            })
        # Handle Speakers table
        if (sh.cell(row, 7)):
            event_speakers = sh.cell(row, 7).value.split(';')
            for speaker in event_speakers:
                speakers.insert({
                    "name" : speaker.strip().replace("'", "''"),
                    "session" : True,
                    "session_id": session_id,
                })
    elif (sh.cell(row, 3).value.strip() == 'Sub'):
        subsession_id = row
        subsessions.insert({   
            "id" : str(subsession_id),
            "parent_id" : str(session_id), 
            "date" : sh.cell(row, 0).value.strip(),
            "time_start" : sh.cell(row, 1).value.strip(),
            "time_end" : sh.cell(row, 2).value.strip(),
            "title" : "%s" % (sh.cell(row, 4).value.replace("'", "''").strip()),
            "location" : "%s" % (sh.cell(row, 5).value.replace("'", "''").strip()),
            "description" : "%s" % (sh.cell(row, 6).value.replace("'", "''").strip()),
            "speaker" : "%s" % (sh.cell(row, 7).value.replace("'", "''").strip()), 
        })
        # Handle Speakers table
        if (sh.cell(row, 7)):
            event_speakers = sh.cell(row, 7).value.split(';')
            for speaker in event_speakers:
                speakers.insert({
                    "name" : speaker.strip().replace("'", "''"),
                    "session" : False,
                    "session_id": subsession_id,
                })
    else:
        print('Unable to determine whether the event is a SESSION or a SUBSESSION')

print('Done Importing Agenda!')

sessions.close()
subsessions.close()
speakers.close()

