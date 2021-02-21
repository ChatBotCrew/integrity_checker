#!/bin/python3
import xlsxwriter

fileName = "table.xlsx"
def generate_table(items):
    tableFields = [
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

    print("[INFO]: Starting table generation ...") 

    workBook = xlsxwriter.Workbook(fileName)
    sheet = workBook.add_worksheet()
    sheet.set_column(0,0, 5)
    for i in range(1, len(tableFields)):
        sheet.set_column(i, i, 50)

    # sheet.set_column(1,1, 40)
    # sheet.set_column(2,2, 50)
    # sheet.set_column(3,4, 30)
    text = workBook.add_format({'text_wrap': True})
    
    # Set Table header
    sheet.write(0,0, "ID")
    sheet.write(0,1, "Programmname")

    for i in range(len(tableFields)):
        sheet.write(0,i+2, tableFields[i])

    for row, name in enumerate(items):
        # increment row because header row has already been written
        #print("[INFO]: Generating {0} entry".format(name))
        row += 1
        item = items[name]
        sheet.write(row, 0, items[name]['id'])
        sheet.write(row, 1, name)

        for col, field in enumerate(tableFields):
            # increment column because name column has already been written
            col += 2
            try:
                sheet.write(row, col, item['fields'][field]['value'], text)
            except (KeyError):
                sheet.write(row, col, "No entry in item", text)

    workBook.close()

    print("[INFO]: Finished table generation ...")
