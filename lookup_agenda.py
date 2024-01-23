#!/usr/bin/python

import sys
from db_table import db_table

column_types = {'date', 'time_start', 'time_end', 'title', 'location', 'description', 'speaker'}
# Read stdin and output error messages if necessary
if (len(sys.argv) == 3):
    column = sys.argv[1].lower()
    input = sys.argv[2].replace("'", "''")
    if (column not in column_types):
        print('Argument 1 does not match an existing column')
        sys.exit()
else:
    print('Exactly 2 arguments expected')
    sys.exit()

# Set up Database table schemas
sessions = db_table("sessions", { 
    "id": "integer PRIMARY KEY", 
    "date": "text", 
    "time_start": "text", 
    "time_end": "text", 
    "title": "text", 
    "location": "text", 
    "description": "text",
    "speaker" : "text"
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

values = [] # Build output with this list

# Handle the data differently depending on whether the column is speaker or not
if (column == 'speaker'):
    speakers_output = speakers.select(where={"name" : input})
    # For each speaker entry, search either the session or subsession table 
    # for the corresponding event details
    for row in speakers_output:
        if (row['session'] == 'True'):
            session_results = sessions.select(where={"id" : row["session_id"]})
            for result in session_results:
                result['session'] = 'Session'
                values.append(result)
        else:
            subsession_results = subsessions.select(where={"id" : row["session_id"]})
            for result in subsession_results:
                result['session'] = 'Subsession'
                values.append(result)
else:
    session_id_set = [] # Keep track of which sessions have already been selected
    subsession_id_set = [] 

    sessions_output = sessions.select(where={column : input})
    for row in sessions_output:
        row['session'] = 'Session'
        values.append(row)
        session_id_set.append(row['id'])

    subsession_output = subsessions.select(where={column : input})
    for row in subsession_output:
        row['session'] = 'Subsession'
        values.append(row)
        subsession_id_set.append(row['id'])

    # For each session, (if the subsession has yet to be outputted), output the subsession(s)
    for session_id in session_id_set:
        results = subsessions.select(where={"parent_id" : session_id})
        if results != []:
            for result in results:
                if (subsession_id_set.count(result['id']) == 0):
                    result['session'] = 'Subsession'
                    values.append(result)


# 3. Print the result onto the screen
if (values.count == 0):
    print('No Results Found')
for value in values:
    print("%s\t%s\t%s\t%s\t%s\t%s\t%s" % 
          (value['date'], value['time_start'], value['time_end'], 
           value['title'], value['location'], value['description'], value['session']))


sessions.close()
subsessions.close()
speakers.close()