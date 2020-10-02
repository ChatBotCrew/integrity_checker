#!/bin/python3

import requests
import re
from http import HTTPStatus
from requests.exceptions import ConnectTimeout, ReadTimeout
from urllib3.exceptions import InsecureRequestWarning


def check_url(url):
    try:
        status_code = requests.get(
            url,
            timeout=10,
            verify=False
        ).status_code

        return status_code
    except (ConnectTimeout, ReadTimeout):
        return 408


def find_all_links(text):
    regex = re.compile(
        r'\b(?:https?|http):' +
        r'[\w/#~:.?+=&%@!\-.:?\\-]+?' +
        r'(?=[.:?\-]*(?:[^\w/#~:.?+=&%@!\-.:?\-]|$))'
    )
    links = regex.findall(text)
    return links


def check_links(items):
    # This template contains all fields to be checked and
    # is not representative of all fields existing in a codebeamer tracker
    textFields = [
        'Programminformationen',
        'Antragsformular',
        'Kurzbeschreibung des Programms',
        'Konditionen',
        'Anlaufstelle',
        'Spezielle Informationen',
    ]
    findings = 0
    message = ""
    message += "############################################################\n"
    message += "# Starting link check.\n"
    message += "############################################################\n\n"
    # This prevents the script from spamming warnings when disabling SSL verification.
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    for name in sorted(items.keys()):
        item = items[name]
        nonExistingFields = []

        #print("[INFO]: Checking " + name + " ...")

        links = []
        for (index, field) in enumerate(textFields):
            # At this point we can't be sure if the field exists or not.
            # If that is not the case an exception will be triggered. This
            # exception will remove the entry of the non existing field from
            # `textFields` and since the operation failed no entry will be
            # made for links. After that every new list will be made on the bases
            # of these two lists, so no inconsistency should arise.
            try:
                foundLinks = find_all_links(item['fields'][field]['value'])
                links.append(foundLinks)
            except (KeyError):
                nonExistingFields.append(field)

        # remove non existing fields
        textFields = list(
            filter(lambda field: field not in nonExistingFields, textFields))

        # Status codes contains a list of lists, where every list
        # contains tuples of all links in one field-item and their
        # corresponding status codes.
        linkResponses = []
        for textLinks in links:
            statusCodeText = [check_url(url) for url in textLinks]
            unfilteredLinkResponses = zip(textLinks, statusCodeText)

            # remove succesfull codes
            linkResponses.append(
                list(filter(lambda response: str(response[1])[0] != '2', unfilteredLinkResponses)))


        for (index, linkResponsesText) in enumerate(linkResponses):
            # Check if list contains any failed url requests
            if not linkResponsesText:
                continue

            # Maybe factor this out into a class or named struct 
            # and make formatting part of the main function
            findings += 1

            message +="  {0} - TrackerID {1}:\n".format(name, item['id'])
            message +="  Tracker Field : " + textFields[index] + "\n"
            for link, statusCode in linkResponsesText:
                message += "  - URL         : " + link + "\n"
                message += "  - Error Type  : " + "{0} - {1}".format(statusCode, HTTPStatus(statusCode).phrase) + "\n"
            message += "\n" 

    if findings > 0:
        message += "############################################################\n"
        message += "# Finished Link Integrity Check\n"
        message += "# {0} of {1} URLs returned an error.\n".format(str(findings), len(items))
        message += "############################################################\n\n"
    else:
        message += "\n############################################################\n"
        message += "# None Of The Checks Failed\n"
        message += "############################################################\n"

    return (message)
