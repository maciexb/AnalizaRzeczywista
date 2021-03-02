import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys, getopt
import os
import numpy as np

os.chdir("D:\\Dokumenty\\SGH_3semestr\\PodstawyAproksymacji\\Projekt_Allegro")

try:
    opts, args = getopt.getopt(sys.argv[1:], "s:e:n:")
except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    sys.exit(2)

start = 2300000
end = 2300002
filename = 'ceneo.csv'

for opt in opts:
    if opt[0] == '-s':
        start = int(opt[1])
    if opt[0] == '-e':
        end = int(opt[1])
    if opt[0] == '-n':
        filename = opt[1]

tableList = []
df = pd.DataFrame(columns=['id','breadcrumbs', 'rec', 'text','score'])

print('Running scraper for products rangge:',start,end,'and saving to', filename)
for i in range(start,end):
    URL = 'https://www.ceneo.pl/' + str(i) + '#tab=reviews_scroll'
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, 'html.parser')
    print(i)

    
    reviews = soup.find_all('div',class_='user-post user-post__card js_product-review')
        
    if soup.find('div',class_='product-breadcrumb-2020') != None:
        breadcrumbs = soup.find('div',class_='product-breadcrumb-2020').text.replace('\n'," ").replace("  "," ").strip().replace('\r', '')
    else:
        continue

    for review in reviews:
        
        if review.find('span',class_='user-post__author-recomendation') == None:
            rec = 'Brak'
        else:
            rec = review.find('span',class_='user-post__author-recomendation').text.replace('\n'," ").replace("  "," ").strip().replace('\r', '')
        score = review.find('span',class_='user-post__score-count').text.replace('\n'," ").replace("  "," ").strip().replace('\r', '')
        rev = review.find('div','user-post__text').text.replace('\n'," ").replace("  "," ").strip().replace('\r', '')
        df = df.append({'id':i,'breadcrumbs':breadcrumbs,'rec':rec,'text':rev,'score':score}, ignore_index=True)
    if i % 100 == 0:            
        df.to_csv(filename,sep=';', encoding='utf_8_sig', mode='a', header=False)
        df = pd.DataFrame(columns=['id','breadcrumbs', 'rec', 'text','score'])
