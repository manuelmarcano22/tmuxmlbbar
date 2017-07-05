from bs4 import BeautifulSoup
import requests
import urllib


url = "http://mlb.mlb.com/stats/league_leaders.jsp"


r = urllib.urlopen(url).read()
soup = BeautifulSoup(r)
print type(soup)

