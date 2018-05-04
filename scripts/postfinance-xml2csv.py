import glob
import xml.etree.ElementTree as eTree
import csv

# Create array of XML files to parse
xmlFiles = glob.glob('/usr/src/postfinance-xml2csv/xml2csv/*.xml')

# Define namespace
namespace = {
    'Document': 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.04'
}

# Per XML file
for xmlFile in xmlFiles:

    # Generate corresponding CSV file with header row
    with open(xmlFile + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['Amount', 'Currency', 'Date', 'Info', 'Reference'])

        # Parse XML file
        root = eTree.parse(xmlFile).getroot()
        transactions = root.findall('Document:BkToCstmrStmt/Document:Stmt/Document:Ntry', namespace)
        for transaction in transactions:
            amount = float(transaction.find('Document:Amt', namespace).text)
            if transaction.find('Document:CdtDbtInd', namespace).text == 'DBIT':
                amount = amount * -1
            currency = transaction.find('Document:Amt', namespace).get('Ccy')
            date = transaction.find('Document:BookgDt/Document:Dt', namespace).text
            info = transaction.find('Document:AddtlNtryInf', namespace).text
            reference = transaction.find('Document:AcctSvcrRef', namespace).text

            # Write transaction row to CSV file
            writer.writerow([amount, currency, date, info, reference])
        
