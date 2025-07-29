from footystats.leagues import *
from footystats.webscrapping import *
from footystats.utils import sortURLbyDate, reduceDataFromStartDate
from footystats.utils import argsort_dates
from pathlib import Path
import json
import time
from datetime import datetime, timezone, timedelta

utc_plus_2 = timezone(timedelta(hours=2))

def sortDictFromDates(data:dict)->None:
    """
        sort the data according to dates in the growing order
        
        :param data: dict generated from getFixtures()
        :type data: dict
        :return: None since it modifies an existing dict
        :rtype: None
    """
    indexes = argsort_dates(data['date'],"%d/%m/%Y")
    for k in data.keys():
        n = [data[k][i] for i in indexes]
        data[k] = n

def getLeagueSourceData(x:League,update:bool=False)->dict:
    """
    Craft a json database of the data received for ONE league only
    the full chain is applied:
    - (1) requests the main league url
    - (2) requests the team Button and load the page
    - (3) from the Team page, parse the form to have all season urls
    - (4) for each season url, parse the teams table, get urls for 
    each team of considered season
    - (5) for each team, get fiwtures button and parse the related table
    All data are stored in a json dict
    A time sleep of 0.8 sec temporizes to avoid ban due to request overflooding
    
    :param x: League object (dataclass from leagues.py)
    :type x: League
    :return: dict ex {"2024/2025":{"arsenal-fc"{...}, "liverpool-fc":{...}}}
    :rtype: dict
    :raises TypeError: if something else that a League object
    is given in argument
    """
    if not isinstance(x, League):
        raise TypeError("Expected instance of League (Dataclass)")
    teamsUrl:str        = goToTeams(url=x.base_url)
    seasons_urls:dict   = getURLfromForm(url=teamsUrl)
    reduceDataFromStartDate(seasons_urls=seasons_urls, startDate=x.start_date)
    fullData:dict       = {}
    #
    if update:
        seasons_urls["urls"]    = [seasons_urls["urls"][-1]]
        seasons_urls["label"]   = [seasons_urls["label"][-1]]
    print(''.join(('=') for i in range(59)))
    print(f"BUILDING SOURCES FOR {x.name.upper()}")
    print(''.join(('=') for i in range(59)))
    for season_url, season_label in zip(seasons_urls["urls"],seasons_urls["label"]):
        fullData[season_label]  = {}
        teamsOfSeason:dict      = getTeamsFromSeason(url=season_url)
        #
        status      = '{:<26}'.format('AQUISITION START FOR')
        datestr     = '{:^18} ||'.format(datetime.now(utc_plus_2).strftime("%H:%M:%S"))
        seasonstr   = '{:<9} ||'.format(season_label)
        print(status+seasonstr+datestr)
        #
        for i,team_url in enumerate(teamsOfSeason["urls"]):
            teamName:str        = teamsOfSeason["label"][i]
            print('{:<57}||'.format(teamName))
            teamFixturesUrl:str = goToTeamFixtures(url=team_url)
            # after clik
            second_seasons_url  = getURLfromForm(teamFixturesUrl)
            reduceDataFromStartDate(seasons_urls=second_seasons_url, startDate=x.start_date)
            try:
                pos:int             = second_seasons_url["label"].index(season_label)
            except ValueError:
                print(season_url)
                break
                
            currentUrl          = second_seasons_url["urls"][pos]
            #
            data:dict           = getFixtures(url=currentUrl)
            sortDictFromDates(data)
            fullData[season_label][teamName]=data
            #
            time.sleep(1.2)
        status = '{:<26}'.format('AQUISITION COMPLETE FOR')
        datestr     = '{:^18} ||'.format(datetime.now(utc_plus_2).strftime("%H:%M:%S"))
        seasonstr   = '{:<9} ||'.format(season_label)
        sep = ''.join(('=') for i in range(59))
        print(status+seasonstr+datestr)
        print(''.join(('=') for i in range(59)))
        # break
    return dict(fullData)
 
def makeSources(x:Leagues, path:str="")->None:
    """
    extract the sources using webscrapping for one or all league
    source data are stored in a dict with 6 keys:
    competition - date - hour - venue - opponent - score
    The input argument is a Enum "Leagues" by ex Leagues.LALIGA
    If the input is Leagues.ALL, all sources are built
    
    :param x: League object (available from leagues (list of League)
    :type x: League
    :param path: path to repertory where sources will be saved
    :type path: str
    :return: None
    :rtype: None
    :raises TypeError: if input not type Leagues (Enum)
    """
    if not isinstance(x,Leagues):
        raise TypeError("Expected instance Leagues(Enum)")

    if x==Leagues.ALL:
        for league in leagues:
            filename = league.name.lower()+"_sources.json"
            savepath=Path(path).joinpath(filename)
            data        = getLeagueSourceData(league)
            with open(savepath,"w") as f:
                json.dump(data,f)
            f.close()
    else:
        cLeague     = leagues[x.value]
        filename    = x.name.lower()+"_sources.json"
        savepath    = Path(path).joinpath(filename)
        data        = getLeagueSourceData(cLeague)
        with open(savepath,"w") as f:
            json.dump(data,f)
        f.close()

def updateSources(x:Leagues, pathroot:str="")->None:
    """
    reload all pages for current season to rewrite the sources
    only the current season is modified by adding informations
    the path of existing sources must be indicated
    
    :param x: League object to select league of interest
    :type x: League (Enum)
    :param pathroot: path for rep. where sources are saved
    :type pathroot: str
    :return: None
    :rtype: None
    :raises TypeError: if x not a League (Enum)
    :raises FileNotFoundError: if pathroot does not exist
    """
    if not Path(pathroot).exists():
        raise FileNotFoundError(f"Path does not exist: {pathroot}")
    if not isinstance(x,Leagues):
        raise TypeError(f"Expected an Enum Leagues instead of {type(x)}")

    if x==Leagues.ALL:
        for league in leagues:
            filename    = league.name.lower()+"_sources.json"
            dest        = Path(pathroot).joinpath(filename)
            d:dict      = loadSources(Leagues.value,pathroot)
            upd:dict     = getLeagueSourceData(x=league,update=True)
            d[list(upd)[-1]] = upd
            
            with open(savepath,"w") as f:
                json.dump(data,f)
            f.close()
    else:
        cLeague     = leagues[x.value]
        d:dict      = loadSources(x,pathroot)
        upd:dict    = getLeagueSourceData(x=cLeague,update=True)
        d[list(upd)[-1]] = upd[list(upd)[-1]]
        filename    = x.name.lower()+"_sources.json"
        dest        = Path(pathroot).joinpath(filename)
        with open(dest,"w") as f:
            json.dump(d,f)
        f.close()

def loadSources(x:Leagues, pathroot:str="")->dict:
    """
    returns a json dict with the sources for one league
    reminder, the sources contain scrapped data
    
    :param x: League object to select the league to work with
    :type x: League (Enum)
    :param pathroot: path for rep. where sources are saved
    :type pathroot: str
    :return: dict with sources data (key:list)
    :rtype: dict
    :raises TypeError: if given x is not a Leagues (Enum)
    :raises FileNotFoundError: if pathroot does not exist
    """
    if not Path(pathroot).exists():
        raise FileNotFoundError(f"Path does not exist: {pathroot}")
    if not isinstance(x,Leagues):
        raise TypeError(f"Expected an Enum Leagues instead of {type(x)}")
    cLeague     = leagues[x.value]
    filename    = x.name.lower()+"_sources.json"
    dest        = Path(pathroot).joinpath(filename)
    with open(dest,"r") as f:
        data=json.load(f)
    f.close()
    print(''.join(('=') for i in range(59)))
    print('{:^55}'.format("LOADED "+x.name.upper()+" SOURCES"))
    print(''.join(('=') for i in range(59)))
    return dict(data)

def checkAllSeasonsValidity(x:Leagues, pathroot:str="")->bool:
    """
    load sources related to League x,
    for each sasons, for each team, the nb of matches
    for the championship is controlled
    If a team has not the same number of matches than
    another, return False
    
    :param x: League object to select the league to work with
    :type x: League (Enum)
    :param pathroot: path for rep. where sources are saved
    :type pathroot: str
    :return: True or False
    :rtype: bool
    :raises TypeError: if given x is not a Leagues (Enum)
    :raises FileNotFoundError: if pathroot does not exist
    """
    if not Path(pathroot).exists():
        raise FileNotFoundError(f"Path does not exist: {pathroot}")
    if not isinstance(x,Leagues):
        raise TypeError(f"Expected an Enum Leagues instead of {type(x)}")
    
    ErrorList={"season":[],"team":[]}
    if x.name != Leagues.ALL:
        data = loadSources(x,pathroot)

        for season in data.keys():
            n=[]
            for team in data[season].keys():
                weeks = data[season][team]['week']
                nb_weeks = len(list(filter(lambda x : x!=-1, weeks)))
                n.append(nb_weeks)
            #
            if len(list(set(n)))!=1:
                ErrorList["season"].append(season)
                ErrorList["team"].append(team)
    return ErrorList