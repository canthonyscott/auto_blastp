#! /bin/bash

# Create sqlite databse if it doesnt exist
/usr/bin/python3 /create_database.py

# load the provided data into the database
echo -e ".separator ","\n.import /data/data.csv antibodies" | sqlite3 /data/antibody.db

#/usr/bin/python3 /perform_blasts.py
