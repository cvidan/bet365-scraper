# Bet365 Scraper

This is a Python script to grab data for betting odds from the site https://bet365.com/ using Selenium.

## Why Selenium?

I would have preferred to use something like BeautifulSoup, but Bet365 has always been my go-to site for sportsbetting, and as far as I can tell there isn't a way to link directly to a market. For example, there is nothing along the lines of https://bet365.com/basketball/futures/nba/mvp as a way to get to the market for the NBA's Most Valuable Player. So instead, using Selenium we navigate there in Firefox from the home page.

## How to use

The script uses geckodriver for Selenium. The path it expects to find it is 'C:\Program Files\geckodriver\geckodriver.exe'.

Run the SeleniumScraper.py file with three parameters (each exactly as they appear on the site):
1) The sport (e.g. "Basketball")
2) The market (e.g. "NBA Futures 2018/19")
3) The particular bet (e.g. "Regular Season MVP")

So for example,
``` python SeleniumScraper.py "Basketball" "NBA Futures 2018/19" "Regular Season MVP" ```
