import streamlit as st
import pandas as pd
import numpy as np

import scipy as sp

#import plotly.graph_objects as go
import plotly.express as px

#from PIL import Image

def load_data(path):
    data=pd.read_csv(path)
    return data


#Load Data
data=load_data(r"C:\Users\User\OneDrive\MSBA 325 - Data Visualization\Assignments\Ghina Koteich, A2\covid_19_data.csv")

#Data Pre-processing
#Rename columns for better synchronization with the remaining columns 
data=data.rename(columns={'Last Update':'LastUpdate'})
#Remove rows with insignificant/misspelled values in column Country/Region
data=data[(data['Country/Region']!='Others') & (data['Country/Region']!='(\'St. Martin\',)') & (data['Country/Region']!='Gambia, The')]
#Sort the "Country/Region" column according to the number of confirmed cases
data_confirmed=((data.groupby('Country/Region').sum()).sort_values(by=["Confirmed"], ascending=False)).reset_index()

#Highest 20 countries in number of confirmed cases
data_confirmed_20=data_confirmed.iloc[:20,:]

#Treat missing values 
data_state=data.dropna()
data_state.isnull().sum()
data_obs= data.groupby('ObservationDate').sum().reset_index()


#DataVisualization using Plotly 
scatter=px.scatter(data_confirmed, x="Confirmed", y="Deaths", color=data_confirmed['Country/Region'], 
           size='Deaths',
           size_max=60, title= 'Number of Coronavirus Deaths compared to the number of Confirmed cases in the Study\'s Countries'
          )

pie_chart = px.pie(data_confirmed_20, values = 'Deaths',names='Country/Region', height=600, 
                  title= "Highest 20 countries in number of Coronavirus Deaths")

pie_chart.update_traces(textposition='inside', textinfo='percent+label')

pie_chart.update_layout(
    title_x = 0.5,
    geo=dict(
        showframe = False,
        showcoastlines = False,
    ))

bar = px.bar(data_confirmed_20, x="Country/Region", y=["Confirmed", "Deaths", "Recovered"], title="Highest 20 Countries in Number of Confirmed Coronavirus Cases and their Respective Deaths and Recovered Cases")

data_obs_vis = data_obs.melt(id_vars='ObservationDate', 
                 value_vars=['Confirmed', 
                             'Recovered', 
                             'Deaths'], 
                 var_name='Ratio', 
                 value_name='Value')

line_fig = px.line(data_obs_vis, x="ObservationDate", y="Value", line_shape="spline",color='Ratio', 
              title='The Variation of number of Confirmed cases, Recovered cases, and Deaths with Time')

map= px.choropleth(data, locations="Country/Region",locationmode = "country names",color='Confirmed', hover_name="Country/Region",
             animation_frame="ObservationDate",color_continuous_scale=px.colors.sequential.Plasma, projection= "natural earth", 
              title= "The Global Spread of Coronavirus from January to April 2020")



#Load Books Data 
books=load_data(r'C:\Users\User\OneDrive\MSBA 325 - Data Visualization\Assignments\Ghina Koteich, A2\bestsellers with categories.csv')

#Pre-processing Books Data 
#Sort Year column 
books.sort_values('Year', inplace=True)

#Plotly Visualization
hist=px.histogram(books, x='Price', y='Reviews', histfunc='sum', color='Genre', title='The Variation of Number of Reviews as function of Price')


violin=px.violin(books, y='Price', x='Genre', color='Genre', box=True, points='all', title='No Association between Price and Genre of the Books')


box_books=px.box(books, x='User Rating', y='Author', orientation='h', color='Genre', notched=True, title= 'The Relationship between Author and User Rating of books')


fig = px.bar(books, x="Genre", y="User Rating", color="Genre",
  animation_frame="Year", title='The variation of number of Reviews of each Genre as function of time (years)'
            )



#Title 
st.title('Streamlit Data Visualization')
st.subheader('_Choose from the sidebar select box a data to visualize_')


box = st.sidebar.selectbox("Available Data for Visualization:", [' ','Novel Corona Virus 2019 Dataset','Amazon Top 50 Bestselling Books 2009 - 2019'])

list_books=['Histogram', 'Violin Plot', 'Box Plot','Box Plot with Animation']
list_corona=['Scatter Plot', 'Pie Chart', 'Bar Plot','Line Plot', 'Animated Map']

#Spaces
st.markdown('###')

if box == ' ':
    #image = Image.open(r'C:\Users\User\Desktop\data2.jpg')
    
    #st.image(image)
    st.write('Data')

if box =='Amazon Top 50 Bestselling Books 2009 - 2019':
    

    st.write(':small_red_triangle_down: The dataset has information about 550 books that were sold on Amazon from 2009 to 2019. The books have been categorized into fiction and non-fiction using Goodreads.') 
    st.write('What affects the book sales?')
    st.markdown('#')
    
    if st.checkbox('Show Dataset'):
        st.write(books)
    
    st.markdown('###')

    result=st.radio('Select Visualization Type:', list_books)
    if result=='Histogram':
        st.write(hist)
    
    elif result=='Violin Plot':
        st.write(violin)    
    elif result=='Box Plot':
        st.write(box_books)
    elif result=='Box Plot with Animation':
        st.write(fig)

    st.markdown('#')

    st.write(':warning: Low priced books are getting more sales.')
    st.write(':warning: Non-fiction books are more viewed.')

    st.markdown('#')
  
    st.write(':heavy_check_mark: Publishers of low book sales can run book giveaways or offer free copies to Amazon top reviewers.')



if box == 'Novel Corona Virus 2019 Dataset':
    

    st.write(':small_red_triangle_down: 2019 Novel Coronavirus (2019-nCoV) is a virus (more specifically, a coronavirus) identified as the cause of an outbreak of respiratory illness first detected in Wuhan, China. Early on, many of the patients in the outbreak in Wuhan, China reportedly had some link to a large seafood and animal market, suggesting animal-to-person spread. However, a growing number of patients reportedly have not had exposure to animal markets, indicating person-to-person spread is occurring. At this time, it’s unclear how easily or sustainably this virus is spreading between people - CDC. This dataset has daily level information on the number of affected cases, deaths and recovery from 2019 novel coronavirus.')
    st.markdown('#')
    if st.checkbox('Show Dataset'):
        st.write(data)
    st.markdown('###')
    result=st.radio('Select Visualization Type:', list_corona)
    if result=='Scatter Plot':
        st.write(scatter)
    elif result=='Pie Chart':
        st.write(pie_chart)
    elif result=='Bar Plot':
        st.write(bar)
    elif result=='Line Plot':
        st.write(line_fig)
    elif result=='Animated Map':
        st.write(map)
    st.markdown('#')

    st.write(':warning: The number of Corona virus affected cases is rapidly increasing over time.')
    st.write(':warning: The increase in some countries is severely sharper than others.')

    st.markdown('#')
  
    st.write(':heavy_check_mark: People around the world should have access to safe and effective vaccines to end the COVID-19 pandemic.')

