# Integrity Checker

This projet is quality of life tooling for the data backend of
[wir-bleiben-liquide](https://github.com/ChatBotCrew/liquide-bleiben). 
It's purpose is to automate the checking of different aspects of
data qulity like:
- availability of links
- markdown formatting mistakes
- missing fields
- create a `xlsx` file with all fields

# Setup

For this project to work to secrets need to be given:
1. An token for the codebeamer API (`./integrity_checker.py`, replace `<token>`)
3. Credentials for an email account (`./send_mail.py`)
Additionally one can enter a list of recipients in `./send_mail.py`
as well.

With no argument parsing implemented to enable or disable parts of
the program comment out the specific functions calls in the main
function of `./integrity_checker.py`.

## Requirements

To run this project you need to have [python3](https://realpython.com/installing-python/)
and [pip3](https://pip.pypa.io/en/stable/installing/) installed.
When these requirements are met you can install all
needed packages with `pip3 install -r <path to requirements.txt>`.

# Running it

When you have entered all necessary secrets [see Setup](#setup) you
can start the script from it's directory by invoking `python3 integrity_checker.py`.

# TODO
- program control over argument parsing
  - trackers of what status shall be checked 
  - what checks should be done
  - enable/disable email notifcation -  control over content and metadata
- proper logging
- project setup with poetry
- config or at least env file for secrets
