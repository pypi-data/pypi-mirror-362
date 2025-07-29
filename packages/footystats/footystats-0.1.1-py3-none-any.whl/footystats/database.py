#database.py
import re
from datetime import datetime
from pathlib import Path
from footystats.leagues import *
from footystats.sources import loadSources
from footystats.debug import debugDatabase
import json

def makeDatabase(x:Leagues=None,sourcesRep:str="",saveRep:str="", debug:bool=False, debugYear:str="2000")->dict:
    """
    compute the full database for the league indicated in x
    This is a dictionnary with many informations as:
    week played, score, result, opponent, ladder, ladder at home
    ladder when playing outside, goal scored at home, outside, etc.
    the database is saved at pathRepSave
    
    :param x: league for which the database is built
    :type x: dict
    :param sourcesRep: path to repertory containing sources
    :type sourcesRep: str
    :param saveRep: repertory path to save the built database
    :raise FileNotFoundError: if either sourcesRep or 
    saveRep is not valid
    :raise TypeError; if given x is not a League Enum
    """
    if not Path(sourcesRep).exists():
        raise FileNotFoundError(f"Path to sources does not exist: {sourcesRep}")
    if not Path(saveRep).exists():
        raise FileNotFoundError(f"Path to save databases does not exist: {saveRep}")
    if not isinstance(x,Leagues):
        raise TypeError(f"Expected an Enum Leagues instead of {type(x)}")
    if x.name != "ALL":
        sources:dict = loadSources(x,sourcesRep)
        database:dict= {}
        #
        initializeDatabase(sources,database)
        addWeekVenueOpponent(sources,database)
        #
        computeGoalsAndResults(sources,database)
        computeCumulatedGoals(database)
        computePoints(database)
        computeGeneralLadder(database)
        computeHomeLadder(database)
        computeAwayLadder(database)
        computeForms(database,8)
        computeOpponentInfos(database)
        if debug:
            debugDatabase(x,database,debugYear)
        # SAVE DATABASE
        fname:str = "database_"+x.name.lower()+".json"
        sp = Path(saveRep).joinpath(fname)
        with open(sp,"w") as f:
            json.dump(database,f)
        f.close()
    else:
        for l in Leagues:
            if l.name!="ALL":
                sources:dict = loadSources(l,sourcesRep)
                database:dict= {}
                #
                initializeDatabase(sources,database)
                addWeekVenueOpponent(sources,database)
                #
                # prepareDatabaseFile()
                computeGoalsAndResults(sources,database)
                computeCumulatedGoals(database)
                computePoints(database)
                computeGeneralLadder(database)
                computeHomeLadder(database)
                computeAwayLadder(database)
                computeForms(database,8)
                computeOpponentInfos(database)
                if debug:
                    debugDatabase(l,database,debugYear)
                # SAVE DATABASE
                fname:str = "database_"+l.name.lower()+".json"
                sp = Path(saveRep).joinpath(fname)
                with open(sp,"w") as f:
                    json.dump(database,f)
                f.close()

def initializeDatabase(sources:dict,database:dict)->None:
    """
    insert the necessary basic keys for the database
    first, season labels are added
    secondly, teams are added to each corresponding seasons
    to summarize, the database is structured like
    database[season][team]{key1:[],...keyn:[]}
    
    :param sources: sources for current leagues
    :type sources: dict
    :param database: evolving database which will be updated
    :type database: dict
    :return: None
    :rtype: None
    """
    for s in sources.keys():
        database.update((s,{}) for i in range(1))
        for t in sources[s].keys():
            database[s][t]={}

def addWeekVenueOpponent(sources:dict,databaseToUpdate:dict)->None:
    """
    insert basic informations as played week,
    venue of the match, hour, date and opponent,
    litteral month, litteral day
    
    :param sources: sources for current leagues
    :type sources: dict
    :param database: evolving database which will be updated
    :type database: dict
    :return: None
    :rtype: None
    """
    d:dict={}
    for s in sources.keys():
        for t in sources[s].keys():
            _ = {"week":[],"venue":[],"date":[],"hour":[],
            "month":[],"day":[],"opponent":[]}
            for idx,week in enumerate(sources[s][t]['week']):
                if week != -1:
                    date = sources[s][t]['date'][idx]
                    hour = sources[s][t]['hour'][idx]
                    if hour=="":
                        hour="-:-"
                    venue = sources[s][t]['venue'][idx]
                    day  = str(datetime.strptime(date,"%d/%m/%Y").strftime("%A")).lower()
                    month = str(datetime.strptime(date,"%d/%m/%Y").strftime("%B")).lower()
                    opp = sources[s][t]['opponent'][idx]
                    _["week"].append(str(week))
                    _["venue"].append(venue)
                    _["date"].append(date)
                    _["hour"].append(hour)
                    _["day"].append(day)
                    _["month"].append(month)
                    _["opponent"].append(opp)
            databaseToUpdate[s][t].update((k,_[k]) for k in _.keys())

def computeGoalsAndResults(sources:dict, databaseToUpdate:dict)->None:
    """
    Computes the column Result, GF, GA, HTGF, HTGA
    
    :param sources: sources dictionnary (json) of current league
    :type sources: dict
    :param databaseToUpdate: database to update with scored/taken goals
    :type databaseToUpdate: dict
    :return: None
    :rtype: None
    """
    forbiddens=["-:-","dnp","abor."]
    d:dict={}
    for s in sources.keys():
        for t in sources[s].keys():
            _ = {"result":[],"gf":[],"ga":[],"htgf":[],"htga":[]}
            for idx,week in enumerate(sources[s][t]['week']):
                if week != -1:
                    score_data = sources[s][t]['score'][idx]
                    result     = "-:-"
                    if score_data not in forbiddens:
                        scores:list = score_data.split()
                        gf:int = int(scores[0].split(':')[0])
                        ga:int = int(scores[0].split(':')[1])
                        if gf>ga:
                            result = "W"
                        elif gf==ga:
                            result="D"
                        else:
                            result="L"
                        
                        if len(scores)>1:
                            scoreHT=re.sub(r'[()]', '', scores[1])
                            
                            htgf = "-:-"
                            htga = "-:-"
                            if scoreHT.find('dec.')==-1 and scoreHT!="":
                                htgf:int = int(scoreHT.split(':')[0])
                                htga:int = int(scoreHT.split(':')[1])
                        else:
                            htgf="-:-"
                            htga="-:-"
                        _["result"].append(result)
                        _["gf"].append(gf)
                        _["ga"].append(ga)
                        _["htgf"].append(htgf)
                        _["htga"].append(htga)
                    else:
                        _["result"].append("-:-")
                        _["gf"].append("-:-")
                        _["ga"].append("-:-")
                        _["htgf"].append("-:-")
                        _["htga"].append("-:-")
            databaseToUpdate[s][t].update((k,_[k]) for k in _.keys())

def computeCumulatedGoals(databaseToUpdate:dict)->None:
    """
    computes 9 list of cumulated goal scored / taken / difference
    cumulated goals scored, (cgf), goals taken (cga), goal diff (cgd)
    cumulated goald specific to home matches: cgf_home, cga_home, cgd_home
    cumulated goald specific to away matches: cgf_home, cga_home, cgd_home
    
    :param databaseToUpdate: database to update with cumulated goals
    :type databaseToUpdate: dict
    :return: None
    :rtype: None
    """
    accumulate = lambda x : [sum(x[0:i+1]) if i>0 
                        else x[0] for i in range(len(x))]
    for s in databaseToUpdate.keys():
        for t in databaseToUpdate[s].keys():
            cgf, cgf_home, cgf_away = ([] for i in range(3))
            cga, cga_home, cga_away = ([] for i in range(3))
            cgd, cgd_home, cgd_away = ([] for i in range(3))
            for w in range(len(databaseToUpdate[s][t]['week'])):
                venue = databaseToUpdate[s][t]['venue'][w]
                try:
                    gf = int(databaseToUpdate[s][t]['gf'][w])
                    ga = int(databaseToUpdate[s][t]['ga'][w])
                    gd = gf-ga
                except ValueError:
                    gf = 0
                    ga = 0
                    gd = 0
                #
                cgf.append(gf)
                cga.append(ga)
                cgd.append(gd)
                #
                if venue=="h":
                    cgf_home.append(gf)
                    cga_home.append(ga)
                    cgd_home.append(gd)
                    cgf_away.append(0)
                    cga_away.append(0)
                    cgd_away.append(0)
                else:
                    cgf_home.append(0)
                    cga_home.append(0)
                    cgd_home.append(0)
                    cgf_away.append(gf)
                    cga_away.append(ga)
                    cgd_away.append(gd)
            #
            cgf=accumulate(cgf)
            cga=accumulate(cga)
            cgd=accumulate(cgd)
            cgf_home = accumulate(cgf_home)
            cga_home = accumulate(cga_home)
            cgd_home = accumulate(cgd_home)
            cgf_away = accumulate(cgf_away)
            cga_away = accumulate(cga_away)
            cgd_away = accumulate(cgd_away)
            #
            databaseToUpdate[s][t]["cgf"]=cgf
            databaseToUpdate[s][t]["cga"]=cga
            databaseToUpdate[s][t]["cgd"]=cgd
            databaseToUpdate[s][t]["cgf_home"]=cgf_home
            databaseToUpdate[s][t]["cga_home"]=cga_home
            databaseToUpdate[s][t]["cgd_home"]=cgd_home
            databaseToUpdate[s][t]["cgf_away"]=cgf_away
            databaseToUpdate[s][t]["cga_away"]=cga_away
            databaseToUpdate[s][t]["cgd_away"]=cgd_away

def computePoints(databaseToUpdate:dict)->None:
    """
        compute points earned along season for each team
        three types of points: general (home + away),
        points earned at home and points earned outside
        The main database is updated with neaw keys
        
        :param databaseToUpdate: main database to update
        :type databaseToUpdate: dict
        :return: None
        :rtype: None
    """
    accumulate = lambda x : [sum(x[0:i+1]) if i>0 
                        else x[0] for i in range(len(x))]
    for s in databaseToUpdate.keys():
        for t in databaseToUpdate[s].keys():
            generalPts,homePts,awayPts = ([] for i in range(3))
            for w in range(len(databaseToUpdate[s][t]['week'])):
                venue   = databaseToUpdate[s][t]['venue'][w]
                result  = databaseToUpdate[s][t]['result'][w]
                if result=="W":
                    generalPts.append(3)
                    if venue=="h":
                        homePts.append(3)
                        awayPts.append(0)
                    else:
                        homePts.append(0)
                        awayPts.append(3)
                elif result=="D":
                    generalPts.append(1)
                    if venue=="h":
                        homePts.append(1)
                        awayPts.append(0)
                    else:
                        homePts.append(0)
                        awayPts.append(1)
                else:
                    generalPts.append(0)
                    homePts.append(0)
                    awayPts.append(0)
            databaseToUpdate[s][t]["points"]=accumulate(generalPts)
            databaseToUpdate[s][t]["homepoints"]=accumulate(homePts)
            databaseToUpdate[s][t]["awaypoints"]=accumulate(awayPts)

def computeGeneralLadder(databaseToUpdate:dict)->None:
    """
    computes the ladder position after each played week
    
    :param databaseToUpdate: main database to update
    :type databaseToUpdate: dict
    :return: None
    :rtype: None
    """
    sort = lambda x : sorted(range(len(x)),key = x.__getitem__)
    for s in databaseToUpdate.keys():
        nbw = len(databaseToUpdate[s][next(iter(databaseToUpdate[s].keys()))]['week'])
        teams=list(databaseToUpdate[s].keys())
        for t in databaseToUpdate[s].keys():
            databaseToUpdate[s][t]["ladder"]=[]
        for i in range(nbw):
            scores=[]
            for t in databaseToUpdate[s].keys():
                pts=databaseToUpdate[s][t]['points'][i]
                iscore  = 10000*pts
                iscore += 100*databaseToUpdate[s][t]['cgd'][i]
                iscore += 10 * databaseToUpdate[s][t]['cgf'][i]
                scores.append(iscore)
            sortedIndex=sort(scores)
            sortedTeams=[teams[i] for i in sortedIndex][::-1]
            [databaseToUpdate[s][tt]['ladder'].append(idx+1) for idx,tt in enumerate(sortedTeams)]
            
def computeHomeLadder(databaseToUpdate:dict)->None:
    """
    computes the ladder position after each played week
    considering only points earned at home
    
    :param databaseToUpdate: main database to update
    :type databaseToUpdate: dict
    :return: None
    :rtype: None
    """
    sort = lambda x : sorted(range(len(x)),key = x.__getitem__)
    for s in databaseToUpdate.keys():
        nbw = len(databaseToUpdate[s][next(iter(databaseToUpdate[s].keys()))]['week'])
        teams=list(databaseToUpdate[s].keys())
        for t in databaseToUpdate[s].keys():
            databaseToUpdate[s][t]["homeladder"]=[]
        for i in range(nbw):
            scores=[]
            for t in databaseToUpdate[s].keys():
                pts=databaseToUpdate[s][t]['homepoints'][i]
                iscore  = 10000*pts
                iscore += 100*databaseToUpdate[s][t]['cgd_home'][i]
                iscore += 10 * databaseToUpdate[s][t]['cgf_home'][i]
                scores.append(iscore)
            sortedIndex=sort(scores)
            sortedTeams=[teams[i] for i in sortedIndex][::-1]
            [databaseToUpdate[s][tt]['homeladder'].append(idx+1) for idx,tt in enumerate(sortedTeams)]

def computeAwayLadder(databaseToUpdate:dict)->None:
    """
    computes the ladder position after each played week
    considering only points earned outside
    
    :param databaseToUpdate: main database to update
    :type databaseToUpdate: dict
    :return: None
    :rtype: None
    """
    sort = lambda x : sorted(range(len(x)),key = x.__getitem__)
    for s in databaseToUpdate.keys():
        nbw = len(databaseToUpdate[s][next(iter(databaseToUpdate[s].keys()))]['week'])
        teams=list(databaseToUpdate[s].keys())
        for t in databaseToUpdate[s].keys():
            databaseToUpdate[s][t]["awayladder"]=[]
        for i in range(nbw):
            scores=[]
            for t in databaseToUpdate[s].keys():
                pts=databaseToUpdate[s][t]['awaypoints'][i]
                iscore  = 10000*pts
                iscore += 100*databaseToUpdate[s][t]['cgd_away'][i]
                iscore += 10 * databaseToUpdate[s][t]['cgf_away'][i]
                scores.append(iscore)
            sortedIndex=sort(scores)
            sortedTeams=[teams[i] for i in sortedIndex][::-1]
            [databaseToUpdate[s][tt]['awayladder'].append(idx+1) for idx,tt in enumerate(sortedTeams)]

def computeForms(databaseToUpdate:dict,period:int)->None:
    """
    compute the forms from the n previous matches
    the form is a kind of reduced ladder computed
    over the the n last matches
    
    :param databaseToUpdate: main database to update with key form
    :type databaseToUpdate: dict
    :param period: number of past matches t consider to compute the form
    :type period: int
    :return: None
    :rype: None
    """
    sort = lambda x : sorted(range(len(x)),key = x.__getitem__)
    accumulate = lambda x : [sum(x[0:i+1]) if i>0 
                        else x[0] for i in range(len(x))]
    for s in databaseToUpdate.keys():
        nbw = len(databaseToUpdate[s][next(iter(databaseToUpdate[s].keys()))]['week'])
        teams=list(databaseToUpdate[s].keys())
        for t in databaseToUpdate[s].keys():
            databaseToUpdate[s][t]["form"]=[]
        for i in range(nbw):
            tableScore:list=[]
            for t in databaseToUpdate[s].keys():
                min_index = max(0,i-period)
                # GOALS
                gf = databaseToUpdate[s][t]['gf'][min_index:min_index+period]
                ga = databaseToUpdate[s][t]['ga'][min_index:min_index+period]
                array_a, array_f = [],[]
                for f,a in zip(gf,ga):
                    try:
                        array_f.append(int(f))
                        array_a.append(int(a))
                    except ValueError:
                        array_f.append(0)
                        array_a.append(0)
                array_f=accumulate(array_f)
                array_a=accumulate(array_a)
                
                total_gf = array_f[-1]
                total_ga = array_a[-1]
                total_gd = total_gf-total_ga
                # PTS
                pts=0
                for r in databaseToUpdate[s][t]['result'][min_index:min_index+period]:
                    if r=="W":
                        pts+=3
                    if r=="D":
                        pts+=1
                iscore = 10000*pts+100*total_gd+10*total_gf
                tableScore.append(iscore)
                #
            sortedIndex=sort(tableScore)
            sortedTeams=[teams[i] for i in sortedIndex][::-1]
            [databaseToUpdate[s][tt]['form'].append(idx+1) for idx,tt in enumerate(sortedTeams)]

def computeOpponentInfos(databaseToUpdate:dict)->None:
    """
    computes for each week the opponent relative
    infos like actual ladder, homeladder,awayladder and form
    Cautious: since the ladders are calculated at end of the 
    considered week, the ladders are taken at week-1 because
    what is relevant is the ladders or form of opponentbe before
    the confrontation takes place.
    For the first played week, since no statistics are possible,
    ladders and forms are set to -1
    
    :param databaseToUpdate: main database to update with key form
    :type databaseToUpdate: dict
    :return: None
    :rtype: None
    """
    for s in databaseToUpdate.keys():
        for t in databaseToUpdate[s].keys():
            databaseToUpdate[s][t]['opponent_ladder']=[]
            databaseToUpdate[s][t]['opponent_homeladder']=[]
            databaseToUpdate[s][t]['opponent_awayladder']=[]
            databaseToUpdate[s][t]['opponent_form']=[]
            for idx,week in enumerate(databaseToUpdate[s][t]['week']):
                if idx==0:
                    databaseToUpdate[s][t]['opponent_ladder'].append(-1)
                    databaseToUpdate[s][t]['opponent_homeladder'].append(-1)
                    databaseToUpdate[s][t]['opponent_awayladder'].append(-1)
                    databaseToUpdate[s][t]['opponent_form'].append(-1)
                else:
                    opp = databaseToUpdate[s][t]['opponent'][idx]
                    opp_ladder = databaseToUpdate[s][opp]['ladder'][idx-1]
                    opp_homeladder = databaseToUpdate[s][opp]['homeladder'][idx-1]
                    opp_awayladder = databaseToUpdate[s][opp]['awayladder'][idx-1]
                    opp_form = databaseToUpdate[s][opp]['form'][idx-1]
                    #
                    databaseToUpdate[s][t]['opponent_ladder'].append(opp_ladder)
                    databaseToUpdate[s][t]['opponent_homeladder'].append(opp_homeladder)
                    databaseToUpdate[s][t]['opponent_awayladder'].append(opp_awayladder)
                    databaseToUpdate[s][t]['opponent_form'].append(opp_form)

def loadDatabase(x:Leagues, pathToDatabase:str)->dict:
    """
    load the database for the list selected with x
    
    :param x: select a league
    :type x: Leagues (Enum)
    :param pathToDatabase: path of repertory where databases are stored
    :type pathToDatabase: str
    :return: a database as a dict
    :rtype: dict
    """
    if not Path(pathToDatabase).exists():
        raise FileNotFoundError(f"Path to database does not exist: {pathToDatabase}")
    if not isinstance(x,Leagues):
        raise TypeError(f"Expected an Enum Leagues instead of {type(x)}")
    fname:str = "database_"+x.name.lower()+".json"
    p = Path(pathToDatabase).joinpath(fname)
    if not Path(p).exists():
        raise FileNotFoundError(f"Database not found: {fname}")
    with open(p,"r") as f:
        data = json.load(f)
    f.close()
    return dict(data)