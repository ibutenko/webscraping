# webscraper
Web scraping is to grab data from Web, and there are probably thousands of Web pages explaining how to do it in Python, however, it still took time for me to do what I wanted to do. In March I started consolidating COVID-19 stats from different resources into an Excel file to save historical records. Every day I went to a few Web sites to get stats for the WA state, so I could understand trends. So, I copied 4-5 numbers a day from a couple Web sited. Then I realized I need to get to the county level in prder to properly interpret the results, and I found just the site I've been looking for, however, the amount of numbers for me to copy just multiplied. Web sites, data and formats kept changing, and I created a few Python utils, which do a few things for me: 

1. Get a table from a web page as a dataframe - whether this is a regular page, or it is a JavaScript code (= Selenium)
2. Locate the data I need
3. Update an Excel file
4. Do other useful operations

The class currently supports 3 use cases:

### 1. Load HTML directly and exteract table data by table name.
url = 'https://www.worldometers.info/coronavirus/country/us/'
table = "usa_table_countries"
ws = webscraper(url)
df = ws.getWebTable(table)

### 2. Load HTML via  Selenium, and then exteract table data by table name.  Works when pages require JS.
url = 'https://www.doh.wa.gov/Emergencies/Coronavirus'
table = "table-striped"
ws = webscraper(url)
df = ws.getWebTable(table, True)

### 3. Retrieve a CSV file from GitHub.
today = date.today().strftime("%m-%d-%Y")
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{0}.csv'.format(today)
ws = webscraper(url)
df = ws.getGitTable()

## Utility methods in the class:

def getTableValue(self, indexname, rowvalue, colname):
        """ Returns a value of a cell in a dataframe. Somewhat similar to LOOKUP in Excel.
        indexname (string) - index column name (to search for a value in).
        rowvalue (string) - what to search for.
        colname (string) - column name to return value from 
        """ 

def archive(self, fname, compress = False):
        """ Store a timestamped copy of a dataframe as csv
        df (dataframe) - data to store.
        fname (string) - part of the filename, i.e. if fname = "test", file name will be 2020-05-01-test.csv 
        compress (bool) - whether to compress to .gz. Default = False
        """
    

(To be continued)
