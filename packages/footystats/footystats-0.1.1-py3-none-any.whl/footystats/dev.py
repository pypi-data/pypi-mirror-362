from footystats.leagues import Leagues
from footystats.sources import makeSources
from footystats.database import makeDatabase
from footystats.database import loadDatabase
from pathlib import Path


if __name__ == '__main__':
    sourcesroot=Path("D:\FOOTBALL\sources")
    databaseroot=Path("D:\FOOTBALL\databases")
    #
    # makeSources(Leagues.PRIMEIRALIGA, thepathroot)
    # updateSources(Leagues.SERIEA,thepathroot)
    
    makeDatabase(Leagues.LALIGA, sourcesroot, databaseroot,debug=True,debugYear="2024")
    
    database = loadDatabase(Leagues.LALIGA,databaseroot)
