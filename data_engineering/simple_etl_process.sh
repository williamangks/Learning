#!/bin/bash

# get the access log file
wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0250EN-SkillsNetwork/labs/Bash%20Scripting/ETL%20using%20shell%20scripting/web-server-access-log.txt.gz"
# unzip using gunzip the access log file
gunzip web-server-access-log.txt.gz

# Extract phase
echo "Extracting data"
# Extract the columns 1 (timestamp), 2(latitude), 3(longitude), 4(visitorid)
cut -d# -f1-4 web-server-access-log.txt > extracted-data.txt

# Transform phase
echo "Transforming data"
# read extracted data and replace the colons with commas
tr "#" "," < extracted-data.txt > transformed-data.csv

# Load phase
echo "Loading data"
# Send query instructions to connect to database template1 and copy the file to table access_log
echo "\c template1; \COPY access_log FROM '/home/project/transformed-data.csv' DELIMITERS ',' CSV HEADER;" | psql --username=postgres --host=localhost

# Verifying the data journey by querying the database.
echo "Verifying..."
# Send query instructions to look at the result in the database
echo '\c template1; \\SELECT * FROM access_log;' |psql --username=postgres --host=localhost

