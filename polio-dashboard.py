
#import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np
import panel as pn
pn.extension ("tabulator", template="material", sizing_mode="stretch_width")
import holoviews as hv
import folium
import hvplot.pandas
# import datetime as dt
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import date,timedelta
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import requests
import time
import hashlib


#   Page configuration
st.set_page_config(
    page_title="DASHBOARD Polio",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.sidebar.success("SELECT A PAGE OR REPORT.")


#ya code data fetch larny la lia ha simple
# #loading online csv
# url="https://kobo.humanitarianresponse.info/api/v2/assets/aGQGms9UUYqNz6sUfwvgxu/export-settings/esHVLDDdUVgCxpJDsFt7gUi/data.csv"#,";")
# #s = requests.get(url).content
# df_google_sheet=pd.read_csv(url, on_bad_lines='skip', sep=";")
# df=df_google_sheet


# # Ya code app ko fast karny ka lia ha
#loading online csv
# data = "https://kobo.humanitarianresponse.info/api/v2/assets/aGQGms9UUYqNz6sUfwvgxu/export-settings/esHVLDDdUVgCxpJDsFt7gUi/data.csv"

# @st.cache(hash_funcs={requests.Response: lambda _: int(time.time())})
# def load_data():
#     response = requests.get(data)
#     df = pd.read_csv(data, sep=';', on_bad_lines='skip')
#     return df

# df = load_data()
# st.write(df)
# st.write("Data last updated at: ", time.ctime(time.time()))
# df=load_data()


# Ya code app ko fast karny ka lia ha

# def load_data():

#     #loading online csv
#     data="https://kobo.humanitarianresponse.info/api/v2/assets/aGQGms9UUYqNz6sUfwvgxu/export-settings/esHVLDDdUVgCxpJDsFt7gUi/data.csv"#,";")
#     # s = requests.get(url).content
#     data=pd.read_csv(data, on_bad_lines='skip', sep=";")
#     df = pd.DataFrame(data)
#     return df

# @st.cache(suppress_st_warning=True,allow_output_mutation=True)


# URL = "https://kobo.humanitarianresponse.info/api/v2/assets/aGQGms9UUYqNz6sUfwvgxu/export-settings/esHVLDDdUVgCxpJDsFt7gUi/data.csv"

# last_data_update_time = None

# def hash_data(data):
#     data_str = data.to_csv().encode()
#     return hashlib.sha256(data_str).hexdigest()

# @st.cache(suppress_st_warning=True,allow_output_mutation=True, hash_funcs={pd.DataFrame: hash_data})
# def get_data():
#     data = pd.read_csv(URL, sep=";", on_bad_lines='skip')
#     return data

# data = get_data()

# if st.button("Refresh data"):
#     new_data = get_data()
#     if new_data.equals(data) == False:
#         data = new_data
#         last_data_update_time = time.time()
#         st.warning(f"Data updated at {last_data_update_time}. New data is available.")

# # Continue processing data as needed...




URL = "https://kobo.humanitarianresponse.info/api/v2/assets/aGQGms9UUYqNz6sUfwvgxu/export-settings/esHVLDDdUVgCxpJDsFt7gUi/data.csv"

last_data_update_time = None
def get_data_timestamp():
    response = requests.head(URL)
    last_modified = response.headers.get('last-modified')
    last_modified_time = time.mktime(time.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z'))
    return last_modified_time

@st.cache(suppress_st_warning=True,allow_output_mutation=True)
def get_data():
    data = pd.read_csv(URL, sep=";", on_bad_lines='skip')
    return data

data = get_data()
data_timestamp = get_data_timestamp()

if st.button("Refresh data"):
    new_data = get_data()
    new_data_timestamp = get_data_timestamp()
    if new_data_timestamp != data_timestamp:
        data = new_data
        data_timestamp = new_data_timestamp
        st.warning(f"Data updated at {data_timestamp}. New data is available.")


def get_data_timestamp():
    response = requests.head(URL)
    last_modified = response.headers.get('last-modified')
    if last_modified is None:
        return None
    last_modified_time = time.mktime(time.strptime(last_modified, '%a, %d %b %Y %H:%M:%S %Z'))
    return last_modified_time




# #AZAM CODE Feature 1 Minimalize the Defaut (ap hide kar sakty ho header and footer jis pa streamlit likha hota ha)
# hide_menu_style = """
#     <style>
#     MainMenue {visibility: hidden;}
#     footer {visibility: hidden;}
#     </style>
#     """
# st.markdown(hide_menu_style, unsafe_allow_html=True)
# # useful_data=df_google_sheet[["Enumerator Name","Enumerator Mobile","Survey Day","Union Council","UC","DISTRICT","TEHISL","Vaccination_Strategy","Monthly_Target"]]
# #1- Load the CSV file and extract the unique values from the "UC" column and sort A-Z:
# unique_ucs = sorted(data["UC"].unique())
# #2- Create the selectbox and assign it to a variable:
# # uc_selectbox = st.selectbox("SELECT UC:",unique_ucs)
# # st.markdown(f"<span style='color: red;'>SELECT UC</span>",unsafe_allow_html=True)
# uc_selectbox = st.radio("SELECT UC:",unique_ucs)
# #2.1- radio button ko horizontal to vertically ma convert kar day ga space ki bachat ho gai:
# st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

# #3- Display the data for the selected Uc:
# selected_data = data[data["UC"] == uc_selectbox]
# #3.1 - ya extra code ha is ma jab wo uc select kary ga us ka count b ajay ga selected
# count = selected_data.count()[0]
# st.markdown(f"<span style='color: red;'>Total count till Date: {count}</span>",unsafe_allow_html=True)
# #4- Display the data for the selected Uc IN TABLE:




# gb = GridOptionsBuilder.from_dataframe(data)
# gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
# gb.configure_side_bar() #Add a sidebar
# # gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
# gridOptions = gb.build()

# grid_response = AgGrid(
#     selected_data,
#     gridOptions=gridOptions,
#     data_return_mode='AS_INPUT', 
#     update_mode='MODEL_CHANGED', 
#     fit_columns_on_grid_load=False,
#     # theme='blue', #Add theme color to the table
#     enable_enterprise_modules=True,
#     height=540, 
#     width='100%',
#     reload_data=True
# )



# #Column names ko change karna
# selected_data.rename(columns = {'_GPS_latitude':'lat'}, inplace = True)
# selected_data.rename(columns = {'_GPS_longitude':'lon'}, inplace = True)
# #Column ma sa nan wali values ko khatm karna
# selected_data.dropna(subset=['lat'], inplace=True)
# selected_data.dropna(subset=['lon'], inplace=True)
# count = selected_data.count()[0]
# st.markdown(f"<span style='color: red;'>Total count GPS till Date RECEIVE: {count}</span>",unsafe_allow_html=True)
# #Display the GPS IN MAPBOX
# st.map(selected_data)










# # selected_data.dropna(subset=['city'], inplace=True)

# # st.map(selected_data, marker_size=0.5)

# # LAT = selected_data["lat"]
# # LON = selected_data["lon"]
# # city = selected_data["city"]



# # df= ['']
# # st.write(selected_data)

# # LAT = selected_data["lat"]
# # LON = selected_data["lon"]
# # name = selected_data["name"]

# # st.map(LAT, LON)
# # count = selected_data.count()[0]
# # st.markdown(f"<span style='color: red;'>Total count GPS till Date RECEIVE: {count}</span>",unsafe_allow_html=True)
# # #Display the GPS IN MAPBOX
# # st.map(selected_data, text=name)