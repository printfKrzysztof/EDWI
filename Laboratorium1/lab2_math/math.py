import numpy as np

def import_data(file_name):
    with open(file_name, 'r') as file:
        data = file.read().splitlines()
    return data

def parse_geographics(geographics):
    parsed_geographics = []
    for geo in geographics:
        lat, lon = geo.split('/')
        parsed_geographics.append((float(lat), float(lon)))
    return parsed_geographics

def find_most_common_cities(cities):
    city_counts = {}
    for city in cities:
        city_counts[city] = city_counts.get(city, 0) + 1
    sorted_cities = sorted(city_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_cities[:2]

def find_max_rectangle_coordinates(coordinates):
    latitudes = [coord[0] for coord in coordinates]
    longitudes = [coord[1] for coord in coordinates]
    min_latitude = min(latitudes)
    max_latitude = max(latitudes)
    min_longitude = min(longitudes)
    max_longitude = max(longitudes)
    return min_latitude, max_latitude, min_longitude, max_longitude

def divide_into_sectors(geo, min_lat, max_lat, min_lon, max_lon):
    lat_step = (max_lat - min_lat) / 4
    lon_step = (max_lon - min_lon) / 4

    sectors = []
    
    for lat,lon in geo:
        for i in range(4):
            for j in range(4):
                if min_lat+i*lat_step <= lat and max_lat- (3-i) * lat_step >= lat and min_lon+j*lon_step <= lon and max_lon- (3-j) * lon_step >= lon:
                    sectors.append(i*4 + j + 1)
        
    
    return sectors

# Importing data
zip_codes = import_data('lab2_math/zip_codes.txt')
cities = import_data('lab2_math/cities_final.txt')
geographics = import_data('lab2_math/geographics.txt')

# Parsing geographics data
parsed_geographics = parse_geographics(geographics)

# Finding two most common cities
most_common_cities = find_most_common_cities(cities)

print(most_common_cities)
# Filtering zip codes and geographics for the two most common cities
common_city_zip_codes = {}
common_city_geographics = {}
for city, _ in most_common_cities:
    common_city_geographics[city] = [parsed_geographics[i] for i, city_name in enumerate(cities) if city_name == city]
    common_city_zip_codes[city] = [zip_codes[i] for i, city_name in enumerate(cities) if city_name == city]

# Finding max rectangle coordinates for each city
max_rectangles = {}
for city, coordinates in common_city_geographics.items():
    min_lat, max_lat, min_lon, max_lon = find_max_rectangle_coordinates(coordinates)
    max_rectangles[city] = (min_lat, max_lat, min_lon, max_lon)
    
# -----------------
# | 1 | 2 | 3 | 4 |
# | 5 | 6 | 7 | 8 |
# | 9 |10 |11 |12 |
# |13 |14 |15 |16 |
# -----------------
# Dividing max rectangles into sectors and filling it
sectors = {}
for city, coords in max_rectangles.items():
    min_lat, max_lat, min_lon, max_lon = coords
    sectors[city] = divide_into_sectors(common_city_geographics[city], min_lat, max_lat, min_lon, max_lon)


for city, coords in max_rectangles.items():
    #Make file name with city name in it like city.txt
    min_lat, max_lat, min_lon, max_lon = coords
    file_name = f"{city.replace(' ', '_')}.txt"  # Replace spaces with underscores in city name for file name
    
    with open(file_name, 'w') as file:
        #First line: min_lat max_lat min_lon max_lon
        file.write(f"{min_lat} {max_lat} {min_lon} {max_lon}\n")
        
        for code, sector in zip(common_city_zip_codes[city], sectors[city]):
            #All other lines: sector_code zip_code
            file.write(f"{sector} {code}\n")
