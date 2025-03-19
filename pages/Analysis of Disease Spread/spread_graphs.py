import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import config

############# Loading CSV file and Caching them #####################################
def load_spread_df(path):
    spread_df = pd.read_csv(path)
    column_names = spread_df.columns.to_list()
    column_names = [i.replace("_"," ").title() for i in column_names]
    spread_df.columns = column_names
    return spread_df

########################### Plotting Graphs ###############################
def plot_graph(spread_df):
    st.subheader("Time-Series Visualization of Disease Spread")
    st.write('''This interactive line graph visualizes the spread of the disease over time.
                You can use the radio button in the sidebar to select different parameters such as new/total cases and deaths,
                both in absolute numbers and per million population. Additionally, the multiselect box allows you
                to compare multiple countries simultaneously, helping to analyze trends across different regions.''')
    parameter = st.sidebar.radio(
        "Choose the parameter.",
        ['New Cases','Total Cases', 'New Deaths','Total Deaths',
          'New Cases Per Million', 'Total Cases Per Million',
          'New Deaths Per Million', 'Total Deaths Per Million'],
        horizontal=False,
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
    fig.update_layout(xaxis_title = "Date", yaxis_title = parameter)
    st.plotly_chart(fig)

######################### Main Code ###################### 

# Showing the title
title = "Analysis of Disease Spread"
st.set_page_config(page_title = title)
st.title(title)

if 'spread_df' not in st.session_state:
    st.session_state.spread_df = load_spread_df(config.SPREAD_FILE_PATH)

plot_graph(st.session_state.spread_df)
