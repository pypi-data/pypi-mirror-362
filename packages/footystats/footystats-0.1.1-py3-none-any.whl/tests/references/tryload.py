import json, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests

rooturl:str = "https://www.worldfootball.net"

def getFixtures(url:str)->dict:
    """
    prerequisites: get a team url, obtain the url to fixtures
    fetch fixtures stored in a table
    returns a dict with follow. keys->round date opponnent venue score
    :param url: url team fixtures
    :type url: str
    :return: parsed JSON data 
        {round - date - hour - venue - opponent - score}
    :rtype:dict
    :raises RuntimeError: If the request fails
    :raises ValueError: if a returned list of json dict is empty
    or lists in dict do not have the same size 
    """
    try:
        my_requests=requests.get(url)
        my_requests.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e}") from e
    #
    data = {"round":[],"date":[],"hour":[],"venue":[],"opponent":[],"score":[]}
    html_page=my_requests.content.decode('utf-8')
    soup = BeautifulSoup(html_page, "html.parser")
    
    table = soup.find('table', class_='standard_tabelle')
    # =========================================================================
    # 1. Know how many data columns in table
    # =========================================================================
    nb_column:int = 0
    if table:
        for tr in table.find_all('tr'):
            if tr:
                for th in tr.find_all('th'):
                    if th:
                        if th.get('colspan')!=None:
                            nb_column += int(th.get('colspan'))
                        else:
                            nb_column+= 1
                if nb_column!=0:
                    break
    # =========================================================================
    # 2. parse / store data from table
    # =========================================================================
        for tr in table.find_all('tr'):
            if tr:
                if tr.find('td'):
                    tds = tr.find_all('td')
                    if len(tds)>1:
                        round_      = tds[0].get_text().lower()
                        date        = tds[1].get_text().lower()
                        hour        = tds[2].get_text().lower()
                        venue       = tds[3].get_text().lower()
                        opponent    = tds[5].find('a')['href'].split('/')[2]
                        score       = tds[6].get_text().lower()
                        #
                        data["round"].append(round_)
                        data["date"].append(date)
                        data["hour"].append(hour)
                        data["venue"].append(venue)
                        data["opponent"].append(opponent)
                        data["score"].append(score.strip())
    #
    sizes = [len(data[k]) for k in data.keys()]
    if 0 in sizes:
        raise ValueError("Expected a non-empty list")
    if len(set(sizes))>1:
        raise ValueError("Some lists do not have the same size")
    return data

p = r"D:\FOOTBALL\project_root\tests\references\webscrapping\getfixtures"

l = [os.path.join(p,x) for x in os.listdir(p)]
with open(l[0],'r') as f:
    c=f.readlines()
f.close()

data={"url":[], "reference":[]}
for pa in c:
    stuff = getFixtures(pa)
    data["url"].append(pa)
    data["reference"].append(stuff)

sp=os.path.join(p,'references.json')
with open(sp,'w') as f:
    json.dump(data,f)
f.close()