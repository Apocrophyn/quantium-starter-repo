import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Read the processed data
df = pd.read_csv('data/processed_sales_data.csv')

# Convert date to datetime
df['date'] = pd.to_datetime(df['date'])

# Group by date and calculate total sales
daily_sales = df.groupby('date')['sales'].sum().reset_index()

# Create the line chart
fig = px.line(
    daily_sales, 
    x='date', 
    y='sales',
    title='Daily Sales Over Time'
)

# Add vertical line for price increase date
price_increase_date = '2021-01-15'
fig.add_vline(
    x=price_increase_date,
    line_dash="dash",
    line_color="red",
    annotation_text="Price Increase",
    annotation_position="top right"
)

# Customize the layout
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Total Sales ($)",
    hovermode='x unified'
)

# Define the app layout
app.layout = html.Div([
    html.H1(
        'Soul Foods Pink Morsel Sales Analysis',
        style={'textAlign': 'center', 'color': '#2c3e50', 'padding': '20px'}
    ),
    html.Div([
        dcc.Graph(
            id='sales-chart',
            figure=fig
        )
    ], style={'padding': '20px'})
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True) 