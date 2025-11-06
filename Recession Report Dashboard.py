import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load the automobile sales dataset
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv'
)

app = dash.Dash(__name__)

# Define list of years for the year dropdown
year_list = sorted(data['Year'].unique().tolist())

app.layout = html.Div(children=[
    html.H1(
        'Automobile Sales Statistics Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 24,
            'marginBottom': 20
        }
    ),

    # Report Type dropdown
    html.Div([
        html.Label('Select Report Type:', style={'fontSize': '18px', 'fontWeight': 'bold', 'marginLeft': '20px'}),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            placeholder='Select a report type',
            value='Recession Period Statistics',
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center',
                'marginLeft': '20px'
            }
        )
    ]),

    # Year selection dropdown
    html.Div([
        html.Label('Select Year:', style={'fontSize': '18px', 'fontWeight': 'bold', 'marginLeft': '20px'}),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select-year',
            value='Select-year',
            disabled=True,
            style={
                'width': '80%',
                'padding': '3px',
                'font-size': '20px',
                'text-align-last': 'center',
                'marginLeft': '20px'
            }
        )
    ]),

    # Message container for displaying custom messages
    html.Div(id='message-container', style={
        'padding': '20px',
        'margin': '20px',
        'fontSize': '16px',
        'textAlign': 'center',
        'borderRadius': '5px'
    }),

    # Output display division with className and id
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flex-wrap': 'wrap', 'width': '100%'})
    ])

])

# CALLBACK 1: Enable/disable the year dropdown based on statistics selection
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_stat):
    """
    This callback enables or disables the year selection dropdown based on 
    the user's choice of report type.
    """
    if selected_stat == 'Yearly Statistics':
        return False
    else:
        return True

# CALLBACK 3: Display message based on selected statistics
@app.callback(
    Output(component_id='message-container', component_property='children'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_message(selected_stat):
    """
    This callback displays a custom message based on the selected report type.
    """
    if selected_stat == 'Recession Period Statistics':
        return html.Div([
            html.P("📊 Recession Period Statistics Report", style={'fontWeight': 'bold', 'fontSize': '18px', 'color': '#503D36'}),
            html.P("This report shows statistics for all recession periods in the dataset.", style={'color': '#666'}),
            html.P("Note: Year selection is disabled for this report type as it displays all recession periods.", style={'color': '#FF6B6B', 'fontStyle': 'italic'})
        ], style={
            'backgroundColor': '#FFF3CD',
            'border': '2px solid #FFC107',
            'borderRadius': '5px',
            'padding': '15px'
        })
    
    elif selected_stat == 'Yearly Statistics':
        return html.Div([
            html.P("📈 Yearly Statistics Report", style={'fontWeight': 'bold', 'fontSize': '18px', 'color': '#503D36'}),
            html.P("This report shows statistics for a specific year.", style={'color': '#666'}),
            html.P("Please select a year from the dropdown above to view the report.", style={'color': '#0066CC', 'fontStyle': 'italic'})
        ], style={
            'backgroundColor': '#D1ECF1',
            'border': '2px solid #17A2B8',
            'borderRadius': '5px',
            'padding': '15px'
        })
    
    else:
        return html.Div([
            html.P("👋 Welcome to the Dashboard", style={'fontWeight': 'bold', 'fontSize': '18px', 'color': '#503D36'}),
            html.P("Please select a report type from the dropdown above to get started.", style={'color': '#666'})
        ], style={
            'backgroundColor': '#E7F3FF',
            'border': '2px solid #0066CC',
            'borderRadius': '5px',
            'padding': '15px'
        })

# CALLBACK 2: Update the graphs in the output container
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_stat, selected_year):
    """
    This callback dynamically generates and displays graphs based on the user's 
    selection from the dropdown menus.
    """
    
    if selected_stat == 'Recession Period Statistics':
        # Filter the data for recession periods (where Recession equals 1)
        recession_data = data[data['Recession'] == 1]

        if recession_data.empty:
            return [html.Div("No data for recession periods!", 
                           style={'color': 'red', 'fontSize': 18, 'padding': '20px'})]

        # TASK 2.5: Create 4 plots for Recession Period Statistics

        # Plot 1: Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(yearly_rec, 
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation Over Recession Period (Year Wise)",
                labels={'Automobile_Sales': 'Average Sales', 'Year': 'Year'},
                markers=True,
                line_shape='linear'
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type and represent as a Bar chart
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Automobile Sales by Vehicle Type During Recession",
                labels={'Automobile_Sales': 'Average Sales', 'Vehicle_Type': 'Vehicle Type'},
                color='Automobile_Sales',
                color_continuous_scale='Viridis'
            )
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Advertising Expenditure Share by Vehicle Type During Recession"
            )
        )

        # Plot 4: Develop a Bar chart for the effect of unemployment rate on vehicle type and sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate (%)', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales',
                barmode='group'
            )
        )

        # Return all 4 charts in a 2x2 grid layout
        return [
            html.Div(className='chart-item', 
                    children=[
                        html.Div(children=R_chart1, style={'display': 'inline-block', 'width': '48%', 'margin': '1%'}),
                        html.Div(children=R_chart2, style={'display': 'inline-block', 'width': '48%', 'margin': '1%'})
                    ], 
                    style={'display': 'flex', 'flexWrap': 'wrap', 'width': '100%'}),
            html.Div(className='chart-item', 
                    children=[
                        html.Div(children=R_chart3, style={'display': 'inline-block', 'width': '48%', 'margin': '1%'}),
                        html.Div(children=R_chart4, style={'display': 'inline-block', 'width': '48%', 'margin': '1%'})
                    ], 
                    style={'display': 'flex', 'flexWrap': 'wrap', 'width': '100%'})
        ]

    elif selected_stat == 'Yearly Statistics':
        # Check for Yearly Statistics
        if str(selected_year).isdigit():
            input_year = int(selected_year)
            yearly_data = data[data['Year'] == input_year]

            if yearly_data.empty:
                return [html.Div(f'No data for year {input_year}!', 
                               style={'color': 'red', 'fontSize': 18, 'padding': '20px'})]

            # TASK 2.6: Create 4 plots for Yearly Report Statistics

            # Plot 1: Yearly Automobile sales using line chart for the whole period
            # grouping data for plotting - Use the columns Year and Automobile_Sales
            yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
            Y_chart1 = dcc.Graph(
                figure=px.line(yas,
                    x='Year',
                    y='Automobile_Sales',
                    title="Average Yearly Automobile Sales Across All Years",
                    markers=True,
                    labels={'Automobile_Sales': 'Average Sales', 'Year': 'Year'}
                )
            )

            # Plot 2: Total Monthly Automobile sales using line chart
            # grouping data for plotting - Use the columns Month and Automobile_Sales
            mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
            Y_chart2 = dcc.Graph(
                figure=px.line(mas,
                    x='Month',
                    y='Automobile_Sales',
                    title=f'Total Monthly Automobile Sales in {input_year}',
                    markers=True,
                    labels={'Automobile_Sales': 'Total Sales', 'Month': 'Month'}
                )
            )

            # Plot 3: Bar chart for average number of vehicles sold by vehicle type in the given year
            # grouping data for plotting - Use the columns Vehicle_Type and Automobile_Sales
            avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
            Y_chart3 = dcc.Graph(
                figure=px.bar(avr_vdata,
                    x='Vehicle_Type',
                    y='Automobile_Sales',
                    title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year),
                    labels={'Vehicle_Type': 'Vehicle Type', 'Automobile_Sales': 'Average Sales'},
                    color='Automobile_Sales',
                    color_continuous_scale='Blues'
                )
            )

            # Plot 4: Pie chart for Total Advertisement Expenditure for each vehicle
            # grouping data for plotting - Use the columns Vehicle_Type and Advertising_Expenditure
            exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
            Y_chart4 = dcc.Graph(
                figure=px.pie(exp_data,
                    values='Advertising_Expenditure',
                    names='Vehicle_Type',
                    title='Total Advertisement Expenditure for Each Vehicle'
                )
            )

            # Return all 4 charts in a 2x2 grid layout
            return [
                html.Div(className='chart-item', 
                        children=[
                            html.Div(children=Y_chart1, style={'display': 'inline-block', 'width': '48%', 'margin': '1%'}),
                            html.Div(children=Y_chart2, style={'display': 'inline-block', 'width': '48%', 'margin': '1%'})
                        ], 
                        style={'display': 'flex', 'flexWrap': 'wrap', 'width': '100%'}),
                html.Div(className='chart-item', 
                        children=[
                            html.Div(children=Y_chart3, style={'display': 'inline-block', 'width': '48%', 'margin': '1%'}),
                            html.Div(children=Y_chart4, style={'display': 'inline-block', 'width': '48%', 'margin': '1%'})
                        ], 
                        style={'display': 'flex', 'flexWrap': 'wrap', 'width': '100%'})
            ]
        else:
            return [html.Div("Please select a valid year.", 
                           style={'color': 'blue', 'fontSize': 18, 'padding': '20px'})]

    else:
        return [html.Div("", style={'padding': '20px'})]

if __name__ == '__main__':
    app.run(debug=True)


