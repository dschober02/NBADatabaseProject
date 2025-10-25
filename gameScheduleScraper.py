import requests
from bs4 import BeautifulSoup
import time
import re

headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
}

nba_team_code = {
    "Boston Celtics": "BOS",
    "Brooklyn Nets": "BRK",
    "New York Knicks": "NYK",
    "Philadelphia 76ers": "PHI",
    "Toronto Raptors": "TOR",
    "Golden State Warriors": "GSW",
    "LA Clippers": "LAC",
    "Los Angeles Lakers": "LAL",
    "Phoenix Suns": "PHO",
    "Sacramento Kings": "SAC",
    "Chicago Bulls": "CHI",
    "Cleveland Cavaliers": "CLE",
    "Detroit Pistons": "DET",
    "Indiana Pacers": "IND",
    "Milwaukee Bucks": "MIL",
    "Dallas Mavericks": "DAL",
    "Houston Rockets": "HOU",
    "Memphis Grizzlies": "MEM",
    "New Orleans Pelicans": "NOP",
    "San Antonio Spurs": "SAS",
    "Atlanta Hawks": "ATL",
    "Charlotte Hornets": "CHO",
    "Miami Heat": "MIA",
    "Orlando Magic": "ORL",
    "Washington Wizards": "WAS",
    "Denver Nuggets": "DEN",
    "Minnesota Timberwolves": "MIN",
    "Oklahoma City Thunder": "OKC",
    "Portland Trail Blazers": "POR",
    "Utah Jazz": "UTA"
}

URLS = ['https://www.basketball-reference.com/boxscores/202504190IND.html', 'https://www.basketball-reference.com/boxscores/202504190DEN.html', 'https://www.basketball-reference.com/boxscores/202504190DEN.html', 'https://www.basketball-reference.com/boxscores/202504190NYK.html',
 'https://www.basketball-reference.com/boxscores/202504190LAL.html', 'https://www.basketball-reference.com/boxscores/202504200OKC.html',
 'https://www.basketball-reference.com/boxscores/202504200BOS.html', 'https://www.basketball-reference.com/boxscores/202504200CLE.html',
 'https://www.basketball-reference.com/boxscores/202504200HOU.html', 'https://www.basketball-reference.com/boxscores/202504210NYK.html',
 'https://www.basketball-reference.com/boxscores/202504210DEN.html', 'https://www.basketball-reference.com/boxscores/202504220IND.html',
 'https://www.basketball-reference.com/boxscores/202504220OKC.html', 'https://www.basketball-reference.com/boxscores/202504220LAL.html',
 'https://www.basketball-reference.com/boxscores/202504230BOS.html', 'https://www.basketball-reference.com/boxscores/202504230CLE.html',
 'https://www.basketball-reference.com/boxscores/202504230HOU.html', 'https://www.basketball-reference.com/boxscores/202504240DET.html',
 'https://www.basketball-reference.com/boxscores/202504240MEM.html', 'https://www.basketball-reference.com/boxscores/202504240LAC.html',
 'https://www.basketball-reference.com/boxscores/202504250ORL.html', 'https://www.basketball-reference.com/boxscores/202504250MIL.html',
 'https://www.basketball-reference.com/boxscores/202504250MIN.html', 'https://www.basketball-reference.com/boxscores/202504260MIA.html',
 'https://www.basketball-reference.com/boxscores/202504260MEM.html', 'https://www.basketball-reference.com/boxscores/202504260LAC.html',
 'https://www.basketball-reference.com/boxscores/202504260GSW.html', 'https://www.basketball-reference.com/boxscores/202504270DET.html',
 'https://www.basketball-reference.com/boxscores/202504270MIN.html', 'https://www.basketball-reference.com/boxscores/202504270ORL.html',
 'https://www.basketball-reference.com/boxscores/202504270MIL.html', 'https://www.basketball-reference.com/boxscores/202504280MIA.html',
 'https://www.basketball-reference.com/boxscores/202504280GSW.html', 'https://www.basketball-reference.com/boxscores/202504290IND.html',
 'https://www.basketball-reference.com/boxscores/202504290NYK.html', 'https://www.basketball-reference.com/boxscores/202504290BOS.html',
 'https://www.basketball-reference.com/boxscores/202504290DEN.html', 'https://www.basketball-reference.com/boxscores/202504300HOU.html',
 'https://www.basketball-reference.com/boxscores/202504300LAL.html']

file = open('gameTable.txt', 'w')

file.write(f"""
    CREATE TABLE Game (
        Game_ID INT NOT NULL PRIMARY KEY,
        Date varchar(20)
);

    CREATE TABLE Schedule (
        Game_ID INT NOT NULL PRIMARY KEY,
        Team_Code char(3)
);
    """)
counter = 0
for url in URLS:
    try:
        counter += 1
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        # Each team name appears inside <strong><a> tags within divs with class 'scorebox'
        scorebox = soup.find("div", class_="scorebox")
        team_links = scorebox.find_all("a", href=re.compile(r"^/teams/([A-Z]{3})/"))
        print(team_links)
        time.sleep(5)

        date = soup.find('div', class_='scorebox_meta')
        date = date.find_all("div")[0].strip()

        file.write(f'INSERT INTO Schedule (Game_ID, Date) VALUES ({counter}, {date});\n'
                   f'INSERT INTO Game (Game_ID, Date) VALUES ({counter}, {nba_team_code[team_links[0]]});\n)'
                   f'INSERT INTO Game (Game_ID, Date) VALUES ({counter}, {nba_team_code[team_links[1]]});\n)')


    except Exception as e:
        print(e)