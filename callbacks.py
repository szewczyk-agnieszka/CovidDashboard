from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime

from app import app

# DATA MAPPING
fg_filepath = 'data/full_grouped.csv'
cwl_filepath = 'data/country_wise_latest.csv'
dw_filepath = 'data/day_wise.csv'
wm_filepath = 'data/worldometer_data.csv'

# IMPORT DATA
fg = pd.read_csv(fg_filepath)
cwl = pd.read_csv(cwl_filepath)
dw = pd.read_csv(dw_filepath)
wm = pd.read_csv(wm_filepath)


# PAGE WORLD
@app.callback(
    Output('fig1_4', 'figure'),
    [Input('user_choice_world', 'value')]
)
def update_graph1_4(value):

    if value == 'Confirmed':
        n = px.colors.sequential.Burg
    elif value == 'Recovered':
        n = px.colors.sequential.algae
    elif value == 'Deaths':
        n = px.colors.sequential.Purp

    fig1_4 = px.choropleth(fg, locations='Country/Region', color=value, locationmode='country names',
                           animation_frame='Date',
                           projection='natural earth',
                           color_continuous_scale=n,
                           hover_name='Country/Region', hover_data={'Country/Region': False}
                           )\
        .update_layout(title={'text': 'Cases over time by country',
                              'y': 0.9,
                              'x': 0.5,
                              }
                       )
    return fig1_4


@app.callback(
    Output('fig1_5', 'figure'),
    [Input('user_choice_world', 'value')]
)
def update_graph1_5(value):

    if value == 'Confirmed':
        c = ['rgb(231,41,138)']
    elif value == 'Recovered':
        c = ['rgb(27,158,119)']
    elif value == 'Deaths':
        c = ['rgb(117,112,179)']

    fig1_5 = px.line(dw, x='Date', y=value, width=950, color_discrete_sequence=c)\
        .update_layout(plot_bgcolor='white',
                       title={'text': 'Cases over time',
                              'y': 0.9,
                              'x': 0.5,
                              },
                       xaxis=dict(title='',
                                  showline=False,
                                  showgrid=True,
                                  gridcolor='rgb(204, 204, 204)'
                                  ),
                       yaxis=dict(title='',
                                  showline=False,
                                  showgrid=True, gridcolor='rgb(204, 204, 204)',
                                  zeroline=True, zerolinewidth=4, zerolinecolor='rgb(204, 204, 204)'
                                  )
                       )
    return fig1_5


@app.callback(
    Output('fig1_6', 'figure'),
    [Input('user_choice_world', 'value')]
)
def update_graph1_6(value):

    temp = pd.merge(fg[['Date', 'Country/Region', 'Confirmed', 'Deaths', 'Recovered']],
                    dw[['Date', 'Confirmed', 'Deaths', 'Recovered']], on='Date')
    temp['% Confirmed'] = round(temp['Confirmed_x'] / temp['Confirmed_y'], 3) * 100
    temp['% Deaths'] = round(temp['Deaths_x'] / temp['Deaths_y'], 3) * 100
    temp['% Recovered'] = round(temp['Recovered_x'] / temp['Recovered_y'], 3) * 100

    if value == 'Confirmed':
        c = px.colors.sequential.Burg
    elif value == 'Recovered':
        c = px.colors.sequential.algae
    elif value == 'Deaths':
        c = px.colors.sequential.Purp

    fig1_6 = px.bar(temp, x='Date', y='% ' + value, color='Country/Region',
                    range_y=(0, 100),
                    color_discrete_sequence=c
                    )\
        .update_layout(plot_bgcolor='white',
                       title={'text': '% Cases over time by country',
                              'y': 0.9,
                              'x': 0.5,
                              },
                       showlegend=False,
                       xaxis=dict(title='',
                                  showline=False,
                                  ),
                       yaxis=dict(title='',
                                  showline=False,
                                  showgrid=True, gridcolor='rgb(204, 204, 204)'
                                  )
                       )

    return fig1_6


# PAGE WHO
@app.callback(
    Output('fig2_2', 'figure'),
    Input('value_x', 'value'),
    Input('value_y', 'value'),
    Input('xaxis_type', 'value'),
    Input('yaxis_type', 'value'),
)
def update_graph2_2(value_x, value_y, xaxis_type, yaxis_type):

    fig2_2 = px.scatter(wm, y=value_y, color='WHO Region', x=value_x,
                        hover_name='Country/Region',
                        color_discrete_map={'Europe': 'rgb(127, 60, 141)',
                                            'WesternPacific': 'rgb(242, 183, 1)',
                                            'Americas': 'rgb(17, 165, 121)',
                                            'South-EastAsia': 'rgb(231, 63, 116)',
                                            'Africa': 'rgb(57, 105, 172)',
                                            'EasternMediterranean': 'rgb(128, 186, 90)'
                                            }
                        )\
        .update_layout(plot_bgcolor='white',
                       showlegend=False,
                       xaxis=dict(showline=False,
                                  showgrid=True, gridcolor='rgb(204, 204, 204)'
                                  ),
                       yaxis=dict(showline=False,
                                  showgrid=True, gridcolor='rgb(204, 204, 204)'
                                  ),
                       height=465,
                       )\
        .update_xaxes(type='log' if xaxis_type == 'Log' else 'linear') \
        .update_yaxes(type='log' if yaxis_type == 'Log' else 'linear')

    return fig2_2


@app.callback(
    Output('fig2_3', 'figure'),
    Input('user_choice_who', 'value')
)
def update_graph2_3(value):

    who = fg.groupby('WHO Region')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum()
    who['Fatality Rate in %'] = round((who['Deaths'] / who['Confirmed']) * 100, 2)
    who['Recovery Rate in %'] = round((who['Recovered'] / who['Confirmed']) * 100, 2)
    who.reset_index(inplace=True)

    fig2_3 = px.bar(who.sort_values(value), y=value, x='WHO Region', text=value, color='WHO Region',
                    color_discrete_map={'Europe': 'rgb(127, 60, 141)',
                                        'Western Pacific': 'rgb(242, 183, 1)',
                                        'Americas': 'rgb(17, 165, 121)',
                                        'South-East Asia': 'rgb(231, 63, 116)',
                                        'Africa': 'rgb(57, 105, 172)',
                                        'Eastern Mediterranean': 'rgb(128, 186, 90)'
                                        },
                    )\
        .update_traces(texttemplate='%{text:.2s}') \
        .update_layout(plot_bgcolor='white',
                       legend_orientation='h',
                       legend_y=-1,
                       xaxis=dict(title='',
                                  tickangle=-45,
                                  showline=False,
                                  showgrid=False,
                                  ),
                       yaxis=dict(title='',
                                  showline=False,
                                  showgrid=True, gridcolor='rgb(204, 204, 204)',
                                  zeroline=True, zerolinecolor='rgb(204, 204, 204)')
                       )

    return fig2_3


# PAGE OTHERS
@app.callback(
    Output('fig3_1', 'figure'),
    Input('user_choice_top', 'value')
)
def update_graph3_1(value):

    top = cwl.sort_values(by='Confirmed', ascending=False)[:10]
    top_country = top['Country/Region'].values
    fg_top = fg[fg['Country/Region'].isin(top_country)]

    fig3_1 = px.line(fg_top, x='Date', y=value, color='Country/Region',
                     color_discrete_map={'US': 'rgb(127, 60, 141)',
                                         'Brazil': 'rgb(17, 165, 121)',
                                         'India': 'rgb(57, 105, 172)',
                                         'Russia': 'rgb(242, 183, 1)',
                                         'South Africa': 'rgb(231, 63, 116)',
                                         'Mexico': 'rgb(128, 186, 90)',
                                         'Peru': 'rgb(230, 131, 16)',
                                         'Chile': 'rgb(0, 134, 149)',
                                         'United Kingdom': 'rgb(207, 28, 144)',
                                         'Iran': 'rgb(249, 123, 114)'
                                         }
                     ) \
        .update_layout(plot_bgcolor='white',
                       xaxis=dict(title='',
                                  showline=False,
                                  showgrid=True,
                                  gridcolor='rgb(204, 204, 204)'
                                  ),
                       yaxis=dict(title='',
                                  showline=False,
                                  showgrid=True, gridcolor='rgb(204, 204, 204)',
                                  zeroline=True, zerolinewidth=4, zerolinecolor='rgb(204, 204, 204)'
                                  ),
                       updatemenus=[dict(type="buttons",
                                         direction="left",
                                         buttons=list([dict(args=[{"yaxis.type": "linear"}],
                                                            label="LINEAR",
                                                            method="relayout"
                                                            ),
                                                       dict(args=[{"yaxis.type": "log"}],
                                                            label="LOG",
                                                            method="relayout"
                                                            )
                                                       ]),
                                         ),
                                    ]
                       )
    return fig3_1


@app.callback(
    Output('fig3_4', 'figure'),
    Input('user_choice_europe', 'value')
)
def update_graph3_4(value):

    europe = fg.groupby(['WHO Region', 'Country/Region'])[
        'WHO Region', 'Confirmed', 'Deaths', 'Recovered', 'Active'].sum()
    europe.reset_index(inplace=True)
    europe = europe[europe['WHO Region'] == 'Europe']

    if value == 'Confirmed':
        c = ['rgb(231,41,138)']
    elif value == 'Recovered':
        c = ['rgb(27,158,119)']
    elif value == 'Deaths':
        c = ['rgb(117,112,179)']
    elif value == 'Active':
        c = ['rgb(217,95,2)']

    fig3_4 = px.histogram(europe, x=value,
                          nbins=50,
                          marginal='box',
                          hover_data={'Country/Region': True},
                          color_discrete_sequence=c
                          ) \
        .update_layout(title={'text': value + ' cases distribution in Europe',
                              'y': 0.9,
                              'x': 0.5,
                              },
                       plot_bgcolor='white',
                       xaxis=dict(title='',
                                  showline=False,
                                  showgrid=True, gridcolor='rgb(204, 204, 204)'
                                  ),
                       yaxis=dict(title='',
                                  showline=False,
                                  showgrid=True, gridcolor='rgb(204, 204, 204)'
                                  )
                       )

    return fig3_4


@app.callback(
    Output('fig3_6', 'figure'),
    Input('user_choice_poland', 'value')
)
def update_graph3_6(value):

    fg_poland = fg[fg['Country/Region'] == 'Poland']
    fg_poland = fg_poland[fg_poland['Confirmed'] > 0]

    d_1 = datetime.datetime.strptime('2020-03-16', "%Y-%m-%d").timestamp() * 1000  # School closures
    d_2 = datetime.datetime.strptime('2020-03-20', "%Y-%m-%d").timestamp() * 1000  # Epidemic State of Emergency
    d_3 = datetime.datetime.strptime('2020-03-25', "%Y-%m-%d").timestamp() * 1000  # Movement restrictions
    d_4 = datetime.datetime.strptime('2020-04-20',
                                     "%Y-%m-%d").timestamp() * 1000  # Defrosting of the Polish economy - Stage I
    d_5 = datetime.datetime.strptime('2020-05-04',
                                     "%Y-%m-%d").timestamp() * 1000  # Defrosting of the Polish economy - Stage II
    d_6 = datetime.datetime.strptime('2020-05-18',
                                     "%Y-%m-%d").timestamp() * 1000  # Defrosting of the Polish economy - Stage III
    d_7 = datetime.datetime.strptime('2020-05-30',
                                     "%Y-%m-%d").timestamp() * 1000  # Defrosting of the Polish economy - Stage IV

    if value == 'New recovered':
        c = ['rgb(27,158,119)']
    elif value == 'New deaths':
        c = ['rgb(117,112,179)']
    elif value == 'New cases':
        c = ['rgb(217,95,2)']

    fig3_6 = px.bar(fg_poland, x='Date', y=value,
                    title=value + ' in Poland over time',
                    color_discrete_sequence=c
                    ) \
        .add_vline(x=d_1, line_width=0.5, line_dash="dot",
                   annotation_text='School closures',
                   annotation_textangle=-90,
                   annotation_position='left top'
                   ) \
        .add_vline(x=d_2, line_width=0.5, line_dash="dot",
                   annotation_text='Epidemic State of Emergency',
                   annotation_textangle=-90,
                   annotation_position='left top'
                   ) \
        .add_vline(x=d_3, line_width=0.5, line_dash="dot",
                   annotation_text='Movement restrictions',
                   annotation_textangle=-90,
                   annotation_position='left top'
                   ) \
        .add_vline(x=d_4, line_width=0.5, line_dash="dot",
                   annotation_text='Defrosting of the Polish economy - Stage I',
                   annotation_textangle=-90,
                   annotation_position='left top'
                   ) \
        .add_vline(x=d_5, line_width=0.5, line_dash="dot",
                   annotation_text='Defrosting of the Polish economy - Stage II',
                   annotation_textangle=-90,
                   annotation_position='left top'
                   ) \
        .add_vline(x=d_6, line_width=0.5, line_dash="dot",
                   annotation_text='Defrosting of the Polish economy - Stage III',
                   annotation_textangle=-90,
                   annotation_position='left top'
                   ) \
        .add_vline(x=d_7, line_width=0.5, line_dash="dot",
                   annotation_text='Defrosting of the Polish economy - Stage IV',
                   annotation_textangle=-90,
                   annotation_position='left top'
                   ) \
        .update_layout(title={'y': 0.95,
                              'x': 0.5,
                              },
                       plot_bgcolor='white',
                       xaxis_title='',
                       yaxis=dict(title='',
                                  showline=False,
                                  showgrid=True, gridcolor='rgb(204, 204, 204)'
                                  ),
                       height=750
                       )
    return fig3_6
