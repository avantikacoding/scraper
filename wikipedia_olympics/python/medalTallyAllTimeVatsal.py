import requests
from bs4 import BeautifulSoup
import json

def scrape_olympics_medal_tally(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table containing the medal tally
    table = soup.find('table', {'class': 'wikitable sortable'})
    
    # Initialize a list to store the medal tally data
    if table is None:
        print("Table not found on the page.")
        return
    
    medal_tally = []

    # Iterate over each row in the table
    for row in table.find_all('tr')[1:]:
        # Get the cells in the row
        cells = row.find_all( ['th', 'td'])
        # print(cells)
        # Extract the data from the cells
        # print(len(cells),'jdjdjdjdj')
        if len(cells) >= 6:
            rank = cells[0].get_text(strip=True)
            country = cells[1].get_text(strip=True)
            gold = cells[2].get_text(strip=True)
            silver = cells[3].get_text(strip=True)
            bronze = cells[4].get_text(strip=True)
            total = cells[5].get_text(strip=True)
            
            # Append the data as a dictionary to the medal_tally list
            medal_tally.append({
                'Country': country,
                'Rank': rank,
                'Gold': gold,
                'Silver': silver,
                'Bronze': bronze,
                'Total': total
            })
    
    return medal_tally

# URL of the Olympics medal tally page on Wikipedia
url = 'https://en.wikipedia.org/wiki/Summer_Olympic_Games'

# Scrape the medal tally data
medal_tally = scrape_olympics_medal_tally(url)

# Print the scraped data
# for entry in medal_tally:
#     print(entry)
json_object = json.dumps(medal_tally, indent=4)
 
# Writing to sample.json
with open("summerAllTime.json", "w") as outfile:
    outfile.write(json_object)
# print(medal_tally)
