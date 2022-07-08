import pandas as pd
import numpy as npdd

import dash
from dash import Dash
from dash import dcc
from dash import html
from dash import dash_table

import plotly.graph_objects as go
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px

app = dash.Dash(__name__)
server = app.server

PISAMI_LOGO = "https://pisami.ibague.gov.co/app/PISAMI/librerias/imagenes/index/logo_pisami_original.png"
CORR_ONE_LOGO = "https://www.correlation-one.com/hubfs/c1logo_white.png"

## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------

def load_the_table():
    table_df = pd.read_excel(
        'df_training_translated.xlsx',
        index_col=0
    )
    table_df.reset_index(level=0)
    train_ID = table_df.index
    table_df.insert(0, "Train ID", train_ID)
    table_df.columns
    
    
    table_headers = {'Train ID': 'Train ID',
                 'pqr': 'Original PQR',
                 'tipo': 'PQR Type',
                 'pqr_clean': 'Cleaned PQR',
                 'pqr_translate': 'Translated PQR',
                 'tipo_token': 'TOKEN'
                }
    
    table_df.rename(columns=table_headers, inplace=True)
    
    table_df = table_df[['Train ID', 'Original PQR', 'PQR Type', 'Cleaned PQR', 'TOKEN', 'Translated PQR']]
    
    return table_df

table_df = load_the_table()

## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## Define Table function

table_1 = dash_table.DataTable(
    id="fl-table",
    columns=[{"name": i, "id": i} for i in table_df.columns],
    data=table_df.to_dict("records"),
    editable=False,
    column_selectable="single",
    row_deletable=False,
    selected_columns=[],
    selected_rows=[],
    page_action="native",
    page_current=0,
    page_size=25
)


## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------
## Create Plotly Elements
## --------------------------------------------------------------------------------------------------------------

## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## Top Nav bar
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    html.Img(src=PISAMI_LOGO, className="logo_1"),
                ),
                href="https://pisami.ibague.gov.co/app/PISAMI/index.php",
                target="_blank",
                className="nav_logo_1"
            ),

            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    html.Img(src=CORR_ONE_LOGO, className="logo_2"),
                ),
                href="https://www.correlation-one.com/?hsLang=en",
                target="_blank",
                className="nav_logo_2"
            ),
        ]
    ),
    color="dark",
    dark=True,
    className = "topnav",
)

## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## Card

card_model = dbc.Card(
    [
        dbc.CardImg(src="https://hopin.com/quiin/organizations/pictures/000/098/495/original/ds4a-logo_2x.png?1621189739",
                    top=True,
                    className="card-image"),
        dbc.CardBody(
            [
                html.H4("Model: Linear SVM", className="card-title"),
                html.P(
                    "Current Population",
                    className="card-text",
                    id="card_num1"
                ),
            ],
        ),
    ], className='the-card'
)


## Define HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout
## Define HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout
## Define HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout
## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------
## Define HTML Layout - START
## --------------------------------------------------------------------------------------------------------------


## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## Filter table by page number
app.layout = html.Div([
    html.P(children='Ibague PQRS', id='the_title'),
    navbar,
    
    html.Div([html.H2(children='Training Data', style={'text-align':'center'}),
              dbc.Button("form", href="http://team209ds4a.atwebpages.com",  target="_blank", className="button_1", id="my_button"),
             dbc.Button("DASH", href="http://team209ds4a.atwebpages.com/dashboard.html",  target="_blank", className="button_2", id="my_button_2")
             ]),
    
    html.Div([
        html.Div(
            [table_1],
            className='table-with-paggination',
            id='pagination-contents'
        ),
        
        html.Div([
           card_model
        ],
            className="card-container")
    ],
        className="charts_1"),
    
])

## --------------------------------------------------------------------------------------------------------------
## Define HTML Layout END
## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------



@app.callback(
    Output("card_num1", "children"),
    Input("fl-table", "active_cell")
)

def update_card(slct_rows_names):
    if slct_rows_names:
        col = table_df[slct_rows_names["column_id"]]
        val = col[slct_rows_names["row"]]
        return val


if __name__ == "__main__":
    app.run_server(debug=False)
