#!/bin/python3
import re

    

def check_wiki_text(items):
    wikiTextFields = [
        'Spezielle Voraussetzungen',
        'Kurzbeschreibung des Programms',
        'Zusätzliche Informationen'
    ]
    checks = {
        'False List Syntax': r'^~- .*',
    }

    message = ""
    message += "############################################################\n"
    message += "# Starting syntax check for Wiki entries\n"
    message += "############################################################\n\n"

    print("Generating rules ...")
    # turn definitions into regex parsers\
    checks = {check: re.compile(checks[check], re.MULTILINE) for check in checks}

    # Definition necessary to create nested dict
    # entries on the fly
    findings = {"":{"":[""]}}
    for name in items:
        item = items[name]
        for field in wikiTextFields:
            for check in checks.keys():
                raw_finding = []
                try:
                    raw_finding = checks[check].findall(item['fields'][field]['value'])
                except (KeyError):
                    # No action required, since checking for missing fields is done
                    # by other
                    ()
                if raw_finding:
                    try:
                        findings[name][field].append(check)
                    except (KeyError):
                        findings[name] = {field:[check]}

    # Remove initialization entry to be
    # able to make correct emptyness check
    del findings[""]

    if findings:
        findingCount = 0
        itemCount = 0

        for item in sorted(findings.keys()):
            message += "  {0} - ID {1}:\n".format(item, items[item]['id'])
            itemCount += 1
            for field in findings[item]:
                message += "    " + field + ":\n"
                if findings[item][field]:
                    message += "    - Failed checks: \n"
                    for check in findings[item][field]:
                        message += ("      - " + check + "\n")
                        findingCount +=1
        
        message += "\n"

        message += "############################################################\n"
        message += "# Finished Syntax Check\n"
        message += "# {0} Of {1} Items {2} Checks Failed: \n".format(itemCount, len(items), findingCount)
        message += "############################################################\n\n"
    else:
        message +="############################################################"
        message +="# No failed checks"
        message +="############################################################\n\n"

    return message