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

################## Overview ###################################
@st.fragment
def overview(spread_df):
    st.subheader('Overview')
    total_cases = 773956770 
    total_deaths = 7016159
    case_fatality_rate = (total_deaths/total_cases)*100
    
    col1, col2, col3 = st.columns(3)
    
    col1.metric(label="Total COVID-19 Cases", value=f"{total_cases:,}")
    col2.metric(label="Total COVID-19 Deaths", value=f"{total_deaths:,}")
    col3.metric(label="Case Fatality Rate", value= f"{case_fatality_rate:.6f}%")


############ Choropleth Animation #############################
@st.fragment
def choropleth_animation(choropleth_df):
    
    st.subheader("Choropleth Animation of Global and Regional Spread of the Disease Over Time")
    st.write('''This interactive choropleth animation visualizes the spread of the disease over time.
              Use the selectbox to adjust the scope of the map, focusing on a specific continent or the entire
              world. You can also switch between different parameters, such as Total Cases and Total Cases
              Per Million, to gain deeper insights into the impact of the disease across different regions.
              The animation helps track trends over time, highlighting how different areas have been affected.
              ''')
    
    col1, col2 = st.columns(2)
    with col1:
        scope = st.selectbox(
            "Choose the scope.",
            ['World', 'Asia','Europe','Africa', 'North America', 'South America'],
        ).lower()

    with col2:
        parameter = st.selectbox(
            "Choose the parameter.",
            ["Total Cases", "Total Cases Per Million"],
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

########################### Plotting Graphs ###############################
@st.fragment
def plot_graph(spread_df):
    st.subheader("Time-Series Visualization of Disease Spread")
    st.write('''This interactive line graph visualizes the spread of the disease over time.
                You can select different parameters such as new/total cases and deaths, both in absolute numbers
                and per million population. Additionally, the multiselect box allows you to compare multiple
                countries simultaneously, helping to analyze trends across different regions.''')
    parameter = st.selectbox(
        "Choose the parameter.",
        ['New Cases','Total Cases', 'New Deaths','Total Deaths',
          'New Cases Per Million', 'Total Cases Per Million',
          'New Deaths Per Million', 'Total Deaths Per Million'],
    )
    options = st.multiselect(
        "Select the countries",
        spread_df['Country'].unique(),
        ["World"],
    )
    use_log = False
    if('Total' in parameter):
        use_log = st.checkbox("Use Log Scale", value=False)

    fig = px.line(spread_df[spread_df["Country"].isin(options)],
                x = 'Date', y=parameter, color='Country', log_y=use_log)
    fig.update_layout(xaxis_title = "Date", yaxis_title = parameter, hovermode='x unified')
    st.plotly_chart(fig)

######################### Main Code ###################### 
# Showing the title
title = "Analysis of Disease Spread"
st.set_page_config(page_title = title)
st.title(title)

if 'spread_df' not in st.session_state:
    st.session_state.spread_df = load_spread_df(config.SPREAD_FILE_PATH)

if'choropleth_df' not in st.session_state:
    st.session_state.choropleth_df = load_choropleth_df(st.session_state.spread_df)

tabs = st.tabs(['Overview', 'Map','Timeseries'])

with tabs[0]:
    overview(st.session_state.spread_df)
with tabs[1]:
    choropleth_animation(st.session_state.choropleth_df)
with tabs[2]:    
    plot_graph(st.session_state.spread_df)

