# webscraping
Web scraping is to grab data from Web, and there are probably thousands of Web pages explaining how to do it in Python, however, it still took time for me to do what I wanted to do. In March I started consolidating COVID-19 stats from different resources into an Excel file to save historical records. Every day I went to a few Web sites to get stats for the WA state, so I could understand trends. So, I copied 4-5 numbers a day from a couple Web sited. Then I realized I need to get to the county level in prder to properly interpret the results, and I found just the site I've been looking for, however, the amount of numbers for me to copy just multiplied. Web sites, data and formats kept changing, and I created a few Python utils, which do a few things for me: 

1. Get a table from a web page as a dataframe - whether this is a regular page, or it is a JavaScript code (= Selenium)
2. Locate the data I need
3. Update an Excel file
4. Do other useful operations

I generalized all of those and want to share. 
(To be continued)
