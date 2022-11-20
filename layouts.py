from dash import dcc, html
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import datetime

from app import app

navbarcurrentpage = {
    'text-decoration': 'underline',
    'text-decoration-color': 'black',
    'text-decoration-style': 'double'
}

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

# TRANSFORM DATA AND GRAPHS

# PAGE WORLD
temp = dw[['Date', 'Deaths', 'Recovered', 'Active']].tail(1)
temp = temp.melt(value_vars=['Active', 'Deaths', 'Recovered'])

fig1_1 = px.treemap(temp, path=['variable'], values='value',
                    color_discrete_sequence=px.colors.qualitative.Dark2,
                    ) \
    .update_traces(textposition='middle center', textinfo='label+value',
                   hovertemplate=None
                   ) \
    .update_layout(
    height=90,
    margin=dict(autoexpand=False, l=10, r=10, t=0, b=0)
)

fig1_2 = px.area(dw, x='Date', y=['Recovered', 'Active', 'Deaths'],
                 labels={'variable': 'Cases'},
                 color_discrete_sequence=px.colors.qualitative.Dark2
                 ) \
    .update_layout(plot_bgcolor='white',
                   legend_orientation='h',
                   xaxis=dict(title='',
                              showline=False,
                              showgrid=True, gridcolor='rgb(204, 204, 204)',
                              rangeslider_visible=True
                              ),
                   yaxis=dict(title='',
                              showline=False,
                              showgrid=True, gridcolor='rgb(204, 204, 204)',
                              autorange=True, fixedrange=False
                              )
                   )

fig1_3 = px.scatter_geo(fg, locations='Country/Region', color="WHO Region", locationmode='country names',
                        size='Confirmed',
                        animation_frame='Date',
                        projection='natural earth',
                        color_discrete_sequence=px.colors.qualitative.Dark2,
                        hover_name="Country/Region", hover_data={'Country/Region': False},
                        height=540
                        ) \
    .update_traces(marker_sizemin=2
                   )

# PAGE WHO
who = fg.groupby('WHO Region')['Confirmed', 'Deaths', 'Recovered', 'Active'].sum()
who['Fatality Rate in %'] = round((who['Deaths'] / who['Confirmed']) * 100, 2)
who['Recovery Rate in %'] = round((who['Recovered'] / who['Confirmed']) * 100, 2)
who.reset_index(inplace=True)

fig2_1 = px.bar(who, x='WHO Region', y=['Recovered', 'Active', 'Deaths'],
                labels={'value': '', 'Date': '', 'variable': 'Cases'},
                color_discrete_sequence=px.colors.qualitative.Dark2
                ) \
    .update_layout(plot_bgcolor='white',
                   legend_orientation='h',
                   legend_y=1.1,
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

who_s = fg.groupby(['WHO Region', 'Country/Region'])['WHO Region', 'Deaths', 'Recovered', 'Active'].sum()
who_s.reset_index(inplace=True)
who_s = who_s.melt(id_vars=['WHO Region', "Country/Region"], value_vars=['Recovered', 'Active', 'Deaths'],
                   var_name='Case', value_name='Count')

fig2_2 = px.sunburst(who_s, path=['WHO Region', 'Country/Region', 'Case', 'Count'],
                     maxdepth=3,
                     width=900, height=600,
                     title='Basic Statistics for WHO Region and country'
                     ) \
    .update_traces(hovertemplate=None
                   )

fig2_4 = make_subplots(rows=2, cols=2,
                       specs=[[{'type': 'pie'}, {'type': 'pie'}], [{'type': 'pie'}, {'type': 'pie'}]],
                       subplot_titles=('Confirmed cases', 'Recovered cases', 'Deaths cases', 'Active cases')) \
    .add_trace(go.Pie(labels=who['WHO Region'], values=who['Confirmed'],
                      name='Confirmed',
                      marker_colors=['rgb(57, 105, 172)', 'rgb(17, 165, 121)', 'rgb(128, 186, 90)', 'rgb(127, 60, 141)',
                                     'rgb(231, 63, 116)', 'rgb(242, 183, 1)']),
               1, 1) \
    .add_trace(go.Pie(labels=who['WHO Region'], values=who['Recovered'],
                      name='Recovered'),
               1, 2) \
    .add_trace(go.Pie(labels=who['WHO Region'], values=who['Deaths'],
                      name='Deaths'),
               2, 1) \
    .add_trace(go.Pie(labels=who['WHO Region'], values=who['Active'],
                      name='Active'),
               2, 2) \
    .update_layout(showlegend=False,
                   height=600)

# PAGE OTHERS

top = cwl.sort_values(by='Confirmed', ascending=False)[:10]
top_country = top['Country/Region'].values

fig3_2 = px.scatter(top, x="Confirmed", y="Deaths", size='Recovered',
                    color='Country/Region',
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
                                        },
                    hover_name="Country/Region", ) \
    .update_layout(title=' 2D Plot of Confirmed, Deaths and Recovered Cases',
                   plot_bgcolor='white',
                   xaxis=dict(showline=False,
                              showgrid=True, gridcolor='rgb(204, 204, 204)'
                              ),
                   yaxis=dict(showline=False,
                              showgrid=True, gridcolor='rgb(204, 204, 204)'
                              )
                   )

fig3_3 = px.scatter_3d(top, x='Confirmed', z='Deaths', y='Recovered',
                       color='Country/Region', log_x=True,
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
                                           }) \
    .update_layout(title='3D Plot of Confirmed, Deaths and Recovered Cases',
                   showlegend=False
                   )

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

fig3_5 = px.line(fg_poland, x='Date', y=['Confirmed', 'Deaths', 'Recovered', 'Active'],
                 labels={'variable': 'Cases'},
                 title='Basic Statistics of Covid 19 in Poland',
                 color_discrete_map={'Confirmed': 'rgb(231,41,138)',
                                     'Deaths': 'rgb(117,112,179)',
                                     'Recovered': 'rgb(27,158,119)',
                                     'Active': 'rgb(217,95,2)'
                                     }
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
    .update_layout(plot_bgcolor='white',
                   title={
                       'y': 0.95,
                       'x': 0.5,
                   },
                   xaxis_title='',
                   yaxis=dict(title='',
                              showline=False,
                              showgrid=True, gridcolor='rgb(204, 204, 204)',
                              zeroline=True, zerolinewidth=4, zerolinecolor='rgb(204, 204, 204)'
                              ),
                   height=790
                   )


# FUNCTIONS

def get_header():
    header = html.Div([
        html.H1(children='The spread of Covid 19',
                style={'textAlign': 'center', 'color': 'black'})
    ], style={'background-color': 'LightGrey'})

    return header


def get_navbar(p='world'):
    navbar_world = html.Div([

        html.Div([], className='col-3'),
        html.Div([
            dcc.Link(html.H4(children='World', style=navbarcurrentpage), href='/apps/world')
        ], className='col-2'),
        html.Div([
            dcc.Link(html.H4(children='WHO Region'), href='/apps/who')
        ], className='col-2'),
        html.Div([
            dcc.Link(html.H4(children='Others'), href='/apps/others')
        ], className='col-2'),
        html.Div([], className='col-3')

    ], className='row', style={'background-color': 'white', 'box-shadow': '2px 5px 5px 1px rgba(0, 0, 0, .5)'})

    navbar_who = html.Div([

        html.Div([], className='col-3'),
        html.Div([
            dcc.Link(html.H4(children='World'), href='/apps/world')
        ], className='col-2'),
        html.Div([
            dcc.Link(html.H4(children='WHO Region', style=navbarcurrentpage), href='/apps/who')
        ], className='col-2'),
        html.Div([
            dcc.Link(html.H4(children='Others'), href='/apps/others')
        ], className='col-2'),
        html.Div([], className='col-3')

    ], className='row', style={'background-color': 'white', 'box-shadow': '2px 5px 5px 1px rgba(0, 0, 0, .5)'})

    navbar_others = html.Div([

        html.Div([], className='col-3'),
        html.Div([
            dcc.Link(html.H4(children='World'), href='/apps/world')
        ], className='col-2'),
        html.Div([
            dcc.Link(html.H4(children='WHO Region'), href='/apps/who')
        ], className='col-2'),
        html.Div([
            dcc.Link(html.H4(children='Others', style=navbarcurrentpage), href='/apps/others')
        ], className='col-2'),
        html.Div([], className='col-3')

    ], className='row', style={'background-color': 'white', 'box-shadow': '2px 5px 5px 1px rgba(0, 0, 0, .5)'})

    if p == 'world':
        return navbar_world
    elif p == 'who':
        return navbar_who
    else:
        return navbar_others


def get_emptyrow(h='25px'):
    emptyrow = html.Div([

        html.Div([
            html.Br()
        ], className='col-12')

    ], className='row', style={'height': h})

    return emptyrow


# LAYOUT PAGE WORLD
world = html.Div([

    get_header(),

    get_navbar('world'),

    get_emptyrow(),

    html.Div([

        html.Div([
            html.Div([
                dcc.Graph(id='fig1_1', figure=fig1_1),
                dcc.Graph(id='fig1_2', figure=fig1_2)
            ], className='card_container'),
        ], className='col-6'),
        html.Div([
            html.Div([
                dcc.Graph(id='fig1_3', figure=fig1_3)
            ], className='card_container'),
        ], className='col-6')

    ], className='row'),

    get_emptyrow(),

    html.Div([

        html.Div([
            html.Div([], className='col-3'),
            html.Div([
                dcc.Dropdown(id='user_choice_world',
                             options=[{'label': cases, "value": cases} for cases in
                                      {'Confirmed', 'Recovered', 'Deaths'}],
                             value='Confirmed', clearable=False,
                             style={"color": "#000000"}),
            ], className='col-6'),
            html.Div([], className='col-3'),
        ], className='row'),

        html.Div([
            html.Div([
                dcc.Graph(id='fig1_4', figure={})
            ], className='col-4'),
            html.Div([
                dcc.Graph(id='fig1_5', figure={})
            ], className='col-4'),
            html.Div([
                dcc.Graph(id='fig1_6', figure={})
            ], className='col-4')
        ], className='row')

    ], className='card_container'),

])

# LAYOUT PAGE WHO
who = html.Div([

    get_header(),

    get_navbar('who'),

    get_emptyrow(),

    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='fig2_1', figure=fig2_1)
            ], className='card_container'),
            get_emptyrow(),
            html.Div([
                html.Div([
                    html.Div([
                        html.H6(['X-axis']),
                        dcc.Dropdown(id='value_x',
                                     options=[{'label': cases, "value": cases}
                                              for cases in
                                              {'TotalCases', 'TotalDeaths', 'TotalRecovered', 'Population'}],
                                     value='Population', clearable=False,
                                     style={"color": "#000000"}),
                        dcc.RadioItems(['Linear ', 'Log'], value='Log', id='xaxis_type')
                    ], className='col-6'),

                    html.Div([
                        html.H6(['Y-axis']),
                        dcc.Dropdown(id='value_y',
                                     options=[{'label': cases, "value": cases}
                                              for cases in
                                              {'TotalCases', 'TotalDeaths', 'TotalRecovered', 'Population'}],
                                     value='TotalCases', clearable=False,
                                     style={"color": "#000000"}),
                        dcc.RadioItems(['Linear ', 'Log'], value='Log', id='yaxis_type')
                    ], className='col-6')
                ], className='row'),
                dcc.Graph(id='fig2_2', figure={})
            ], className='card_container')

        ], className='col-6'),

        html.Div([
            html.Div([
                dcc.Dropdown(id='user_choice_who',
                             options=[{'label': cases, "value": cases}
                                      for cases in who.columns if cases != 'WHO Region'],
                             value='Confirmed', clearable=False,
                             style={"color": "#000000"}),
                dcc.Graph(id='fig2_3', figure={}),

                dcc.Graph(id='fig2_4', figure=fig2_4)
            ], className='card_container')
        ], className='col-6')

    ], className='row'),

])

# LAYOUT PAGE OTHERS
others = html.Div([

    get_header(),

    get_navbar('top'),

    get_emptyrow(),

    html.H4(['Top 10 Affected Countries'], className='card_container_other'),

    get_emptyrow(),

    html.Div([
        dcc.Graph(id='fig3_1', figure={}),

        html.Div([

            html.Div([], className='col-4'),
            html.Div([
                dcc.Dropdown(id='user_choice_top',
                             options=[{'label': cases, "value": cases} for cases in
                                      {'Confirmed', 'Recovered', 'Deaths', 'Active'}],
                             value='Confirmed', clearable=False,
                             style={"color": "#000000"}),
            ], className='col-4'),
            html.Div([], className='col-4'),

        ], className='row'),

    ], className='card_container'),

    get_emptyrow(),

    html.Div([
        html.Div([
            dcc.Graph(id='fig3_2', figure=fig3_2)
        ], className=' col-8'),

        html.Div([
            dcc.Graph(id='fig3_3', figure=fig3_3)
        ], className=' col-4')

    ], className='row card_container'),

    get_emptyrow(),

    html.H4(['Europe'], className='card_container_other'),

    get_emptyrow(),

    html.Div([
        dcc.Graph(id='fig3_4', figure={}),

        html.Div([

            html.Div([], className='col-4'),
            html.Div([
                dcc.Dropdown(id='user_choice_europe',
                             options=[{'label': cases, "value": cases} for cases in
                                      {'Confirmed', 'Recovered', 'Deaths', 'Active'}],
                             value='Confirmed', clearable=False,
                             style={"color": "#000000"}),
            ], className='col-4'),
            html.Div([], className='col-4'),

        ], className='row'),

    ], className='card_container'),

    get_emptyrow(),

    html.H4(['Poland'], className='card_container_other'),

    get_emptyrow(),

    html.Div([

        html.Div([
            html.Div([
                dcc.Graph(id='fig3_5', figure=fig3_5)
            ], className='card_container'),
        ], className='col-6'),
        html.Div([
            html.Div([
                dcc.Graph(id='fig3_6', figure={}),
                dcc.Dropdown(id='user_choice_poland',
                             options=[{'label': cases, "value": cases} for cases in
                                      {'New cases', 'New recovered', 'New deaths'}],
                             value='New cases', clearable=False,
                             style={"color": "#000000"})
            ], className='card_container'),
        ], className='col-6')

    ], className='row')

])
