from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go

app = Dash(__name__,external_stylesheets=[dbc.themes.COSMO])
server = app.server

df=pd.read_excel('2024.02.28_Updated Transp. Index 2023.xlsx',sheet_name='Full Dataset_Board', nrows=500)
#data2=data[data['Date Local'].str.slice(0,4).astype(int) >= 2006]

#app = Dash(__name__)
# app.layout = dbc.Container(
#     dbc.Alert("Hello Bootstrap!", color="success"),
#     className="p-5",
# )

def company_list(sector):
    dfcs = df.loc[df['GICS.Sector'] == sector,['Company.Name','CM7a.GHG.Emissions.','CM7b.GHG.Emissions.'
                                                       ,'CM7c.GHG.Emissions.','TCFD New','CM9.Land.use.and.eco','Water amount Index','water stress index','Revenue']]
    dfcs.rename(columns={"Company.Name": "Company","CM7a.GHG.Emissions.": "GHG Scope 1 Emission", "CM7b.GHG.Emissions.": "GHG Scope 2 Emission",
                     "CM7c.GHG.Emissions.": "GHG Scope 3 Emission", "TCFD New": "TCFD",
                     "CM9.Land.use.and.eco": "Biodiversity", "Water amount Index": "Water Disclosure",
                     "water stress index": "Water Stress Disclosure",
                     "Revenue": "Revenue"},inplace=True)
    
    dfcs = dfcs.sort_values(by=['Revenue'], ascending=False)
    
    companies = dfcs['Company'].tolist()
    top_companies = dfcs.head(10)['Company'].tolist()
    
    return sorted(companies), sorted(top_companies)

def trafficlight(sector,company_list):
    dfcs = df.loc[df['GICS.Sector'] == sector,['Company.Name','CM7a.GHG.Emissions.','CM7b.GHG.Emissions.'
                                                       ,'CM7c.GHG.Emissions.','TCFD New','CM9.Land.use.and.eco','Water amount Index','water stress index','Revenue']]
    dfcs.rename(columns={"Company.Name": "Company","CM7a.GHG.Emissions.": "GHG Scope 1 Emission", "CM7b.GHG.Emissions.": "GHG Scope 2 Emission",
                     "CM7c.GHG.Emissions.": "GHG Scope 3 Emission", "TCFD New": "TCFD",
                     "CM9.Land.use.and.eco": "Biodiversity", "Water amount Index": "Water Disclosure",
                     "water stress index": "Water Stress Disclosure",
                     "Revenue": "Revenue"},inplace=True)
    
    mask = dfcs['Company'].isin(company_list)
    
    dfcs_melted = dfcs[mask].melt(id_vars=['Company'], var_name='Metric', value_name='Status')
    

    dfcs_melted['Status'].astype('string')
    categorical_mapping = {1.0: 'Full Disclosure', 0.5: 'Partial Disclosure', 0.0: 'No Disclosure'}
    dfcs_melted['Status'] = dfcs_melted['Status'].map(categorical_mapping)
    
    fig = px.scatter(dfcs_melted, y="Company", x="Metric", color="Status",
                     color_discrete_sequence=['#4E7E6B','#FFD100','#F47C30'],
                     #width = 2000, 
                     height = 1000, 
                     #title='Disclosure Status for Consumer Staples Environmental Metrics'
                    )
    fig.update_traces(marker_size=25)
    fig.update_layout(plot_bgcolor="white", font_family='Helvetica', title_font_family="Helvetica",
                      title_x=0.5,xaxis=dict(side="top"),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None))
    fig.update_yaxes(categoryorder='category descending', title=None)
    fig.update_xaxes(title=None)
    fig.add_shape(
        type="line",
        x0=0,
        y0=1,
        x1=1,
        y1=1,
        line=dict(
            color="black",
            width=1,
        ),
        xref="paper",
        yref="paper"
    )
    
    return fig

# def temporaldist(state, gas):
#     data5=data2.loc[(data2['State'] == state),['State','Date Local',gas[0],gas[1],gas[2]]]
#     data5['Year']=data5['Date Local'].str.slice(0,4)
#     data5.drop(['Date Local'],axis=1,inplace=True)
#     data5=data5.groupby(['State','Year',gas[2]], as_index=False).mean()
    
#     fig = go.Figure()

#     fig.add_trace(go.Scatter(x=data5['Year'], y=data5[gas[1]], mode='lines',
#                              name='AQI',
#                              line=dict(color='#003B5C', width=2),
#                              connectgaps=True
#     ))

#     # endpoints
#     fig.add_trace(go.Scatter(
#         x=data5['Year'],
#         y=data5[gas[1]],
#         mode='markers',
#         marker=dict(color='#003B5C', size=8),
#         name="",
#         showlegend=False
#     ))
    
#     fig.add_trace(go.Scatter(x=data5['Year'], y=data5[gas[0]], mode='lines',
#                              name='Mean ({unit})'.format(unit=data5[gas[2]][0]),
#                              line=dict(color='#F47C30', width=4),
#                              connectgaps=True
#     ))

#     # endpoints
#     fig.add_trace(go.Scatter(
#         x=data5['Year'],
#         y=data5[gas[0]],
#         mode='markers',
#         marker=dict(color='#F47C30', size=12),
#         name="",
#         showlegend=False
#     ))
    
#     fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)',
#                       'paper_bgcolor': 'rgba(0, 0, 0, 0)'},
#                       title={
#                           'text': "Temporal trend",
#                           'y':0.9,
#                           'x':0.5,
#                           'xanchor': 'center',
#                           'yanchor': 'top'},
#                       legend=dict(
#                           orientation="h",
#                           yanchor="bottom",
#                           y=1.02,
#                           xanchor="right",
#                           x=1
#                       ),
#                       xaxis_title="Year",
#                       yaxis_title="Measure")
    
#     return fig


navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/Impact_Logo_Wht_PMScoated.png', height="30px"))
                    ],
                    align="center",
                    className="g-0",
                ),
                href="#",
                style={"textDecoration": "none"},
            ),
            dbc.Row(
                    [dbc.Col(dbc.NavbarBrand("OFG Case Study", className="ms-2")),
                     dbc.Col(width=1)
                    ],
                    align="center",
                    className="g-0",
                ),
            html.A()
        ],fluid=True
    ),
    color="#313339",
    dark=True,
)

card1=dbc.Card([
    dbc.CardHeader("Disclosure Status for Consumer Staples Environmental Metrics",style={'background-color': '#C3D7EE', 'text-align': 'center','font-weight': 'bold','font-style': 'italic'}),
    dbc.CardBody(
        [
            dbc.Row([dbc.Col(dcc.Graph(id="trafficlight"))]),
            dbc.Row([dbc.Col(html.P(id="test"))])
                ])
    
],className="m-1")


card2=dbc.Card([
    dbc.CardHeader("Selection",style={'background-color': '#C3D7EE', 'text-align': 'center','font-weight': 'bold','font-style': 'italic'}),
    dbc.CardBody(
        [
            dbc.Row([
                dbc.Col([
                    html.P("Sector",style={ 'display': 'flex',  'justify-content':'center'})],width=12)
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(options = [{'label': x, 'value': x} for x in set(df['GICS.Sector'].tolist()) if x is not None and not pd.isnull(x)],
                    value='Consumer Staples',
                    id='sector_select')
                ,width=12)
            ]),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.P("Companies",style={ 'display': 'flex',  'justify-content':'center'})],width=12)
            ]),
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(multi=True,
                    id='company_select')
                ,width=12)
            ])
        ])
    
],className="m-1")

app.layout = html.Div([
    dbc.Row([dbc.Col(navbar)],className="mb-4"),
    dbc.Row([dbc.Col([card2],width=3),dbc.Col([card1],width=9)],className="mb-4 ml-3")
])


@callback(
    Output('trafficlight', 'figure'),
    [State('sector_select', 'value')],
    [Input('company_select', 'value')]
)
def update_statew(sector,company_list):
    #gas_units = ['{k} Mean'.format(k=gas),'{k} AQI'.format(k=gas),'{k} Units'.format(k=gas)]
    fig=trafficlight(sector,company_list)
    return fig


@callback(
    [Output('company_select', 'options'),
     Output('company_select', 'value')],
    [Input('sector_select', 'value')]
)
def update_companylist(sector):
    companies, top_companies = company_list(sector)
    options = [{'label': x, 'value': x} for x in companies]
    value = top_companies
    return options,value

# @callback(
#     Output('timedist', 'figure'),
#     [Input('state_select', 'value'),
#      Input('gas_select2', 'value')]
# )
# def update_timew(state,gas):
#     gas_units = ['{k} Mean'.format(k=gas),'{k} AQI'.format(k=gas),'{k} Units'.format(k=gas)]
#     fig=temporaldist(state,gas_units)
#     return fig

if __name__ == '__main__':
    app.run(debug=True, port=8000)
