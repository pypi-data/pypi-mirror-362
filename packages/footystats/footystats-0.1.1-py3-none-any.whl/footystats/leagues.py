from dataclasses import dataclass
from typing import List
from enum import Enum

#error direct at the sources: these teams have no data
teams_to_exclude:list=[
    "troyes-af"
] 

class Leagues(Enum):
    PREMIERLEAGUE = 0
    LALIGA = 1
    LIGUE1 = 2
    BUNDESLIGA = 3
    SERIEA = 4
    CHAMPIONSHIP = 5
    LALIGA2 = 6
    LIGUE2 = 7
    BUNDESLIGA2 = 8
    SERIEB = 9
    PRIMEIRALIGA = 10
    EREDIVISIE = 11
    ALL = 12

@dataclass
class League:
    name: str
    start_date:int
    base_url:str

leagues: List[League] = [
    League(
    name        ="PremierLeague", 
    start_date  =1950,
    base_url    ="https://www.worldfootball.net/competition/eng-premier-league/"
    ),   # 0
    League(
    name        ="LaLiga", 
    start_date  =1950,
    base_url    ="https://www.worldfootball.net/competition/esp-primera-division/"
    ),   # 1
    League(
    name        ="Ligue1", 
    start_date  =1950,
    base_url    ="https://www.worldfootball.net/competition/fra-ligue-1/"
    ),   # 2
    League(
    name        ="Bundesliga", 
    start_date  =1969,
    base_url    ="https://www.worldfootball.net/competition/bundesliga/"
    ),   # 3
    League(
    name        ="SerieA",
    start_date  =1950,
    base_url    ="https://www.worldfootball.net/competition/ita-serie-a/"
    ),   # 4
    League(
    name        ="Championship", 
    start_date  =1950,
    base_url    ="https://www.worldfootball.net/competition/eng-championship/"
    ),    # 5
    League(
    name        ="SegundaLiga", 
    start_date  =1969,
    base_url    ="https://www.worldfootball.net/competition/esp-segunda-division/"
    ),     # 6
    League(
    name        ="Ligue2", 
    start_date  =1993,
    base_url    ="https://www.worldfootball.net/competition/fra-ligue-2/"
    ),          # 7
    League(
    name        ="Bundesliga2", 
    start_date  =1993,
    base_url    ="https://www.worldfootball.net/competition/2-bundesliga/"
    ),     # 8
    League(
    name        ="SerieB",
    start_date  =1994,
    base_url    = "https://www.worldfootball.net/competition/ita-serie-b/"
    ),          # 9
    League(
    name        ="PrimeraLiga", 
    start_date  =1969,
    base_url    ="https://www.worldfootball.net/competition/por-primeira-liga/"
    ),     # 10
    League(
    name        ="Eredivisie", 
    start_date  =1960,
    base_url    = "https://www.worldfootball.net/competition/ned-eredivisie/"
    )       # 11
    ]