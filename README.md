### INF601 - Advanced Programming in Python
### Rachel White
### Check In Bot
 
 
# Project Title
 
Practice Hub Check-in Bot
 
## Description
 Automated bot designed to interface with the class Practice Hub REST API. The bot will track instructor posts and submits replies on a structured timeframe.

## AI Usage
Hand-written components: project setup, core program structure, API configuration, environment variable usage, post filtering logic, check-in identification, and GitHub Actions workflow configuration.

AI-assisted components: exception handling for HTTP 423 responses, testing ideas, syntax checking, debugging, and reviewing code for spacing or formatting errors.

## Getting Started
 
### Dependencies
 
* Python 3.11+
* Packages listed in [requirements.txt](requirements.txt) (currently `requests>=2.31.0`)
 
### Installing
 
* Clone or download this repository
* Install the required packages:
```
pip install -r requirements.txt
```
 
### Executing program
 
The program can be run manually from a terminal after the required environment variables have been configured.

python checkinbot.py
 
## Help
 
If the program cannot connect to the Practice Hub, verify that the API URL and API token are configured correctly.

If the bot receives HTTP 423, the check-in window is closed. The program handles this response without terminating the entire collection process.

If a check-in has already been answered by the bot, the program skips it to prevent duplicate replies.
 
## Authors
Rachel White
 
## Version History
 
* 0.1
    * Initial Release
 
## License
 
 
## Acknowledgments
 
Inspiration, code snippets, etc.

