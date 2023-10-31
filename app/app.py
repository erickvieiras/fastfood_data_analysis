import pandas as pd
import numpy as np
import plotly.express as px
import data_preprocessing as dp
import matplotlib as plt
import seaborn as sns
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import io
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Page config and load data===================================================================================================================
st.set_page_config(layout="wide")
df = pd.read_csv('../dataset/zomato.csv', low_memory=False, encoding='ISO-8859-1')
df = dp.data_cleaning(df)

#function convert to dataset download=========================================================================================================
def convert_df(dataset):
    csv_data = dataset.to_csv(index=False)
    return csv_data

csv_data = convert_df(df)

#sidebar=======================================================================================================================================
image = Image.open('../img/logo.png')
st.sidebar.image(image)
st.sidebar.title('Restaurant Analytics Finder')
start_value, end_value = st.sidebar.select_slider('Select a Rating Range:', options= np.sort(df['aggregate_rating'].unique()), value=(0, 2.4))


price_range = st.sidebar.multiselect("Select Countries to analyze Restaurants:",
        df.loc[:, "countries"].unique().tolist(),default=["Brazil", "England", "New Zeland", "Indonesia", "Qatar", "Canada"])


option = st.sidebar.selectbox('Select the Type Location:', ('Restaurant', 'City', 'Country'))

bool_param = st.sidebar.selectbox('Select the Highest or Lowest cost for a dish:', ('Highest', 'Lowest'))

#main page=====================================================================================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Home', 'Ratings', 'Geografic View', 'Countries and restaurants', 'Cities and Cuisines'])

with tab1:

    st.header('About Project')
    st.markdown("Restaurant Analytics Finder is a project using public data bringing together the largest number of registered Restaurants by country, with the purpose of helping you find the best culinary option closest to you or your next destination.") 
    st.markdown("The project offers a multitude of options among countries, cuisines and locations with the most varied characteristics.")
    st.markdown("The data analyzed has a series of features that help in decision-making and consumer behavior based on their experience in a particular country, restaurant and cuisine. Among the features we can highlight:")
    st.markdown("1 - Country, City, Restaurant, Cuisine and type of dish;")
    st.markdown("2 - Address and location of each restaurant;")
    st.markdown("3 - Restaurants that deliver online and those that make reservations")
    st.markdown("4 - Currency and Prices;")
    st.markdown("5 - Ratings and votes.")

    st.download_button(
        label="Download CSV Project File",
        data=csv_data,
        file_name='Fastfood Data Analysis.csv',
        mime='text/csv',
    )
    with st.expander('Dataset Information'):
        st.dataframe(df)

with tab2:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Restaurants", df['restaurant_id'].nunique())
    col2.metric("Ratings", df['votes'].sum())
    col3.metric("Cuisines", df['cuisines'].nunique())
    col4.metric("Online Deliveries", df['has_online_delivery'].loc[df['has_online_delivery'] == 'Yes'].count())

    on = st.toggle('Active Range')

    if on:
        start_value, end_value = st.select_slider('Select a Rating Range', options= np.sort(df['aggregate_rating'].unique()), value=(0, 2.4))

    df_aux = df.loc[(df['aggregate_rating'] >= start_value) & (df['aggregate_rating'] <= end_value) ]
    aux = df_aux.groupby(['restaurant_name', 'cuisines'])['aggregate_rating'].mean().reset_index().sort_values(['aggregate_rating'], ascending = False).drop_duplicates(subset=['aggregate_rating']).head(10)
    graph = px.bar(aux, x = 'restaurant_name', y = 'aggregate_rating', color = 'cuisines', text_auto='0.2s', title = 'TOP 10 CUISINE BY RATING')
    st.plotly_chart(graph, use_container_width= True)
    with st.expander('More Info'):
        st.dataframe(aux)
    

    columns1, columns2, columns3 = st.columns(3)
    
    with columns1:
        df_aux = df.loc[(df['aggregate_rating'] >= start_value) & (df['aggregate_rating'] <= end_value) ]
        aux2 = df_aux.groupby(['rating_text'])['aggregate_rating'].mean().reset_index().sort_values(['aggregate_rating'], ascending = True)
        graph2 = px.bar(aux2, x = 'rating_text', y = 'aggregate_rating', text_auto='0.2s', color = 'rating_text', title = 'AVERAGE RATINGS BY EVALUATION CATEGORY')
        st.plotly_chart(graph2, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux2)

    with columns2:
        df_aux = df.loc[(df['aggregate_rating'] >= start_value) & (df['aggregate_rating'] <= end_value) ]
        aux3 = df_aux.groupby(['price_range'])['aggregate_rating'].mean().reset_index().sort_values(['aggregate_rating'], ascending = True)
        graph3 = px.bar(aux3, x = 'price_range', y = 'aggregate_rating', text_auto='0.2s', color = 'price_range', title = 'AVERAGE RATINGS BY DISH')
        st.plotly_chart(graph3, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux3)

    with columns3:
        df_aux = df.loc[(df['aggregate_rating'] >= start_value) & (df['aggregate_rating'] <= end_value) ]
        aux4 = df_aux.groupby(['has_online_delivery'])['aggregate_rating'].mean().reset_index()
        graph4 = px.pie(aux4, names = 'has_online_delivery', values = 'aggregate_rating', color = 'has_online_delivery', title = 'RATINGS AVERAGE BY ONLINE DELIVERIES')
        st.plotly_chart(graph4, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux4)
    cl1, cl2 = st.columns(2)
    with cl1:
        operation = st.selectbox('Select the of Operation: ', ('Mean', 'Total'))
    with cl2:
        bool_param_ = st.selectbox('Select the type of Vote: ', ('Best', 'Worst'))

    if bool_param_ == 'Best':
        bool_param_ = False
    else:
        bool_param_ = True

    if operation == 'Mean':
        aux8 = df_aux.groupby(['countries'])['votes'].mean().reset_index().sort_values(['votes'], ascending = bool_param_)
        graph8 = px.bar(aux8, x = 'countries', y = 'votes', text_auto='0.2s', color = 'countries', title = 'AVERAGE VOTES BY COUNTRY')
        st.plotly_chart(graph8, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux8)
    else:
        aux8 = df_aux.groupby(['countries'])['votes'].sum().reset_index().sort_values(['votes'], ascending = bool_param_)
        graph8 = px.bar(aux8, x = 'countries', y = 'votes', text_auto='0.2s', color = 'countries', title = 'TOTAL VOTES BY COUNTRY')
        st.plotly_chart(graph8, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux8)

with tab3:
    countries = st.multiselect(
        "Choose the countries you want to check",
        df.loc[:, "countries"].unique().tolist(),
        default=["Brazil", "England", "United States of America", "Indonesia", "Canada"]
    )


    def create_map(df_map, zoom=10):

        if len(countries) > 0:
            df_map = df_map[df_map['countries'].isin(countries)] 
            f = folium.Figure(width=1920, height=1080)

            m = folium.Map(max_bounds=True, location=[df_map["latitude"].mean(), df_map["longitude"].mean()], zoom_start=zoom).add_to(f)

            marker_cluster = MarkerCluster().add_to(m)

            for _, line in df_map.iterrows():

                name = line["restaurant_name"]
                price_for_two = line["average_cost_for_two"]
                cuisine = line["cuisines"]
                currency = line["currency"]
                rating = line["aggregate_rating"]
                color = f'{line["color_code"]}'

                html = "<p><strong>{}</strong></p>"
                html += "<p>Price: {},00 ({}) para dois"
                html += "<br />Type: {}"
                html += "<br />Aggragate Rating: {}/5.0"
                html = html.format(name, price_for_two, currency, cuisine, rating)

                popup = folium.Popup(
                    folium.Html(html, script=True),
                    max_width=500,
                )

                folium.Marker(
                    [line["latitude"], line["longitude"]],
                    popup=popup,
                    icon=folium.Icon(color=color, icon="home", prefix="fa"),
                ).add_to(marker_cluster)

            folium_static(m, width=1024, height=768)
        else:
            f = folium.Figure(width=1920, height=1080)

            m = folium.Map(max_bounds=True, location=[df_map["latitude"].mean(), df_map["longitude"].mean()], zoom_start=zoom).add_to(f)

            marker_cluster = MarkerCluster().add_to(m)

            for _, line in df_map.iterrows():

                name = line["restaurant_name"]
                price_for_two = line["average_cost_for_two"]
                cuisine = line["cuisines"]
                currency = line["currency"]
                rating = line["aggregate_rating"]
                color = f'{line["color_code"]}'

                html = "<p><strong>{}</strong></p>"
                html += "<p>Price: {},00 ({}) para dois"
                html += "<br />Type: {}"
                html += "<br />Aggragate Rating: {}/5.0"
                html = html.format(name, price_for_two, currency, cuisine, rating)

                popup = folium.Popup(
                    folium.Html(html, script=True),
                    max_width=500,
                )

                folium.Marker(
                    [line["latitude"], line["longitude"]],
                    popup=popup,
                    icon=folium.Icon(color=color, icon="home", prefix="fa"),
                ).add_to(marker_cluster)

            folium_static(m, width=1024, height=768)

    create_map(df, zoom=2)


with tab4:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Countries", df['countries'].nunique())
    col2.metric("Restaurants", df['restaurant_id'].nunique())
    col3.metric("Cuisines", df['cuisines'].nunique())
    col4.metric("Online Deliveries", df['has_online_delivery'].loc[df['has_online_delivery'] == 'Yes'].count())
    
    on = st.toggle('Active Multiselect')
    if on:
        price_range = st.multiselect("Select countries to analyze behavior:", 
                                     df.loc[:, "countries"].unique().tolist(),default=["Brazil", "England", "New Zeland", "Indonesia", "Qatar", "Canada"])

    if len(price_range) > 0:
        df_aux = df.loc[df['countries'].isin(price_range)]
        df_aux = df_aux.loc[df_aux['countries'] != 'India']
        aux3 = df_aux.groupby(['countries', 'price_range'])['restaurant_id'].count().reset_index()
        graph3 = px.bar(aux3, x = 'countries', y = 'restaurant_id', text_auto='0.2s', color = 'price_range', title = 'PRICING OF GOURMET DISHES BY COUNTRY')
        st.plotly_chart(graph3, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux3)
    else:
        df_aux = df.loc[df['countries'] != 'India']
        aux3 = df_aux.groupby(['countries', 'price_range'])['restaurant_id'].count().reset_index()
        graph3 = px.bar(aux3, x = 'countries', y = 'restaurant_id', text_auto='0.2s', color = 'price_range', title = 'PRICING OF GOURMET DISHES BY COUNTRY')
        st.plotly_chart(graph3, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux3)

    cols1, cols2 = st.columns(2)
    with cols1:
        if len(price_range) > 0:
            df_aux = df.loc[df['countries'].isin(price_range)]        
            aux5 = df_aux.groupby(['has_table_booking'])['restaurant_id'].count().reset_index().sort_values(['restaurant_id'], ascending = False)
            graph5 = px.bar(aux5, x = 'has_table_booking', y = 'restaurant_id', text_auto='0.2s', color = 'has_table_booking', title = 'VOLUMETRY OF RESTAURANTS THAT HAS TABLE BOOKING')
            st.plotly_chart(graph5, use_container_width=True)
            with st.expander('More Info'):
                st.dataframe(aux5)
        else:     
            aux5 = df_aux.groupby(['has_table_booking'])['restaurant_id'].count().reset_index().sort_values(['restaurant_id'], ascending = False)
            graph5 = px.bar(aux5, x = 'has_table_booking', y = 'restaurant_id', text_auto='0.2s', color = 'has_table_booking', title = 'VOLUMETRY OF RESTAURANTS THAT HAS TABLE BOOKING')
            st.plotly_chart(graph5, use_container_width=True)
            with st.expander('More Info'):
                st.dataframe(aux5)


    with cols2:
        aux6 = df.groupby(['has_online_delivery'])['restaurant_id'].count().reset_index()
        graph6 = px.pie(aux6, names = 'has_online_delivery', values = 'restaurant_id', color = 'has_online_delivery', title = 'VOLUMETRY OF RESTAURANTS THAT MAKE ONLINE DELIVERIES')
        st.plotly_chart(graph6, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux6)

    cols4, cols5 = st.columns(2)
    with cols4:
        aux2 = df.groupby(['countries'])['has_online_delivery'].count().reset_index().sort_values(['countries'], ascending = False).head(5)
        graph2 = px.bar(aux2, x = 'countries', y = 'has_online_delivery', text_auto='0.2s', color = 'countries', title = 'TOP 5 COUNTRIES THAT MAKE THE MOST ONLINE DELIVERIES')
        st.plotly_chart(graph2, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux2)
    with cols5:
        aux2 = df.groupby(['countries', 'currency'])['restaurant_id'].count().reset_index().sort_values(['countries'], ascending = False).drop_duplicates(subset=['countries']).head(5)
        graph2 = px.bar(aux2, x = 'currency', y = 'restaurant_id', text_auto='0.2s', color = 'countries', title = 'TOP 5 MOST USED CURRENCIES BY COUNTRIES')
        st.plotly_chart(graph2, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux2)       

with tab5:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Restaurants", df['restaurant_id'].nunique())
    col2.metric("Cities", df['city'].nunique())
    col3.metric("Cuisines", df['cuisines'].nunique())
    col4.metric("Online Deliveries", df['has_online_delivery'].loc[df['has_online_delivery'] == 'Yes'].count())

    on = st.toggle('Active Selectbox')
    if on:
        col5, col6 = st.columns(2)
        with col5:
            option = st.selectbox('Select the location with the highest average custome for 2:', ('Restaurant', 'City', 'Country'))
        with col6:
            bool_param = st.selectbox('Select the highest or lowest cost for a dish for 2:', ('Highest', 'Lowest'))

    if bool_param == 'Highest':
        bool_param = False
    else:
        bool_param = True

    if option == 'City':
        df_aux = df[df['average_cost_for_two'] != 0]
        aux8 = df_aux.groupby(['city', 'countries','currency'])['average_cost_for_two'].mean().reset_index().sort_values(['average_cost_for_two'], ascending = bool_param).drop_duplicates(subset=['countries']).head(10)
        graph8 = px.bar(aux8, x = 'city', y = 'average_cost_for_two', text_auto='0.2s', color = 'currency', title = 'TOP 10 CITIES BY AVERAGE COST OF DISHES FOR 2')
        st.plotly_chart(graph8, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux5)
    elif option == 'Country':
        df_aux = df[df['average_cost_for_two'] != 0]
        aux8 = df_aux.groupby(['countries', 'currency'])['average_cost_for_two'].mean().reset_index().sort_values(['average_cost_for_two'], ascending = bool_param).drop_duplicates(subset=['countries']).head(10)
        graph8 = px.bar(aux8, x = 'countries', y = 'average_cost_for_two', text_auto='0.2s', color = 'currency', title = 'TOP 10 COUNTRIES BY AVERAGE COST OF DISHES FOR 2')
        st.plotly_chart(graph8, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux8)
    else:
        df_aux = df[df['average_cost_for_two'] != 0]
        aux8 = df_aux.groupby(['restaurant_name', 'countries', 'currency'])['average_cost_for_two'].mean().reset_index().sort_values(['average_cost_for_two'], ascending = bool_param).drop_duplicates(subset=['countries']).head(10)
        graph8 = px.bar(aux8, x = 'restaurant_name', y = 'average_cost_for_two', text_auto='0.2s', color = 'currency', title = 'TOP 10 RESTAURANTS BY AVERAGE COST OF DISHES FOR 2')
        st.plotly_chart(graph8, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux8)

    columns10, columns11 = st.columns(2)
    with columns10:
        if option == 'City':
            aux8 = df_aux.groupby(['city', 'countries','currency'])['cuisines'].nunique().reset_index().sort_values(['cuisines'], ascending = bool_param).drop_duplicates(subset=['countries']).head(10)
            graph8 = px.bar(aux8, x = 'city', y = 'cuisines', text_auto='0.2s', color = 'currency', title = 'TOP 10 CITIES BY WITH UNIQUE CUISINE INDEX')
            st.plotly_chart(graph8, use_container_width=True)
            with st.expander('More Info'):
                st.dataframe(aux5)

        elif option == 'Country':
            aux8 = df_aux.groupby(['countries', 'currency'])['cuisines'].nunique().reset_index().sort_values(['cuisines'], ascending = bool_param).drop_duplicates(subset=['countries']).head(10)
            graph8 = px.bar(aux8, x = 'countries', y = 'cuisines', text_auto='0.2s', color = 'currency', title = 'TOP 10 COUNTRIES BY WITH UNIQUE CUISINE INDEX')
            st.plotly_chart(graph8, use_container_width=True)
            with st.expander('More Info'):
                st.dataframe(aux8)
        else:
            aux8 = df_aux.groupby(['restaurant_name', 'countries', 'currency'])['cuisines'].nunique().reset_index().sort_values(['cuisines'], ascending = bool_param).drop_duplicates(subset=['countries']).head(10)
            graph8 = px.bar(aux8, x = 'restaurant_name', y = 'cuisines', text_auto='0.2s', color = 'currency', title = 'TOP 10 RESTAURANTS BY UNIQUE CUISINE INDEX')
            st.plotly_chart(graph8, use_container_width=True)
            with st.expander('More Info'):
                st.dataframe(aux8)

    with columns11:
        if option == 'City':
            aux8 = df_aux.groupby(['city', 'countries','currency'])['aggregate_rating'].mean().reset_index().sort_values(['aggregate_rating'], ascending = bool_param).drop_duplicates(subset=['countries']).head(10)
            graph8 = px.bar(aux8, x = 'city', y = 'aggregate_rating', text_auto='0.2s', color = 'currency', title = 'TOP 10 CITIES BY BY AVERAGE RATINGS')
            st.plotly_chart(graph8, use_container_width=True)
            with st.expander('More Info'):
                st.dataframe(aux5)

        elif option == 'Country':
            aux8 = df_aux.groupby(['countries', 'currency'])['aggregate_rating'].mean().reset_index().sort_values(['aggregate_rating'], ascending = bool_param).drop_duplicates(subset=['countries']).head(10)
            graph8 = px.bar(aux8, x = 'countries', y = 'aggregate_rating', text_auto='0.2s', color = 'currency', title = 'TOP 10 COUNTRIES BY BY AVERAGE RATINGS')
            st.plotly_chart(graph8, use_container_width=True)
            with st.expander('More Info'):
                st.dataframe(aux8)

        else:
            aux8 = df_aux.groupby(['restaurant_name', 'countries', 'currency'])['aggregate_rating'].mean().reset_index().sort_values(['aggregate_rating'], ascending = bool_param).drop_duplicates(subset=['countries']).head(10)
            graph8 = px.bar(aux8, x = 'restaurant_name', y = 'aggregate_rating', text_auto='0.2s', color = 'currency', title = 'TOP 10 RESTAURANTS BY AVERAGE RATINGS')
            st.plotly_chart(graph8, use_container_width=True)
            with st.expander('More Info'):
                st.dataframe(aux8)

    operation = st.selectbox('Select the of Operation:', ('Mean', 'Total'))
    if operation == 'Mean':
        aux8 = df_aux.groupby(['price_range'])['votes'].mean().reset_index().sort_values(['votes'], ascending = bool_param)
        graph8 = px.bar(aux8, x = 'price_range', y = 'votes', text_auto='0.2s', color = 'price_range', title = 'AVERAGE VOTES BY TYPE OF DISH')
        st.plotly_chart(graph8, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux8)
    else:
        aux8 = df_aux.groupby(['price_range'])['votes'].sum().reset_index().sort_values(['votes'], ascending = bool_param)
        graph8 = px.bar(aux8, x = 'price_range', y = 'votes', text_auto='0.2s', color = 'price_range', title = 'TOTAL VOTES BY TYPE OF DISH')
        st.plotly_chart(graph8, use_container_width=True)
        with st.expander('More Info'):
            st.dataframe(aux8)
