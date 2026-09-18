# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),

    # ---------------------------------------------------
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # ---------------------------------------------------
    
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'}
        ] + [
            {'label': site, 'value': site}
            for site in spacex_df['Launch Site'].unique()
        ],
        value='ALL',
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # ---------------------------------------------------
    # TASK 2: Add a pie chart
    # ---------------------------------------------------

    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    html.P("Payload range (Kg):"),

    # ---------------------------------------------------
    # TASK 3: Add a slider to select payload range
    # ---------------------------------------------------

    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={
            0: '0',
            1000: '1000',
            2000: '2000',
            3000: '3000',
            4000: '4000',
            5000: '5000',
            6000: '6000',
            7000: '7000',
            8000: '8000',
            9000: '9000',
            10000: '10000'
        },
        value=[min_payload, max_payload]
    ),

    # ---------------------------------------------------
    # TASK 4: Add a scatter chart
    # ---------------------------------------------------

    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    ),
])


# =======================================================
# TASK 2:
# Callback for site-dropdown and success-pie-chart
# =======================================================

@app.callback(
    Output(
        component_id='success-pie-chart',
        component_property='figure'
    ),
    Input(
        component_id='site-dropdown',
        component_property='value'
    )
)
def get_pie_chart(entered_site):

    # If ALL sites are selected
    if entered_site == 'ALL':

        # Count successful and unsuccessful launches
        success_counts = (
            spacex_df['class']
            .value_counts()
            .reset_index()
        )

        success_counts.columns = ['class', 'count']

        fig = px.pie(
            success_counts,
            values='count',
            names='class',
            title='Total Launch Outcomes'
        )

    # If a specific launch site is selected
    else:

        filtered_df = spacex_df[
            spacex_df['Launch Site'] == entered_site
        ]

        success_counts = (
            filtered_df['class']
            .value_counts()
            .reset_index()
        )

        success_counts.columns = ['class', 'count']

        fig = px.pie(
            success_counts,
            values='count',
            names='class',
            title=f'Launch Outcomes for {entered_site}'
        )

    return fig


# =======================================================
# TASK 4:
# Callback for site-dropdown and payload-slider
# =======================================================

@app.callback(
    Output(
        component_id='success-payload-scatter-chart',
        component_property='figure'
    ),
    [
        Input(
            component_id='site-dropdown',
            component_property='value'
        ),
        Input(
            component_id='payload-slider',
            component_property='value'
        )
    ]
)
def get_scatter_chart(entered_site, payload_range):

    # Get selected payload range
    low, high = payload_range

    # Filter by payload range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # If a specific launch site is selected
    if entered_site != 'ALL':

        filtered_df = filtered_df[
            filtered_df['Launch Site'] == entered_site
        ]

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Payload Mass vs. Launch Outcome'
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run()