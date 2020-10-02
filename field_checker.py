#!/bin/python3

def check_fields(items):

    # These are all fields served by the api and
    # not necessarly all fields existing in a tracker
    templateFields = [
        'Anlaufstelle',
        'Antragsformular',
        'Ausgeschlossene Branche(n)',
        'Bundesland',
        'Bürgschaftssumme',
        'Bürgschaftssumme MAX',
        'Bürgschaftssumme MIN',
        'De Minimis relevant?',
        'Förderung',
        'Förderung MAX',
        'Förderung MIN',
        'Förderung gilt nur für Sitz?',
        'Förderungsart',
        'Förderungsnehmer',
        'Jahresbilanzsumme',
        'Jahresbilanzsumme MAX',
        'Konditionen',
        'Kurzbeschreibung des Programms',
        'Laufzeit',
        'Laufzeit MAX',
        'Laufzeit MIN',
        'Legacy ID',
        'Mitarbeiter (Vollzeitäquivalent)',
        'Mitarbeiter MAX',
        'Mitarbeiter MIN',
        'Nur für Kapitalgesellschaften',
        'Programminformationen',
        'Rechtsform',
        'Spezielle Voraussetzungen',
        'Tilgungsfreier Zeitraum',
        'Umsatz',
        'Umsatz MAX',
        'Umsatz MIN',
        'Unternehmensalter',
        'Unternehmensalter MAX',
        'Unternehmensalter MIN',
        'Verantwortliche Institution',
        'Zusätzliche Informationen'
    ]

    missingFieldsCount = { field: 0 for field in templateFields}
    message = ""
    message += "\n############################################################\n"
    message += "# Starting Tracker Field Completeness Check\n" 
    message += "############################################################\n\n"

    result = {}
    for name in items:
        item = items[name]
        missingFields = templateFields - item['fields'].keys()

        for field in missingFields:
            missingFieldsCount[field] += 1
        
        if missingFields:
            result[name] = missingFields

    itemCounter = len(result)
    fieldCounter = 0
    for name in sorted(result.keys()):
        fieldCounter += len(result[name]) 
        message += "  {0} - TrackerID {1} misses the following fields:\n".format(name, items[name]['id'])
        for field in result[name]:
            message += "    - " + field + "\n"

    message += "\n"
    message += "############################################################\n"
    message += "# {0} Fields In {1} Items Were Found Missing\n".format(fieldCounter , itemCounter)
    message += "############################################################\n\n"


    if itemCounter in missingFieldsCount.values():
        message += "############################################################\n"
        message += "# Fields Missing In Every Item\n"
        message += "############################################################\n\n"
        for field in sorted(missingFieldsCount.keys()):
            if missingFieldsCount[field] == itemCounter:
                message += "  " + field + "\n"
    else:
        message += "############################################################\n"
        message += "  No Fields Found That Were Missing In All Items\n"
        message += "############################################################\n\n"

    return message