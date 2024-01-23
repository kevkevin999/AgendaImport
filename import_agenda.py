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
    # TODO handle incorrect argument values
    agenda = xlrd.open_workbook(sys.argv[1])
else:
    print('Minimum 1 argement expected')
    sys.exit()

# 2. Design a SQLite Database table schema allowing to store agenda information
# Table 1: All SESSIONs (each session will have an id, date, time start/end, title, location, description)
# Table 2: All SUBSESSIONs (each subsession will have same columns as SESSIONs, but also which SESSION the subsession is a child of)
# Table 3: Speakers (each speaker will be assosciated with a SESSION id - for sessions this is just the id, 
# but for subsessions, this will be the session id of the parent - and an optional subsession id field and a session/subsession distinction). 

from db_table import db_table
sessions = db_table("sessions", { 
    "id": "integer PRIMARY KEY", 
    "date": "date", 
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
    "date": "date", 
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


# 3. Parse the content of the excel file and store the content in the table you designed
# While parsing the excel file, keep a running count of the number of sessions counted (id)
# Each subsession's parent id is equal to the above number

# Open the 'Agenda' sheet
sh = agenda.sheet_by_index(0)
session_id = -1 # Assume the first row is NOT a subsession
subsession_id = -1
currently_session = False

# For each row starting from row 16
for row in range (15, sh.nrows):
    # Add data to the correct table
    if (sh.cell(row, 3).value.strip() == 'Session'):
        session_id = row
        currently_session = True
        sessions.insert({   
            "id" : str(row), 
            "date" : sh.cell(row, 0).value,
            "time_start" : sh.cell(row, 1).value,
            "time_end" : sh.cell(row, 2).value,
            "title" : "%s" % (sh.cell(row, 4).value.replace("'", "''")),
            "location" : "%s" % (sh.cell(row, 5).value.replace("'", "''")),
            "description" : "%s" % (sh.cell(row, 6).value.replace("'", "''")),
            "speaker" : "%s" % (sh.cell(row, 7).value.replace("'", "''")),        
            })
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
        currently_session = False
        subsessions.insert({   
            "id" : str(subsession_id),
            "parent_id" : str(session_id), 
            "date" : sh.cell(row, 0).value,
            "time_start" : sh.cell(row, 1).value,
            "time_end" : sh.cell(row, 2).value,
            "title" : "%s" % (sh.cell(row, 4).value.replace("'", "''")),
            "location" : "%s" % (sh.cell(row, 5).value.replace("'", "''")),
            "description" : "%s" % (sh.cell(row, 6).value.replace("'", "''")),
            "speaker" : "%s" % (sh.cell(row, 7).value.replace("'", "''")), 
        })
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
    
    # Add data to the speakers table (if the speaker cell is not empty)
    if (sh.cell(row, 7)):
        event_speakers = sh.cell(row, 7).value.split(';')
        for speaker in event_speakers:
            if (speaker.strip() != ""):
                print(speaker)
                speakers.insert({
                    "name" : speaker.strip().replace("'", "''"),
                    "session" : currently_session,
                    "session_id": session_id if currently_session else subsession_id ,
                })

sessions.close()
subsessions.close()
speakers.close()

