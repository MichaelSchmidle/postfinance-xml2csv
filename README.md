# PostFinance XML to CSV Converter

The script ``scripts/postfinance-xml2csv.py`` converts—as its name suggests—XML files provided by PostFinance to simple CSV files. Any XML file found in the subfolder ``xml`` will be converted into a CSV file in the subfolder ``csv``. The naming of the CSV files is intended to reflect its content (i.e. specify account and month).

For convenience, a [``docker-compose``](https://docs.docker.com/compose/) file is included to run the script in a suitable Python environment.
