import os
import glob
import xml.etree.ElementTree as eTree
from datetime import datetime
import csv

# Create array of XML files to parse
xmlFiles = glob.glob('xml/*.xml')

# Per XML file
for xmlFile in xmlFiles:

    # Parse XML file
    root = eTree.parse(xmlFile).getroot()

    # Set the namespace, also defines the supported CAMT version
    namespace = {'Document': 'urn:iso:std:iso:20022:tech:xsd:camt.053.001.04'}

    # Define metadata
    iban = root.find('Document:BkToCstmrStmt/Document:Stmt/Document:Acct/Document:Id/Document:IBAN', namespace).text
    owner = root.find('Document:BkToCstmrStmt/Document:Stmt/Document:Acct/Document:Ownr/Document:Nm', namespace).text
    closingDate = datetime.strftime(datetime.strptime(root.find('Document:BkToCstmrStmt/Document:Stmt/Document:FrToDt/Document:ToDtTm', namespace).text, '%Y-%m-%dT%H:%M:%S'), '%Y-%m-%d')

    # Generate corresponding CSV file with header row
    with open('csv/' + iban + '-' + closingDate + '.csv', 'w', newline = '') as csvFile:
        writer = csv.writer(csvFile, delimiter = ";")
        writer.writerow(['IBAN', 'Owner', 'Amount', 'Currency', 'Date', 'Info', 'Reference'])
        transactions = root.findall('Document:BkToCstmrStmt/Document:Stmt/Document:Ntry', namespace)
        for transaction in transactions:
            amount = float(transaction.find('Document:Amt', namespace).text)
            if transaction.find('Document:CdtDbtInd', namespace).text == 'DBIT':
                amount = amount * -1
            currency = transaction.find('Document:Amt', namespace).get('Ccy')
            date = datetime.strftime(datetime.strptime(transaction.find('Document:BookgDt/Document:Dt', namespace).text, '%Y-%m-%d'), '%Y-%b-%d')
            info = transaction.find('Document:AddtlNtryInf', namespace).text
            reference = transaction.find('Document:AcctSvcrRef', namespace).text

            # Write transaction row to CSV file
            writer.writerow([iban, owner, amount, currency, date, info, reference])
