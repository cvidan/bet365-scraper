from requests import get
from bs4 import BeautifulSoup
import sys
from datetime import datetime


class VegasInsiderScraper:

    teams = ["Hawks",
             "Nets",
             "Celtics",
             "Hornets",
             "Bulls",
             "Cavaliers",
             "Mavericks",
             "Nuggets",
             "Pistons",
             "Warriors",
             "Rockets",
             "Pacers",
             "Clippers",
             "Lakers",
             "Grizzlies",
             "Heat",
             "Bucks",
             "T-Wolves",    # discrepancy (was Timberwolves)
             "Pelicans",
             "Knicks",
             "Thunder",
             "Magic",
             "76ers",
             "Suns",
             "Blazers",
             "Spurs",
             "Kings",
             "Raptors",
             "Jazz",
             "Wizards"]

    def __init__(self, url, output_filename):
        self.__output_filename = output_filename
        self.__page = get(url)
        if self.__page.status_code == 200:
            self.__soup = BeautifulSoup(self.__page.content, "html.parser")
        else:
            sys.exit(1)
        self.__team_odds_pairs = []

    def scrape(self):
        div = self.__soup.find(id="_")
        text = div.get_text().split('\n\n\n\n')
        num_teams = int(len(text) / 2)
        text = text[:num_teams*2]
        for i in range(len(text)):
            text[i] = text[i].lstrip()
        self.__create_team_odds_list(text)
        self.__append_to_csv()

        # table = self.__soup.find_all('table', class_="table-wrapper cellTextNorm")[0]
        # rows = table.find_all('tr')[1:]
        # num_teams = len(rows)
        # if num_teams == 30:
        #     self.__create_team_odds_list(rows)
        #     self.__append_to_csv()
        # else:
        #     raise Exception("There is data for " + str(num_teams) + " rather than the expected 30")

    def __create_team_odds_list(self, text):
        i = 0
        while i < len(text):
            team = text[i]
            odds = self.__convert_to_decimal(text[i + 1])
            self.__team_odds_pairs.append((team, odds))
            i += 2
        # for i in range(len(text)):
        #     row = text[i].find_all('td')
        #     team = row[0].get_text()
        #     odds = self.__convert_to_decimal(row[1].get_text())
        #     self.__team_odds_pairs.append((team, odds))
        return self.__team_odds_pairs.sort()

    def __convert_to_decimal(self, odds):
        sign = odds[0]
        value = int(odds[1:])
        if sign == '-':
            new_odds = (100 / value) + 1.0
        else:
            new_odds = (value / 100) + 1.0
        # numerator = int(odds.split('/')[0])
        # denominator = int(odds.split('/')[1])
        # new_odds = numerator / denominator + 1
        if new_odds.is_integer():
            return str(int(new_odds))
        else:
            return str(round(new_odds, 9))

    def __append_to_csv(self):
        output_record = datetime.now().strftime("%Y-%m-%d")
        scraped_teams = "DATE"
        for pair in self.__team_odds_pairs:
            scraped_teams += "," + pair[0].split(" ")[-1]
        for odds in self.__create_list_of_scraped_teams(scraped_teams):
            output_record += "," + odds
        with open(self.__output_filename, "a") as out_file:
            out_file.write(output_record + "\n")

    def __create_list_of_scraped_teams(self, scraped_teams):
        i = 0
        odds_list = []
        for team in self.teams:
            if team not in scraped_teams:
                odds_list.append("10000")
            else:
                odds_list.append(self.__team_odds_pairs[i][1])
                i += 1
        return odds_list



if __name__ == "__main__":
    url = "https://www.sportsbook.ag/sbk/sportsbook4/nba-betting/nba-futures-championship.sbk"
    filename = "C:\\Users\\curti\\OneDrive\\Documents\\odds.txt"
    scraper = VegasInsiderScraper(url, filename)
    scraper.scrape()
