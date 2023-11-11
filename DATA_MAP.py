# -*- coding: utf-8 -*-
import json
import pandas as pd

df = pd.read_json('tenders_data.json', orient='records')

df['tender_time'] = df['tender_time'].apply(lambda x: x.split(' ')[1] + ' ' + x.split(' ')[2])

df['tender_time'] = pd.to_datetime(df['tender_time'], format='%d.%m.%y %H:%M:%S')

# df['tender_time'] = df['tender_time'].dt.strftime('%d.%m.%y')

df['tender_price'] = df['tender_price'].str.replace(' ', '')  # Removing spaces
df['tender_price'] = df['tender_price'].str.replace(',', '.')  # Replacing comma with dot for float conversion
df['tender_price'] = df['tender_price'].astype(float)  # Converting to float

# Очистка колонки tender_name от символа "г."
df['tender_from_name'] = df['tender_from_name'].str.replace(' г.', '')

# Creating new columns "region_code" and "region_name" and using a default value if the split doesn't work
df['region_code'] = 0
df['region_name'] = None


def split_region(x):
    parts = x.split('. ', 1)
    if len(parts) == 2 and parts[0].isdigit():
        return [int(parts[0]), parts[1]]
    else:
        return [0, x]


df[['region_code', 'region_name']] = df['tender_from_name'].apply(lambda x: pd.Series(split_region(x)))


def split_region2(x):
    # splitting by dot followed or preceded by spaces
    parts = x.split('. ', 1)
    return pd.Series(parts)


# Assigning the output to region_code and region_name
df[['region_code', 'region_name']] = df['tender_from_name'].apply(split_region2)

# Replace non-digit character in region_code to NaN then fillna with 0
df['region_code'] = df['region_code'].str.replace('\D+', '', regex=True)
df['region_code'].replace('', 0, inplace=True)

# Converting to integer
df['region_code'] = df['region_code'].astype(int)
df['region_name'] = df['region_name'].fillna('Unknown region') # или другое уместное значение по умолчанию к вашему усмотрению
df.drop('tender_from_name', axis=1, inplace=True)

print(df.dtypes)
print(df)
import folium
from geopy.geocoders import Nominatim
import pandas as pd

# Assuming you have a DataFrame df with the required columns

# Filter rows with region_code not equal to 0
df_filtered = df[df['region_code'] != 0]

# Create a map centered around Russia
map_russia = folium.Map(location=[55.7558, 37.6176], zoom_start=3)

# Geocode region names to get latitude and longitude
geolocator = Nominatim(user_agent="tenders_map")

for index, row in df_filtered.iterrows():
    location = geolocator.geocode(row['region_name'])
    if location:
        # Add a marker for each tender
        folium.Marker(
            location=[location.latitude, location.longitude],
            popup=f"Tender: {row['tender_name']}\nRegion: {row['region_name']}\nPrice: {row['tender_price']}",
            icon=folium.Icon(color='blue')
        ).add_to(map_russia)

# Save the map as an HTML file
map_russia.save('tenders_map.html')
