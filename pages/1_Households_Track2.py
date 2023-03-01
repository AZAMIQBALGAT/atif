import pandas as pd
import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import numpy as np
import panel as pn
pn.extension ("tabulator", template="material", sizing_mode="stretch_width")
import holoviews as hv
# import datetime as dt
from streamlit_option_menu import option_menu
from datetime import date,timedelta
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode
import urllib



# #loading online csv
# url="https://kobo.humanitarianresponse.info/api/v2/assets/aGQGms9UUYqNz6sUfwvgxu/export-settings/esHVLDDdUVgCxpJDsFt7gUi/data.csv"#,";")
# #s = requests.get(url).content
# data=pd.read_csv(url, on_bad_lines='skip', sep=";")
# df=data
st.set_page_config(layout="wide")


# Ya code app ko fast karny ka lia ha

@st.cache_data(ttl=600,show_spinner="Fetching data from Server Please Wait...") # 👈  Cache data for 1 hour (=3600 seconds)
def load_data():
# df=load_data.clear()
    #loading online csv
    data="https://kobo.humanitarianresponse.info/api/v2/assets/a6rFkn6z2xSjJXAeAebPzu/export-settings/es38HVZ9R7BAcSFtdCxrEFK/data.csv"#,";")
    # s = requests.get(url).content
    data=pd.read_csv(data, on_bad_lines='skip', sep=";")
    df = pd.DataFrame(data)

    return df
if st.button("Click Me To Get Refresh Data"):
    # Clears all singleton caches:
#     st.experimental_singleton.clear()
    load_data.clear()
df=load_data()



start_date = st.date_input('Select start date:')
end_date = st.date_input('Select end date:')
df.rename(columns = {'Enumerator_Name':'Enumerator Name'}, inplace = True)
df.rename(columns = {'Survey_Day':'Survey Day'}, inplace = True)

df['Survey Day'] = pd.to_datetime(df['Survey Day'])
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)
filtered_df = df[df['Survey Day'].between(start_date, end_date)]
# st.dataframe(filtered_df)
st.subheader("ALLL DATA DONWLOAD AND FILTER DATEWISE")
st.text(f"Total number of forms submitted:{df.shape[0]}")
#ya start date and end date ma jab wo date select kary ga us ki total entries ajay gai
count = filtered_df.count()[0]
st.markdown(f"<span style='color: red;'>Total count between Start Date and End Date: {count}</span>",unsafe_allow_html=True)

# today = dt.datetime.today().strftime('%Y-%m-%d')
# current_day_df = df[df['Survey Day'] == today]
# total_entries = len(current_day_df)
# st.write("Total Entries for Today:", total_entries,today)



grid_table = AgGrid(filtered_df,
                    # theme='balham',
                    enable_enterprise_modules=True,
                    fit_column_on_grid_load=True,
                    height=500,
                    width='100%')


filtered_df.rename(columns = {'_GPS_latitude':'Y'}, inplace = True)
filtered_df.rename(columns = {'_GPS_longitude':'X'}, inplace = True)
filtered_df.rename(columns = {'Enumerator Name':'ID'}, inplace = True)

filtered_df.dropna(subset=['Y'], inplace=True)
filtered_df.dropna(subset=['X'], inplace=True)
filtered_df.dropna(subset=['ID'], inplace=True)

count = filtered_df.count()[0]
st.markdown(f"<span style='color: red;'>Total count GPS Start Date and End Date Between RECEIVE: {count}</span>",unsafe_allow_html=True)
# st.write(filtered_df)

filtered_df.columns = filtered_df.columns.str.strip()
subset_of_df = filtered_df

#1ST MAP
some_map = folium.Map(location=[subset_of_df['Y'].mean(),subset_of_df['X'].mean()],zoom_start=5)
for row in subset_of_df.itertuples():
    some_map.add_child(folium.Marker(location=[row.Y,row.X], popup=row.ID))
st_folium(some_map, width=1500, height=950)


#2ND MAP
some_map_2 = folium.Map(location=[subset_of_df['Y'].mean(),
                                subset_of_df['X'].mean()],
                                zoom_start=10)
mc= MarkerCluster()
for row in subset_of_df.itertuples():
    mc.add_child(folium.Marker(location=[row.Y,row.X], popup=row.ID))
some_map_2.add_child(mc)
st_folium(some_map_2, width=1600, height=950)