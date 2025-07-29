# footystats

Install with:

```bash
pip install footystats

This package contains to major functions:
(1) build sources from www.worldfootball.net
(2) build database from the acquired sources

The soccer leagues available are listed in an Enum
This Enum is used as argument for a lot of functions
(1) PremierLeague (callable using Leagues.PREMIERLEAGUE)
(2) Liga (Leagues.LALIGA)
(3) Ligue 1 (Leagues.LIGUE1)
(4) Bundesliga (Leagues.BUNDESLIGA)
(5) Serie A (Leagues.SERIEA)
(6) Championship (Leagues.CHAMPIONSHIP)
(7) Liga2 (Leagues.LALIGA2)
(8) Ligue2 (Leagues.LIGUE2)
(9) Bundesliga (Leaguues.BUNDESLIGA2)
(10) Serie B (Leagues.SERIEB)
(11) PrimeiraLiga (Leagues.PRIMEIRALIGA)
(12) Eredivisie (Leagues.EREDIVISIE)
(13) Leagues.ALL

#################################################################
	(1) BUILD SOURCES webscrapping from online sites
#################################################################

To obtain the sources, prepare a folder to save the sources (json) and
use this path as argument as in the example below:

from footystats.leagues import Leagues
from footystats.sources import makeSources

sourcesRepertory="YOUR_PATH_TO_SOURCES"
makeSources(Leagues.LALIGA, sourcesRepertory) {for specific spanish laLiga)
makeSources(Leagues.ALL, sourcesRepertory) (for all leagues)

You can load the sources using 
from footystats.sources import loadSources

sources:dict = loadSources(Leagues.LALIGA,sourcesRepertory)

#if you want to enrich the sources with more recent data:
from footystats.sources import updateSources

updateSources(Leagues.LALIGA,sourcesRepertory)

To look the produced sources, you can use a debug function
that writes the json dict within.txt file (auto naming of the debug file)
The debug file is exported in the current working directory
from which the script is run.

from footystats.debug import debugDatabase

debugDatabase(Leagues.LALIGA, sources, startYear="2015")
# this will write the sources from season 2015-2016


#################################################################
	(2) BUILD DATABASE: post treatment of sources
#################################################################
 If you have sources, you can proceed to build database.
 Databases are post-treated sources (json dict).
 You also need to establish a repertory where to save the databases
 if you use Leagues.ALL, all database leagues will be build.
 If debug is True, then the .txt files are also exported
 
 from footystats.database import makeDatabase
 
 mySavePathForDatabase:str="PATH_TO_DATABASES"
 
 makeDatabase(Leagues.LALIGA, sourcesRepertory, mySavePathForDatabase,debug=True,debugYear="2020")
  
#################################################################
	(3) Load the database and enjoy for your custom projects
#################################################################
from footystats.database import loadDatabase

 my_database:dict = loadDatabase(Leagues.LALIGA,mySavePathForDatabase)