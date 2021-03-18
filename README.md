# pythonlogscan

Problem Statement
1.	Create a script (whatever scripting language is preferred) to scrape logs for given events. The events will be provided in a text/json file. The events format would look like :
•	[timestamp] [log_level] [thread] This is a data event showing [ID]
•	[timestamp] [log_level] [thread] This is an error event for client [$CLIENT ID] 
Where [] mark the fields in the log, the value for which is to be collected and sent to ELK stack , a data event needs to go to an index named “data” and an error event needs to go to an index “error”
[$] marks protected fields for which the value is to be masked before sending to the ELK stack. 
You are free to change the format to suit your script, though make sure to clearly state the assumptions made and things supported as part of your scraper.

Definition of Done:
•	The script with a proper readme file. 
•	If a hosted ELK could be used to show the data then good, else only printing a valid payload for ELK in a text file or a json dump for ELK would suffice. 

2.	Come up with a valid trigger for the script. 

Definition of Done:
	The detailed description behind choosing the trigger which should include the following:
1.	Implementation feasibility
2.	Performance considerations 
3.	Maximum Data lag between an event occurrence and reporting 



**scanlogs.py**

_Features_
- This is real time log scanner, which parses and process the logs.
- When pattern is matched, Payload is generated for ELK
- When log rotation happens, new log file is read from the begining
- In case log file is not updated and has all the lines processed, program sleeps for a second
- Logs are processed almost on real time basis
- Program itself is using multiprocessing to handle all the files in given folder paralely

_How to Use_
- program does not dependent on any special libraries , default modules like datetime, time, glob, os , sys are used
- program can be run by passing file to python interpreter 

python scanlogs.py 

**dummyLogGenerator**

_Features_
- This program generates random logs and appends to all the log files in given folder
- Log rotation has also been implemented to simulate real world situation
- Program is using multiprocessing to update all the logs in parallel

_How to Use_
- program does not dependent on any special libraries , default modules like datetime, time, glob, os , sys are used
- program can be run by passing file to python interpreter 

python dummyLogGenerator.py 
