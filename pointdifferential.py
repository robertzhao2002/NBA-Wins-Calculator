from urllib.request import urlopen
from bs4 import BeautifulSoup
import statistics as stat
from math import sqrt

#Here is the calculations for the entire league of the given season. I calculated the average point differentials 
# and found the population standard deviation.
def convertText(l):
    for i in range(len(l)):
        points = l[i].text
        if len(points.strip()) > 0:
            l[i] = int(points)
        else:
            l[i] = 0

def average(l):
    sum = 0
    for i in l:
        sum+=i
    return(sum/(len(l)))
year = int(input('Enter year (format: YYYY): '))
seasonmonths = []
url = "https://www.basketball-reference.com/leagues/NBA_{}_games.html".format(year)
html = urlopen(url)
soup = BeautifulSoup(html, features='html.parser')
months = soup.findAll('div', {'class': 'filter'})
for month in months:
    monthtag = month.find_all('a')
    for i in monthtag:
        seasonmonths.append(i.text.lower())
urllist = []
for month in seasonmonths:
    urlformat = "https://www.basketball-reference.com/leagues/NBA_{0}_games-{1}.html".format(year, month)
    urllist.append(urlformat)
pointdifferentials = []
for u in urllist:
    url = u
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')
    visitor = soup.findAll('td', {'data-stat': 'visitor_pts'})
    home = soup.findAll('td', {'data-stat': 'home_pts'})
    convertText(visitor)
    convertText(home)
    for a in range(len(visitor)):
        pointdifferentials.append(abs(visitor[a]-home[a]))
#print(pointdifferentials)
average_pointdifferential = average(pointdifferentials)
population_deviation = stat.pstdev(pointdifferentials)
#print(population_deviation)
print("Teams this season won their games by an average of", str(average_pointdifferential), "points.")
#This is the section for the statistics for a team that season.
team = input('Enter team abbreviation (e.g. ATL for Atlanta Hawks): ')
teamurl = 'https://www.basketball-reference.com/teams/{0}/{1}_games.html'.format(team, year)
html = urlopen(teamurl)
soup = BeautifulSoup(html, features='html.parser')
regseason = soup.findAll('div', {'id': 'all_games'})
for games in regseason:
    selfscore = games.find_all('td', {'data-stat': 'pts'})
    oppscore = games.find_all('td', {'data-stat': 'opp_pts'})
    selfscores = []
    oppscores = []
    for score1, score2 in zip(selfscore, oppscore):
        score1Value = score1.text
        score2Value = score2.text
        if len(score1Value.strip()) > 0 and len(score2Value.strip()) > 0:
            selfscores.append(int(score1.text))
            oppscores.append(int(score2.text))
        else:
            continue
teamdifferential = [] #<0 means loss, >0 means win
true_difference = [] #absolute value of difference
wins = 0
win = True
for i in range(len(selfscores)):
    win = selfscores[i] > oppscores[i]
    if win:
        wins+=1
    teamdifferential.append(selfscores[i] - oppscores[i])
    true_difference.append(abs(selfscores[i] - oppscores[i]))
average_teamdiff = average(true_difference)
sample_dev = stat.stdev(true_difference)
#print(sample_dev)
standard_error = sample_dev/(sqrt(len(selfscores)))
pointrange = (average_teamdiff-2*standard_error, average_teamdiff+2*standard_error)
close_G = 0
close_W = 0
close_L = 0
in_range = 0
in_range_W = 0
in_range_L = 0
decisive_W = 0
decisive_L = 0
for i in teamdifferential:
    ab = abs(i)
    if ab >= pointrange[1]:
        if i > 0:
            decisive_W+=1
        else:
            decisive_L+=1
    elif ab <= pointrange[0]:
        close_G+=1
        if i > 0:
            close_W+=1
        else:
            close_L+=1
    elif ab >= pointrange[0] and ab <= pointrange[1]:
        in_range+=1
        if i > 0:
            in_range_W+=1
        else:
            in_range_L+=1
in_range_prop = in_range_W/in_range
close_prop = close_W/close_G
range_chance = in_range_prop*(1+(1-in_range_prop)/2)
close_chance = close_prop*(1+(1-close_prop)/2)
win_range = (round(decisive_W + (0.95*in_range_prop*in_range) + (0.5*close_prop*close_G)), round(decisive_W + (range_chance*in_range) + (close_chance*close_G)))
#The formula for least wins is the actual proportion of games (in the vitory margin interval) * 0.95 + decisive wins + 50% of close games
#The formula for most wins is the decisive wins + actual proportion of both plus 1/2 of remaining proportion of margin and close games
print("This team went", str(wins)+"-"+str(close_L+in_range_L+decisive_L))
print("This team could've won anywhere from", win_range[0],"to", win_range[1], "games in the", str(year-1)+"-"+str(year), "season based on how close their games were.")




