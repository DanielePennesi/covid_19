import dash
import dash_core_components as dcc
import dash_html_components as html
import main_routines as mr
import datetime
#test

########### Defining variables
tabtitle='Covid-19-Ita'
myheading='Infected Contributions Over Time'
githublink='https://github.com/DanielePennesi/covid_19'
code_surce = html.A('Code on Github by Daniele Pennesi', href=githublink)
########### Create plots
ll_html_output = [html.H1(myheading), html.H2('Italy section'), html.H3('Single click on the legend to hide, double click on the lengend to hide the rest')]
df_all_ita = mr.get_ita_covid_data()  # retrieving italian data from Dipartimento Protezione Civile
max_data = df_all_ita.index.get_level_values('data').max()
date_list = [max_data - datetime.timedelta(days=x*7) for x in range(200)]  # weekly resampling
df_all_ita = df_all_ita.loc[date_list]
fig_ita_ctr, df_ita_ctr = mr.plot_cum_infected_ctr_italy(df_all=df_all_ita)  # creating fig of contributions over time
ll_html_output += [dcc.Graph(id='fig_ita_ctr', figure=fig_ita_ctr), code_surce]
fig_ita_map, df_ita_map = mr.plot_ita_covid_map(df_all=df_all_ita)  # creating fig of Italy map over time
ll_html_output += [dcc.Graph(id='fig_ita_map', figure=fig_ita_map), code_surce, html.H2('Italy Regions section (sorted by number of infections)')]


regions_list = list(df_all_ita.loc[max_data][['totale_casi']].sort_values('totale_casi', ascending=False).index)
dict_regions = {}
for region in regions_list:
    # dict_regions[region] = {}
    fig_region, df_region = mr.plot_cum_infected_ctr_region(df_all=df_all_ita, region=region)
    # dict_regions[region]['region'] = region
    # dict_regions[region]['fig'] = fig
    ll_html_output += [dcc.Graph(id=region + '_ctr', figure=fig_region), code_surce]

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

########### Set up the layout
# app.layout = html.Div(children=[
#     html.H1(myheading),
#     dcc.Graph(
#         id='fig_ita_ctr',
#         figure=fig_ita_ctr
#     ),
#     html.A('Code on Github by Daniele Pennesi', href=githublink),
#     html.Br(),
#     dcc.Graph(
#         id='fig_ita_map',
#         figure=fig_ita_map
#     ),
#     html.A('Code on Github by Daniele Pennesi', href=githublink),
#     html.H1('Italian Regions'),
#
#     ]
# )

app.layout = html.Div(children=ll_html_output)

if __name__ == '__main__':
    app.run_server()
