
from bokeh.layouts import row, column, layout
from bokeh.models import Select, HoverTool
from bokeh.models.widgets import Div, TextInput
from bokeh.plotting import curdoc, figure

import glob
import numpy as np
import pandas as pd


# Functions -------------------------------------------------------------------
def menu1_change(attr, old, new):
    global data
    log_files = glob.glob(logs_path)
    # update menu options
    menu1.options = log_files
    # get new data
    agenda = pd.read_csv(menu1.value)
    data = DataProcessing(agenda)
    # update plots
    update_plots()


def update_plots():
    # section 1
    line1.data_source.data = dict(x=np.arange(1, 13), y=data.adfm)
    # section 2: histogram
    bins = np.unique(data.dfxi)
    bh = np.append(bins, bins.max() + 1)
    hist, _ = np.histogram(data.dfxi, bh)
    bars.data_source.data = dict(left=bins-0.3, right=bins+0.3,
                                 bottom=np.zeros(len(bins)), top=hist)


class DataProcessing(object):
    def __init__(self, ag):
        self.ni = len(ag)
        # fechas
        f = ag[ag.columns[4:]].values
        fechas = list()
        fechas.append(pd.to_datetime(f[:, 0]))
        for i in range(0, 12):
            fechas.append(pd.to_datetime(f[:, i + 1]))
        # días facturados
        dfxm = np.zeros([self.ni, 12])
        for i in range(0, 12):
            dfxm[:, i] = np.array((fechas[i+1] - fechas[i]).days)
            nanxm = np.isnan(dfxm[:, i])
            dfxm[nanxm, i] = 0
        # results
        self.dfxm = dfxm
        self.dfxi = np.sum(dfxm, 1)
        self.adfm = np.mean(dfxm, 0)


# -----------------------------------------------------------------------------
# leer agendas y seleccionar la última
logs_path = 'report/files/*.csv'
log_files = glob.glob(logs_path)
nlf = len(log_files)
agenda = pd.read_csv(log_files[nlf - 1])
data = DataProcessing(agenda)
# parametros
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
         'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
wf = 600
hf = 400
hover = HoverTool(tooltips="""
    <div>
        <div>
            <span style="font-size: 10px; color: #2F2F2F;"> y: </span>
            <span style="font-size: 10px; color: #2F2F2F;"> @y </span>
        </div>
    </div>
    """)
# Bokeh Layout Design <<<<<<<<<<<<<<<<<
# Titles
title1 = Div(text=""" <h1>Agenda 2018: Dashboard</h1> """, width=1000,
             height=40)
menu1 = Select(title='Seleccionar Agenda', value=log_files[nlf - 1],
               options=log_files, width=250, height=40)
menu1.on_change('value', menu1_change)
# section 1: Promedio de dias de lectura x mes
f1 = figure(title='Promedio de Días de Lectura x Mes', plot_height=hf,
            plot_width=wf, tools='pan,box_zoom,reset',
            toolbar_location="above")
f1.xaxis.axis_label = 'mes del año'
f1.yaxis.axis_label = 'días facturados'
f1.add_tools(hover)
line1 = f1.line(x=[0, 1], y=[0, 1], line_color="blue", line_width=2, alpha=1)
# section 2: histograma de cantidad de itinerarios por dia de lectura
f2 = figure(title='Distribución de Itinerarios x Diás de Lectura',
            plot_width=wf, plot_height=hf, tools='pan,box_zoom,reset',
            toolbar_location="above")
el = np.arange(0.7, 15.7, 1)
er = np.arange(1.3, 16.3, 1)
bars = f2.quad(left=el, right=er, bottom=np.zeros(15), top=np.zeros(15),
               color="orange", line_color='white')
f2.xaxis.axis_label = "días facturados al año"
f2.yaxis.axis_label = "itinerarios"
hover2 = HoverTool(tooltips="""
    <div>
        <div>
            <span style="font-size: 10px; color: #2F2F2F;"> y: </span>
            <span style="font-size: 10px; color: #2F2F2F;"> @top </span>
        </div>
    </div>
    """)
f2.add_tools(hover2)
# update plots
update_plots()

# Dashboard <<<<<<<<<<<<<<<<<<<<<<<<<<<
dashboard = layout([
    [title1],
    [menu1],
    [f1, f2]], sizing_mode='fixed')

curdoc().add_root(dashboard)
curdoc().title = "Agenda 2018"
