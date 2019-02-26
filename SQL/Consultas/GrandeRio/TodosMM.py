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


server = '200.233.212.247'
database = 'GrandeRio'
user = 'sa'
password = 'CCO@123456'
driver = '{ODBC Driver 13 for SQL Server}'

connection = pyodbc.connect('DRIVER='+driver+'; Server='+server+'; PORT:1433; DATABASE=' +
                            database+'; UID='+user+'; PWD='+password + '; Trusted_Connection = yes;')

cursor = connection.cursor()
if connection:
    print("\n\nComunicando\n")

sql1 = '''\
    SELECT E3TimeStamp AS Data, 
            CorrenteA AS [CorA], 
            TensaoA AS [TA], 
            CorrenteB AS [CorB], 
            TensaoB AS [TB], 
            CorrenteC AS [CorC], 
            TensaoC AS [TC],
            PotenciaA AS [PotA],
            PotenciaB AS [PotB],
            PotenciaC AS [PotC],
            Potencia AS [Pot],
            FPA,
            FPB,
            FPC,
            FPTotal AS [FP]
    FROM GrandeRio.dbo.hist_TrafoA   
    WHERE (hist_TrafoA.E3TimeStamp >= SMALLDATETIMEFROMPARTS (2018, 12, 14, 23, 50) AND hist_TrafoA.E3TimeStamp <= GETDATE() )
    ORDER BY hist_TrafoA.E3TimeStamp ASC
'''
sql2 = '''\
    SELECT E3TimeStamp AS Data, 
            CorrenteA AS [CorA], 
            TensaoA AS [TA], 
            CorrenteB AS [CorB], 
            TensaoB AS [TB], 
            CorrenteC AS [CorC], 
            TensaoC AS [TC],
            PotenciaA AS [PotA],
            PotenciaB AS [PotB],
            PotenciaC AS [PotC],
            Potencia AS [Pot],
            FPA,
            FPB,
            FPC,
            FPTotal AS [FP]
    FROM GrandeRio.dbo.hist_TrafoB   
    WHERE (hist_TrafoB.E3TimeStamp >= SMALLDATETIMEFROMPARTS (2018, 12, 14, 23, 50) AND hist_TrafoB.E3TimeStamp <= GETDATE() )
    ORDER BY hist_TrafoB.E3TimeStamp ASC
'''

sql3 = '''\
    SELECT E3TimeStamp AS Data, 
            CorrenteA AS [CorA], 
            TensaoA AS [TA], 
            CorrenteB AS [CorB], 
            TensaoB AS [TB], 
            CorrenteC AS [CorC], 
            TensaoC AS [TC],
            PotenciaA AS [PotA],
            PotenciaB AS [PotB],
            PotenciaC AS [PotC],
            Potencia AS [Pot],
            FPA,
            FPB,
            FPC,
            FPTotal AS [FP]
    FROM GrandeRio.dbo.hist_TrafoC   
    WHERE (hist_TrafoC.E3TimeStamp >= SMALLDATETIMEFROMPARTS (2018, 12, 14, 23, 50) AND hist_TrafoC.E3TimeStamp <= GETDATE() )
    ORDER BY hist_TrafoC.E3TimeStamp ASC
'''

trafoA = pd.read_sql_query(sql1, connection)
trafoB = pd.read_sql_query(sql2, connection)
trafoC = pd.read_sql_query(sql3, connection)
#len(trafoA)


def data(df):
    data = {'Data': df['Data'],
            'IA': df['CorA'],
            'IB': df['CorB'],
            'IC': df['CorC'],
            'TA': df['TA'],
            'TB': df['TB'],
            'TC': df['TC'],
            'PotA': df['PotA'],
            'PotB': df['PotB'],
            'PotC': df['PotC'],
            'Pot': df['Pot'],
            'FPA': df['FPA'],
            'FPB': df['FPB'],
            'FPC': df['FPC'],
            'FP': df['FP'],
            'time_fmt': [x.strftime("%Y-%m-%d %H:%M:%S")for x in df['Data']]
            }
    return data

source_trafoA = ColumnDataSource(data=data(trafoA))
source_trafoB = ColumnDataSource(data=data(trafoB))
source_trafoC = ColumnDataSource(data=data(trafoC))


def EixoMinTensao(df):
    minE = list(range(3))
    minE[0] = df['TA'].min()
    minE[1] = df['TB'].min()
    minE[2] = df['TC'].min()
    return min(minE)

def EixoMaxTensao(df):
    maxE = list(range(3))
    maxE[0] = df['TA'].max()
    maxE[1] = df['TB'].max()
    maxE[2] = df['TC'].max()
    return max(maxE)

def EixoMinPotencia(df):
    minE = list(range(4))
    minE[0] = df['PotA'].min()
    minE[1] = df['PotB'].min()
    minE[2] = df['PotC'].min()
    minE[3] = df['Pot'].min()
    return min(minE)

def EixoMaxPotencia(df):
    maxE = list(range(4))
    maxE[0] = df['PotA'].max()
    maxE[1] = df['PotB'].max()
    maxE[2] = df['PotC'].max()
    maxE[3] = df['Pot'].max()
    return max(maxE)

def EixoMinFP(df):
    minE = list(range(4))
    minE[0] = df['FPA'].min()
    minE[1] = df['FPB'].min()
    minE[2] = df['FPC'].min()
    minE[3] = df['FP'].min()
    return min(minE)

def EixoMaxFP(df):
    maxE = list(range(4))
    maxE[0] = df['FPA'].max()
    maxE[1] = df['FPB'].max()
    maxE[2] = df['FPC'].max()
    maxE[3] = df['FP'].max()
    return max(maxE)

fig = dict(plot_width=1400,
            plot_height=600,
            x_axis_label='Data',
            x_axis_type="datetime",
            toolbar_location="below",)


figA_C = figure(y_axis_label='Corrente [A]',
                title="Trafo A - Gráfico Corrente", **fig)
figA_T = figure(y_axis_label='Tensão [V]',
                title="Trafo A - Gráfico Trnsão", **fig)
figA_P = figure(y_axis_label='Potência [kw]',
                title="Trafo A - Gráfico Potência", **fig)
figA_F = figure(y_axis_label='FP',
                title="Trafo A - Gráfico Fator de Potência", **fig)

props = dict(line_width=2, line_alpha=0.7)

A1 = figA_C.line(x='Data', y='IA', source=source_trafoA,
                 line_color=Viridis3[0], **props)
A2 = figA_C.line(x='Data', y='IB', source=source_trafoA,
                 line_color=Viridis3[1], **props)
A3 = figA_C.line(x='Data', y='IC', source=source_trafoA,
                 line_color=Viridis3[2], **props)

A4 = figA_T.line(x='Data', y='TA', source=source_trafoA,
                 line_color=Viridis3[0], **props)
A5 = figA_T.line(x='Data', y='TB', source=source_trafoA,
                 line_color=Viridis3[1], **props)
A6 = figA_T.line(x='Data', y='TC', source=source_trafoA,
                 line_color=Viridis3[2], **props)

A7 = figA_P.line(x='Data', y='PotA', source=source_trafoA,
                 line_color=Viridis3[0], **props)
A8 = figA_P.line(x='Data', y='PotB', source=source_trafoA,
                 line_color=Viridis3[1], **props)
A9 = figA_P.line(x='Data', y='PotC', source=source_trafoA,
                 line_color=Viridis3[2], **props)
A10 = figA_P.line(x='Data', y='Pot', source=source_trafoA,
                  line_color=Category20[20][15], **props)

A11 = figA_F.line(x='Data', y='FPA', source=source_trafoA,
                  line_color=Viridis3[0], **props)
A12 = figA_F.line(x='Data', y='FPB', source=source_trafoA,
                  line_color=Viridis3[1], **props)
A13 = figA_F.line(x='Data', y='FPC', source=source_trafoA,
                  line_color=Viridis3[2], **props)
A14 = figA_F.line(x='Data', y='FP', source=source_trafoA,
                  line_color=Category20[20][15], **props)

houver = HoverTool(tooltips=[
    ('Data', '@time_fmt'),
    ("Corrente A", "@IA{0.00} A"),
    ("Corrente B", "@IB{0.00} A"),
    ("Corrente C", '@IC{0.00} A'),
    ("Tensão A", '@TA{0.00} V'),
    ("Tensão B", '@TB{0.00} V'),
    ("Tensão C", '@TC{0.00} V'),
    ("Potência A", "@PotA{0.00} kw"),
    ("Potência B", "@PotB{0.00} kw"),
    ("Potência C", "@PotC{0.00} kw"),
    ("Potência", "@Pot{0.00} kw"),
    ("FP A", "@FPA{0.000} "),
    ("FP B", "@FPB{0.000} "),
    ("FP C", "@FPC{0.000} "),
    ("FP", "@FP{0.000} "),
],)

figA_C.add_tools(houver)
figA_T.add_tools(houver)
figA_P.add_tools(houver)
figA_F.add_tools(houver)

legfigA_C = Legend(items=[
    ("Corrente Fase A", [A1]),
    ("Corrente Fase B", [A2]),
    ("Corrente Fase C", [A3]),
], location=(0, 150))

legfigA_T = Legend(items=[
    ("Tensão Fase A", [A4]),
    ("Tensão Fase B", [A5]),
    ("Tensão Fase C", [A6]),
], location=(0, 150))

legfigA_P = Legend(items=[
    ("Potência Fase A", [A7]),
    ("Potência Fase B", [A8]),
    ("Potência Fase C", [A9]),
    ("Potência Total", [A10]),
], location=(0, 150))

legfigA_F = Legend(items=[
    ("Fator de Potência Fase A", [A11]),
    ("Fator de Potência Fase B", [A12]),
    ("Fator de Potência Fase C", [A13]),
    ("Fator de Potência Total", [A14]),
], location=(0, 150))

figA_C.add_layout(legfigA_C, 'right')
figA_T.add_layout(legfigA_T, 'right')
figA_P.add_layout(legfigA_P, 'right')
figA_F.add_layout(legfigA_F, 'right')

figA_C.legend.click_policy = 'hide'
figA_T.legend.click_policy = 'hide'
figA_P.legend.click_policy = 'hide'
figA_F.legend.click_policy = 'hide'

layoutA = column(figA_C, figA_T, figA_P, figA_F, sizing_mode="scale_width",)

output_file("SGR_TrafoA.html", title="Grande Rio - Trafo A")
show(layoutA)

fig = dict(plot_width=1400,
           plot_height=600,
           x_axis_label='Data',
           x_axis_type="datetime",
           toolbar_location="below",)

figB_C = figure(y_axis_label='Corrente [A]',
                title="Trafo B - Gráfico Corrente", **fig)
figB_T = figure(y_axis_label='Tensão [V]',
                title="Trafo B - Gráfico Trnsão", **fig)
figB_P = figure(y_axis_label='Potência [kw]',
                title="Trafo B - Gráfico Potência", **fig)
figB_F = figure(y_axis_label='FP',
                title="Trafo B - Gráfico Fator de Potência", **fig)

props = dict(line_width=2, line_alpha=0.7)

A1 = figB_C.line(x='Data', y='IA', source=source_trafoB,
                 line_color=Viridis3[0], **props)
A2 = figB_C.line(x='Data', y='IB', source=source_trafoB,
                 line_color=Viridis3[1], **props)
A3 = figB_C.line(x='Data', y='IC', source=source_trafoB,
                 line_color=Viridis3[2], **props)

A4 = figB_T.line(x='Data', y='TA', source=source_trafoB,
                 line_color=Viridis3[0], **props)
A5 = figB_T.line(x='Data', y='TB', source=source_trafoB,
                 line_color=Viridis3[1], **props)
A6 = figB_T.line(x='Data', y='TC', source=source_trafoB,
                 line_color=Viridis3[2], **props)

A7 = figB_P.line(x='Data', y='PotA', source=source_trafoB,
                 line_color=Viridis3[0], **props)
A8 = figB_P.line(x='Data', y='PotB', source=source_trafoB,
                 line_color=Viridis3[1], **props)
A9 = figB_P.line(x='Data', y='PotC', source=source_trafoB,
                 line_color=Viridis3[2], **props)
A10 = figB_P.line(x='Data', y='Pot', source=source_trafoB,
                  line_color=Category20[20][15], **props)

A11 = figB_F.line(x='Data', y='FPA', source=source_trafoB,
                  line_color=Viridis3[0], **props)
A12 = figB_F.line(x='Data', y='FPB', source=source_trafoB,
                  line_color=Viridis3[1], **props)
A13 = figB_F.line(x='Data', y='FPC', source=source_trafoB,
                  line_color=Viridis3[2], **props)
A14 = figB_F.line(x='Data', y='FP', source=source_trafoB,
                  line_color=Category20[20][15], **props)

houver = HoverTool(tooltips=[
    ('Data', '@time_fmt'),
    ("Corrente A", "@IA{0.00} A"),
    ("Corrente B", "@IB{0.00} A"),
    ("Corrente C", '@IC{0.00} A'),
    ("Tensão A", '@TA{0.00} V'),
    ("Tensão B", '@TB{0.00} V'),
    ("Tensão C", '@TC{0.00} V'),
    ("Potência A", "@PotA{0.00} kw"),
    ("Potência B", "@PotB{0.00} kw"),
    ("Potência C", "@PotC{0.00} kw"),
    ("Potência", "@Pot{0.00} kw"),
    ("FP A", "@FPA{0.000} "),
    ("FP B", "@FPB{0.000} "),
    ("FP C", "@FPC{0.000} "),
    ("FP", "@FP{0.000} "),
],)

figB_C.add_tools(houver)
figB_T.add_tools(houver)
figB_P.add_tools(houver)
figB_F.add_tools(houver)

legfigB_C = Legend(items=[
    ("Corrente Fase A", [A1]),
    ("Corrente Fase B", [A2]),
    ("Corrente Fase C", [A3]),
], location=(0, 150))

legfigB_T = Legend(items=[
    ("Tensão Fase A", [A4]),
    ("Tensão Fase B", [A5]),
    ("Tensão Fase C", [A6]),
], location=(0, 150))

legfigB_P = Legend(items=[
    ("Potência Fase A", [A7]),
    ("Potência Fase B", [A8]),
    ("Potência Fase C", [A9]),
    ("Potência Total", [A10]),
], location=(0, 150))

legfigB_F = Legend(items=[
    ("Fator de Potência Fase A", [A11]),
    ("Fator de Potência Fase B", [A12]),
    ("Fator de Potência Fase C", [A13]),
    ("Fator de Potência Total", [A14]),
], location=(0, 150))

figB_C.add_layout(legfigB_C, 'right')
figB_T.add_layout(legfigB_T, 'right')
figB_P.add_layout(legfigB_P, 'right')
figB_F.add_layout(legfigB_F, 'right')

figB_C.legend.click_policy = 'hide'
figB_T.legend.click_policy = 'hide'
figB_P.legend.click_policy = 'hide'
figB_F.legend.click_policy = 'hide'

layoutB = column(figB_C, figB_T, figB_P, figB_F, sizing_mode="scale_width",)

output_file("SGR_TrafoB.html", title="Grande Rio - Trafo B")
show(layoutB)

figC_C = figure(y_axis_label='Corrente [A]',
                title="Trafo C - Gráfico Corrente", **fig)
figC_T = figure(y_axis_label='Tensão [V]',
                title="Trafo C - Gráfico Trnsão", **fig)
figC_P = figure(y_axis_label='Potência [kw]',
                title="Trafo C - Gráfico Potência", **fig)
figC_F = figure(y_axis_label='FP',
                title="Trafo C - Gráfico Fator de Potência", **fig)

props = dict(line_width=2, line_alpha=0.7)

A1 = figC_C.line(x='Data', y='IA', source=source_trafoC,
                 line_color=Viridis3[0], **props)
A2 = figC_C.line(x='Data', y='IB', source=source_trafoC,
                 line_color=Viridis3[1], **props)
A3 = figC_C.line(x='Data', y='IC', source=source_trafoC,
                 line_color=Viridis3[2], **props)

A4 = figC_T.line(x='Data', y='TA', source=source_trafoC,
                 line_color=Viridis3[0], **props)
A5 = figC_T.line(x='Data', y='TB', source=source_trafoC,
                 line_color=Viridis3[1], **props)
A6 = figC_T.line(x='Data', y='TC', source=source_trafoC,
                 line_color=Viridis3[2], **props)

A7 = figC_P.line(x='Data', y='PotA', source=source_trafoC,
                 line_color=Viridis3[0], **props)
A8 = figC_P.line(x='Data', y='PotB', source=source_trafoC,
                 line_color=Viridis3[1], **props)
A9 = figC_P.line(x='Data', y='PotC', source=source_trafoC,
                 line_color=Viridis3[2], **props)
A10 = figC_P.line(x='Data', y='Pot', source=source_trafoC,
                  line_color=Category20[20][15], **props)

A11 = figC_F.line(x='Data', y='FPA', source=source_trafoC,
                  line_color=Viridis3[0], **props)
A12 = figC_F.line(x='Data', y='FPB', source=source_trafoC,
                  line_color=Viridis3[1], **props)
A13 = figC_F.line(x='Data', y='FPC', source=source_trafoC,
                  line_color=Viridis3[2], **props)
A14 = figC_F.line(x='Data', y='FP', source=source_trafoC,
                  line_color=Category20[20][15], **props)

houver = HoverTool(tooltips=[
    ('Data', '@time_fmt'),
    ("Corrente A", "@IA{0.00} A"),
    ("Corrente B", "@IB{0.00} A"),
    ("Corrente C", '@IC{0.00} A'),
    ("Tensão A", '@TA{0.00} V'),
    ("Tensão B", '@TB{0.00} V'),
    ("Tensão C", '@TC{0.00} V'),
    ("Potência A", "@PotA{0.00} kw"),
    ("Potência B", "@PotB{0.00} kw"),
    ("Potência C", "@PotC{0.00} kw"),
    ("Potência", "@Pot{0.00} kw"),
    ("FP A", "@FPA{0.000} "),
    ("FP B", "@FPB{0.000} "),
    ("FP C", "@FPC{0.000} "),
    ("FP", "@FP{0.000} "),
],)

figC_C.add_tools(houver)
figC_T.add_tools(houver)
figC_P.add_tools(houver)
figC_F.add_tools(houver)

legfigC_C = Legend(items=[
    ("Corrente Fase A", [A1]),
    ("Corrente Fase B", [A2]),
    ("Corrente Fase C", [A3]),
], location=(0, 150))

legfigC_T = Legend(items=[
    ("Tensão Fase A", [A4]),
    ("Tensão Fase B", [A5]),
    ("Tensão Fase C", [A6]),
], location=(0, 150))

legfigC_P = Legend(items=[
    ("Potência Fase A", [A7]),
    ("Potência Fase B", [A8]),
    ("Potência Fase C", [A9]),
    ("Potência Total", [A10]),
], location=(0, 150))

legfigC_F = Legend(items=[
    ("Fator de Potência Fase A", [A11]),
    ("Fator de Potência Fase B", [A12]),
    ("Fator de Potência Fase C", [A13]),
    ("Fator de Potência Total", [A14]),
], location=(0, 150))

figC_C.add_layout(legfigC_C, 'right')
figC_T.add_layout(legfigC_T, 'right')
figC_P.add_layout(legfigC_P, 'right')
figC_F.add_layout(legfigC_F, 'right')

figC_C.legend.click_policy = 'hide'
figC_T.legend.click_policy = 'hide'
figC_P.legend.click_policy = 'hide'
figC_F.legend.click_policy = 'hide'

layoutC = column(figC_C, figC_T, figC_P, figC_F, sizing_mode="scale_width",)

output_file("SGR_TrafoC.html", title="Grande Rio - Trafo C")
show(layoutC)

output_file("GrandeRio.html", title="Grande Rio")
# output_notebook()

painelTrafoA = Panel(child=layoutA, title='Trafo A', sizing_mode="scale_width")
painelTrafoB = Panel(child=layoutB, title='Trafo B', sizing_mode="scale_width")
painelTrafoC = Panel(child=layoutC, title='Trafo C', sizing_mode="scale_width")

grid = gridplot([painelTrafoA, painelTrafoB, painelTrafoC],
                ncols=1, merge_tools=False)
#tabs = Tabs(tabs=[painelTrafoA, painelTrafoB, painelTrafoC,])

gPanel = Panel(child=grid, sizing_mode="scale_width")
tabs = Tabs(tabs=[gPanel])

show(tabs)
