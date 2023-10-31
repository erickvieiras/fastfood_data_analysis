import pandas as pd
import numpy as np
import inflection

def data_cleaning(df):
    #Rename columns
    df.columns = df.columns.map(lambda column_name: '_'.join(column_name.split()).lower())
    #drop NA


    #feature Engineering

    #Creating a new feature to identify the country
    countries = {1: "India", 14: "Australia", 30: "Brazil", 37: "Canada", 94: "Indonesia", 148: "New Zeland", 162: "Philippines",166: "Qatar", 184: "Singapure", 
                189: "South Africa", 191: "Sri Lanka", 208: "Turkey", 214: "United Arab Emirates", 215: "England", 216: "United States of America",}

    df['countries'] = df['country_code'].map(countries)
    df.drop(columns = ['country_code'], axis = 1, inplace = True)

    #Creating a new feature to identify the color for grouping on the map using the folium library in subsequent graphical analyzes
    colors = {"Dark Green":"3F7E00", "Green":"5BA829", "Yellow":"CDD614", "Orange":"FF7800", "White":"FFFCFA", "Red":"E6002A"}
    df['color_code'] = df['rating_color'].map(colors)

    #Deleting some redundant columns that do not add value in the analysis
    df.drop(columns = ['locality', 'locality_verbose', 'switch_to_order_menu'], axis = 1, inplace = True)

    #modifying the 'Price Range' to a categorical variable
    df['price_range'] = df['price_range'].astype(str)
    df['price_range'] = df['price_range'].apply(lambda x: 'cheap' if x == '1' else 'normal' if x == '2' else 'expensive' if x == '3' else 'gourmet')

    #Renaming the column to improve the context of the data it indicates
    df.rename({'is_delivering_now': 'makes_deliveries'}, axis = 1, inplace = True)

    new_order = ['restaurant_id', 'restaurant_name', 'countries', 'city', 'address', 'longitude',
        'latitude', 'cuisines', 'average_cost_for_two', 'currency', 'has_table_booking', 'has_online_delivery', 
        'makes_deliveries', 'price_range', 'aggregate_rating', 'rating_color', 'rating_text',
        'votes', 'color_code']

    df = df[new_order]

    df = df.dropna(subset=['cuisines'])

    return df


