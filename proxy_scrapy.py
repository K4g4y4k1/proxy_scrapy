import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import datetime as dt
 
def proxy_scrapper(URL):
    # Making a GET request from website store in list URL in slot 1 which is the proper url
    r = requests.get(URL[1])

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    # Extract the columns tiltles
    s = soup.find('table', class_="table table-striped table-bordered")
    content = s.find_all('th')
    columns=[col.text for col in content]

    # Extract the table content
    s1 = soup.find('table', class_="table table-striped table-bordered")
    content1 = s1.find_all('tbody')[0].findAll('td')  
    data = np.array([ind.text for ind in content1])

    # Calculating Row and Columns length for Matrix reshape
    rows = int(len(data)/len(columns))
    col_len= len(columns)
    shape = (rows,col_len)

    # Reshaping Data to fit in DataFrame
    data_res= data.reshape(shape)

    # Populating DataFrame with extracted Data
    db = pd.DataFrame(data_res, columns=columns)

    # Avoiding using Russian Proxies
    db = db[~db['Country'].str.contains('Russian')].reset_index().drop('index', axis=1)
    
    # Removing Transparent Proxies from the list
    db = db[~db['Anonymity'].str.contains('transparent')].reset_index().drop('index', axis=1)   
    
    #Export DataFrame in CSV file using URL list slot 0 which is the url title
    #line commented out to provide the possibility to have and export with the today's date and hour of exportation
    #db.to_csv(URL[0]+' '+ str(dt.datetime.today()).split('.')[0].replace(':','_') +'.csv')
    db.to_csv(URL[0]+'.csv')
    
    return db

# Main function that calls for the scrapper depending on user choice
def main():
    URL1 = ['HTTP_Proxy','https://free-proxy-list.net/']
    URL2 = ['Socks Proxy','https://www.socks-proxy.net/']
    """
    choice = input("Please choose between:\n - HTTP proxy (1) \n - Socks proxy (2) \n")
    if choice == "1":
        #db1 = proxy_scrapper(URL1)
        print("HTTP Proxies exported")
        return proxy_scrapper(URL1)
    elif choice == "2": 
        #db2 = proxy_scrapper(URL2),
        print("SOCKS Proxies exported")
        return proxy_scrapper(URL2)
    else:
        print('Please choose 1 or 2')
    """
    proxy_scrapper(URL1)
    print("HTTP Proxies exported")
    proxy_scrapper(URL2)
    print("SOCKS Proxies exported")
    
        
#Automatic Main function launcher        
if __name__ == "__main__": main()
