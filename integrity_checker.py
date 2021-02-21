#!/bin/python3
from link_checker import check_links
from wiki_text_checker import check_wiki_text
from table_generator import generate_table
from send_mail import send_mail

import requests
import json
import os
import sys

# Get environamental values needed for operation
try:
    API_TOKEN = 'Basic ' + os.environ["API_TOKEN"]
    print(API_TOKEN)
except KeyError:
    print("[ERR]: API_TOKEN not provided as environmental variable. Exiting ...")
    sys.exit(1)

try:
    # This value disables the generation of the table
    # as well as seding it via email
    TABLE_DISABLED = os.environ["DISABLE_TABLE"].lower()
except KeyError:
    print("[INFO] DISABLE_TABLE not provided as environmental variable. Setting default: False")
    TABLE_DISABLED = "False"

try:
    LINK_CHECKER_DISABLED = os.environ["DISABLE_LINK_CHECKER"].lower()
except KeyError:
    print("[INFO] DISABLE_LINK_CHECKER not provided as environmental variable. Setting default: False")
    LINK_CHECKER_DISABLED = "False"

try:
    WIKI_CHECKER_DISABLED = os.environ["DISABLE_WIKI_CHECKER"].lower()
except KeyError:
    print("[INFO] DISABLE_WIKI_CHECKER not provided as environmental variable. Setting default: False")
    WIKI_CHECKER_DISABLED = "False"

print(TABLE_DISABLED)
print(LINK_CHECKER_DISABLED)
print(WIKI_CHECKER_DISABLED)

print()

base_url = "https://liquidebleiben.codebeamer.com/api/v3"
request = "/trackers/2221/reports/3017/items?page=1&pageSize=500"
headers = {'Authorization': API_TOKEN, 'Content-Type': 'application/json'}


def parse_items_to_named_dict(content):
    print("[INFO]: Parsing json data ...")
    items = {}
    for i in content:
        item = i['item']

        fields = {}
        for field in item['customFields']:
            name = field['name']
            del field['name']
            fields[name] = field

        items[item['name']] = {
            'id': item['id'],
            'fields': fields
        }
    # print("[INFO]: Parsing successfull ...")
    return items

def main():
    print("[INFO]: ############################################################")
    print("[INFO]: # Starting integirty checker")
    print("[INFO]: ############################################################\n")

    print("[INFO]: Sending request ...")
    answer = requests.get(base_url+request, headers=headers)

    if answer.status_code == 200:
        print("[INFO]: Request successfull...")
    else:
        print("[ERR]: Request failed! Received {0} status code from codebeamer".format(answer.status_code))
        sys.exit(1)

    content = json.loads(answer.content)
    items = parse_items_to_named_dict(content['items'])

    if TABLE_DISABLED == 'true':
        print("[INFO]: Skipping table generation ...")
    else:
        generate_table(items)

    message = ""
    if LINK_CHECKER_DISABLED == 'true':
        print("[INFO]: Skipping link checker ...")
    else:
        message += check_links(items)

    if WIKI_CHECKER_DISABLED == 'true':
        print("[INFO]: Skipping wiki checker ...")
    else:
        message += check_wiki_text(items)

    print("[INFO]: Displaying message to be send ...")
    print(message)
    print("[INFO]: End of message ...")

    send_mail(TABLE_DISABLED, message)

    print("[INFO]: ############################################################")
    print("[INFO]: # Integirty checker finished")
    print("[INFO]: ############################################################\n")

if __name__ == "__main__":
    main()
