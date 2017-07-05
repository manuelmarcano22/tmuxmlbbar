#!/home/mmarcano22/anaconda3/bin/python3
import base64
import requests
from ohmysportsfeedspy import MySportsFeeds                                             
import time
from datetime import date, timedelta, datetime
from sys import stdout
from time import sleep
import os
import json


#define the colors to print to TMUX
class bcolors:
    Y= '#[fg=yellow,bold] '
    RED = '#[fg=red] '


##Print for tmux
class A:
    def __init__(self,pos,char):
        self.pos=pos
        self.char=str(char)
    def move(self):
        self.pos+= -1


#Todays game
def send_request(urlrequest,fordate):
    # Request
    try:
        response = requests.get(
                url=urlrequest,
            params={
                "fordate": fordate
            },
            headers={
                "Authorization": "Basic " + base64.b64encode('manuelmarcano22' + ":" + '221291')
            }
        )
        content=json.loads(response.content)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')
    return content



#Login to API
msf = MySportsFeeds(version="1.0") 
msf.authenticate('username','password')

#get todays and yesterday date
today = datetime.strptime(date.today().strftime('%Y%m%d'), '%Y%m%d') 
yesterday = datetime.strptime(date.today().strftime('%Y%m%d'), '%Y%m%d') - timedelta(days=1)
#Get date in format to call the API
todayurl = today.strftime('%Y%m%d')
yurl = yesterday.strftime('%Y%m%d')


while True:

    try:
        gametod = msf.msf_get_data(league='mlb', season='2017', feed='scoreboard',fordate=todayurl, format='json')
    except:
        gametod = send_request(\
                'https://www.mysportsfeeds.com/api/feed/pull/mlb/2017-regular/scoreboard.json'\
                ,todayurl)


    #Yesterday game
    gamey = msf.msf_get_data(league='mlb', season='2017', feed='scoreboard',fordate=yurl, format='json')

    # Get the scores
    allgamestod = gametod['scoreboard']['gameScore']
    allgamesy = gamey['scoreboard']['gameScore']

    #Populate the lists to print
    #yesterdays game list
    yesterdaylist = ['Yesterdays Games:']
    for i in allgamesy:
        game = i['game']
        hometeam = game['homeTeam']['Abbreviation']
        awayteam = game['awayTeam']['Abbreviation']
        homescore = '('+i['homeScore']+')'
        awayscore = '('+i['awayScore']+')'
        t = '[' + awayteam+awayscore +' at ' + hometeam+homescore +']'
        yesterdaylist.append(t)

    joinlistyes = '--'.join(yesterdaylist)


    #Today game list
    todaylist = ['Today Games:']
    for i in allgamestod:
        game = i['game']
        hometeam = game['homeTeam']['Abbreviation']
        awayteam = game['awayTeam']['Abbreviation']
        try:
            homescore = '('+i['homeScore']+')'
            awayscore = '('+i['awayScore']+')'
            t = '[' + awayteam+awayscore +' at ' + hometeam+homescore +']'
        except:
            t = '[' + awayteam +' at ' + hometeam +']'
        todaylist.append(t)

    joinlisttoday = '--'.join(todaylist)

    leaders = ["Division Leaders:"]

    urldiv = 'https://www.mysportsfeeds.com/api/feed/pull/mlb/2017-regular/division_team_standings.json?teamstats=W,L,GB'

    leads = send_request(urldiv,todayurl)
    leadsall = leads['divisionteamstandings']['division']


    for division in leadsall:
        leaders.append(division['@name']+':')
        for teams in division['teamentry']:
            #leaders.append(teams['team']['Abbreviation']+'('+teams['rank']+')')
            leaders.append(teams['team']['Abbreviation']+'(GB:'+teams['stats']['GamesBack']['#text']+')')

    joinlistlead = '--'.join(leaders)

    text = 'Boo Sam'
    texts =[text,joinlistyes,joinlisttoday,joinlistlead]

    for loops in  range(10):
        for t in texts:
            aas=[]
            for i,j in enumerate(t):
                aas.append(A(i+47+7,j))
                #tmps=['n']
    #        tmp=["/"]+["-"]*48+["\\"]+[' ']*10
            for t in range(len(t)+ 47+7):
                #stdout.write("\b"*60)
                tmp=["#[fg=white]/"]+\
                        ["#[fg=colour1,bold]"]+\
                        ["-"]*8+\
                        ["#[fg=colour166,bold]"]+\
                        ["-"]*8+\
                        ["#[fg=yellow,bold]"]+\
                        ["-"]*8+\
                        ["#[fg=green,bold]"]+\
                        ["-"]*8+\
                        ["#[fg=blue,bold]"]+\
                        ["-"]*8+\
                        ["#[fg=purple,bold]"]+\
                        ["-"]*8+\
                        ["#[fg=white]\\"]+[' ']*10
                tmps=""
#                colors = [1,10,19,28,37,46]
                colors = {"#[fg=colour1,bold]":1,"#[fg=colour166,bold]":10,"#[fg=yellow,bold]":19,"#[fg=green,bold]":28,"#[fg=blue,bold]":37,"#[fg=purple,bold]":46}
                for a in aas:
                    if a.pos!=0 and a.pos < 50+5 and a.pos >0:
                        tmp[a.pos]=a.char
                    a.move()
                #Put colors
                colored = True
                if colored:
                    for key,value in colors.iteritems():
                        tmp[value] = key+tmp[value]
                for i in range(len(tmp)):
                    tmps+=tmp[i]
#                stdout.write("\x1b]2;"+tmps+"\x07")
#                stdout.write(tmps)
#                stdout.flush()
                os.system('echo "'+tmps+'" > ~/games.txt')
                sleep(.2)
