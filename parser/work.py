import requests
from bs4 import BeautifulSoup
import pandas as pd


# Function to extract data from a single page
def extract_data_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    launches = soup.find_all('div', class_='mdl-card')

    data = []
    for launch in launches:
        organisation = launch.find('div', class_='mdl-card__title-text').get_text(strip=True)
        location = launch.find('div', class_='mdl-card__title-text').get_text(strip=True)

        details = launch.find('p', class_='mdl-card__supporting-text').get_text(strip=True)
        price = launch.find('div', class_='price').get_text(strip=True) if launch.find('div', class_='price') else 'N/A'
        status = launch.find('div', class_='status').get_text(strip=True)
        mission_status = launch.find('div', class_='mission-status').get_text(strip=True)

        data.append({
            'Organisation': organisation,
            'Location': location,
            'Details': details,
            'Price': price,
            'Status': status,
            'Mission_Status': mission_status,
        })
    return data


# Loop through pages and collect all data
all_data = []
page = 1
while True:
    print(f'Scraping page {page}')
    url = f'https://nextspaceflight.com/launches/past/?page={page}&search='
    page_data = extract_data_from_page(url)
    if not page_data:  # Break if no more data is found
        break
    all_data.extend(page_data)
    page += 1

# Convert data to a DataFrame and save to a CSV file
df = pd.DataFrame(all_data)
df.to_csv('space_launches.csv', index=False)
print('Data saved to space_launches.csv')