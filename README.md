# NBA-Wins-Calculator

A program that determines a range of how many games a team would have won in a particular season based on their point differentials

Received data from official basketball stats page basketball-reference.com using Python Web Scraper BeautifulSoup4

Developed an algorithm to calculate the range of games won by a team in a season by using a 95% confidence interval of league average point differential that season to determine games that have a 95%-win percentage

Defined the parameters as anything greater than that range were decisive wins (100%-win chance) and lower were decisive losses (100%-lose chance) and games within the interval had probabilities based on how close to zero they were based on a normal distribution
