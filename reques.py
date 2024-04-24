import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import json

statDict={'GK':{},'nGK':{}}
linkList=['https://fminside.net/players/5-fm-243/18026122-thibaut-courtois','https://fminside.net/players/5-fm-243/18004457-kevin-de-bruyne']
for link in linkList:
    requested=requests.get(link)
    requestedText=requested.text
    soup=BeautifulSoup(requestedText,'html.parser')
    statContainer=soup.select_one('div#player_stats')
    statHeaders=statContainer.select('div.column>h3')
    print(f"statHeader len == {len(statHeaders)}")
    statHeaders=[i.text for i in statHeaders]
    print(f"statHeader len == {len(statHeaders)}")
    statNames=statContainer.select('tbody>tr')
    statNames=[i.get('id') for i in statNames]
    if len(statHeaders)==4:
        statDict['GK'][statHeaders[0]]=statNames[:13]
        statDict['GK'][statHeaders[1]]=statNames[13:27]
        statDict['GK'][statHeaders[2]]=statNames[27:35]
        statDict['GK'][statHeaders[3]]=statNames[35:]
    else:
        statDict['nGK'][statHeaders[0]]=statNames[:13]
        statDict['nGK'][statHeaders[1]]=statNames[13:28]
        statDict['nGK'][statHeaders[2]]=statNames[28:]
print(soup.select_one('div#player_stats>div.column>table>tbody>tr').get('id'))
print('----------------------')
print(statDict['GK'])
print('----------------------')
print(statDict['nGK'])