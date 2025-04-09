import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__)

# Custom CSS styles
styles = {
    'container': {
        'max-width': '1200px',
        'margin': '0 auto',
        'padding': '20px',
        'font-family': 'Arial, sans-serif',
        'background-color': '#f8f9fa'
    },
    'header': {
        'text-align': 'center',
        'color': '#2c3e50',
        'padding': '20px',
        'margin-bottom': '30px',
        'background-color': 'white',
        'border-radius': '10px',
        'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'
    },
    'radio-container': {
        'background-color': 'white',
        'padding': '20px',
        'border-radius': '10px',
        'margin-bottom': '20px',
        'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'
    },
    'radio-group': {
        'display': 'flex',
        'justify-content': 'center',
        'gap': '20px'
    },
    'radio-item': {
        'display': 'inline-block',
        'margin-right': '20px',
        'color': '#2c3e50'
    },
    'graph-container': {
        'background-color': 'white',
        'padding': '20px',
        'border-radius': '10px',
        'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'
    }
}

# Read the processed data
df = pd.read_csv('data/processed_sales_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Initialize the app layout
app.layout = html.Div(
    style=styles['container'],
    children=[
        html.H1(
            'Soul Foods Pink Morsel Sales Analysis',
            style=styles['header']
        ),
        html.Div(
            style=styles['radio-container'],
            children=[
                html.H3('Select Region:', style={'text-align': 'center', 'margin-bottom': '15px'}),
                dcc.RadioItems(
                    id='region-filter',
                    options=[
                        {'label': region.capitalize(), 'value': region}
                        for region in ['all'] + sorted(df['region'].unique().tolist())
                    ],
                    value='all',
                    style=styles['radio-group'],
                    inputStyle={'margin-right': '5px'},
                    labelStyle=styles['radio-item']
                )
            ]
        ),
        html.Div(
            style=styles['graph-container'],
            children=[
                dcc.Graph(id='sales-chart')
            ]
        )
    ]
)

@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_graph(selected_region):
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    # Group by date and calculate total sales
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    
    # Create the line chart
    fig = px.line(
        daily_sales,
        x='date',
        y='sales',
        title=f'Daily Sales Over Time - {selected_region.capitalize()} Region' if selected_region != 'all' else 'Daily Sales Over Time - All Regions'
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
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        title_x=0.5,
        title_font_size=20,
        font_family="Arial, sans-serif",
        showlegend=False,
        margin=dict(t=50, l=50, r=30, b=50)
    )
    
    # Update axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0,0,0,0.1)'
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(0,0,0,0.1)'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True) 