import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import HTML
import bokeh.sampledata

from bokeh.plotting import figure, show, output_file, output_notebook
from bokeh.models import ColumnDataSource, HoverTool, Legend, Range1d, LinearAxis, CustomJS, Div
from bokeh.layouts import widgetbox, column, row, gridplot
from bokeh.models.widgets import CheckboxButtonGroup
from bokeh.models.widgets import Tabs, Panel, Button
from bokeh.io import curdoc
from bokeh.palettes import Viridis, Category20, Inferno, Viridis3

from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.layouts import widgetbox

server = '200.233.212.247'
#server = '10.0.0.110\cco_db'
database = 'GrandeRio'
user = 'sa'
password = 'CCO@123456'
driver = '{ODBC Driver 13 for SQL Server}'

connection = pyodbc.connect('DRIVER='+driver+'; Server='+server+'; PORT:1433; DATABASE='+database+'; UID='+user+'; PWD='+password + '; Trusted_Connection = yes;')

cursor = connection.cursor() 
if connection:
    print("\n\nComunicando\n")
    
sql2 = '''\
    SELECT  
        CONCAT(CAST(tA.E3TimeStamp AS date),' ', DATEPART(HOUR,tA.E3TimeStamp), ':00:00') AS Data,
        FORMAT(max(tA.Consumo) - LAG(max(tA.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC), 'N', 'de-de') AS [Trafo A],
        FORMAT(max(tB.Consumo) - LAG(max(tB.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC), 'N', 'de-de') AS [Trafo B],
        FORMAT(max(tC.Consumo) - LAG(max(tC.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC), 'N', 'de-de') AS [Trafo C],
        FORMAT(max(tA.Consumo) - LAG(max(tA.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC)+ 
        max(tB.Consumo) - LAG(max(tB.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC)+
        max(tC.Consumo) - LAG(max(tC.Consumo)) OVER (ORDER BY CAST(tA.E3TimeStamp AS date) ASC, DATEPART(HOUR,tA.E3TimeStamp) ASC), 'N', 'de-de') AS Total
    FROM GrandeRio.dbo.hist_TrafoA tA
    INNER JOIN GrandeRio.dbo.hist_TrafoB tB ON tB.E3TimeStamp = tA.E3TimeStamp 
    INNER JOIN GrandeRio.dbo.hist_TrafoB tC ON tC.E3TimeStamp = tA.E3TimeStamp 
    WHERE (tA.E3TimeStamp >= DATEADD(DAY, -2, GETDATE()) AND tA.E3TimeStamp <= DATEADD(DAY, -1, GETDATE()))
    GROUP BY CAST(tA.E3TimeStamp AS date), DATEPART(HOUR,tA.E3TimeStamp)
    ORDER BY Data ASC
'''
sql3 = '''\
    SELECT  
        CAST(g.E3TimeStamp AS date) AS dia,
        FORMAT(max(g.Consumo) - LAG(max(g.Consumo)) OVER (ORDER BY CAST(g.E3TimeStamp AS date) ASC), 'N', 'de-de') AS Consumo
    FROM GrandeRio.dbo.hist_TrafoA g 
    WHERE (g.E3TimeStamp >= SMALLDATETIMEFROMPARTS (2018, 12, 15, 05, 00) AND g.E3TimeStamp <= GETDATE() )
    GROUP BY CAST(g.E3TimeStamp AS date)
    ORDER BY dia ASC
'''
consumoHora = pd.read_sql_query(sql2, connection)
consumoDia = pd.read_sql_query(sql3, connection)

conHora = consumoHora.drop([0])
conHora['Data'] = pd.to_datetime(conHora['Data'])

def ConsumoHora(df):
    dado = {'Data' : df['Data'],
               'TrafoA' : df['Trafo A'],
               'TrafoB' : df['Trafo B'],
               'TrafoC' : df['Trafo C'],
               'Total' : df['Total'],
               'time_fmt' : [x.strftime("%Y-%m-%d %H:%M:%S")for x in df['Data']]
               }
    return dado
def ConsumoDia(df):
    dado = {'Data' : df['dia'],
               'Consumo' : df['Consumo'],
               'time_fmt' : [x.strftime("%Y-%m-%d %H:%M:%S")for x in df['dia']]
               }
    return dado

source_consumoHora = ColumnDataSource(data=ConsumoHora(conHora))
source_consumoDia = ColumnDataSource(data=ConsumoDia(consumoDia))

fig = dict(plot_width = 1400,
           plot_height = 650,
           x_axis_label='Data', 
           x_axis_type="datetime",      
           toolbar_location="below",
           logo=None,)

fig_Bar = figure(y_axis_label='Consumo [kwh]', title="Trafo A - Gráfico de Consumo por dia", **fig)

props = dict(line_width=2, line_alpha=0.7)

A1 = fig_Bar.vbar(x='Data', top='TrafoA', width=0.9, bottom=0, fill_color=Viridis3[0], source=source_consumoHora)
A2 = fig_Bar.vbar(x='Data', top='TrafoB', width=0.9, bottom=0, fill_color=Viridis3[1], source=source_consumoHora)
A3 = fig_Bar.vbar(x='Data', top='TrafoC', width=0.9, bottom=0, fill_color=Viridis3[2], source=source_consumoHora)
A4 = fig_Bar.line(x='Data', y='Total', source=source_consumoHora, line_color=Category20[20][15], **props)

houverConsumo = HoverTool(tooltips=[
                            ('Data', '@time_fmt'),
                            ("Trafo A", "@TrafoA{0.00} kwh"),
                            ("Trafo B", "@TrafoB{0.00} kwh"),
                            ("Trafo C", "@TrafoC{0.00} kwh"),
                            ("Total", "@Total{0.00} kwh"),
                            ],)
fig_Bar.add_tools(houverConsumo)
legfig_Bar = Legend(items=[
                        ("Trafo A", [A1]),    
                        ("Trafo B", [A2]),
                        ("Trafo C", [A3]),
                        ("Total", [A4]),
                        ], location=(0,150))
fig_Bar.add_layout(legfig_Bar, 'right')

#Tabela
colunas = [
    TableColumn(field="Data", title="Data", formatter=DateFormatter()),
    TableColumn(field="TrafoA", title="Trafo A"),
    TableColumn(field="TrafoB", title="Trafo B"),
    TableColumn(field="TrafoC", title="Trafo C"),
    TableColumn(field="Total", title="Total"),
]

tabela = DataTable(source=source_consumoHora, columns=colunas, width=450, height=630)

layout = row(tabela, fig_Bar,)

output_file("Testes_ConsumoHH.html", title="Grande Rio - Consumo")
output_notebook()
show(layout)