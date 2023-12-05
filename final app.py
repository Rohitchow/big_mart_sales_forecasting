import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

# Load the data
data_file_path = 'Train.csv'  # Update the path if necessary
data = pd.read_csv(data_file_path)

# Preparing data for the dashboard
# Sales Distribution by Item Type
sales_by_item_type = data.groupby('Item_Type')['Item_Outlet_Sales'].sum().reset_index()

# Item Visibility vs Sales
visibility_sales = data[['Item_Visibility', 'Item_Outlet_Sales']]

# Sales Trends Over Years
sales_over_years = data.groupby('Outlet_Establishment_Year')['Item_Outlet_Sales'].sum().reset_index()

# Sales by Outlet Type
sales_by_outlet_type = data.groupby('Outlet_Type')['Item_Outlet_Sales'].sum().reset_index()

# Additional metrics
# Sales vs Item MRP
sales_vs_mrp = data[['Item_MRP', 'Item_Outlet_Sales']]

# Item Type Popularity Over Time
item_type_popularity = data.groupby(['Outlet_Establishment_Year', 'Item_Type'])['Item_Outlet_Sales'].sum().reset_index()

# Sales Distribution by Outlet Size
sales_by_outlet_size = data.groupby('Outlet_Size')['Item_Outlet_Sales'].sum().reset_index()

# Creating the Dash app
app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Big Mart Sales Dashboard'),
    html.Div(children='Dashboard for visualizing sales data.'),

    # Dropdown for filtering by Outlet Location Type
    dcc.Dropdown(
        id='location-dropdown',
        options=[{'label': i, 'value': i} for i in data['Outlet_Location_Type'].unique()],
        value=data['Outlet_Location_Type'].unique()[0],  # Default value
        multi=True
    ),

    # Graph for Sales Distribution by Item Type
    dcc.Graph(id='sales-by-item-type'),

    # Graph for Item Visibility vs Sales
    dcc.Graph(id='visibility-vs-sales'),

    # Graph for Sales Trends Over Years
    dcc.Graph(id='sales-trend'),

    # Graph for Sales by Outlet Type
    dcc.Graph(id='sales-by-outlet-type'),

    # Graph for Sales vs Item MRP
    dcc.Graph(id='sales-vs-mrp'),

    # Graph for Item Type Popularity Over Time
    dcc.Graph(id='item-type-popularity'),

    # Graph for Sales Distribution by Outlet Size
    dcc.Graph(id='sales-by-outlet-size'),
])

# Callback for updating graphs based on selected location
@app.callback(
    [
        Output('sales-by-item-type', 'figure'),
        Output('visibility-vs-sales', 'figure'),
        Output('sales-trend', 'figure'),
        Output('sales-by-outlet-type', 'figure'),
        Output('sales-vs-mrp', 'figure'),
        Output('item-type-popularity', 'figure'),
        Output('sales-by-outlet-size', 'figure')
    ],
    [Input('location-dropdown', 'value')]
)
def update_graph(selected_locations):
    if not isinstance(selected_locations, list):
        selected_locations = [selected_locations]
    # Filter data based on selected location
    filtered_data = data[data['Outlet_Location_Type'].isin(selected_locations)]

    # Update Sales Distribution by Item Type graph
    fig_sales_by_item_type = px.bar(
        filtered_data.groupby('Item_Type')['Item_Outlet_Sales'].sum().reset_index(),
        x='Item_Type', y='Item_Outlet_Sales',
        title='Sales Distribution by Item Type'
    )

    # Update Item Visibility vs Sales graph
    fig_visibility_sales = px.scatter(
        filtered_data, x='Item_Visibility', y='Item_Outlet_Sales',
        title='Item Visibility vs Sales'
    )

    # Update Sales Trends Over Years graph
    fig_sales_trend = px.line(
        filtered_data, x='Outlet_Establishment_Year', y='Item_Outlet_Sales',
        title='Sales Trends Over Years'
    )

    # Update Sales by Outlet Type graph
    fig_sales_by_outlet_type = px.pie(
        filtered_data.groupby('Outlet_Type')['Item_Outlet_Sales'].sum().reset_index(),
        names='Outlet_Type', values='Item_Outlet_Sales',
        title='Sales by Outlet Type'
    )

    # Sales vs Item MRP graph
    fig_sales_vs_mrp = px.scatter(
        filtered_data, x='Item_MRP', y='Item_Outlet_Sales',
        title='Sales vs Item MRP'
    )

    # Item Type Popularity Over Time graph
    fig_item_type_popularity = px.line(
        item_type_popularity, x='Outlet_Establishment_Year', y='Item_Outlet_Sales',
        color='Item_Type', title='Item Type Popularity Over Time'
    )

    # Sales Distribution by Outlet Size graph
    fig_sales_by_outlet_size = px.bar(
        filtered_data.groupby('Outlet_Size')['Item_Outlet_Sales'].sum().reset_index(),
        x='Outlet_Size', y='Item_Outlet_Sales',
        title='Sales Distribution by Outlet Size'
    )

    return fig_sales_by_item_type, fig_visibility_sales, fig_sales_trend, fig_sales_by_outlet_type, fig_sales_vs_mrp, fig_item_type_popularity, fig_sales_by_outlet_size

if __name__== '__main__':
    app.run_server(debug=True)