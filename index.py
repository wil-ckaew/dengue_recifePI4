import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# import from folders/theme changer
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO


# ========== Styles ============ #
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10}
}

config_graph={"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY


# ===== Reading n cleaning File ====== #
df = pd.read_csv('recife-dbf.csv', error_bad_lines=False)
df_cru = df.copy()

# Meses em numeros para poupar memória
df.loc[ df['mês_notificacao'] == 'Jan', 'mês_notificacao'] = 1
df.loc[ df['mês_notificacao'] == 'Fev', 'mês_notificacao'] = 2
df.loc[ df['mês_notificacao'] == 'Mar', 'mês_notificacao'] = 3
df.loc[ df['mês_notificacao'] == 'Abr', 'mês_notificacao'] = 4
df.loc[ df['mês_notificacao'] == 'Mai', 'mês_notificacao'] = 5
df.loc[ df['mês_notificacao'] == 'Jun', 'mês_notificacao'] = 6
df.loc[ df['mês_notificacao'] == 'Jul', 'mês_notificacao'] = 7
df.loc[ df['mês_notificacao'] == 'Ago', 'mês_notificacao'] = 8
df.loc[ df['mês_notificacao'] == 'Set', 'mês_notificacao'] = 9
df.loc[ df['mês_notificacao'] == 'Out', 'mês_notificacao'] = 10
df.loc[ df['mês_notificacao'] == 'Nov', 'mês_notificacao'] = 11
df.loc[ df['mês_notificacao'] == 'Dez', 'mês_notificacao'] = 12

# Algumas limpezas
#df['Valor Pago'] = df['Valor Pago'].str.lstrip('R$ ')
#df.loc[df['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1
#df.loc[df['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0

# Transformando em int tudo que der
df['ds_semana_notificacao'] = df['ds_semana_notificacao'].astype(int)
df['dia_notificacao'] = df['dia_notificacao'].astype(int)
df['mês_notificacao'] = df['mês_notificacao'].astype(int)
df['ano_notificacao'] = df['ano_notificacao'].astype(int)
df['tp_notificacao'] = df['tp_notificacao'].astype(int)


# Criando opções pros filtros que virão
options_month = [{'label': 'Todos os Meses de notificacão', 'value': 0}]
for i, j in zip(df_cru['mês_notificacao'].unique(), df['mês_notificacao'].unique()):
    options_month.append({'label': i, 'value': j})
options_month = sorted(options_month, key=lambda x: x['value']) 

options_team = [{'label': 'Todos os Casos por Ano Notificado', 'value': 0}]
for i in df['notificacao_ano'].unique():
    options_team.append({'label': i, 'value': i})
# ========= Função dos Filtros ========= #
def month_filter(month):
    if month == 0:
        mask = df['mês_notificacao'].isin(df['mês_notificacao'].unique())
    else:
        mask = df['mês_notificacao'].isin([month])
    return mask

def team_filter(team):
    if team == 0:
        mask = df['ano_notificacao'].isin(df['ano_notificacao'].unique())
    else:
        mask = df['ano_notificacao'].isin([team])
    return mask

def convert_to_text(month):
    match month:
        case 0:
            x = 'Todo Ano de notificação'
        case 1:
            x = 'Janeiro'
        case 2:
            x = 'Fevereiro'
        case 3:
            x = 'Março'
        case 4:
            x = 'Abril'
        case 5:
            x = 'Maio'
        case 6:
            x = 'Junho'
        case 7:
            x = 'Julho'
        case 8:
            x = 'Agosto'
        case 9:
            x = 'Setembro'
        case 10:
            x = 'Outubro'
        case 11:
            x = 'Novembro'
        case 12:
            x = 'Dezembro'
    return x


# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    # Armazenamento de dataset
    # dcc.Store(id='dataset', data=df_store),

    # Layout
    # Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([  
                            html.Legend("Analise de Dados")
                        ], sm=8),
                        dbc.Col([        
                            html.I(className='fa fa-eercast', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Projeto Integrador 4")
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="https://github.com/wil-ckaew", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Analise de Dados por casos de dengue Municipio Recife-SP')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ], sm=12, lg=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o mês de notificacao'),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_month,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                            ),
                            html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph3', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph5', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph6', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        # grafico 7
                        html.H4('Dados da semana por Ano'), 
                        dcc.Graph(id='graph7', className='dbc', config=config_graph)
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([
                # Grafico 8 
                html.H4('Dados da semana por Febre'),
                dcc.Graph(id='graph8', className='dbc', config=config_graph)
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),
    
    # Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    # Grafico 9
                    html.H4('Casos da semana por bairro'),
                    dcc.Graph(id='graph9', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    # Grafico 10
                    html.H4("Dados semana por mês notificação por Município"),
                    dcc.Graph(id='graph10', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph11', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Escolha a Caso confirmado'),
                    dbc.RadioItems(
                        id="radio-team",
                        options=options_team,
                        value=0,
                        inline=True,
                        labelCheckedClassName="text-warning",
                        inputCheckedClassName="border border-warning bg-warning",
                    ),
                    html.Div(id='team-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
    ], className='g-2 my-auto', style={'margin-top': '7px'}),


    
], fluid=True, style={'height': '100vh'})


# ======== Callbacks ========== #
# Graph 1 and 2
@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('month-select', 'children'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph1(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    B1_Dados = df.loc[mask]

    #B1_Dados = B1_Dados.groupby(['ds_semana_notificacao', 'mês_notificacao'])['chuva'].sum()
    # B1_Dados = # analise por caso Dengue
    B1_Dados = df.groupby( by=['mês_notificacao'] ).sum().reset_index()[['mês_notificacao', 'ds_semana_notificacao']].sort_values( 'ds_semana_notificacao', ascending=False )
    #Analise_03.head()

  

    B2_Dados = df.groupby('mês_notificacao')['ds_semana_notificacao'].sum().reset_index()

    fig2 = go.Figure(go.Scatter(
        x=B2_Dados['mês_notificacao'], 
        y=B2_Dados['ds_semana_notificacao'], 
        mode='lines', fill='tonexty')
        )
    fig1 = go.Figure(go.Bar(x=B1_Dados['mês_notificacao'], y=B1_Dados['ds_semana_notificacao'], textposition='auto', text=B1_Dados['mês_notificacao']))
    fig1.update_layout(main_config, height=200, template=template)
    fig2.update_layout(main_config, height=200, template=template, showlegend=False)

    select = html.H1(convert_to_text(month))

    return fig1, fig2, select

# Graph 3
@app.callback(
    Output('graph3', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph3(team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = team_filter(team)
    B3_Dados = df.loc[mask]

    B3_Dados = B3_Dados.groupby('ano_notificacao')['ds_semana_notificacao'].sum().reset_index()
    fig3 = go.Figure(go.Scatter(
    x=B3_Dados['ano_notificacao'], y=B3_Dados['ds_semana_notificacao'], mode='lines', fill='tonexty'))
    # grafico 3
    fig3.add_annotation(text='Média de Dados semana por ano de notificacáo', 
        xref="paper", yref="paper",
        font=dict(
            size=17,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
    fig3.add_annotation(text=f"Média : {round(B3_Dados['ds_semana_notificacao'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)

    fig3.update_layout(main_config, height=180, template=template)
    return fig3

# Graph 4
@app.callback(
    Output('graph4', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph4(team, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = team_filter(team)
    B4_Dados = df.loc[mask]

    B4_Dados = B4_Dados.groupby('mês_notificacao')['febre'].sum().reset_index()
    fig4 = go.Figure(go.Scatter(x=B4_Dados['mês_notificacao'], y=B4_Dados['febre'], mode='lines', fill='tonexty'))
    # grafico 4
    fig4.add_annotation(text='Casos Confirmados por Médias por mês de notificacao por febre',
        xref="paper", yref="paper",
        font=dict(
            size=15,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
    fig4.add_annotation(text=f"Média : {round(B4_Dados['febre'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)

    fig4.update_layout(main_config, height=180, template=template)
    return fig4

# Indicators 1 and 2 ------ Graph 5 and 6
@app.callback(
    Output('graph5', 'figure'),
    Output('graph6', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph5(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    B5_Dados = B6_Dados = df.loc[mask]
    
    B5_Dados = B5_Dados.groupby(['mês_notificacao', 'ds_semana_notificacao'])['notificacao_ano'].sum()
    B5_Dados.sort_values(ascending=False, inplace=True)
    B5_Dados = B5_Dados.reset_index()
    fig5 = go.Figure()
    # Grafico 5
    fig5.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span>{B5_Dados['mês_notificacao'].iloc[0]} - Febre </span><br><span style='font-size:70%'>Mês ao Ano notificado - em relação a média</span><br>"},
        value = B5_Dados['notificacao_ano'].iloc[0],
        number = {'prefix': ""},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': B5_Dados['notificacao_ano'].mean()}
    ))

    B6_Dados = B6_Dados.groupby('ds_semana_notificacao')['mês_notificacao'].sum()
    B6_Dados.sort_values(ascending=False, inplace=True)
    B6_Dados = B6_Dados.reset_index()
    fig6 = go.Figure()
    fig6.add_trace(go.Indicator(mode='number+delta',
        # Grafico 6
        title = {"text": f"<span>{B6_Dados['ds_semana_notificacao'].iloc[0]} - Febre </span><br><span style='font-size:70%'>Semana ao Mês - em relação a média</span><br>"},
        value = B6_Dados['mês_notificacao'].iloc[0],
        number = {'prefix': ""},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': B6_Dados['mês_notificacao'].mean()}
    ))

    fig5.update_layout(main_config, height=200, template=template)
    fig6.update_layout(main_config, height=200, template=template)
    fig5.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    fig6.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    return fig5, fig6

# Graph 7
@app.callback(
  Output('graph7', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph7(toggle):
    template = template_theme1 if toggle else template_theme2

    B7_Dados = df.groupby('ds_semana_notificacao')['notificacao_ano'].sum()
    #B7_Dados_group = B7_Dados.groupby('mês_notificacao')['chuva'].sum().reset_index()
    
    #fig7 = px.line(B7_Dados, y="chuva", x="mês_notificacao", color="ds_semana_notificacao")
   # fig7.add_trace(go.Scatter(y=B7_Dados_group["chuva"], x=B7_Dados_group["mês_notificacao"], mode='lines+markers', fill='tonexty', name='total casos grafico 7'))
    fig7 = go.Figure()
    fig7.add_trace(go.Pie(labels=['dasos da semana por notificacao', 'notificacao por ano'], values=B7_Dados, hole=.6))
    


    fig7.update_layout(main_config, yaxis={'title': None}, xaxis={'title': None}, height=190, template=template)
    fig7.update_layout({"legend": {"yanchor": "top", "y":0.99, "font" : {"color":"white", 'size': 10}}})
    return fig7

# Graph 8
@app.callback(
    Output('graph8', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph8(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    B8_Dados = df.loc[mask]

    B8_Dados = B8_Dados.groupby('ds_semana_notificacao')['febre'].sum().reset_index()
    fig8 = go.Figure(go.Bar(
        x=B8_Dados['febre'],
        y=B8_Dados['ds_semana_notificacao'],
        orientation='h',
        textposition='auto',
        text=B8_Dados['febre'],
        insidetextfont=dict(family='Times', size=12)))

    fig8.update_layout(main_config, height=360, template=template)
    return fig8

# Graph 9
@app.callback(
    Output('graph9', 'figure'),
    Input('radio-month', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph9(month, team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    B9_Dados = df.loc[mask]

    mask = team_filter(team)
    B9_Dados = B9_Dados.loc[mask]

    B9_Dados = B9_Dados.groupby('ds_semana_notificacao')['co_bairro_residencia'].sum().reset_index()

    fig9 = go.Figure()
    fig9.add_trace(go.Pie(labels=B9_Dados['ds_semana_notificacao'], values=B9_Dados['co_bairro_residencia'], hole=.7))

    fig9.update_layout(main_config, height=450, template=template, showlegend=False)
    return fig9

# Graph 10
@app.callback(
    Output('graph10', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph10(team, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = team_filter(team)
    df_10 = df.loc[mask]

    df10 = df_10.groupby(['ds_semana_notificacao', 'mês_notificacao'])['co_municipio_infeccao'].sum().reset_index()
    fig10 = px.line(df10, y="co_municipio_infeccao", x="mês_notificacao", color="ds_semana_notificacao")

    fig10.update_layout(main_config, height=400, template=template, showlegend=False)
    return fig10

# Graph 11
@app.callback(
    Output('graph11', 'figure'),
    Output('team-select', 'children'),
    Input('radio-month', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph11(month, team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_11 = df.loc[mask]

    mask = team_filter(team)
    df_11 = df_11.loc[mask]

    fig11 = go.Figure()
    fig11.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span style='font-size:150%'>Febre Total</span><br><span style='font-size:70%'>Em Numeros</span><br>"},
        value = df_11['febre'].sum(),
        number = {'prefix': "Total :"}
    ))

    fig11.update_layout(main_config, height=300, template=template)
    select = html.H1("Todos febre confirmados") if team == 0 else html.H1(team)

    return fig11, select

# Run server
if __name__ == '__main__':
    app.run_server(debug=False)
