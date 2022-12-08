#!/usr/bin/env python
# coding: utf-8

# # Plotly Visualization - Covid 19

# ### Author: Agnieszka Szewczyk

# ## Table of Contents
# * [Import packages and data](#Import-packages-and-data)
# * [Basic Statistics](#Basic-Statistics)
# * [World Statistics](#World-Statistics)
# * [WHO Region Statistics](#WHO-Region-Statistics)
# * [Top 10 Affected Countries Statistics](#Top-10-Affected-Countries-Statistics)
# * [WHO Region - Europe Statistics](#WHO-Region---Europe-Statistics)
# * [Poland Statistics](#Poland-Statistics)

# ## Import packages and data

# In[1]:


import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

import warnings
warnings.filterwarnings("ignore")


# In[2]:


fg=pd.read_csv('C:/Users/ADMIN/Desktop/project visu/full_grouped.csv')


# In[3]:


cwl=pd.read_csv('C:/Users/ADMIN/Desktop/project visu/country_wise_latest.csv')


# In[4]:


dw=pd.read_csv('C:/Users/ADMIN/Desktop/project visu/day_wise.csv')


# In[5]:


wm=pd.read_csv('C:/Users/ADMIN/Desktop/project visu/worldometer_data.csv')


# In[10]:


fg['Date'] = pd.to_datetime(fg['Date'])
fg['Date']=fg["Date"].dt.strftime('%Y-%m-%d')

dw['Date'] = pd.to_datetime(dw['Date'])
dw['Date']=dw["Date"].dt.strftime('%Y-%m-%d')


# ## Basic Statistics

# In[11]:


temp=dw[['Date','Deaths', 'Recovered', 'Active']].tail(1)
temp=temp.melt( value_vars=['Active', 'Deaths', 'Recovered'])
fig = px.treemap(temp, path=['variable'], values='value', 
                 color_discrete_sequence=px.colors.qualitative.Dark2, 
                 title='Basic Statistics for Covid 19 on 27.07.2020'
                )
fig.update_traces(textposition='middle center', textinfo='label+value', 
                  hovertemplate=None
                 )
fig.update_layout( title_font_size=20,
                  width=985, height=170, 
                  margin=dict(autoexpand=False, l=0, r=0, t=60, b=30)
                 )
fig.show()


# In[12]:


fig = px.area(dw, x='Date', y=['Recovered','Active','Deaths'],
              labels={'variable':'Cases'},
              height=700, width=950,
              title='Basic Statistics for Covid 19 over time', 
              color_discrete_sequence =px.colors.qualitative.Dark2
             )
fig.update_layout(title_font_size=20,
                  plot_bgcolor='white',
                  xaxis=dict(title='',
                             showline=False,
                             showgrid=True, gridcolor='rgb(204, 204, 204)',
                             rangeslider_visible=True
                            ),
                  yaxis=dict(title='',
                             showline=False,
                             showgrid=True, gridcolor='rgb(204, 204, 204)',
                             autorange = True, fixedrange= False
                            )
                 )  
fig.show()


# The data that was used for this project comes from the period 22.01-27.07.20. 
# At that time about 16 million cases were confirmed worldwide. The number of active, recovered, deaths cases is constantly growing.

# In[13]:


def plot_basic_line(col, n):
    fig = px.line(dw, x='Date', y=col, width=950, color_discrete_sequence=[n])
    fig.update_layout(title=col+' cases over time', title_font_size=20,
                     plot_bgcolor='white',
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
    if col in ['Deaths / 100 Cases','Recovered / 100 Cases','Deaths / 100 Recovered']:
        fig.update_layout(title=col+' over time',  title_font_size=20)
        
    fig.show()


# In[14]:


plot_basic_line('Confirmed','rgb(231,41,138)')


# Until mid-March there was a small number of confirmed cases. Then the rate of virus spreading increased. 

# In[15]:


plot_basic_line('Recovered','rgb(27,158,119)')


# The plot of recovered cases is similar to plot of confirmed cases. In July the rate of spread of the virus increased again.

# In[16]:


plot_basic_line('New recovered','rgb(27,158,119)')


# The number of new recovered cases is rising day by day.

# In[17]:


plot_basic_line('Active','rgb(217,95,2)')


# Because Covid was spreading around the world, the number of active cases was rising day by day.
# Each day there were more new active cases than new recovered cases.

# In[18]:


plot_basic_line('New cases','rgb(217,95,2)')


# Every day more and more people were considered sick. The changes in growth rate are identical to the plot of confirmed cases.

# In[19]:


plot_basic_line('Deaths','rgb(117,112,179)')


# In[20]:


plot_basic_line('New deaths','rgb(117,112,179)')


# From mid-March to mid-April the number of new deaths cases increased from 300 to 6k. Since April this number has remained largely at this level.

# In[21]:


plot_basic_line('Deaths / 100 Cases','rgb(102,166,30)')


# From Fabruary to May the number of deaths/100 cases was increasing. Then it began to decrease.

# In[22]:


plot_basic_line('Recovered / 100 Cases','rgb(102,166,30)')


# Looking at the plot above, it can be seen that April was a difficult moment. Then the number of recovered cases decreased in comparison to the confirmed ones.

# In[23]:


plot_basic_line('Deaths / 100 Recovered','rgb(230,171,2)')


# At the beginning for every 100 recovered cases were many deaths cases. The world did not yet apply adequate methods of protection. This number dropped rapidly and rose briefly in April.

# ## World Statistics

# In[24]:


fig = px.scatter_geo(fg, locations='Country/Region', color="WHO Region",locationmode='country names',
                      size='Confirmed', 
                      title='Spread of Covid-19',
                      animation_frame='Date',
                      projection='natural earth',
                      color_discrete_sequence=px.colors.qualitative.Dark2,
                      hover_name="Country/Region", hover_data={'Country/Region':False}
                      )
fig.update_traces(marker_sizemin=2
                  )
fig.update_layout(title_font_size=20)
fig


# In[25]:


def plot_world_map(col):
    fig = px.choropleth(fg, locations='Country/Region', color=col, locationmode='country names', 
                        animation_frame='Date',
                        title=col +' cases over time', 
                        projection='natural earth',
                        color_continuous_scale=px.colors.sequential.tempo,
                        hover_name='Country/Region', hover_data={'Country/Region':False}
                        )
    fig.update_layout(title_font_size=20)
    fig.show()


# In[26]:


plot_world_map('Confirmed')


# In[27]:


plot_world_map('Deaths')


# In[28]:


temp = pd.merge(fg[['Date', 'Country/Region', 'Confirmed', 'Deaths']], 
                dw[['Date', 'Confirmed', 'Deaths']], on='Date')
temp['% Confirmed'] = round(temp['Confirmed_x']/temp['Confirmed_y'], 3)*100
temp['% Deaths'] = round(temp['Deaths_x']/temp['Deaths_y'], 3)*100


# In[29]:


def world_pbar(col):
    fig = px.bar(temp, x='Date', y=col, color='Country/Region', 
                 range_y=(0, 100), 
                 title=col+ ' cases from each country'
                )
    fig.update_layout(title_font_size=20,
                  plot_bgcolor='white',
                  xaxis=dict(title='',
                             showline=False,
                            ),
                  yaxis=dict(title='',
                             showline=False,
                             showgrid=True, gridcolor='rgb(204, 204, 204)'
                            )
                 ) 
    fig.show()


# In[30]:


world_pbar('% Confirmed')


# Covid has spread around the world at different times.
# 
# In the first two months almost all confirmed cases came from China, the country where the virus appeared.
# 
# In April and May most of the cases came from France, Germany, Iran, Italy, Spain, US, United Kingdom.
# 
# In June and July most of the cases came from US, Russia, India, Brazil.

# In[31]:


world_pbar('% Deaths')


# In the first two months almost all deaths cases came from China, the country where the virus appeared.
# 
# In April most of the cases came from France, Iran, China, Italy, Spain.
# 
# In May, June and July most of the cases came from Brazil, France, Italy, Maxico, Spain, US, United Kingdom.

# ## WHO Region Statistics

# In[32]:


who=fg.groupby('WHO Region')['Confirmed','Deaths','Recovered', 'Active'].sum()
who['Fatality Rate in %'] = round((who['Deaths'] / who['Confirmed']) * 100, 2)
who['Recovery Rate in %'] = round((who['Recovered'] / who['Confirmed']) * 100,2)
who.reset_index(inplace=True)
who


# In[33]:


fig=px.bar(who, x='WHO Region', y=['Recovered','Active','Deaths'], 
           labels={'value':'', 'Date':'', 'variable':'Cases'},
           height=700, 
           color_discrete_sequence=px.colors.qualitative.Dark2
          )
fig.update_layout(title='Basic Statistics of Covid 19 - WHO Region', title_font_size=20,
                  plot_bgcolor='white',
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
fig.show()


# In[34]:


fig = make_subplots(rows=2, cols=2,
                    specs=[[{'type': 'pie'}, {'type': 'pie'}],[{'type': 'pie'}, {'type': 'pie'}]],
                    subplot_titles=('Confirmed cases','Recovered cases', 'Deaths cases', 'Active cases'))
fig.add_trace(go.Pie(labels=who['WHO Region'], values=who['Confirmed'],
                     name='Confirmed',
                     marker_colors=['rgb(57, 105, 172)','rgb(17, 165, 121)','rgb(128, 186, 90)','rgb(127, 60, 141)' , 'rgb(231, 63, 116)','rgb(242, 183, 1)']),
              1, 1)
fig.add_trace(go.Pie(labels=who['WHO Region'], values=who['Recovered'],
                     name='Recovered'),
              1, 2)
fig.add_trace(go.Pie(labels=who['WHO Region'], values=who['Deaths'],
                     name='Deaths'), 
              2, 1)
fig.add_trace(go.Pie(labels=who['WHO Region'], values=who['Active'],
                     name='Active'),
              2, 2)

fig.update_layout(title_text='Basic Statistics of Covid 19 - WHO Region',
                 width=900, height=600
                 )
fig.show()


# In[35]:


def plot_who_bar(col):
    fig = px.bar(who.sort_values(col), y=col, x='WHO Region', text=col, color='WHO Region', 
                 color_discrete_map={'Europe':'rgb(127, 60, 141)' ,
                                     'Western Pacific': 'rgb(242, 183, 1)',
                                     'Americas': 'rgb(17, 165, 121)',
                                     'South-East Asia':'rgb(231, 63, 116)' ,
                                     'Africa': 'rgb(57, 105, 172)',
                                     'Eastern Mediterranean':'rgb(128, 186, 90)'
                                    }
                )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(title=col+' cases', title_font_size=20,
                     plot_bgcolor='white',
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
    if col in ['Recovery Rate in %','Fatality Rate in %']:
        fig.update_layout(title=col,  title_font_size=20, 
                         yaxis_range=[0,100])
        
    fig.show()


# In[36]:


plot_who_bar('Confirmed')


# In[37]:


plot_who_bar('Recovered')


# In[38]:


plot_who_bar('Active')


# In[39]:


plot_who_bar('Deaths')


# In[40]:


plot_who_bar('Fatality Rate in %')


# In[41]:


plot_who_bar('Recovery Rate in %')


# In[42]:


who_s=fg.groupby(['WHO Region','Country/Region'])['WHO Region','Deaths','Recovered', 'Active'].sum()
who_s.reset_index(inplace=True)
who_s = who_s.melt(id_vars=['WHO Region',"Country/Region"], value_vars=['Recovered','Active','Deaths'],
                 var_name='Case', value_name='Count')


# In[43]:


fig=px.sunburst(who_s, path=['WHO Region', 'Country/Region','Case','Count'],
                maxdepth=3,
                width=900, height=600,
                title='Basic Statistics for WHO Region and country'
                )
fig.update_traces(hovertemplate=None
                 )
fig.show()


# In[44]:


def plot_dep(col_x, col_y):
    fig = px.scatter(wm, y=col_y, color='WHO Region', x=col_x,
                     height=700, 
                     hover_name='Country/Region', 
                     log_x=True, log_y=True,
                     marginal_x='rug',marginal_y='rug',
                     title=col_x+ ' vs '+ col_y,
                     color_discrete_map={'Europe':'rgb(127, 60, 141)' ,
                                         'WesternPacific': 'rgb(242, 183, 1)',
                                         'Americas': 'rgb(17, 165, 121)',
                                         'South-EastAsia':'rgb(231, 63, 116)' ,
                                         'Africa': 'rgb(57, 105, 172)',
                                         'EasternMediterranean':'rgb(128, 186, 90)'
                                         }
                     )
    fig.update_layout(plot_bgcolor='white',
                      xaxis=dict(showline=False,
                                 showgrid=True, gridcolor='rgb(204, 204, 204)'
                                 ),
                      yaxis=dict(showline=False,
                                 showgrid=True, gridcolor='rgb(204, 204, 204)'
                                )
                     )
    fig.show()


# In[45]:


plot_dep('Population','TotalCases')


# Laos, Myanmar, Tanzania, Vietnam have few confirmed cases compared to other countries taking into account their populations.
# 
# San Marino, Bahrain, Qatar have a lot of confirmed cases compared to other countries taking into account their populations.

# In[46]:


plot_dep('TotalCases', 'TotalDeaths')


# Singapore, Qatar have few death cases compared to other countries taking into account the number of confirmed cases.
# 
# Yemen, Hungary have a lot of death cases compared to other countries taking into account the number of confirmed cases.

# In[47]:


plot_dep('TotalCases', 'TotalRecovered')


# Botswana, Bahamas, Gambia, Libya, Honduras have few recovered cases compared to other countries taking into account the number of confirmed cases.

# ## Top 10 Affected Countries Statistics

# In[48]:


top=cwl.sort_values(by='Confirmed', ascending=False)[:10]
top_country=top['Country/Region'].values
fg_top=fg[fg['Country/Region'].isin(top_country)]


# In[49]:


def top_line(col):
    fig=px.line(fg_top, x='Date', y=col, color='Country/Region',
                color_discrete_map={'US':'rgb(127, 60, 141)',
                                    'Brazil' : 'rgb(17, 165, 121)',
                                    'India':'rgb(57, 105, 172)',
                                    'Russia': 'rgb(242, 183, 1)',
                                    'South Africa':'rgb(231, 63, 116)',
                                    'Mexico':'rgb(128, 186, 90)',
                                    'Peru':'rgb(230, 131, 16)',
                                    'Chile':'rgb(0, 134, 149)',
                                    'United Kingdom':'rgb(207, 28, 144)',
                                    'Iran':'rgb(249, 123, 114)' 
                                   }
               )
    fig.update_layout(title=col +' Cases of Top 10 Affected Countries', title_font_size=20,
                      plot_bgcolor='white',
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
                      updatemenus=[dict(type = "buttons",
                                        direction = "left",
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
    fig.show()


# In[50]:


top_line('Confirmed')


# In[51]:


top_line('Deaths')


# In[52]:


top_line('Recovered')


# In[53]:


fig = px.scatter(top, x="Confirmed", y="Deaths",size='Recovered',
                 color='Country/Region',
                 color_discrete_map={'US':'rgb(127, 60, 141)',
                    'Brazil' : 'rgb(17, 165, 121)',
                    'India':'rgb(57, 105, 172)',
                    'Russia': 'rgb(242, 183, 1)',
                    'South Africa':'rgb(231, 63, 116)',
                    'Mexico':'rgb(128, 186, 90)',
                    'Peru':'rgb(230, 131, 16)',
                    'Chile':'rgb(0, 134, 149)',
                    'United Kingdom':'rgb(207, 28, 144)',
                    'Iran':'rgb(249, 123, 114)'
                     },
                 hover_name="Country/Region",)
fig.update_layout(title='Plot of Confirmed, Deaths and Recovered Cases of Top 10 Affected Countries',
                  title_font_size=20,
                  plot_bgcolor='white',
                  xaxis=dict(showline=False,
                             showgrid=True, gridcolor='rgb(204, 204, 204)'
                            ),
                  yaxis=dict(showline=False,
                             showgrid=True, gridcolor='rgb(204, 204, 204)'
                            )
                 )  
fig.show()


# In[54]:


fig = px.scatter_3d(top, x='Confirmed', z='Deaths', y='Recovered',
              color='Country/Region',log_x=True,
                   color_discrete_map={'US':'rgb(127, 60, 141)',
                    'Brazil' : 'rgb(17, 165, 121)',
                    'India':'rgb(57, 105, 172)',
                    'Russia': 'rgb(242, 183, 1)',
                    'South Africa':'rgb(231, 63, 116)',
                    'Mexico':'rgb(128, 186, 90)',
                    'Peru':'rgb(230, 131, 16)',
                    'Chile':'rgb(0, 134, 149)',
                    'United Kingdom':'rgb(207, 28, 144)',
                    'Iran':'rgb(249, 123, 114)'
                     })
fig.update_layout(title='3D Plot of Confirmed, Deaths and Recovered Cases of Top 10 Affected Countries',
                  title_font_size=20
                 )
fig.show()


# Maksyk, Peru, Iran have an exceptional number of deaths compared to confirmed cases.
# 
# Brazil has a lot of recovered cases compared to confirmed cases.
# 
# United Kingdom has extremely few recovered cases.

# ## WHO Region - Europe Statistics

# In[55]:


europe=fg.groupby(['WHO Region','Country/Region'])['WHO Region','Confirmed','Deaths','Recovered', 'Active'].sum()
europe.reset_index(inplace=True)
europe=europe[europe['WHO Region']=='Europe']


# In[56]:


def plot_europe_hist(col, n):
    fig=px.histogram(europe, x=col,
                     nbins=50, 
                     marginal='box',
                     hover_data={'Country/Region': True},
                     color_discrete_sequence=[n]
                    )
    fig.update_layout(title=col+ ' cases distribution in Europe', title_font_size=20,
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
    fig.show()


# In[57]:


plot_europe_hist('Confirmed','rgb(231,41,138)')


# The median of confirmed cases in Europe is approximately 696k.
# 
# The outliers due to confirmed cases: Turkey, Germany, France, Italy, United Kingdom, Spain, Russia.

# In[58]:


plot_europe_hist('Recovered','rgb(27,158,119)')


# The median of recovered cases in Europe is approximately 283k.
# 
# The outliers due to recovered cases:  France, Turkey, Spain, Italy, Germany, Russia.

# In[59]:


plot_europe_hist('Deaths','rgb(117,112,179)')


# The median of deaths cases in Europe is approximately 20k.`
# 
# The outliers due to deaths cases: Sweden, Turkey, Russia, Netherlands, Germany, Belgium, Spain, France, Italy, United Kingdom.

# In[60]:


plot_europe_hist('Active','rgb(217,95,2)')


# The median of active cases in Europe is approximately 231k.
# 
# The outliers due to active cases: Germany, Belgium, Turkey, Sweden, Italy, Spain, France, Russia, United Kingdom.

# ## Poland Statistics

# In[61]:


fg_poland=fg[fg['Country/Region']=='Poland']
fg_poland=fg_poland[fg_poland['Confirmed']>0]


# In[62]:


d_1=datetime.datetime.strptime('2020-03-16', "%Y-%m-%d").timestamp() * 1000 #School closures
d_2=datetime.datetime.strptime('2020-03-20', "%Y-%m-%d").timestamp() * 1000 #Epidemic State of Emergency
d_3=datetime.datetime.strptime('2020-03-25', "%Y-%m-%d").timestamp() * 1000 #Movement restrictions
d_4=datetime.datetime.strptime('2020-04-20', "%Y-%m-%d").timestamp() * 1000 #Defrosting of the Polish economy - Stage I
d_5=datetime.datetime.strptime('2020-05-04', "%Y-%m-%d").timestamp() * 1000 #Defrosting of the Polish economy - Stage II
d_6=datetime.datetime.strptime('2020-05-18', "%Y-%m-%d").timestamp() * 1000 #Defrosting of the Polish economy - Stage III
d_7=datetime.datetime.strptime('2020-05-30', "%Y-%m-%d").timestamp() * 1000 #Defrosting of the Polish economy - Stage IV


# In[63]:


fig=px.line(fg_poland, x='Date', y=['Confirmed','Deaths','Recovered','Active'],
            labels={'variable':'Cases'},
            title='Basic Statistics of Covid 19 in Poland',
            color_discrete_map={'Confirmed':'rgb(231,41,138)' ,
                                     'Deaths':'rgb(117,112,179)',
                                     'Recovered': 'rgb(27,158,119)',
                                     'Active': 'rgb(217,95,2)'
                                    }
           )
fig.add_vline(x=d_1, line_width=0.5, line_dash="dot",
              annotation_text='School closures',
              annotation_textangle=-90,
              annotation_position='left top'
             )
fig.add_vline(x=d_2, line_width=0.5, line_dash="dot",
              annotation_text='Epidemic State of Emergency',
              annotation_textangle=-90,
              annotation_position='left top'
             )
fig.add_vline(x=d_3, line_width=0.5, line_dash="dot",
              annotation_text='Movement restrictions',
              annotation_textangle=-90,
              annotation_position='left top'
             )
fig.add_vline(x=d_4, line_width=0.5, line_dash="dot",
              annotation_text='Defrosting of the Polish economy - Stage I',
              annotation_textangle=-90,
              annotation_position='left top'
             )
fig.add_vline(x=d_5, line_width=0.5, line_dash="dot",
              annotation_text='Defrosting of the Polish economy - Stage II',
              annotation_textangle=-90,
              annotation_position='left top'
             )
fig.add_vline(x=d_6, line_width=0.5, line_dash="dot",
              annotation_text='Defrosting of the Polish economy - Stage III',
              annotation_textangle=-90,
              annotation_position='left top'
             )
fig.add_vline(x=d_7, line_width=0.5, line_dash="dot",
              annotation_text='Defrosting of the Polish economy - Stage IV',
              annotation_textangle=-90,
              annotation_position='left top'
             )
fig.update_layout(title_font_size=20,
                     plot_bgcolor='white',
                      xaxis_title='',
                      yaxis=dict(title='',
                                showline=False,
                                showgrid=True, gridcolor='rgb(204, 204, 204)',
                                zeroline=True, zerolinewidth=4, zerolinecolor='rgb(204, 204, 204)'
                                ),
                  height=800
                     )
fig.show()


# In[64]:


def plot_poland_bar(col,n):
    fig = px.bar(fg_poland,x='Date',y =col ,
                 title=col + ' in Poland over time',
                 color_discrete_sequence=[n]
                )
    fig.add_vline(x=d_1, line_width=0.5, line_dash="dot",
              annotation_text='School closures',
              annotation_textangle=-90,
              annotation_position='left top'
             )
    fig.add_vline(x=d_2, line_width=0.5, line_dash="dot",
              annotation_text='Epidemic State of Emergency',
              annotation_textangle=-90,
              annotation_position='left top'
             )
    fig.add_vline(x=d_3, line_width=0.5, line_dash="dot",
              annotation_text='Movement restrictions',
              annotation_textangle=-90,
              annotation_position='left top'
             )
    fig.add_vline(x=d_4, line_width=0.5, line_dash="dot",
              annotation_text='Defrosting of the Polish economy - Stage I',
              annotation_textangle=-90,
              annotation_position='left top'
             )
    fig.add_vline(x=d_5, line_width=0.5, line_dash="dot",
              annotation_text='Defrosting of the Polish economy - Stage II',
              annotation_textangle=-90,
              annotation_position='left top'
             )
    fig.add_vline(x=d_6, line_width=0.5, line_dash="dot",
              annotation_text='Defrosting of the Polish economy - Stage III',
              annotation_textangle=-90,
              annotation_position='left top'
             )
    fig.add_vline(x=d_7, line_width=0.5, line_dash="dot",
              annotation_text='Defrosting of the Polish economy - Stage IV',
              annotation_textangle=-90,
              annotation_position='left top'
             )
    fig.update_layout(title_font_size=20,
                      plot_bgcolor='white',
                      xaxis_title='',
                      yaxis=dict(title='',
                                 showline=False,
                                 showgrid=True, gridcolor='rgb(204, 204, 204)'
                                ),
                      height=800
                     )
    fig.show()


# In[65]:


plot_poland_bar('New cases','rgb(217,95,2)')


# In[66]:


plot_poland_bar('New recovered','rgb(27,158,119)')


# In[67]:


plot_poland_bar('New deaths','rgb(117,112,179)')


# In Poland the restrictions appeared very quickly, when the number of confirmed cases was around 100.
# 
# The most severe lockdown lasted approximately one month. This was the time when the number of new cases grew steadily. 
# Every day more and more people recived positive test result. There were very few recovered cases.
# 
# Frirst stage of Defrosting of the Polish economy brought an increase of recovered cases and a fairly stable number of new confirmed cases.

# In[ ]:




