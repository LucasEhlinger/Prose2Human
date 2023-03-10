# Prose To Human
A python script that takes .ics calendar files as input, renames the events and makes the calendar available via a web server so that it can be synchronized with users' calendar applications.
This script works perfectly with Agiletime used by my company for some teams.

## Configuration
Use the file "config.json" to set how to rename events.

## Installation
1. Clone the repository

> git clone https://github.com/lucasehlinger/Prose2Human.git

2. Run the script using cron task

> 0 * * * * /usr/bin/python3 /path/to/Prose2Human/process.py >> /path/to/your>Logs>file.log 2>&1

3. Run the command to lunch the docker service

> docker-compose up -d

4. Access the calendar via the web server

> http://localhost:8080/calendar.ics

## How to use it
1. Put your .ics in ./toProcess and wait for processing.

2. Add to your devices the .ics this subscription :
> http(s)://<your ip or FQDN>/Calendar.ics

## Note
Make sure that python3 and docker are installed on your machine.


## ToDo
- Everything in docker, even cron execution or switch to a process.

## Contact
If you have any questions or issues, please contact me with this repo.


## License
Do whatever you want, I don't care !

Thank you for using Prose to Human!