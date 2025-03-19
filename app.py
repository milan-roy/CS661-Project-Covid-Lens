import streamlit as st
import os

pages = {
    "": [st.Page(os.path.join("pages","Home.py"), 
                 title="Home")],
    "Analysis of Disease Spread": [
        st.Page(os.path.join("pages","Analysis of Disease Spread","choropleth_animation.py"), 
                title="Choropleth Animation of Disease Spread"),
        st.Page(os.path.join("pages","Analysis of Disease Spread","spread_graphs.py"),
                title="Time-Series Visualization of Disease Spread"),
    ],
    
}
pg = st.navigation(pages,)
pg.run()