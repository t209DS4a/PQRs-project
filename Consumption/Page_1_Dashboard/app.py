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


## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
## Start application
app = dash.Dash(__name__)
server = app.server


def load_the_table():    
    df = pd.read_csv('https://docs.google.com/spreadsheets/d/' + 
                   '1qCn8flw5T2hFzn6YHBXHVjYyi0f7WttleD47lh276PY' +
                   '/export?gid=1798431102&format=csv',  #1697607596
                 low_memory=False,
                 index_col=0)

    table_headers = {'no_radicacion': 'N° Radicación',
                 'nombre_completo': 'Nombre Completo',
                 'identificacion': 'N° Documento',
                 'fecha_radicacion': 'Fecha Radicación',
                 'descripcion': 'Tipo PQRS',
                 'glb_estado_id': 'Estado'
                }
    table_df = df[['no_radicacion',
                   'nombre_completo',
                   'identificacion',
                   'fecha_radicacion',
                   'descripcion',
                   'glb_estado_id']]
    table_df.rename(columns=table_headers, inplace=True)
    
    return table_df

#path = '/Users/camilosr/Documents/Data Science/DS4A/Project/Characterization/styles/'
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = [path + 'ibague_styles.css']
PISAMI_LOGO = "https://pisami.ibague.gov.co/app/PISAMI/librerias/imagenes/index/logo_pisami_original.png"
CORR_ONE_LOGO = "https://www.correlation-one.com/hubfs/c1logo_white.png"

## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## Define Table function

def generate_table(df, max_rows = 25):
    # Table Header
    table_header = [
        html.Thead(html.Tr([html.Th(col) for col in df.columns]))
    ]
    # Table Body
    table_body = [html.Tr([
        html.Td(df.iloc[i][col]) for col in df.columns
    ]) for i in range(min(len(df), max_rows))]

    table = dbc.Table(
        table_header + table_body,
        id='table_1',
        className='fl-table',
    )
    
    return table


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
## Dropdown and Search Bar elements
dropDown_1 = dcc.Dropdown(
        id="input_tipo_doc",
       options=[
           {'label': 'Search by document number', 'value': 'n_documento'},
           {'label': 'Search by file Number', 'value': 'n_radicacion'},
       ],
    placeholder="Select Search Type",
    )


search_1 = dcc.Input(
    id="input_no_doc",
    placeholder="Type number...",
    debounce=True
)


## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## Main Table

table_1 = generate_table(load_the_table(), max_rows=20)

table_pagination = dbc.Pagination(max_value=7,
                                  first_last=True,
                                  previous_next=True,
                                  id='pages_csr'
                                 )

## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## Pie Charts

table_df = load_the_table()

pie_estados = table_df.groupby(by=["Estado"]).count()
pie_tipos = table_df.groupby(by=["Tipo PQRS"]).count()

pie_estados['Cantidad'] = pie_estados['N° Radicación']
pie_tipos['Cantidad'] = pie_tipos['N° Radicación']

fig_1 = px.pie(pie_estados, values=pie_estados['Cantidad'], names=pie_estados.index)
fig_2 = px.pie(pie_tipos, values=pie_tipos['Cantidad'], names=pie_tipos.index)



## Define HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout
## Define HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout
## Define HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout - HTML Layout
## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------
## Define HTML Layout - START
## --------------------------------------------------------------------------------------------------------------

app.layout = html.Div([
    html.P(children='Ibague PQRS', id='the_title'),
    navbar,
    
    html.Div([
        dropDown_1,
        search_1,
        ],
    className="buscadores"),
    
    html.Div([html.H2(children='Main Charts', style={'text-align':'center'}),
              dbc.Button("Form", href="http://team209ds4a.atwebpages.com",  target="_blank", className="button_1", id="my_button"),
             dbc.Button("Train", href="http://team209ds4a.atwebpages.com/model.html",  target="_blank", className="button_2", id="my_button_2")]),
    
    html.Div([
        html.Div(
            [html.Div(html.Div(generate_table(load_the_table()), className='table-wrapper')),
            html.Div(table_pagination, className='pagination')],
            className='table-with-paggination',
            id='pagination-contents'
        ),
        
        html.Div([
            dcc.Graph(figure=fig_1, id='estados_pie'),
            dcc.Graph(figure=fig_2, id='tipos_pie'),
        ],
            className="pies_1")
    ],
        className="charts_1"),
    
])

## --------------------------------------------------------------------------------------------------------------
## Define HTML Layout END
## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------
## Create Callbacks and functions to make actionable elements
## --------------------------------------------------------------------------------------------------------------

## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## Filter by document type and Radication number
@app.callback(
    dash.dependencies.Output('table_1', 'children'),
    [dash.dependencies.Input('input_tipo_doc', 'value'),
     dash.dependencies.Input('input_no_doc', 'value')]
)

def display_table(input_tipo_doc, input_no_doc):
    if input_tipo_doc is None:
        return dash.no_update
    
    if (not input_tipo_doc or not input_no_doc):
        return dash.no_update
    
    if input_tipo_doc == 'n_radicacion' and len(input_tipo_doc) < 11:
        return generate_table(load_the_table())

    if input_tipo_doc == 'n_documento':
        input_no_doc = int(input_no_doc)
        dff = load_the_table().loc[table_df['N° Documento'] == input_no_doc]
        return generate_table(dff)
    
    if input_tipo_doc == 'n_radicacion':
        dff = load_the_table().loc[table_df['N° Radicación'] == input_no_doc]
        return generate_table(dff)

## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## Filter table by page number
@app.callback(
    dash.dependencies.Output("pagination-contents", "children"),
    [dash.dependencies.Input('pages_csr', 'active_page')]
)
    
def update_table(active_page):
    max_rows = 25
    active_page += 1
    page_df = table_df.iloc[active_page * max_rows : (active_page + 1) * max_rows]
    return generate_table(page_df), table_pagination


## ----------------------------------------------------------------------------
## ----------------------------------------------------------------------------
## start server
if __name__ == '__main__':
    app.run_server(debug=False)
    #app.run_server(debug=False, port=8050)
