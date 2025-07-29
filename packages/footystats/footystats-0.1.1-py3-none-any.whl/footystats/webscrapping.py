from footystats.leagues import leagues
from footystats.leagues import teams_to_exclude
from footystats.utils import sortURLbyDate, verifyRoundWithRightSeason
from footystats.utils import incrementDate
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

rooturl:str = "https://www.worldfootball.net"

def valid_url(url:str)->bool:
    """
    this function is used in getURLfromForm
    It checks if a url contains a forbidden keyword
    This elimintates non-standard seasons
    Sometimes, some seasons have playoff, relegation matches, etc
    The goal is to have ony standard seasons, with no particular situations
    that do not reflect "normal" season
    
    A list of forbidden keywords is established inside the func.
    Cautious, a feature far to be optimal is there:
    to exclude url concerning relegation matches, the word "sued"
    is present in the list of the forbidden keywords.
    The problem is that in SerieB, its excludes the urls
    dealing with fc-suedtirol club.
    Hence, even if its shitty, a specific condition is hardcoded
    
    :param url: url coming from a form (when listing seasons)
    :type url: str
    :return: True or False
    :rtype: bool
    """
    exclude_url_with:list=["playoff","playout","aufstieg","abstieg",
    "uefa-cup","relegation","vorrunde","finale","match-des-champions",
    "groupe","sued","nord"]

    for kw in exclude_url_with:
        if url.find("fc-suedtirol")!=-1:
            return True
        if url.find(kw)!=-1:
            return False
    return True

def goToTeams(url:str)->str:
    """
    Fetch and returns the url of a button (here for "Teams")
    This function takes the league first page (main)
    
    :param url: url of webpage having the seeked button
    :type url: str
    :return: the url of Teams button of the welcome page
    :rtype: str
    :raises RuntimeError: If the request fails
    :raises ValueError: if the returned url is empty string
    """
    try:
        my_requests=requests.get(url)
        my_requests.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e}") from e

    html_page=my_requests.content.decode('utf-8')
    soup = BeautifulSoup(html_page, "html.parser")
    keyword ="teams"
    found_url=None
    for div in soup.find_all('div'):
        for a in div.find_all('a', href=True):
            href = a['href']
            link_text = a.get_text(strip=True)
            if keyword.lower() in link_text.lower() and "/" in href.lower():
                found_url=href
                return rooturl+found_url
                
    if url is None:
        raise ValueError("Expected a non-empty string for url")

def getURLfromForm(url:str)->dict:
    """
    Fetch all season urls and associated texts contained in a <form>
    
    :param url: url of webpage to parse to find and parse the form
    :type url: str
    :return: Parsed JSON data with two keys: (1) urls and (2) labels
    :rtype: dict
    :raises RuntimeError: If the request fails
    :raises ValueError: if a returned list of json dict is empty
    """ 
    try:
        my_requests=requests.get(url)
        my_requests.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e} for {url}") from e

    html_page=my_requests.content.decode('utf-8')
    soup = BeautifulSoup(html_page, "html.parser")
    data = {"urls":[],"label" : []}
    for form in soup.find_all('form'):
        if form:
            for select in form.find_all('select'):
                if select:
                    options = select.find_all('option')
                    for option in options:
                        value   = option.get('value')
                        text    = option.get_text()
                        if(value.find("/")!=-1):
                            iurl = rooturl+value
                            if valid_url(iurl):
                                data['urls'].append(rooturl+value)
                                data['label'].append(text)
    sizes = [len(data[k]) for k in data.keys()]
    if 0 in sizes:
        raise ValueError("Expected a non-empty list")
    sortURLbyDate(data)
    return dict(data)

def getTeamsFromSeason(url:str)->dict:
    """
    Scrap the "Teams" page to parse the table containing team.
    
    :param url: url of webpage to parse to find and parse the table
    :type url: str
    :return: Parsed JSON data (urls - teamname - pathToLogo)
    :rtype: dict
    :raises RuntimeError: If the request fails
    :raises ValueError: if a returned list of json dict is empty
    """
    try:
        my_requests=requests.get(url)
        my_requests.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e}") from e
    
    html_page=my_requests.content.decode('utf-8')
    soup = BeautifulSoup(html_page, "html.parser")
    data = {"urls":[],"label" : [],'img':[]}
    
    table = soup.find('table', class_='standard_tabelle')
    if table:
        for tr in table.find_all('tr'):
            if tr:
                tds         = tr.find_all('td')
                target      = tds[1].get_text()
                target_link = rooturl+tds[1].find('a')['href']
                target_name = target_link.split("/")[-2]
                if target_name not in teams_to_exclude:
                    data['urls'].append(target_link)
                    data['label'].append(target_name)
                #
                img = tds[0].find('a').find('img')['src']
                data['img'].append(img)
                
    sizes = [len(data[k]) for k in data.keys()]
    if 0 in sizes:
        raise ValueError("Expected a non-empty list")
    return dict(data)
                
def goToTeamFixtures(url:str)->str:
    """
    Fetch and returns the url of a button (here for "Fixtures")
    
    :param url: url of webpage having the seeked button
    :type url: str
    :return: the url of Teams button of the welcome page
    :rtype: str
    :raises RuntimeError: If the request fails
    :raises ValueError: if the returned url is empty string
    """
    try:
        my_requests=requests.get(url)
        my_requests.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Request failed: {e}") from e

    html_page=my_requests.content.decode('utf-8')
    soup = BeautifulSoup(html_page, "html.parser")
    keyword ="fixtures"
    found_url=None
    for div in soup.find_all('div'):
        for a in div.find_all('a', href=True):
            href = a['href']
            link_text = a.get_text(strip=True)
            if keyword.lower() in link_text.lower() and "/" in href.lower():
                found_url=href
                return rooturl+found_url
    if url is None:
        raise ValueError("Expected a returned non-empty string for url")
    return url

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
    url_split       = url.split('/')
    yearInUrl:int   = int(list(filter(lambda x : x!="",url_split))[-2])
    year_prev:int   = yearInUrl-1
    seasonlabel     = str(year_prev)+"/"+str(yearInUrl)
    #
    data = {"round":[],
            "date":[],
            "hour":[],
            "venue":[],
            "opponent":[],
            "score":[],
            "week":[]}
    #
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
                        #
                        nweek           = -1
                        weekUrl:str     = tds[0].find('a')['href']
                        findSpieltag    = weekUrl.find('spieltag')!=-1
                        findRightSeason = verifyRoundWithRightSeason(seasonlabel,weekUrl)
                        if findSpieltag and findRightSeason:
                            items = tds[0].find('a')['href'].split('/')
                            items = list(filter(lambda x : x != "", items))
                            nweek = int(items[-1])
                        #
                        round_      = tds[0].get_text().lower()
                        date        = tds[1].get_text().lower()
                        if date =="":
                            previousdate    = data["date"][-1]
                            date = incrementDate(previousdate,1)

                        hour        = tds[2].get_text().lower()
                        venue       = tds[3].get_text().lower()
                        try:
                            opponent    = tds[5].find('a')['href'].split('/')[2]
                        except TypeError:
                            opponent    ="undefined"
                        score       = tds[6].get_text().lower()
                        #
                        data["week"].append(nweek)
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