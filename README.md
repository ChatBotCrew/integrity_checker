# Integrity Checker

This projet is a quality of life tooling for the data backend of
[wir-bleiben-liquide](https://github.com/ChatBotCrew/liquide-bleiben). 
It's purpose is to automate the checking of different aspects of
data qulity like:
- availability of links
- markdown formatting mistakes
- create a `xlsx` file with all fields

# Setup

The script can either be run as is or as a part of
docker container. For building the container a dockerfile
is provided. Build the docker container with 
`docker build -t <image-name> .`. The dockerized
script can be run with `docker run -e <list of environemental variables> <image-name> --name <container-name>`.
When running the script without docker make sure the follwing requirements
are met:
- [python3](https://realpython.com/installing-python/)
- [pip3](https://pip.pypa.io/en/stable/installing/) 
- necessary python packeges (install with `pip3 install -r <path to requirements.txt>`
Whe all requirement are met just run the `integrity_checker.py` script (make sure all envrionmental variables ar set).

## Configuration over environmental variables

### Necessary variables

| Key              | Description                                                        |
| ---              | -----------                                                        |
| API_TOKEN        | Basic Auth token for Codebeamer (Only token not basic auth string) |
| FROM_ADDR        | Email address of sending email account                             |
| FROM_ADDR_PW     | Password of email account                                          |
| SMTP_SERVER      | SMTP-Server of email account                                       |
| SMTP_SERVER_PORT | SMTP-Server port                                                   |
| RECIPIENTS       | Space seperated list                                               |

### Optional variables

| Key                  | Description                                            |
| ---                  | -----------                                            |
| DISABLE_TABLE        | Bool (as string)                                       |
| DISABLE_LINK_CHECKER | Bool (as string)                                       |
| DISABLE_WIKI_CHECKER | Bool (as string)                                       |
| MAX_TIMEOUT          | Number in seconds until http requests counts as failed |
