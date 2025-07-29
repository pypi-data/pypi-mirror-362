#debug.py

from pathlib import Path
from footystats.leagues import Leagues

def debugDatabase(x:Leagues,d:dict, startYear:str)->None:
    """
    write the database ductionnary in a .txt file
    the debug files are written in the current directory
    from which the script is run
    This function also works for sources

    :param x: league for which the database is built
    :type x: Leagues (Enum)
    :param d: database that is exported into .txt file
    :type d: dict
    :return: None
    :rtype: None
    """
    cwd = Path.cwd()
    fname = x.name.lower()+"_debug.txt"
    sp = cwd.joinpath(fname)
    with open(sp,"w") as f:
        f.write(x.name.upper()+'\n')
        f.write(''.join(('=') for i in range(55))+'\n')
        seasons = makeSeasonList(list(d.keys()),startYear)
        for s in seasons:
            f.write('\t'+s+'\n')
            for t in d[s].keys():
                f.write('\t\t'+t+'\n')
                label=""
                for k in d[s][t].keys():
                    label += '{:<26}'.format(k)
                f.write(label+'\n')
                for i in range(len(d[s][t][next(iter(d[s][t].keys()))])):
                    val=""
                    for k in d[s][t].keys():
                        try:
                            val += '{:<26}'.format(str(d[s][t][k][i]))
                        except:
                            print(k, len(d[s][t][k]))
                    f.write(val+'\n')
    f.close()

def makeSeasonList(seasonlabels:list,start:str)->list:
    """
    generates a list containing season labels 
    from the year given in "start"
    for example, if start is 2019,
    the the list returned is [2019/2020, 2020/...]
    
    :param seasonlabels: the keys of the database
    :type seasonlabels: list
    :param start: the year of the first season to
    consider
    :type start: str
    :return: a reduced list of keys of the database
    :rtype: list
    """
    for i,s in enumerate(seasonlabels):
        y1:str=s.split('/')[0]
        if y1==start:
            break
    return list(seasonlabels[i::])
        