
### COVID 19 MONITORING ### - START

def get_ita_covid_data():
    # Importing libraries and input data
    import pandas as pd

    df_all = pd.read_csv(
        'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv')
    # description of the fields
    '''
    'data'--> data 
    'stato'--> ITA
    'codice_regione'--> codice regione
    'denominazione_regione'--> nome regione (N.B. Trentino Alto Adige è diviso nelle sue due provincie autonome Bolzano e Trento)
    'lat'--> latitudine
    'long'--> longitudine
    'ricoverati_con_sintomi'--> numero cumulato di ATTUALMENTE ricoverati NON in terapia intensiva
    'terapia_intensiva'--> numero cumulato di ATTUALMENTE ricoverati in terapia intensiva
    'totale_ospedalizzati'--> somma tra ATTUALMENTE ricoerati_con_sintomi e ATTUALMENTE in terapia_intensiva
    'isolamento_domiciliare'--> numero cumulato di ATTUALMENTE positivi e ATTUALMENTE non ospedalizzati 
    'totale_attualmente_positivi'--> somma tra ATTUALMENTE totale_ospedalizzati e isolamento_domiciliare
    'nuovi_attualmente_positivi'--> differenza tra totale_attualmente_positivi a T e T-1
    'dimessi_guariti'--> numero cumulato di guariti
    'deceduti'--> numero cumulato di deceduti
    'totale_casi'--> somma tra deceduti, dimessi_guariti, totale_attualmente_positivi
    'tamponi'--> numero cumulato di tamponi effettuati
    '''

    df_all['data'] = pd.to_datetime(df_all['data']).dt.date

    # creating a dataframe without regions contribution (Italy level)
    df_italy = df_all.drop(columns=['stato', 'codice_regione', 'lat', 'long'])
    df_italy = df_italy.groupby('data').sum()

    # numero abitanti per regione
    # ToDo: find a way to download instead of hardcoding them
    dict_num_ab = {'Lombardia': 10060574,
                   'Lazio': 5879082,
                   'Campania': 5801692,
                   'Sicilia': 4999891,
                   'Veneto': 4905854,
                   'Emilia Romagna': 4459477,
                   'Piemonte': 4356406,
                   'Puglia': 4029053,
                   'Toscana': 3729641,
                   'Calabria': 1947131,
                   'Sardegna': 1639591,
                   'Liguria': 1550640,
                   'Marche': 1525271,
                   'Abruzzo': 1311580,
                   'Friuli Venezia Giulia': 1215220,
                   'P.A. Trento': 541098,
                   'P.A. Bolzano': 531178,
                   'Umbria': 882015,
                   'Basilicata': 562869,
                   'Molise': 305617,
                   "Valle d'Aosta": 125666}

    # densità popolazione per regione: numero abitanti per km2
    # ToDo: find a way to download instead of hardcoding them
    dict_dens = {'Lombardia': 422,
                 'Lazio': 341,
                 'Campania': 424,
                 'Sicilia': 194,
                 'Veneto': 267,
                 'Emilia Romagna': 199,
                 'Piemonte': 172,
                 'Puglia': 206,
                 'Toscana': 162,
                 'Calabria': 128,
                 'Sardegna': 68,
                 'Liguria': 286,
                 'Marche': 162,
                 'Abruzzo': 121,
                 'Friuli Venezia Giulia': 153,
                 'P.A. Trento': 72,
                 'P.A. Bolzano': 72,
                 'Umbria': 104,
                 'Basilicata': 56,
                 'Molise': 69,
                 "Valle d'Aosta": 39}

    df_all['num_abitanti'] = df_all['denominazione_regione'].replace(dict_num_ab)
    df_all['dens_pop'] = df_all['denominazione_regione'].replace(dict_dens)
    df_all = df_all.set_index(['data', 'denominazione_regione'])

    return df_all

def get_esp_covid_data():

    import pandas as pd

    df_all = pd.read_csv(
        'https://raw.githubusercontent.com/Secuoyas-Experience/covid-19-es/master/datos-comunidades-csv/covid-19-ES-CCAA-DatosCasos.csv')

    return

def plot_ita_covid_map(df_all):
    # sources:
    # https://plot.ly/python/dropdowns/
    # https://plot.ly/python/scatter-plots-on-maps/
    # https://plot.ly/python/bubble-maps/
    import plotly.express as px
    import pandas as pd
    df_all_to_plot = df_all.reset_index()
    df_all_to_plot['data'] = df_all_to_plot['data'].astype('str')

    ll_cols = ['totale_casi', 'deceduti', 'dimessi_guariti', 'totale_attualmente_positivi']

    df_map_plot = pd.DataFrame()
    for col in ll_cols:
        temp = df_all_to_plot[['data', 'denominazione_regione', 'long', 'lat', col]].rename(columns={col: 'value'})
        temp['label'] = col
        df_map_plot = pd.concat([df_map_plot, temp])

    fig = px.scatter_geo(df_map_plot,
                         lon=df_map_plot['long'],
                         lat=df_map_plot['lat'],
                         hover_name="denominazione_regione", size="value",
                         animation_frame="data", size_max=50, width=1000, height=800, color="label"
                         )

    fig.update_layout(geo_scope='europe',
                      title='<b>Italy</b> COVID-19 spreading over time (zoom on Italy and press "play" button)<br>Source: <a href="https://github.com/pcm-dpc/COVID-19">Dipartimento della Protezione Civile</a>')

    return fig, df_map_plot

def plot_infected_ctr(df, area, total_or_delta):
    # sources:
    # https://plot.ly/python/bar-charts/
    # https://plot.ly/python/multiple-axes/
    # https://plot.ly/python/legend/#legend-position
    import plotly.graph_objects as go

    df['dimessi_guariti'] = df['dimessi_guariti'] * (-1)
    fig = go.Figure()
    x = list(df.index)
    for col in df.columns:
        if col !='tamponi':
            fig.add_trace(go.Bar(
                name=col + ' (left axis)',
                x=x,
                y=list(df[col]),
                yaxis='y1'))
        else:
            fig.add_trace(go.Scatter(
                name='tamponi'+ ' (right axis)',
                x=x,
                y=list(df['tamponi']),
                yaxis='y2'))
    # Change the bar mode
    # # fig.update_layout(barmode='stack')
    fig.update_layout(barmode = 'relative',
                      title ='<b>' + area + '</b>' + ': COVID-19 ' + total_or_delta + ' infected contributions over time<br>Source: <a href="https://github.com/pcm-dpc/COVID-19">Dipartimento della Protezione Civile</a>',
                      yaxis=dict(
                          # anchor="x",
                          # overlaying="y",
                          # side="left"
                      ),
                      yaxis2=dict(
                          anchor="x",
                          overlaying="y",
                          side="right",
                          ),
                     legend=dict(x=0, y=1), width=1000, height=800)

    return fig

def plot_cum_infected_ctr_italy(df_all):

    df_all_to_plot = df_all.reset_index()
    df_all_to_plot['data'] = df_all_to_plot['data'].astype('str')

    df_ctr_italy_plot = df_all_to_plot.copy()
    df_ctr_italy_plot = df_ctr_italy_plot.drop(columns=['denominazione_regione', 'stato', 'codice_regione', 'lat', 'long'])

    df_ctr_italy_plot = df_ctr_italy_plot.groupby('data').sum()

    ll_cols = ['ricoverati_con_sintomi', 'terapia_intensiva', 'deceduti', 'isolamento_domiciliare', 'dimessi_guariti',
               'tamponi']
    df_ctr_italy_plot = df_ctr_italy_plot[ll_cols]
    fig = plot_infected_ctr(df_ctr_italy_plot, area='Italy', total_or_delta='total')

    return fig, df_ctr_italy_plot

def plot_delta_infected_ctr_italy(df_all, diff_or_pct_change='diff'):

    df_all_to_plot = df_all.reset_index()
    df_all_to_plot['data'] = df_all_to_plot['data'].astype('str')

    df_ctr_italy_plot = df_all_to_plot.copy()
    df_ctr_italy_plot = df_ctr_italy_plot.drop(
        columns=['denominazione_regione', 'stato', 'codice_regione', 'lat', 'long'])

    df_ctr_italy_plot = df_ctr_italy_plot.groupby('data').sum()
    ll_cols = ['ricoverati_con_sintomi', 'terapia_intensiva', 'deceduti', 'isolamento_domiciliare', 'dimessi_guariti',
               'tamponi']
    df_ctr_italy_plot = df_ctr_italy_plot[ll_cols]
    if diff_or_pct_change=='diff':
        df_delta_ctr_italy_plot = df_ctr_italy_plot.diff()
        total_or_delta = 'delta'
    elif diff_or_pct_change=='pct_change':
        df_delta_ctr_italy_plot = df_ctr_italy_plot.pct_change()
        total_or_delta = 'percentage change (w.r.t. the same category)'

    fig = plot_infected_ctr(df_delta_ctr_italy_plot, area='Italy', total_or_delta=total_or_delta)

    return fig, df_delta_ctr_italy_plot

def plot_cum_infected_ctr_region(df_all, region='Lombardia'):

    df_region = df_all.loc[(slice(None), region), :]
    df_region = df_region.reset_index().set_index('data')
    df_region = df_region.drop(columns=['denominazione_regione', 'stato', 'codice_regione', 'lat','long'])

    ll_cols = ['ricoverati_con_sintomi', 'terapia_intensiva', 'deceduti', 'isolamento_domiciliare', 'dimessi_guariti', 'tamponi']
    df_region = df_region[ll_cols]

    fig = plot_infected_ctr(df=df_region, area=region, total_or_delta='total')

    return fig, df_region

def plot_analysis_across_regions(df_all, field, base=None):

    from qlib.reporting import reporting as repo

    df_regions = df_all[[field]]

    if base != None:
        df_regions = df_all[[field]].div(df_all['num_abitanti'], axis=0)
        ytickformat = '0.2%'
    else:
        df_regions = df_all[[field]]
        ytickformat = None

    df_regions = df_regions.unstack()

    df_regions.columns = df_regions.columns.droplevel()

    fig = repo.plotly_plot(df_regions, out='fig', legend_orientation='v', title=field, ytickformat=ytickformat)

    return fig, df_regions


### COVID 19 MONITORING ### - END