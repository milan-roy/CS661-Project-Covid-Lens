import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config
import numpy as np

############# Loading CSV file and Caching them #####################################
def load_spread_df(path):
    spread_df = pd.read_csv(path)
    column_names = spread_df.columns.to_list()
    column_names = [i.replace("_"," ").title() for i in column_names]
    spread_df.columns = column_names
    return spread_df

def load_choropleth_df(spread_df):
    choropleth_df = spread_df.dropna()
    choropleth_df['Date'] = pd.to_datetime(choropleth_df['Date'])
    choropleth_df['year_month'] = choropleth_df['Date'].dt.to_period('M')
    choropleth_df = choropleth_df.groupby(['Country', 'year_month']).last().reset_index()
    choropleth_df.drop('year_month', axis=1, inplace=True)
    choropleth_df['Date'] = choropleth_df['Date'].dt.date
    return choropleth_df

############ Choropleth Animation #############################
def choropleth_animation(choropleth_df):
    
    st.subheader("Choropleth Animation of Global and Regional Spread of the Disease Over Time")
    st.write("This interactive choropleth animation visualizes the spread of the disease over time. Use the sidebar to adjust the scope of the map, focusing on a specific continent or the entire world. You can also switch between different parameters, such as Total Cases and Total Cases Per Million, to gain deeper insights into the impact of the disease across different regions. The animation helps track trends over time, highlighting how different areas have been affected.")
    scope = st.sidebar.radio(
        "Choose the scope.",
        ['World', 'Asia','Europe','Africa', 'North America', 'South America'],
        key="scope",
        horizontal=False,
    ).lower()

    parameter = st.sidebar.radio(
        "Choose the parameter.",
        ["Total Cases", "Total Cases Per Million"],
        key = "Parameter",
        horizontal = False
    )

    fig = px.choropleth(
                choropleth_df,
                locations='Isocode',
                color = parameter,
                hover_name='Country',
                color_continuous_scale='Greens',
                animation_frame='Date',
                title=f'{parameter} Over Time For {scope.title()}',
                range_color=[0,10e5],
                scope=scope,
    )
    fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 300
    fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 0
    fig.update_layout(
        width=1500,  
        height = 500,
        margin=dict(l=0, r=0, t=50, b=0) 
    )
    st.plotly_chart(fig,use_container_width=False)

######################### Main Code ###################### 

# Showing the title
title = "Analysis of Disease Spread"
st.set_page_config(page_title = title)
st.title(title)

if 'spread_df' not in st.session_state:
    st.session_state.spread_df = load_spread_df(config.SPREAD_FILE_PATH)

if'choropleth_df' not in st.session_state:
    st.session_state.choropleth_df = load_choropleth_df(st.session_state.spread_df)

choropleth_animation(st.session_state.choropleth_df)


