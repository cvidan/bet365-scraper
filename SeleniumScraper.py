from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from sys import argv

# The parameters, in order, are the names of the sport, market, and particular bet.
# E.g. >python SeleniumScraper.py "Basketball" "NBA Futures 2018/19" "Regular Season MVP"
SPORT = str(argv[1])
MARKET = str(argv[2])
BET = str(argv[3])

# firefox_options = Options().add_argument("--headless")
# firefox_options.add_argument("--headless")
# driver = webdriver.Firefox(executable_path='C:\Program Files\geckodriver\geckodriver.exe', options=firefox_options)
driver = webdriver.Firefox(executable_path='C:\Program Files\geckodriver\geckodriver.exe')

if __name__ == '__main__':
    # teams = ["ATL Hawks",
    #          "BKN Nets",
    #          "BOS Celtics",
    #          "CHA Hornets",
    #          "CHI Bulls",
    #          "CLE Cavaliers",
    #          "DAL Mavericks",
    #          "DEN Nuggets",
    #          "DET Pistons",
    #          "GS Warriors",
    #          "HOU Rockets",
    #          "IND Pacers",
    #          "LA Clippers",
    #          "LA Lakers",
    #          "MEM Grizzlies",
    #          "MIA Heat",
    #          "MIL Bucks",
    #          "MIN Timberwolves",
    #          "NO Pelicans",
    #          "NY Knicks",
    #          "OKC Thunder",
    #          "ORL Magic",
    #          "PHI 76ers",
    #          "PHX Suns",
    #          "POR Trail Blazers",
    #          "SA Spurs",
    #          "SAC Kings",
    #          "TOR Raptors",
    #          "UTA Jazz",
    #          "WAS Wizards"]

    # All the ugly Try-Except blocks are to decrease the runtime of the script. Without them, the script hits errors
    # with trying to access elements which haven't loaded on the page yet. The Try-Except loop basically just keeps
    # trying to access the elements until they've loaded. The other solution I tried was to sleep() for a set time
    # before trying to access the elements. However, it seriously reduced the runtime so I'm sticking with the ugliness.

    driver.get('https://www.bet365.com/')
    driver.find_element_by_link_text("English").click()

    # go to Basketball markets
    while True:
        try:
            left_menu_div = driver.find_elements_by_class_name("wn-WebNavModule")
            left_menu = left_menu_div[0].find_elements_by_class_name("wn-Classification")
            break
        except:
            pass
    for link in left_menu:
        if link.text == SPORT:
            link.click()
            break

    # go to Futures
    while True:
        try:
            driver.find_elements_by_class_name("sl-LiveInPlayHeader_ButtonBarButton")[1].click()
            break
        except:
            pass

    # find the bet
    while True:
        try:
            nba_futures_div = driver.find_element_by_class_name("sm-MarketGroup")
            break
        except:
            pass
    bets = nba_futures_div.find_elements_by_class_name("sm-CouponLink_Label")
    for bet in bets:
        if bet.text == BET:
            bet.click()
            break

    # grab data
    while True:
        try:
            win_outright_div = driver.find_element_by_class_name("gl-MarketGroupContainer")
            teams = win_outright_div.find_elements_by_class_name("gl-Participant_Name")
            american_odds = win_outright_div.find_elements_by_class_name("gl-Participant_Odds")
            break
        except:
            pass

    # make new list with decimal odds
    num_teams = len(teams)
    if num_teams == 30:
        team_odds_pairs = []
        for i in range(len(teams)):
            sign = american_odds[i].text[0]
            value = int(american_odds[i].text[1:])
            if sign == '-':
                new_odds = (100 / value) + 1.0
            else:
                new_odds = (value / 100) + 1.0

            team_odds_pairs.append((teams[i].text, new_odds))
        team_odds_pairs.sort()
        driver.close()
    else:
        raise Exception("There is data for " + str(num_teams) + " rather than the expected 30!")

    # output the data
    output_record = datetime.now().strftime("%Y-%m-%d")
    for pair in team_odds_pairs:
        if pair[1].is_integer():
            odds = int(pair[1])
        else:
            odds = round(pair[1], 9)
        output_record += "," + str(odds)
    print(output_record)
    # print(datetime.now().strftime("%Y-%m-%d"))
    # for pair in team_odds_pairs:
    #     print(str(pair[0]) + "," + str(pair[1]))
    #     # print(pair[1])

