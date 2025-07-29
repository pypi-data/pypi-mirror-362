import unittest
import os
import json
from pathlib import Path
from fb_database_api.leagues import leagues
from fb_database_api.webscrapping import goToTeams
from fb_database_api.webscrapping import getURLfromForm
from fb_database_api.webscrapping import getTeamsFromSeason
from fb_database_api.webscrapping import goToTeamFixtures
from fb_database_api.webscrapping import getFixtures

class TestLeague(unittest.TestCase):
    def test_baseurl(self):
        self.assertEqual(leagues[0].base_url,"https://www.worldfootball.net/competition/eng-premier-league/")
        self.assertEqual(leagues[1].base_url,"https://www.worldfootball.net/competition/esp-primera-division/")
        self.assertEqual(leagues[2].base_url,"https://www.worldfootball.net/competition/fra-ligue-1/")
        self.assertEqual(leagues[3].base_url,"https://www.worldfootball.net/competition/bundesliga/")
        self.assertEqual(leagues[4].base_url,"https://www.worldfootball.net/competition/ita-serie-a/")
        self.assertEqual(leagues[5].base_url,"https://www.worldfootball.net/competition/eng-championship/")
        self.assertEqual(leagues[6].base_url,"https://www.worldfootball.net/competition/esp-segunda-division/")
        self.assertEqual(leagues[7].base_url,"https://www.worldfootball.net/competition/fra-ligue-2/")
        self.assertEqual(leagues[8].base_url,"https://www.worldfootball.net/competition/2-bundesliga/")
        self.assertEqual(leagues[9].base_url,"https://www.worldfootball.net/competition/ita-serie-b/")
        self.assertEqual(leagues[10].base_url,"https://www.worldfootball.net/competition/por-primeira-liga/")
        self.assertEqual(leagues[11].base_url,"https://www.worldfootball.net/competition/ned-eredivisie/")

    def test_goToTeams(self):
        self.assertEqual(goToTeams(leagues[0].base_url),"https://www.worldfootball.net/players/eng-premier-league-2025-2026/")
        self.assertEqual(goToTeams(leagues[1].base_url),"https://www.worldfootball.net/players/esp-primera-division-2025-2026/")
        self.assertEqual(goToTeams(leagues[2].base_url),"https://www.worldfootball.net/players/fra-ligue-1-2025-2026/")
        self.assertEqual(goToTeams(leagues[3].base_url),"https://www.worldfootball.net/players/bundesliga-2025-2026/")
        self.assertEqual(goToTeams(leagues[4].base_url),"https://www.worldfootball.net/players/ita-serie-a-2025-2026/")
        self.assertEqual(goToTeams(leagues[5].base_url),"https://www.worldfootball.net/players/eng-championship-2025-2026/")
        self.assertEqual(goToTeams(leagues[6].base_url),"https://www.worldfootball.net/players/esp-segunda-division-2025-2026/")
        self.assertEqual(goToTeams(leagues[7].base_url),"https://www.worldfootball.net/players/fra-ligue-2-2025-2026/")
        self.assertEqual(goToTeams(leagues[8].base_url),"https://www.worldfootball.net/players/2-bundesliga-2025-2026/")
        self.assertEqual(goToTeams(leagues[9].base_url),"https://www.worldfootball.net/players/ita-serie-b-2024-2025-playout/")  #a modif plus tard
        self.assertEqual(goToTeams(leagues[10].base_url),"https://www.worldfootball.net/players/por-primeira-liga-2024-2025/")
        self.assertEqual(goToTeams(leagues[11].base_url),"https://www.worldfootball.net/players/ned-eredivisie-2025-2026/")

class TestForms(unittest.TestCase):
    def setUp(self):
        self.pathToRefs:str = Path(__file__).parent/"references"/"webscrapping"/"geturlfromform"
        self.urls:list=[
        "https://www.worldfootball.net/players/eng-premier-league-2025-2026/",
        "https://www.worldfootball.net/players/esp-primera-division-2024-2025/",
        "https://www.worldfootball.net/players/fra-ligue-1-2025-2026/",
        "https://www.worldfootball.net/players/bundesliga-2025-2026/",
        "https://www.worldfootball.net/players/ita-serie-a-2025-2026/",
        "https://www.worldfootball.net/players/eng-championship-2025-2026/",
        "https://www.worldfootball.net/players/esp-segunda-division-2024-2025/",
        "https://www.worldfootball.net/players/fra-ligue-2-2025-2026/",
        "https://www.worldfootball.net/players/2-bundesliga-2025-2026/",
        "https://www.worldfootball.net/players/ita-serie-b-2025-2026/",
        "https://www.worldfootball.net/players/por-primeira-liga-2024-2025/",
        "https://www.worldfootball.net/players/ned-eredivisie-2025-2026/"
    ]    

    def loadReferences(self)->list:
        l= [os.path.join(self.pathToRefs,x) for x in os.listdir(self.pathToRefs)]
        return sorted(l, key = lambda x : int(os.path.basename(x).split('_')[0]))

    def test_forms(self):
        listReferences = self.loadReferences()
        for url,refpath in zip(self.urls,listReferences):
            tempdata    = getURLfromForm(url=url)
            refdata={}
            with open(refpath,'r') as f:
                refdata     = json.load(f)
            f.close()
            self.assertEqual(tempdata["urls"],refdata["urls"],f"{url}")

class TestTeamsFromSeason(unittest.TestCase):
    def setUp(self):
        self.pathToRefs:str = Path(__file__).parent/"references"/"webscrapping"/"getteamsfromseason"/"references.json"
    
    def test_getTeamInfos(self):
        with open(self.pathToRefs, "r") as f:
            stuff=json.load(f)
        f.close()
        for i,url in enumerate(stuff["url"]):
            data = getTeamsFromSeason(url)
            self.assertEqual(data,stuff["reference"][i],f"Failed with it: {url}")

class TestGoToTeamFixtureUrl(unittest.TestCase):
    def setUp(self):
        self.pathToRefs:str = Path(__file__).parent/"references"/"webscrapping"/"gototeamfixtures"/"references.json"
    
    def test_getTeamInfos(self):
        with open(self.pathToRefs, "r") as f:
            stuff=json.load(f)
        f.close()
        for i,url in enumerate(stuff["url"]):
            data = goToTeamFixtures(url)
            self.assertEqual(data,stuff["reference"][i],f"Failed with it: {url}")

class TestGetFixtures(unittest.TestCase):
    def setUp(self):
        self.pathToRefs:str = Path(__file__).parent/"references"/"webscrapping"/"getfixtures"/"references.json"
    
    def test_getFixtures(self):
        with open(self.pathToRefs, "r") as f:
            stuff=json.load(f)
        f.close()
        for i,url in enumerate(stuff["url"]):
            data = getFixtures(url)
            self.assertEqual(data,stuff["reference"][i],f"Failed with it: {url}")


if __name__ == "__main__":
    unittest.main()