from requests import get
from bs4 import BeautifulSoup
import sys
from datetime import datetime


class VegasInsiderScraper:

    def __init__(self, url, output_filename):
        self.__output_filename = output_filename
        self.__page = get(url)
        if self.__page.status_code == 200:
            self.__soup = BeautifulSoup(self.__page.content, "html.parser")
        else:
            sys.exit(1)
        self.__team_odds_pairs = []

    def scrape(self):
        table = self.__soup.find_all('table', class_="table-wrapper cellTextNorm")[0]
        rows = table.find_all('tr')[1:]
        num_teams = len(rows)
        if num_teams == 30:
            self.__create_team_odds_list(rows)
            self.__append_to_csv()
        else:
            raise Exception("There is data for " + str(num_teams) + " rather than the expected 30")

    def __create_team_odds_list(self, rows):
        for i in range(len(rows)):
            row = rows[i].find_all('td')
            team = row[0].get_text()
            odds = self.__convert_to_decimal(row[1].get_text())
            self.__team_odds_pairs.append((team, odds))
        return self.__team_odds_pairs.sort()

    def __convert_to_decimal(self, odds):
        numerator = int(odds.split('/')[0])
        denominator = int(odds.split('/')[1])
        new_odds = numerator / denominator + 1
        if new_odds.is_integer():
            return str(int(new_odds))
        else:
            return str(round(new_odds, 9))

    def __append_to_csv(self):
        output_record = datetime.now().strftime("%Y-%m-%d")
        for pair in self.__team_odds_pairs:
            odds = str(pair[1])
            output_record += "," + odds
        with open(self.__output_filename, "a") as out_file:
            out_file.write(output_record + "\n")


if __name__ == "__main__":
    vi_url = "http://www.vegasinsider.com/nba/odds/futures/"
    filename = "C:\\Users\\curti\\OneDrive\\Documents\\odds.txt"
    scraper = VegasInsiderScraper(vi_url, filename)
    scraper.scrape()
