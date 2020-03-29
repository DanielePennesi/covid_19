import dash
import dash_core_components as dcc
import dash_html_components as html
import main_routines as mr
#test
########### Create plot
df_all_ita = mr.get_ita_covid_data()
fig_ita_ctr, df_ita_ctr = mr.plot_cum_infected_ctr_italy(df_all=df_all_ita)
fig_ita_map, df_ita_map = mr.plot_ita_covid_map(df_all=df_all_ita)

########### Define your variables
tabtitle='Covid-19-Ita'
myheading='Infected Contributions Over Time'
githublink='https://github.com/DanielePennesi/Covid19Monitor'

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading),
    dcc.Graph(
        id='fig_ita_ctr',
        figure=fig_ita_ctr
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    dcc.Graph(
        id='fig_ita_map',
        figure=fig_ita_map
    ),
    html.A('Code on Github', href=githublink)

    ]
)

if __name__ == '__main__':
    app.run_server()