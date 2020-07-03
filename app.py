#!/usr/bin/env python
# coding: utf-8

# In[1]:


from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np

from datetime import datetime as dt
import plotly.express as px

app = dash.Dash(__name__)
server = app.server


# In[3]:


# prepare data

years = [2016, 2017, 2018]
file_list = []
for year in years:
    df = pd.read_csv("data/acc_" + str(year) + ".csv", parse_dates=[9, 11])
    df["Year"] = year
    file_list.append(df)

df_acc = pd.concat(file_list)
df_acc.columns

#acc_by_time = df_acc.Date.value_counts()
#acc_by_hour = acc_by_time.groupby(acc_by_time.index.Date).sum()


# In[4]:


# app layout

app.layout = html.Div(children=[
    html.Div(children=[
        html.H3(children='United Kingdom accidents data'),
        html.H6(children='Accidents overview 2016-2018', style={'marginTop': '-15px', 'marginBottom': '30px'})
    ], style={'textAlign': 'center'}),
    
    html.Div(children=[
        ################### Filter box ###################### 
        html.Div(children=[
            html.Label('Filter by date (M-D-Y):'),
            dcc.DatePickerRange(
                id='input_date',
                number_of_months_shown=2,
                persistence=True,
                month_format='DD/MM/YYYY',
                show_outside_days=True,
                minimum_nights=0,
                initial_visible_month=dt(2017, 1, 1),
                min_date_allowed=dt(2016, 1, 1),
                max_date_allowed=dt(2018, 12, 31),
                start_date=dt.strptime("2018-06-01", "%Y-%m-%d").date(),
                end_date=dt.strptime("2018-12-31", "%Y-%m-%d").date()
            ),
            #html.Div(id='output_date'),

            html.Label('Day of the week:', style={'paddingTop': '2rem'}),
            dcc.Dropdown(
                id='input_days',
                options=[
                    {'label': 'Sun', 'value': '1'},
                    {'label': 'Mon', 'value': '2'},
                    {'label': 'Tue', 'value': '3'},
                    {'label': 'Wed', 'value': '4'},
                    {'label': 'Thurs', 'value': '5'},
                    {'label': 'Fri', 'value': '6'},
                    {'label': 'Sat', 'value': '7'}
                ],
                value=['1', '2', '3', '4', '5', '6', '7'],
                multi=True
            ),

            html.Label('Accident Severity:', style={'paddingTop': '2rem', 'display': 'inline-block'}),
            dcc.Checklist(
                id='input_acc_sev',
                options=[
                    {'label': 'Fatal', 'value': '1'},
                    {'label': 'Serious', 'value': '2'},
                    {'label': 'Slight', 'value': '3'}
                ],
                value=['1', '2', '3'],
            ),

            html.Label('Speed limits (mph):', style={'paddingTop': '2rem'}),
            dcc.RangeSlider(
                    id='input_speed_limit',
                    min=20,
                    max=70,
                    step=10,
                    value=[20, 70],
                    marks={
                        20: '20',
                        30: '30',
                        40: '40',
                        50: '50',
                        60: '60',
                        70: '70'
                    },
            ),
            #html.Div(id='output_speed_limit', style={'paddingBottom': '2rem',})

        ], className="four columns",
        style={'padding':'2rem', 'margin':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'marginTop': '2rem'} ),

        ######################################### 
        # Number statistics & number of accidents each day

        html.Div(children=[
            html.Div(children=[
                html.Div(children=[
                    html.H3(id='no_acc', style={'fontWeight': 'bold'}),
                    html.Label('Total accidents', style={'paddingTop': '.3rem'}),
                ], className="three columns number-stat-box"),

                html.Div(children=[
                    html.H3(id='no_cas', style={'fontWeight': 'bold', 'color': '#f73600'}),
                    html.Label('Casualties', style={'paddingTop': '.3rem'}),
                ], className="three columns number-stat-box"),

                html.Div(children=[
                    html.H3(id='no_veh', style={'fontWeight': 'bold', 'color': '#00aeef'}),
                    html.Label('Total vehicles', style={'paddingTop': '.3rem'}),
                ], className="three columns number-stat-box"),

                html.Div(children=[
                    html.H3(id='no_days', style={'fontWeight': 'bold', 'color': '#a0aec0'}),
                    html.Label('Number of days', style={'paddingTop': '.3rem'}),
                ], className="three columns number-stat-box"),
            ], style={'margin':'1rem', 'display': 'flex', 'justify-content': 'space-between', 'width': '100%', 'flex-wrap': 'wrap'}),

            # Line chart for accidents per day
            html.Div(children=[
                dcc.Graph(id='acc_line_chart')
            ], className="twleve columns", style={'padding':'.3rem', 'marginTop':'1rem', 'marginLeft':'1rem', 'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white', }),

        ], className="eight columns", style={'backgroundColor': '#f2f2f2', 'margin': '1rem'})
    ], style={'display': 'flex', 'flex-wrap': 'wrap'}),
    
    html.Div(children=[
        # Bar chart for accidents per hour
        html.Div(children=[
            dcc.Graph(id='acc_bar_chart')
        ], className="six columns widget-box"),
        
        html.Div(children=[
            dcc.Graph(id='acc_box_chart')
        ], className="three columns widget-box"),
        
        html.Div(children=[
            dcc.Graph(id='acc_dist_chart')
        ], className="three columns widget-box")
    ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between', 'margin': '1rem', 'marginBottom': '2rem'}),
    
    
    html.Div(children=[
        # Map
        html.Div(children=[
            dcc.Graph(id='acc_map')
        ], className="twleve columns", style={'padding':'2rem',  'boxShadow': '#e3e3e3 4px 4px 2px', 'border-radius': '10px', 'backgroundColor': 'white'}),
    
    ], style={'margin': '1rem', })
    
    
    
], style={'padding': '2rem'})


# In[5]:


######### Callback for top statistics ##############################
@app.callback(
    [Output(component_id='no_acc', component_property='children'),
     Output('no_cas', 'children'),
     Output('no_veh', 'children'),
     Output('no_days', 'children'),
    ],
    [Input('input_date', 'start_date'),
     Input('input_date', 'end_date'),
     Input('input_days', 'value'),
     Input('input_acc_sev', 'value'),
     Input('input_speed_limit', 'value'),
    ])
def update_statistics(start_date, end_date, input_days, input_acc_sev, input_speed_limit):
    # filter by date
    df_update = df_acc.loc[(start_date <= df_acc['Date']) & (end_date >= df_acc['Date'])]
    # by weekdays
    if input_days:
        df_update = df_update[df_update['Day_of_Week'].isin(input_days)]
        
    # by accident severity
    if(input_acc_sev):
        df_update = df_update[df_update['Accident_Severity'].isin(input_acc_sev)]
        
    # filter by speed limits
    df_update = df_update.loc[(input_speed_limit[0] <= df_update['Speed_limit']) & (input_speed_limit[1] >= df_update['Speed_limit'])]
    
    days = dt.strptime(end_date, "%Y-%m-%d") - dt.strptime(start_date, "%Y-%m-%d")
    
    return len(df_update), sum(df_update['Number_of_Casualties']), sum(df_update['Number_of_Vehicles']), days.days


# In[6]:


######### Callback for accidents line chart ##############################
@app.callback(
    Output('acc_line_chart', 'figure'),
    [Input('input_date', 'start_date'),
     Input('input_date', 'end_date'),
    ])
def update_line_chart(start_date, end_date):
    # filter by date
    df_update = df_acc.loc[(start_date <= df_acc['Date']) & (end_date >= df_acc['Date'])]
    #acc_by_day = pd.DataFrame(df_update.Date.value_counts().sort_index().reset_index())
    #acc_by_day.columns=["Date", "Number"]
    acc_by_day = df_update.Date.value_counts().sort_index()
    
    return {
        'data': [dict(
            x=acc_by_day.index,
            y=acc_by_day.values,
            type='scatter',
            mode='line',
            marker={ 'size': 15, 'opacity': 0.5, 'line': {'width': 0.5, 'color': 'white'} },
            line={'color': "#7bc7ff"}
        )],
        'layout': dict(
            title={"text": "Number of accidents occured in the given date range"},
            margin={'l': 40, 'b': 40, 't': 60, 'r': 20},
            hovermode='closest',  
            height=300,
        )
    }


# In[7]:


######### Callback for accidents bar chart ##############################
@app.callback(
    Output('acc_bar_chart', 'figure'),
    [Input('input_date', 'start_date'),
     Input('input_date', 'end_date'),
     Input('input_days', 'value'),
     Input('input_acc_sev', 'value'),
     Input('input_speed_limit', 'value'),
    ])
def update_bar_chart(start_date, end_date, input_days, input_acc_sev, input_speed_limit):
    # filter by date
    df_update = df_acc.loc[(start_date <= df_acc['Date']) & (end_date >= df_acc['Date'])]
    if input_days:
        df_update = df_update[df_update['Day_of_Week'].isin(input_days)]
    if(input_acc_sev):
        df_update = df_update[df_update['Accident_Severity'].isin(input_acc_sev)]   
    df_update = df_update.loc[(input_speed_limit[0] <= df_update['Speed_limit']) & (input_speed_limit[1] >= df_update['Speed_limit'])]
    acc_by_time = df_update.Time.value_counts()
    acc_by_hour = acc_by_time.groupby(acc_by_time.index.hour).sum()
    
    return {
        'data': [dict(
            x=acc_by_hour.index,
            y=acc_by_hour.values,
            #text=acc_by_day.index,
            type="bar",
            marker={ 'size': 15, 'opacity': 0.5, 'color': acc_by_hour.index, 'colorscale': 'Viridis' },
        )],
        'layout': dict(
            title={"text": "Number of accidents occured in each hour"},
            margin={'l': 40, 'b': 20, 't': 60, 'r': 20},
            hovermode='closest',        
        )
    }


# In[8]:


######### Callback for accidents box chart ##############################
@app.callback(
    Output('acc_box_chart', 'figure'),
    [Input('input_date', 'start_date'),
     Input('input_date', 'end_date'),
     Input('input_days', 'value'),
     Input('input_acc_sev', 'value'),
     Input('input_speed_limit', 'value'),
    ])
def update_box_chart(start_date, end_date, input_days, input_acc_sev, input_speed_limit):
    # filter by date
    df_update = df_acc.loc[(start_date <= df_acc['Date']) & (end_date >= df_acc['Date'])]
    if input_days:
        df_update = df_update[df_update['Day_of_Week'].isin(input_days)]
    if(input_acc_sev):
        df_update = df_update[df_update['Accident_Severity'].isin(input_acc_sev)]   
    df_update = df_update.loc[(input_speed_limit[0] <= df_update['Speed_limit']) & (input_speed_limit[1] >= df_update['Speed_limit'])]
    
    acc_box = pd.DataFrame(df_update["Date"].value_counts().reset_index())
    acc_box.columns = ["Date", "Count"]
    acc_box["Current_Range"] = "Current_Range"
    
    return {
        'data': [dict( x=acc_box["Current_Range"], y=acc_box["Count"], type="box", points="all", mode='box' )],
        'layout': dict(
            title={"text": "Box plot for selected dates"},
            margin={'l': 40, 'b': 15, 't': 65, 'r': 20},
            hovermode='closest',        
        )
    }


# In[9]:


######### Callback for accidents table ##############################
@app.callback(
    Output('acc_dist_chart', 'figure'),
    [Input('input_date', 'start_date'),
     Input('input_date', 'end_date'),
     Input('input_days', 'value'),
     Input('input_acc_sev', 'value'),
     Input('input_speed_limit', 'value'),
    ])
def update_table(start_date, end_date, input_days, input_acc_sev, input_speed_limit):
    # filter by date
    df_update = df_acc.loc[(start_date <= df_acc['Date']) & (end_date >= df_acc['Date'])]
    if input_days:
        df_update = df_update[df_update['Day_of_Week'].isin(input_days)]
    if(input_acc_sev):
        df_update = df_update[df_update['Accident_Severity'].isin(input_acc_sev)]   
    df_update = df_update.loc[(input_speed_limit[0] <= df_update['Speed_limit']) & (input_speed_limit[1] >= df_update['Speed_limit'])]
    
    acc_table = pd.DataFrame(df_update["Date"].value_counts().reset_index())
    acc_table.columns = ["Date", "Count"]
    acc_table['Date'] = acc_table['Date'].dt.strftime('%d/%m/%Y')
    return {
        'data': [dict(
            header=dict(values=["Date", "Accident counts"], fill_color='paleturquoise', align='left', font={'color': 'white'}, fill={'color': 'black'} ),
            cells=dict(values=[acc_table.Date, acc_table.Count], fill_color='lavender', align='left'),
            type="table",
        )],
        'layout': dict( title={"text": "Data table"}, margin={'l': 30, 'b': 15, 't': 65, 'r': 30} )
    }


# In[10]:


######### Callback for accidents map ##############################
@app.callback(
    Output('acc_map', 'figure'),
    [Input('input_date', 'start_date'),
     Input('input_date', 'end_date'),
     Input('input_days', 'value'),
     Input('input_acc_sev', 'value'),
     Input('input_speed_limit', 'value'),
    ])
def update_map(start_date, end_date, input_days, input_acc_sev, input_speed_limit):
    # filter by date
    df_update = df_acc.loc[(start_date <= df_acc['Date']) & (end_date >= df_acc['Date'])]
    if input_days:
        df_update = df_update[df_update['Day_of_Week'].isin(input_days)]
    if(input_acc_sev):
        df_update = df_update[df_update['Accident_Severity'].isin(input_acc_sev)]   
    df_update = df_update.loc[(input_speed_limit[0] <= df_update['Speed_limit']) & (input_speed_limit[1] >= df_update['Speed_limit'])]
    df_update['Accident_Severity_text'] = df_update['Accident_Severity']     .map({1: "Fatal", 2: "Serious", 3: "Slight"})
    
    df_update['text'] = "Date: " + df_update['Date'].dt.strftime('%d %b %Y')                         + "\n" + " |  Accident Severity: " + df_update['Accident_Severity_text']                         + "\n" + " |  Number of Vehicles: " + df_update['Number_of_Vehicles'].apply(str)                         + "\n" + " |  Number of Casualties: " + df_update['Number_of_Casualties'].apply(str)                         + "\n" + " |  Speed limit: " + df_update['Speed_limit'].apply(str)     
    return {
        'data': [dict(
            lat=df_update['Latitude'], 
            lon=df_update['Longitude'],
            name=df_update['Date'],
            type='scattermapbox',
            text=df_update['text'],
        )],
        'layout': dict(
            title={"text": "Position of accidents"},
            margin={'l': 20, 'b': 15, 't': 60, 'r': 20},
            height=700,
            mapbox={
                "style": "dark", 
                "center": {"lon": -1.474351, "lat": 53.381173},
                "accesstoken": "pk.eyJ1IjoieWx3LXNoZWYiLCJhIjoiY2tiYXpicmNiMGFyYjMwbWJpbGE0Y29odSJ9.ygksJJTy3si1ZGcYb82DpA",
                "zoom": 8,
                
            }
        )
    }


# In[11]:


if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




