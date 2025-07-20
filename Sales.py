import dash
from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

# Load your CSV file
df = pd.read_csv('PSales.csv')  

# Initialize Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Product Sales Dashboard", style={'textAlign': 'center', 'color': '#0f02f5'}),

    html.Div([
        html.Label("Select Category:", style={'fontWeight': 'bold', 'textAlign': 'center', 'color': '#0f02f5'}),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': c, 'value': c} for c in df['Category'].unique()],
            multi=True,
            placeholder="Select one or more categories"
        )
    ]),

    html.Div([
        html.Div([dcc.Graph(id='bar-chart')], style={'flex': '1', 'padding': '10px'}),
        html.Div([dcc.Graph(id='pie-chart')], style={'flex': '1', 'padding': '10px'}),
        html.Div([dcc.Graph(id='sunburst-chart')], style={'flex': '1', 'padding': '10px'}),
    ], style={'display': 'flex'}),
])

# Callback
@app.callback(
    Output('bar-chart', 'figure'),
    Output('pie-chart', 'figure'),
    Output('sunburst-chart', 'figure'),
    Input('category-dropdown', 'value')
)
def update_charts(selected_categories):
    if not selected_categories:
        return dash.no_update, dash.no_update, dash.no_update

    filtered_df = df[df['Category'].isin(selected_categories)]

    bar_fig = px.bar(
        filtered_df.groupby('SubCategory')['Sales'].sum().reset_index(),
        x='SubCategory',
        y='Sales',
        title='Sales by SubCategory',
        labels={'Sales': 'Total Sales'}
    )

    pie_fig = px.pie(
        filtered_df.groupby('SubCategory')['Profit'].sum().reset_index(),
        names='SubCategory',
        values='Profit',
        title='Profit by Category'
    )

    sunburst_fig = px.sunburst(
        filtered_df,
        path=['Category', 'SubCategory', 'Discount'],
        values='Discount',
        title='Discount Breakdown'
    )

    return bar_fig, pie_fig, sunburst_fig

app.run(debug=True)

