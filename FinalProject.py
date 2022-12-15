"""
Class: CS230--Section 4
Name: Tan Jin Tin, Cheryl
Date: 14 December 2022
Description: Final Project - Interactive Data-Explorer
I pledge that I have completed the programming assignment independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""
# To run program in terminal: streamlit run FinalProject.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk

DATAFILE = "Volcano_Eruptions.csv"

# Function to read data file
def get_data(filename):
    df = pd.read_csv(filename)
    return df


# Function to update primary volcano types
def update_file(df):
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Caldera(s)': 'Caldera'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Complex(es)': 'Complex'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Cone(s)': 'Cone'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Explosion crater(s)': 'Explosion crater'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Fissure vent(s)': 'Fissure vent'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Lava cone(es)': 'Lava cone'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Lava cone(s)': 'Lava cone'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Lava dome(s)': 'Lava dome'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Maar(s)': 'Maar'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Pyroclastic cone(s)': 'Pyroclastic cone'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Shield(s)': 'Shield'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Stratovolcano(es)': 'Stratovolcano'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Stratovolcano?': 'Stratovolcano'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Submarine(es)': 'Submarine'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Tuff cone(s)': 'Tuff cone'})
    df['Primary Volcano Type'] = df['Primary Volcano Type'].replace({'Tuff ring(s)': 'Tuff ring'})
    df.to_csv(DATAFILE, index=False)


# Start of Website
st.title("Volcanic Eruptions Worldwide")
st.image("volcano.jpg")
st.markdown(
    """Explore volcanic eruptions all around the world -- Learn more about the locations of volcanoes,
their primary type, height, rock type and more!""")

# Query 1 - Volcanoes by Geography
st.header("1. Volcanoes by Geography")
st.subheader("Pick a region")
st.markdown(
    """Use the "Region" dropdown list in the sidebar to pick a region. View the list of volcanoes in your selected region here. 
    You can also check out the country, activity evidence, last known eruption, and subregion of these volcanoes.""")
df1 = get_data(DATAFILE)
regions = df1['Region'].unique()
region_choice = st.sidebar.selectbox('Region', regions)
new_df = df1.query('Region == @region_choice')
st.write(new_df[['Volcano Name', 'Country', 'Activity Evidence', 'Last Known Eruption', 'Subregion']])

# Map
st.markdown(
    """View a map of all the volcanoes in your selected region below.""")
midpoint = (np.average(new_df["Latitude"]), np.average(new_df["Longitude"]))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state=pdk.ViewState(
        latitude=midpoint[0],
        longitude=midpoint[1],
        zoom=11,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=new_df[['Latitude', 'Longitude']],
            get_position=["Longitude", "Latitude"],
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=3,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_fill_color=[255, 140, 0],
            get_line_color=[0, 0, 0],
        ),
    ],
))

# Query 2 - Volcanoes by Primary Type
st.header("2. Volcanoes by Primary Type")
st.subheader("Pick a volcano type")
st.markdown(
    """Use the "Primary Volcano Type" multi-select dropdown list in the sidebar to pick 1 or more volcano type(s). View the list of 
    volcano names and tectonic settings of your selected primary volcano type(s) here.""")
update_file(df1)
pri_type = df1['Primary Volcano Type'].unique()
pri_type_list = pri_type.tolist()
pri_type_list.sort()
vol_choice = st.sidebar.multiselect('Primary Volcano Type', pri_type_list)
filtered_df1 = df1[df1['Primary Volcano Type'].isin(vol_choice)]
filtered_df1 = filtered_df1.sort_values(by='Primary Volcano Type')
st.write(filtered_df1[['Volcano Name', 'Primary Volcano Type', 'Tectonic Setting']])

# Chart 1 - Bar Chart of Number of Volcanoes for Each Volcano Type
if st.checkbox("Click to display bar chart of number of volcanoes for each primary volcano type"):
    freq = df1.groupby(['Primary Volcano Type'])['Primary Volcano Type'].count()
    freq_dict = freq.to_dict()
    freq_list = list(freq_dict.values())
    pri_type_list = list(freq_dict.keys())
    chart = plt.figure()
    plt.bar(pri_type_list, freq_list, color ='maroon')
    plt.xticks(range(len(freq_list)), pri_type_list, rotation='vertical')
    plt.xlabel('Primary Volcano Types')
    plt.ylabel('Number of Volcanoes')
    plt.title('Bar Chart of Number of Volcanoes for Each Volcano Type')

    for x,y in zip(pri_type_list,freq_list):
        label = "{:n}".format(y)
        plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(0,5),
                 ha='center')
    st.pyplot(chart)

# Query 3 - Volcanoes by Height
st.header("3. Volcanoes by Elevation")
st.subheader("Pick an elevation range")
st.markdown(
    """Use the "Elevation Slider" in the sidebar to filter the volcanoes by elevation (m). View the list of volcanoes
    and their elevations within the specified elevation range here.""")
height = df1['Elevation (m)'].unique()
height_list = height.tolist()
min_height = min(height_list)
max_height = max(height_list)
start_val, end_val = st.sidebar.slider("Elevation Slider", value=[min_height, max_height])
filtered_df2 = df1[(df1['Elevation (m)'] >= start_val) & (df1['Elevation (m)'] <= end_val)]
filtered_df2 = filtered_df2.sort_values(by='Elevation (m)')
st.write(filtered_df2[['Volcano Name', 'Elevation (m)']])

# Chart 2 - Line Graph of Number of Volcanoes Against Elevation (m)
if st.checkbox("Click to display line graph of number of volcanoes against elevation (m)"):
    labels = ['-5700 <= x <= -2555', '-2555 < x <= 590', '590 < x <= 3735', '3735 < x <= 6879']
    elevation = df1['Elevation (m)']
    elevation = elevation.tolist()
    count = 0
    count1 = 0
    count2 = 0
    count3 = 0
    for x in elevation:
        if -5700 <= x <= -2555:
            count += 1
        elif -2555 < x <= 590:
            count1 += 1
        elif 590 < x <= 3735:
            count2 += 1
        elif 3735 < x <= 6879:
            count3 += 1
    freq_list = [count, count1, count2, count3]
    chart = plt.figure()
    plt.style.use('ggplot')
    plt.plot(labels,freq_list,linestyle=":",marker="o")
    plt.xticks(labels)
    plt.xlabel("Elevation (m)")
    plt.ylabel('Number of Volcanoes')
    plt.title("Line Graph of Number of Volcanoes Against Elevation (m)")

    for x,y in zip(labels,freq_list):
        label = "{:n}".format(y)
        plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(0,5),
                 ha='center')
    st.pyplot(chart)

# Query 4 - Volcanoes by Rock Type
st.header("4. Volcanoes by Rock Type")
st.subheader("Pick a dominant rock type")
st.markdown(
    """Use the "Dominant Rock Type" multi-select dropdown list in the sidebar to pick 1 or more rock type(s). View the list of 
    volcano names, regions, and subregions of your selected dominant rock type(s) here.""")
df1['Dominant Rock Type'] = df1['Dominant Rock Type'].fillna('None')
df1.to_csv(DATAFILE, index=False)
rock_type = df1['Dominant Rock Type'].unique()
rock_type_list = rock_type.tolist()
rock_choice = st.sidebar.multiselect('Dominant Rock Type', rock_type_list)
filtered_df1 = df1[df1['Dominant Rock Type'].isin(rock_choice)]
filtered_df1 = filtered_df1.sort_values(by='Dominant Rock Type')
st.write(filtered_df1[['Volcano Name', 'Region', 'Subregion', 'Dominant Rock Type']])

# Chart 3 - Pie Chart of Number of Volcanoes for Each Dominant Rock Type
if st.checkbox("Click to display pie chart of percentage of volcanoes for each dominant rock type"):
    freq = df1.groupby(['Dominant Rock Type'])['Dominant Rock Type'].count()
    freq_dict = freq.to_dict()
    freq_list = list(freq_dict.values())
    freq_array = np.array(freq_list)
    rock_type_list = list(freq_dict.keys())
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue', 'aquamarine', 'pink', 'red', 'orange', 'purple', 'brown', "indigo", "grey"]
    chart = plt.figure()
    plt.title('Pie Chart of Percentage of Volcanoes for Each Dominant Rock Type')
    percent = 100.*freq_array/freq_array.sum()
    patches, texts = plt.pie(freq_array, colors=colors, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(rock_type_list, percent)]
    plt.legend(labels, loc='center left', bbox_to_anchor=(-1, .5), fontsize=10)
    st.pyplot(chart)

# End of Program
