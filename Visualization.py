
from sympy.solvers.diophantine.diophantine import length
from dash import Dash, dcc, html, Input, Output, callback
from operator import index
from sqlite3 import Row
from pandas import DataFrame
from sympy import false
from numpy import column_stack
from matplotlib.pyplot import axis
import sympy
import plotly.graph_objects as go
from sympy.core.numbers import NaN
import pandas as pd
import numpy as np
from pandas import merge_ordered
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.express as px
import json
df1 = pd.read_csv("local_events_kozani_2025.csv")
df2 = pd.read_csv("urban_mobility_kozani_2025.csv")
df1.dtypes
df2.dtypes
df_merged = pd.merge(df2,df1, on =["Date","City"],suffixes=(None,"Event"))
df = df_merged.convert_dtypes()
# Save to new CSV file
#df_merged.to_csv('merged.csv', index=False)

parking_occupancy_mean = round(df_merged["ParkingOccupancy"].mean(skipna= True),1)
#print (parking_occupancy_mean)
df["ParkingOccupancy"] =df["ParkingOccupancy"].fillna(parking_occupancy_mean)

#Filling NaN values in BussPassengers with the mean of weekend and weekday values
weekend_df = df[df["DayType"]== "Weekend"]
weekday_df = df[df["DayType"]== "Weekday"]
weekend_bus_passenger_mean = round(weekend_df["BusPassengers"].mean(skipna = True),0)
weekday_bus_passenger_mean = round(weekday_df["BusPassengers"].mean(skipna = True),0)
#weekend_values = np.where((df['BusPassengers'].isnull())&(df['WeekendFlag']==1))
weekend_Passenger_values = (df['BusPassengers'].isnull())&(df['WeekendFlag']==1)
weekday_Passenger_values= (df['BusPassengers'].isnull())&(df['WeekendFlag']==0)
df.loc[weekend_Passenger_values,'BusPassengers'] = weekend_bus_passenger_mean
df.loc[weekday_Passenger_values,'BusPassengers'] = weekday_bus_passenger_mean

#Filling NaN values in BikeTrips with ffill cause of correlation with neighboring values
df.loc[:,'BikeTrips'] = df.loc[:,'BikeTrips'].ffill()

#Filling NaN values in TrafficCount with the mean of weekend and weekday values
weekend_traffic_mean = round(weekend_df["TrafficCount"].mean(skipna = True),0)
weekday_traffic_mean = round(weekday_df["TrafficCount"].mean(skipna = True),0)
weekend_traffic_values = (df['TrafficCount'].isnull())&(df['WeekendFlag']==1)
weekday_traffic_values= (df['TrafficCount'].isnull())&(df['WeekendFlag']==0)
df.loc[weekend_traffic_values,'TrafficCount'] = weekend_traffic_mean
df.loc[weekday_traffic_values,'TrafficCount'] = weekday_traffic_mean


def unique_non_null(s):
    return s.dropna().unique()

#Fill Missing Values in Attendance and Capacity depending the mean of their relative values per EventType
unique_EventType = unique_non_null(df['EventType'])
for item in unique_EventType:
    #print(item)
    Attendance_mean = round(df.loc[df['EventType'] == item,'Attendance'].mean(skipna = True),0)
    Capacity_mean = round(df.loc[df['EventType'] == item,'VenueCapacity'].mean(skipna = True),0)
    PerCent = round((Attendance_mean / Capacity_mean) * 100,0)
    df.loc[(df['EventType']== item) & (df['Attendance'].isna()),'Attendance'] = round((df.loc[(df['EventType']== item) & (df['Attendance'].isna()),'VenueCapacity'] * PerCent) / 100,0)
    df.loc[(df['EventType']== item) & (df['VenueCapacity'].isna()),'VenueCapacity'] = round((df.loc[(df['EventType']== item) & (df['VenueCapacity'].isna()),'Attendance'] * 100) / PerCent,0)
    #print(df.loc[df['EventType']== item,('Attendance','VenueCapacity')])

#Fill missing values with No Event in ZoneEvent & EventType
df["ZoneEvent"] =df["ZoneEvent"].fillna("No Event")
df["EventType"] =df["EventType"].fillna("No Event")

df.loc[df['Attendance'] > 0 ,'IsEvent'] = 1
df.loc[df['Attendance'] == 0 ,'IsEvent'] = 0

df.to_csv('AfterFillingValues.csv', index=False)


a1 = df['BusPassengers']
a2 = df['BikeTrips']
a3 = df['ParkingOccupancy']
a4 = df['TrafficCount']
a5 = df['TransportStrainIndex']
a6 = df['IsHoliday']
a7 = df['WeekendFlag']
a8 = df['IsEvent']
a9 = df['Attendance']
public_traffic_vec = np.vectorize(lambda x,y,z: (x+y)/z)
public_transport_pref = public_traffic_vec(a1,a2,a4)


weekend_strain_mean = round(weekend_df["TransportStrainIndex"].mean(skipna = True),0)
weekday_strain_mean = round(weekday_df["TransportStrainIndex"].mean(skipna = True),0)
Event_transport_strain_vec = np.vectorize(lambda x,y,z: ((x-weekend_strain_mean)*y + (x-weekday_strain_mean)*(1-y))* z)
Event_transport_strain_cor = Event_transport_strain_vec(a5,a7,a8)
Event_traffic_percent_increase_func = np.vectorize(lambda x,y,z: (100*(y*(1-(z*0.5)))/x))
Event_traffic_percent_increase = Event_traffic_percent_increase_func(a4,a9,public_transport_pref)
#Event_transport_strain_inc_func
#Event_transport_strain_inc
weekend_parking_mean = round(weekend_df["ParkingOccupancy"].mean(),0)
weekday_parking_mean = round(weekday_df["ParkingOccupancy"].mean(),0)
Event_parking_occupancy_increase_func = np.vectorize(lambda x,y,z: 100*(y*((x-weekend_parking_mean)/weekend_parking_mean) + (1-y)*((x-weekday_parking_mean)/weekday_parking_mean))* z)
Event_parking_occupancy_percent_increase = Event_parking_occupancy_increase_func(a3,a7,a8)
#print(Event_parking_occupancy_percent_increase.mean())

df['Date']= pd.to_datetime(df['Date'])
df.set_index('Date',inplace= True)
df['Day'] = df.index.day_name()
df.reset_index(inplace= True)



unique_Zone  = unique_non_null(df['Zone'])
unique_day = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
df_day = pd.DataFrame(index= unique_day, columns= ('TrafficCount','ParkingOccupancy','TransportStrainIndex'))
df_day = df_day.fillna(0) # With 0s rather than NaNs

for item in unique_day:
    df_day.loc [item,'TrafficCount'] = round(df.loc[df['Day'] == item,'TrafficCount'].mean(),0)
    df_day.loc [item,'ParkingOccupancy'] = round(df.loc[df['Day'] == item,'ParkingOccupancy'].mean(),2)
    df_day.loc [item,'TransportStrainIndex'] = round(df.loc[df['Day'] == item,'TransportStrainIndex'].mean(),2)


df_day['Day'] = df_day.index
df_day.reset_index(inplace= True,drop = False)

df['TrafficEventIncrease'] = Event_traffic_percent_increase
df['TrafficEventIncrease'] = round(df['TrafficEventIncrease'],1)
#df.to_csv('day.csv', index=False)
"""
sns.set_style()

TrafficPerDayPlot=sns.barplot(data= df_day ,y="TrafficCount",x= "Day" ,hue="ParkingOccupancy",palette="ch:s=-.5,r=2,d=.4,l=.8,g=0.5",saturation=1,alpha = 0.8)
plt.ylim(13000,18000)
plt.ylabel('Traffic Count')

ParkingOccupancyChart=sns.displot(data= df, hue= df.loc[df['ZoneEvent']!="No Event","EventType"],x= "ParkingOccupancy",palette="colorblind",kde= True,bins=15,stat='count',alpha = 0.4,multiple = "dodge")
Trafficchart=sns.displot(data= df,x= "TrafficEventIncrease",hue= df.loc[df['ZoneEvent']!="No Event","ZoneEvent"],palette="colorblind",kde = True ,multiple="dodge",stat='count',alpha= 0.4)

df["BikeTripsRM3"]=df['BikeTrips'].rolling(window=3).mean()
df["BikeTripsRM7"]=df['BikeTrips'].rolling(window=7).mean()
sns.lineplot(x= df.index,y= "BikeTrips",data=df)
plt.figure(figsize=(10, 6))
plt.scatter(df.Date, df['BikeTrips'], label='Bike Trips',alpha = 0.4,marker= '.')
plt.plot(df.Date, df['BikeTripsRM7'], label='7-Day Rolling Mean', linestyle='solid', color='purple')
plt.title('Bike Trips Trends with Rolling Mean')
plt.xlabel('Date')
plt.ylabel('Bike Trips')
plt.legend()
plt.grid(True)
plt.show()
"""
# Dash Traffic Count Interactive Plot
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

heatmap_df= df[df['EventType']!='No Event']
fig= px.density_heatmap(
    heatmap_df,
    x='Attendance',
    y='ParkingOccupancy',
    color_continuous_scale="Viridis",
    title="Event Attendance vs Parking Occupancy",
    nbinsx=25,
    nbinsy=15,
)
fig.update_layout(
    clickmode='event+select',
    xaxis_title="Attendance",
    yaxis_title="Parking Occupancy",
    coloraxis_colorbar_title="Count"
)

app.layout = html.Div([
    html.H1('Traffic Count in City of Kozani'),
    html.H2('Select filters'),
    dcc.Dropdown(
        id='event-dropdown',
        options=[{'label': i, 'value': i} for i in df['EventType'].unique()],
        value=df['EventType'].unique()[1],
        clearable = True,
        placeholder= 'Select a type of Event'
    ),
    dcc.Dropdown(
        id='zone-dropdown',
        options=[{'label': i, 'value': i} for i in df['Zone'].unique()],
        value=None,
        clearable = True,
        placeholder= 'Select a Zone'
    ),
    dcc.Dropdown(
        id='hue-dropdown',
        options=[{'label': 'Weekend', 'value': 1},{'label': 'Holiday', 'value': 0}],
        value= None,
        clearable = True,
        placeholder= 'Discern Data by Weekend-Weekday or Holiday'
    ),


    html.Div(id='display-count'),
    dcc.Graph(id='line-chart'),
    html.H2('Heatmap'),
    dcc.Graph(id='heatmap',figure=fig),

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),
        
        html.Div([
            dcc.Markdown("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
            """),
            html.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
])

@callback(
    Output('line-chart', 'figure'),
    [Input('event-dropdown', 'value'),Input('zone-dropdown', 'value'),Input('hue-dropdown', 'value')]
)
def update_line_chart(selected_event,selected_zone,selected_hue):

    if selected_event is None:
        filtered_df = df[df['Zone'] == selected_zone]
    if selected_zone is None:
        filtered_df = df[df['EventType'] == selected_event]
    else:
        filtered_df = df[(df['EventType'] == selected_event)&(df['Zone'] == selected_zone)]
    if selected_hue == 1:
        fig=px.line(filtered_df,x='Date',y='TrafficCount',color='WeekendFlag',line_dash='WeekendFlag')
    if selected_hue == 0:
        fig=px.line(filtered_df,x='Date',y='TrafficCount',color='IsHoliday',line_dash='IsHoliday',markers= True)        
    if selected_hue is None:
        fig=px.line(filtered_df,x='Date',y='TrafficCount')
    return fig

@app.callback( 
    Output('display-count', 'children'),
    [Input('event-dropdown', 'value'),Input('zone-dropdown', 'value')])
def get_count(selected_event,selected_zone):
    if selected_event is None:
        count_df = df[df['Zone'] == selected_zone]
    if selected_zone is None:
        count_df = df[df['EventType'] == selected_event]
    else:
        count_df = df[(df['EventType'] == selected_event)&(df['Zone'] == selected_zone)]
    return "Number of Dates = "+ str(count_df.shape[0])+ " and Traffic Count mean= " +str(round(count_df['TrafficCount'].mean(),1))


@callback(
    Output('hover-data', 'children'),
    Input('heatmap', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@callback(
    Output('click-data', 'children'),
    Input('heatmap', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@callback(
    Output('selected-data', 'children'),
    Input('heatmap', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@callback(
    Output('relayout-data', 'children'),
    Input('heatmap', 'relayoutData'))
def display_relayout_data(relayoutData):
    return json.dumps(relayoutData, indent=2)

app.run(debug=True)

#END OF DASH INTERACTIVE PLOT




