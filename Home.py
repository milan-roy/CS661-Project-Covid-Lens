# import streamlit as st
# import os

# pages = {
#     "": [st.Page(os.path.join("pages","Home.py"), 
#                  title="Home")],
#     "": [
#         st.Page(os.path.join("pages","Disease_Spread.py"),
#                 title="Analysis of Disease Spread")
#     ],
    
# }
# pg = st.navigation(pages,)
# pg.run()

import streamlit as st
st.set_page_config(
    page_title="CovidLens",
    page_icon=":mag:"
)
st.title("CovidLens: A lens on Covid data trends")