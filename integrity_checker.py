#!/bin/python3
from link_checker import check_links
from wiki_text_checker import check_wiki_text
from table_generator import generate_table
from field_checker import check_fields
from send_mail import send_mail

from argparse import ArgumentParser
import requests
import json
import sys


max_timeout = 10
base_url = "https://liquidebleiben.codebeamer.com/api/v3"
request = "/trackers/2221/reports/3017/items?page=1&pageSize=500"
api_token = "Basic <token>"
headers = {'Authorization': api_token, 'Content-Type': 'application/json'}


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
    print("############################################################")
    print("# This program pulls all finder related data from the")
    print("# \"Wir bleiben liquide\" codebeamer instance and executes")
    print("# different checks on them. To make this work you have to")
    print("# provide this script with a valid api token.")
    print("#")
    print("# Enjoy :)")
    print("############################################################\n")

#   parser = ArgumentParser(
#       description="This is an cli tool to check different")

#   parser.add_argument(
#       'file_path',
#       type=Path,
#       metavar='file',
#       help='Path to the file to be checked'
#   )

    print("[INFO]: Sending request ...")
    answer = requests.get(base_url+request, headers=headers)

    if answer.status_code == 200:
        print("[INFO]: Request successfull...")
    else:
        print("[ERR]: Request failed! Received {0} status code from codebeamer".format(answer.status_code))
        sys.exit(1)

    content = json.loads(answer.content)
    items = parse_items_to_named_dict(content['items'])

    generate_table(items)

    message = ""
    message += check_links(items) +\
        check_wiki_text(items) +\
        check_fields(items)

    send_mail(message)
if __name__ == "__main__":
    main()
