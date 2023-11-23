#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    html.H1(app.title, style={'textAlign':'center', 'color': '#503D36', 'font-size':0})#May include style for title
    html.Div([#TASK 2.2: Add two dropdown menus 
        html.Label("Select Statistics:"),
          dcc.Dropdown(id='dropdown-statistics', 
                   options=[
                           {'label':'Yearly Satistics ', 'value': 'Yearly Satistics'},
                           {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                           ],
                           placeholder='Select a report type',
                           value='Select Statistics',
                           style={'width': '80%', 'padding': '3px', 'front-size': '20px', 'text-align-last': 'center'}
                       ]),
             html.Div([
                 dcc.Dropdown(id='select-year',
                              options=[{'label': i, 'value': i} for i in year_list],
                              placeholder='Year',
                              style={'width': '80%', 'padding': '3px', 'front-size': '20px', 'text-align-last': 'center'}
                              ]),
                      html.Div(id='output-container', className='chart-grid', style={'display':'flex'})
                      ])

#TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='select year', component_property='disabled'),
    [Input(component_id='dropdown-statistics',component_property='disabled')]
)

def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics': 
        return False
    else: 
        return True

#Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='children'),Input(component_id='dropdown-statistics', component_property='children')]
)


def update_output_container(input_year, selected_statistics):
    if selected_statistics == 'Recession Period Statistics':
        elif selected_statistics == 'Yearly Statistics'
    else:
        return None
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
#TASK 2.5: Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise)
        # use groupby to create relevant data for plotting
        yearly_rec=recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Plot1 = dcc.Graph(
            figure=px.line(yearly_rec), 
            x='Year',
            y='Automobile_Sales',
            title="Average Automobile Sales fluctuation over Recession Period"))

#Plot 2 Calculate the average number of vehicles sold by vehicle type       
        # use groupby to create relevant data for plotting
        average_sales = data.groupby('Vehicle_Type')['Automobile_sales']mean().reset_index()                           
        Plot2  = dcc.Graph(figure=px.scatter(average_sales,
        x="Vehicle_Type",
        y="Automobile_Sales",
        title="Average Vehicle Sales by Type During Recession Period",
    )
        
# Plot 3 Pie chart for total expenditure share by vehicle type during recessions
        # use groupby to create relevant data for plotting
         exp_rec= recession_data.groupby('Vehicle_Type)['Amount'].sum().reset_index()
         exp_rec['Expense_Share'] = exp_rec['Amount'] / exp_rec['Amount'].sum()
         Plot3 = dcc.Graph(
            figure=px.pie(exp_rec,
            values='Expense_Share',
            names='Vehicle_Type',
            title="Vehicle Type During Recession"
            )
        )

# Plot 4 bar chart for the effect of unemployment rate on vehicle type and sales
         unemp_effect = recession_data.groupby(['Vehicle_Type', 'Unemployment_Rate'])['Automobile_Sales'].mean().reset_index()

        Plot4 = dcc.Graph(
            figure=px.bar(unemp_effect,
                           x='Vehicle_Type',
                           y='Automobile_Sales',
                           color='Unemployment_Rate',
                           title="Effect of Unemployment Rate on Vehicle Sales During Recessions"
                           )
        )


        return [
            html.Div(className='chart-item', children=[html.Div(children='Plot1'),html.Div(children='Plot2')]),
            html.Div(className='chart-item', children=[html.Div(children='Plot3'),html.Div('Plot4')])
            ]

# TASK 2.6: Create and display graphs for Yearly Report Statistics
 # Yearly Statistic Report Plots                             
    elif (input_year and selected_statistics=='Yearly Report Statistics') :
        yearly_data = data[data['Year'] == input_year]
                              
#TASK 2.5: Creating Graphs Yearly data
                              
#plot 1 Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales Trend'))
            
# Plot 2 Total Monthly Automobile sales using line chart.
        Y_chart2 = dcc.Graph(figure=px.line(yearly_data, x='Month', y='Automobile_Sales', title="Monthly Automobile Sales"))

            # Plot bar chart for average number of vehicles sold during the given year
        avr_vdata=yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata,
                  x='Vehicle_Type',
                  y='Automobile_Sales',
                  title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)),
)

            # Total Advertisement Expenditure for each vehicle using pie chart
        exp_data=yearly_data.groupby('Vehicle_Type')['Amount'].sum().reset_index()
        exp_data['Expense_Share'] = exp_data['Amount'] / exp_data['Amount'].sum()

Y_chart4 = dcc.Graph(
    figure=px.pie(exp_data,
                  values='Expense_Share',
                  names='Vehicle_Type',
                  title="Total Advertisement Expenditure for each vehicle in the year {}".format(input_year))
)


#TASK 2.6: Returning the graphs for displaying Yearly data
        return [
                html.Div(className='chart-item', children=[html.Div(children=Y_chart1),html.Div(children=Y_chart2)],style={flex: 1}),
                html.Div(className='chart-item', children=[html.Div(children=Y_chart3),html.Div(children=Y_chart4)],style={flex: 1})
                ]
        
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

