import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
 
# Making a GET request
r = requests.get('https://free-proxy-list.net/')
 
# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
 
s = soup.find('table', class_="table table-striped table-bordered")
content = s.find_all('th')
columns=[col.text for col in content]


s1 = soup.find('table', class_="table table-striped table-bordered")
content1 = s1.find_all('tbody')[0].findAll('td')
  
data = np.array([ind.text for ind in content1])
rows = int(len(data)/len(columns))
col_len= len(columns)

shape = (rows,col_len)

data_res= data.reshape(shape)

db = pd.DataFrame(data_res, columns=columns)

db.to_csv('proxy_list.csv')
