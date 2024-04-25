import requests
from bs4 import BeautifulSoup


def fetch_data_and_extract_info(i, j):
    url = f"https://www.geonames.org/postalcode-search.html?q={i}-{j}&country=PL"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        postal_codes = soup.find_all(text=lambda t: t and len(t) == 6 and t[:2].isdigit() and t[2] == '-' and t[3:].isdigit())
        geographics = soup.find_all(text=lambda t: t and '/' in t)
        cities = soup.find_all('td', recursive=True)

        if len(cities) >= 3:
            city_name = cities[6].get_text().strip()
            if city_name and postal_codes and geographics:
                return postal_codes[0], geographics[3], city_name
    return None, None, None


with open('zip_codes.txt', 'w') as zip_file, \
     open('geographics.txt', 'w') as geo_file, \
     open('cities.txt', 'w') as city_file:

    for i in range(100):
        for j in range(1000):
            i_str = str(i).zfill(2)
            j_str = str(j).zfill(3)
            postal_code, geographic, city = fetch_data_and_extract_info(i_str, j_str)
            if postal_code:
                zip_file.write(postal_code + '\n')
                geo_file.write(geographic + '\n')
                city_file.write(city + '\n')

