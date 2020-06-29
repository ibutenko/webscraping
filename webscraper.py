import os
import os.path
from os import path
import requests
import urllib.request
import time
import pandas as pd
import subprocess
from bs4 import BeautifulSoup
from datetime import date
import datetime
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl


class webscraper:
    """
    Web scraper utilities to extract table data from Web pages.
    """

    def getTableDF(url, table, extended = False, convert = True):
        """ Extract data from a table in a Web page, return a dataframe.
        url (string) - address of a Webpage.
        table (string) - class name of a table.
        extended (bool)- use Selenium, when pages require JS. Default is False.
        convert (bool) - convert values to int. Default is True.
        """
        page_source = ""

        if extended:
            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--incognito')
            options.add_argument('--headless')
            options.add_argument('log-level=3') # Valid values are from 0 to 3: INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3.
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            driver.get(url)
            time.sleep(2)
            page_source = driver.page_source
            driver.quit()
        else:
            response = requests.get(url)
            page_source = response.text
        
        soup = BeautifulSoup(page_source, "html.parser")

        htmltable = soup.find("table", attrs={"class": table})
        n_columns = 0
        n_rows=0
        column_names = []

        # Find number of rows and columns
        # we also find the column titles if we can
        for row in htmltable.find_all('tr'):    
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)

            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())

        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")

        columns = column_names if len(column_names) > 0 else range(0, n_columns)

        df = pd.DataFrame(columns = columns, index= range(0,n_rows))
        row_marker = 0
        for row in htmltable.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                # Note: using comma here is a bad practice from globalization perspective.
                df.iat[row_marker,column_marker] = column.get_text().strip('\n').strip().replace(',', '')
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
                
        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(int)  
            except ValueError:
                pass

        return df
                        
    def getTableValue(df, indexname, rowvalue, colname):
        """ Returns a value of a cell in a dataframe. Somewhat similar to LOOKUP in Excel.
        indexname (string) - index column name (to search for a value in).
        rowvalue (string) - what to search for.
        colname (string) - column name to return value from 
        """ 
        wa = df.loc[df[indexname] == rowvalue]
        res = wa[colname].to_string(header=False, index=False).split('\n')[0]
        return int(res)

    def archive(df, fname, compress = False):
        """ Store a timestamped copy of a dataframe as csv
        df (dataframe) - data to store.
        fname (string) - part of the filename, i.e. if fname = "test", file name will be 2020-05-01-test.csv 
        compress (bool) - whether to compress to .gz. Default = False
        """
        path = os.path.dirname(os.path.abspath(__file__))
        today = date.today().strftime("%Y-%m-%d")
        fn = ""
        fname = "-" + fname
        if compress:
            ext = 'csv.gz'
            fn = "{0}\\{1}{2}.{3}".format(path, today, fname, ext)
            # compression_opts = dict(method='zip', archive_name='out.csv')  
            df.to_csv(fn, index=False, compression="gzip")
        else:
            ext = 'csv'
            fn = "{0}\\{1}{2}.{3}".format(path, today, fname, ext)
            df.to_csv(fn.format('csv'), index=False)
        print("Archived to ", fn)

    def __init__(self, url, table):
        self.url, self.table = url, table
