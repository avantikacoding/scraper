import requests
from bs4 import BeautifulSoup
import json

def scrape_olympics_medal_tally(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing the medal tally
        table = soup.find('table', {'class': 'wikitable sortable notheme plainrowheaders jquery-tablesorter'})
        
        # Initialize a list to store the medal tally data
        if table is None:
            raise Exception("Table not found on the page.")
        
        medal_tally = []    

        rows = table.find_all('tr')

        rankedRow= -1
        for index in range(1, len(rows) - 1):
            row = rows[index]
            cells = row.find_all(['th', 'td'])
            if len(cells) >= 6:
                rankedRow = index
                rank = cells[0].get_text(strip=True)
                country = cells[1].get_text(strip=True)
                gold = cells[2].get_text(strip=True)
                silver = cells[3].get_text(strip=True)
                bronze = cells[4].get_text(strip=True)
                total = cells[5].get_text(strip=True)
            elif len(cells) == 5:
                lastRow = rows[rankedRow].find_all(['th', 'td'])
                rank = lastRow[0].get_text(strip=True)
                country = cells[0].get_text(strip=True)
                gold = cells[1].get_text(strip=True)
                silver = cells[2].get_text(strip=True)
                bronze = cells[3].get_text(strip=True)
                total = cells[4].get_text(strip=True)
            
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
    
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)
    except Exception as e:
        print("Error:", e)

    return None

url = 'https://en.wikipedia.org/wiki/2020_Summer_Olympics_medal_table'
medal_tally = scrape_olympics_medal_tally(url)

if medal_tally is not None:
    json_object = json.dumps(medal_tally, indent=4)
    with open("final.json", "w") as outfile:
        outfile.write(json_object)
