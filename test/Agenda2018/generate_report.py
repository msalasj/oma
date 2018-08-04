
from bokeh.io import output_file, save, curdoc
from bokeh.layouts import column, layout
from bokeh.models import HoverTool
from bokeh.models.widgets import Div
from bokeh.plotting import figure

import datetime
# import glob
import numpy as np
import pandas as pd


# Functions -------------------------------------------------------------------
def update_plots():
    # section 1
    text12.text = 'Promedio: {0:.2f}'.format(np.mean(data.adfm))
    line1.data_source.data = dict(x=np.arange(1, 13), y=data.adfm)
    # section 2: histogram
    text22.text = 'Promedio: {0:.2f}'.format(np.mean(data.dfxi))
    bins = np.unique(data.dfxi)
    bh = np.append(bins, bins.max() + 1)
    hist, _ = np.histogram(data.dfxi, bh)
    bars.data_source.data = dict(left=bins-0.3, right=bins+0.3,
                                 bottom=np.zeros(len(bins)), top=hist)
    # section 3
    text32.text = 'Promedio: {0:.2f}'.format(np.mean(data.traslados))
    line3.data_source.data = dict(x=np.arange(1, 13), y=data.traslados)


class DataProcessing(object):
    def __init__(self, ag):
        self.ni = len(ag)
        # fechas
        f = ag[ag.columns[19:]].values
        fechas = list()
        fechas.append(pd.to_datetime(f[:, 0], format='%d/%m/%Y'))
        for i in range(0, 12):
            fechas.append(pd.to_datetime(f[:, i + 1], format='%d/%m/%Y'))
        vencimientos = [24, 21, 21, 23, 24, 22, 24, 24, 21, 24, 23, 21]
        # días facturados
        dfxm = np.zeros([self.ni, 12])
        self.traslados = np.zeros(12)
        for i in range(0, 12):
            dfxm[:, i] = np.array((fechas[i+1] - fechas[i]).days)
            nanxm = np.isnan(dfxm[:, i])
            dfxm[nanxm, i] = 0
            # vencimientos
            diasi = np.array(fechas[i+1].day)
            self.traslados[i] = sum(diasi > vencimientos[i])
        # results
        self.dfxm = dfxm
        self.dfxi = np.sum(dfxm, 1)
        self.adfm = np.mean(dfxm, 0)


# -----------------------------------------------------------------------------
# Ini Report
curdoc()
unicom = '1120'
report_name = './data/unicoms/report_' + unicom + '.html'
output_file(report_name)
# leer agendas
logs_path = 'data/unicoms/Agenda.' + unicom + '.csv'
# log_files = glob.glob(logs_path)
# nlf = len(log_files)
agenda = pd.read_csv(logs_path)
data = DataProcessing(agenda)
# parametros
meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
         'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
wf = 400
hf = 300
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
# section 1: Promedio de dias de lectura x mes
text11 = Div(text='<h3>Promedio de Días de Lectura x Mes</h3>',
             width=wf, height=20)
text12 = Div(text=' ', width=wf, height=20)
f1 = figure(title=' ', plot_height=hf,
            plot_width=wf, tools='pan,box_zoom,reset',
            toolbar_location="above")
f1.xaxis.axis_label = 'mes del año'
f1.yaxis.axis_label = 'días facturados'
f1.add_tools(hover)
line1 = f1.line(x=[0, 1], y=[0, 1], line_color="blue", line_width=2, alpha=1)
w1 = column([text11, text12, f1])
# section 2: histograma de cantidad de itinerarios por dia de lectura
text21 = Div(text='<h3>Distribución de Itinerarios x Diás de Lectura</h3>',
             width=wf, height=20)
text22 = Div(text=' ', width=wf, height=20)
f2 = figure(title='', plot_width=wf, plot_height=hf,
            tools='pan,box_zoom,reset', toolbar_location="above")
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
w2 = column([text21, text22, f2])
# section 3: Cantidad de Itinerarios Trasladados
text31 = Div(text='<h3>Itinerarios Trasladados x Mes</h3>',
             width=wf, height=20)
text32 = Div(text=' ', width=wf, height=20)
f3 = figure(title=' ', plot_height=hf,
            plot_width=wf, tools='pan,box_zoom,reset',
            toolbar_location="above")
f3.xaxis.axis_label = 'mes del año'
f3.yaxis.axis_label = 'cantidad de itinerarios'
f3.add_tools(hover)
line3 = f3.line(x=[0, 1], y=[0, 1], line_color="blue", line_width=2, alpha=1)
w3 = column([text31, text32, f3])
# section 4
title2 = Div(text=""" <h3>Distribución de Dias Facturaddos x Mes</h3> """,
             width=1000, height=40)
# update plots
update_plots()

# Dashboard <<<<<<<<<<<<<<<<<<<<<<<<<<<
dashboard = layout([
    [title1],
    [w1, w2, w3]], sizing_mode='fixed')
save(dashboard, title='Agenda 2018')
