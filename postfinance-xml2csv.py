import os
import glob
import xml.etree.ElementTree as eTree
import re
from datetime import datetime
import csv

# Function to extract XML namespace from element
def namespace(element):
    namespace = re.match('\{(.*)\}', element.tag)
    return namespace.group(1) if namespace else ''

# Determin base directory of this script
baseDir = os.path.dirname(__file__) + '/'

# Create array of XML files to parse
xmlFiles = glob.glob(baseDir + 'xml/*.xml')

# Per XML file
for xmlFile in xmlFiles:

    # Parse XML file
    root = eTree.parse(xmlFile).getroot()

    # Set the namespace
    ns = {'Document': namespace(root)}

    # Define metadata
    iban = root.find('Document:BkToCstmrStmt/Document:Stmt/Document:Acct/Document:Id/Document:IBAN', ns).text
    owner = root.find('Document:BkToCstmrStmt/Document:Stmt/Document:Acct/Document:Ownr/Document:Nm', ns).text
    closingDate = root.findall('Document:BkToCstmrStmt/Document:Stmt/Document:Bal', ns)[1].find('Document:Dt/Document:Dt', ns).text

    # Generate corresponding CSV file with header row
    with open(baseDir + 'csv/' + iban + '-' + closingDate + '-' + os.path.basename(xmlFile) + '.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['IBAN', 'Owner', 'Amount', 'Currency', 'Date', 'Info', 'Reference'])
        transactions = root.findall('Document:BkToCstmrStmt/Document:Stmt/Document:Ntry', ns)
        for transaction in transactions:
            amount = float(transaction.find('Document:Amt', ns).text)
            if transaction.find('Document:CdtDbtInd', ns).text == 'DBIT':
                amount = amount * -1
            currency = transaction.find('Document:Amt', ns).get('Ccy')
            date = transaction.find('Document:BookgDt/Document:Dt', ns).text
            info = transaction.find('Document:AddtlNtryInf', ns).text
            reference = transaction.find('Document:AcctSvcrRef', ns).text

            # Write transaction row to CSV file
            writer.writerow([iban, owner, amount, currency, date, info, reference])        
