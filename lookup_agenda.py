#!/usr/bin/python

import sys
from db_table import db_table

# (from README)
# 1. Parse the command line arguments to retrieve the conditions that the sessions we are looking for must match.
# 2 inputs. 1st input must match: {date, time_start, time_end, title, location, description, speaker}, otherwise return an error
# 2nd input is a custom value
column_types = {'date', 'time_start', 'time_end', 'title', 'location', 'description', 'speaker'}

if (len(sys.argv) == 3):
    column = sys.argv[1].lower()
    input = sys.argv[2]
    print("%s : %s" % (column, input))
    if (column not in column_types):
        print('Argument 1 does not match an existing column')
        sys.exit()
    
else:
    print('Exactly 2 arguments expected')
    sys.exit()

# 2. Lookup the data you imported for the matching records
# Start by looking in the SESSIONS table. Are there any matches here?
    # if Yes, Save those rows! Then, look in SUBSESSIONs table, 
    # grab all rows that either match the search criteria or have the same parent_id of a selected session.
    # if No, proceed to look at SUBSESSIONS 
# Different approach for speaker. Grab all rows where speaker name matches. If a row is a 'Session', note the session_id. 
    # Then, go grab all subsessions with the saved session_ids

sessions = db_table("sessions", { 
    "id": "integer PRIMARY KEY", 
    "date": "date", 
    "time_start": "text", 
    "time_end": "text", 
    "title": "text", 
    "location": "text", 
    "description": "text"  
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
})

speakers = db_table("speaker", {   
    "name": "text", 
    "session" : "boolean", # true = session, false = subsession 
    "session_id" : "integer",
    "parent_id": "integer", # optional field 
})

# TODO use different approach for speakers
sessions.select(where={column : input})
# TODO from the above query, if a subsession has a parent_id that matches an id from the above query, also return that row

# 3. Print the result onto the screen