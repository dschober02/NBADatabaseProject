import pandas as pd
import bs4
from bs4 import BeautifulSoup
import requests
import time

# These are the headers we will use in our GET request
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
        "Version/17.0 Safari/605.1.15"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

# These are all teams that participated in the 2025 NBA playoffs
nba_playoff_teams_2024 = {
    # Eastern Conference
    "BOS": "Boston Celtics",
    "NYK": "New York Knicks",
    "MIL": "Milwaukee Bucks",
    "CLE": "Cleveland Cavaliers",
    "ORL": "Orlando Magic",
    "IND": "Indiana Pacers",
    "MIA": "Miami Heat",
    "PHI": "Philadelphia 76ers",

    # Western Conference
    "OKC": "Oklahoma City Thunder",
    "DEN": "Denver Nuggets",
    "MIN": "Minnesota Timberwolves",
    "LAC": "Los Angeles Clippers",
    "DAL": "Dallas Mavericks",
    "PHO": "Phoenix Suns",
    "LAL": "Los Angeles Lakers",
    "NOP": "New Orleans Pelicans"
}

URL1 = "https://www.basketball-reference.com/teams/"
URL2 = "/2025.html#all_roster"

# We will make up a fake player ID using a counter, all else will be grabbed from basketball-reference.com


def rosterInserts():
    out = open("rosterInserts.txt", "w")
    dataFrame = {
        "Player ID" : [],
        "Player Name" : [],
        "Team Code": [],
        "Position" : [],
        "Height" : [],
        "Weight" : []
    }
    df = pd.DataFrame(dataFrame)
    counter = 0  # This is for the created player id
    # table creation statement
    # NOTE: Will have to create teams table first due to foreign key constraint in roster
    sql = f"""
    CREATE TABLE roster (
        Player_ID INT NOT NULL PRIMARY KEY,
        Player_Name VARCHAR(100),
        Team_Code VARCHAR(3) NOT NULL,
        Position VARCHAR(50),
        Height VARCHAR(10),
        Weight VARCHAR(10),
        FOREIGN KEY (Team_Code) REFERENCES teams(Team_Code)
);
    """
    out.write(sql)
    for team in nba_playoff_teams_2024.keys():
        print(team)
        try:
            # URL composition: "https://www.basketball-reference.com/teams/" + "BOS" + "/2025.html#all_roster"
            response = requests.get((URL1 + team + URL2), headers=HEADERS)
            time.sleep(3) # Hit limiting to adhere to basketball reference scraping rules
            soup = bs4.BeautifulSoup(response.text, "lxml")
            roster = soup.find("table", id="roster")
            for row in roster.find_all('tr'):
                columns = row.find_all(['td', 'th'])
                # data - ['No.', 'Player', 'Pos', 'Ht', 'Wt', 'Birth Date', 'Birth', 'Exp', 'College']
                data = [col.get_text(strip=True) for col in columns]
                if data[1] != "Player":
                    if '\'' in data[1]:
                        data[1] = data[1].replace('\'', '`')
                    counter += 1
                    row = {
                        'Player ID' : counter,
                        'Player Name' : data[1],
                        'Team Code' : team,
                        'Position' : data[2],
                        'Height' : data[3],
                        'Weight' : data[4],}
                    df.loc[len(df)] = row
            print(df)

        except Exception as e:
            print(f"Could not scrape roster for {nba_playoff_teams_2024[team]}: {e}")
    for _, row in df.iterrows():
        sql = f"""
        INSERT INTO roster (Player_ID, Player_Name, Team_Code, Position, Height, Weight) 
        VALUES ({row['Player ID']}, '{row['Player Name']}', '{row['Team Code']}', '{row['Position']}', '{row['Height']}', '{row['Weight']}');"""
        out.write(sql)
    out.close()

def teamsInserts():
    out = open("teamsInserts.txt", "w")
    sql = f"""
                CREATE TABLE teams(
                    Team_Code VARCHAR(3) NOT NULL PRIMARY KEY,
                    Team_Name VARCHAR(40)
                );
                """
    out.write(sql)
    # team is the three-character code for the playoff teams
    for team in nba_playoff_teams_2024.keys():
        sql = f"""
        INSERT INTO teams (Team_Name, Team_Code) VALUES ('{nba_playoff_teams_2024[team]}'   , '{team}'); 
        """
        out.write(sql)
    out.close()
rosterInserts()
teamsInserts()



