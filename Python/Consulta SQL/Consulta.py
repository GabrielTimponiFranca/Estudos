import pyodbc
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# import plotly as py
# import plotly.plotly as py
# import plotly.tools as plotly_tools
# import plotly.graph_objs as go
from IPython.display import HTML
import bokeh.sampledata

plotly_tools.set_credentials_file(username='Timponi', api_key='ZJn0u55o3l5c6w2MMPdS')

#server = '10.0.0.110\cco_db'
server = '200.233.212.247'
database = 'GrandeRio'
user = 'sa'
password = 'CCO@123456'
driver = '{ODBC Driver 13 for SQL Server}'

connection = pyodbc.connect('DRIVER='+driver+'; Server='+server+'; PORT:1433; DATABASE='+database+'; UID='+user+'; PWD='+password + '; Trusted_Connection = yes;')

cursor = connection.cursor() 
if connection:
    print("\n\nComunicando\n")

sql = '''\
    SELECT E3TimeStamp AS Data, 
            CorrenteA AS [Corrente A], 
            TensaoA AS [Tensão A], 
            CorrenteB AS [Corrente B], 
            TensaoB AS [Tensão B], 
            CorrenteC AS [Corrente C], 
            TensaoC AS [Tensão C], 
            Potencia AS [Potência]
    FROM GrandeRio.dbo.hist_TrafoC   
    WHERE (hist_TrafoC.E3TimeStamp >= SMALLDATETIMEFROMPARTS (2018, 12, 14, 23, 50) AND hist_TrafoC.E3TimeStamp <= GETDATE() )
    ORDER BY hist_TrafoC.E3TimeStamp ASC
'''
#cursor = cursor.execute(sql)
#tables = cursor.fetchall()
#for i in tables:
    #print(i[0])
 #   plt.plot(i[0], i[1])
#print("Salvo no diretorio: ", os.getcwd())

df = pd.read_sql_query(sql, connection)

#df.colums=['Data', 'Corrente A', 'Tensão A', 'Corrente B', 'Tensão B', 'Corrente C', 'Tensão C', 'Potência']


#type(df)

#%matplotlib notebook

#df'].plot()




#print(df)

#print(df[0:3])

#print(df.head())

#print(df.T)

#print(df)
#print(df.dtypes)
#HTML(df.to_html('table table-striped'))
#print(HTML)
plt.title("Gráfico de Corrente")
plt.xlabel("Data")
plt.ylabel("[A]")

#for c in cursor:
#    print(c[0], c[1], c[3], c[5], c[7] )

# layout = go.Layout(title= 'Trafo C - Gráfico de Corrente',
#                   xaxis= dict(
#                   title= 'Data'),
#                   yaxis= dict(
#                   title= 'Corrente [A]'))
# correnteA = go.Scattergl(x = df['Data'], y = df['Corrente A'],mode='lines', name='Fase A')
# correnteB = go.Scattergl(x = df['Data'], y = df['Corrente B'],mode='lines', name='Fase B')
# correnteC = go.Scattergl(x = df['Data'], y = df['Corrente C'],mode='lines', name='Fase C')
# dados = [correnteA, correnteB, correnteC]
# fig = go.Figure(data=dados, layout=layout)
# py.iplot(fig, height=1300, width=800)
# urlCorrente = py.plot(dados, height=1300, width=800, auto_open=False)
# #print (urlCorrente)
# figC = plotly_tools.get_subplots(rows=1,columns=1, print_grid=True)
# figC['layout']['xaxis{}'.format(1)].update( title='Data' )
# figC['layout']['yaxis{}'.format(1)].update( title='Corrente [A]' )
# figC['layout'].update(showlegend=False,height=1300,width=800, title='Trafo C - Gráfico de Corrente')
# figC['data'] = dados

# html_string = '''
# <html>   
#     <body>
#         <h1>Shopping Grande Rio</h1>

#         <!-- *** Section 1 *** --->
#         <h2>Trafo C - Gráfico de Corrente</h2>
#         <iframe width="1300" height="800" frameborder="0" seamless="seamless" scrolling="no" \
# src="''' + urlCorrente + '''.embed?width=800&height=550"></iframe>      
             
#     </body>
# </html>'''

# f = open('Trafo C Corrente.html','w')
# f.write(html_string)
# f.close()



from bokeh.plotting import figure, output_file, show, output_notebook
from bokeh.models import ColumnDataSource, HoverTool, DatetimeTickFormatter, NumeralTickFormatter
from bokeh.models.widgets import Tabs, Panel
#from IPython.display import IFrame
#from bokeh.layouts import widgetbox
#from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider

#hover_tool.formatters = { "close date": "datetime"}

output_file("teste_04.html")
output_notebook()

# create some widgets
#slider = Slider(start=dataIni, end=dataFim, value=1, step=.1, title="Slider")
#dateSlider = DateRangeSlider(title="Range data: ", start=dataIni, end=DataFim, step=1)


#button_group = RadioButtonGroup(labels=["Option 1", "Option 2", "Option 3"], active=0)
#select = Select(title="Option:", value="foo", options=["foo", "bar", "baz", "quux"])
#button_1 = Button(label="Button 1")
#button_2 = Button(label="Button 2")

# put the results in a row
#show(widgetbox(button_1, slider, button_group, select, button_2, width=300))

df['tooltip'] = [x.strftime("%Y-%m-%d %H:%M:%S") for x in df['Data']]

x = pd.to_datetime(df['Data'])
y1 = df['Corrente A']
y2 = df['Corrente B']
y3 = df['Corrente C']
y4 = df['Potência']
y5 = df['Potência'].std()
y6 = df['Potência'].mean()

select_tools = ['box_zoom',
                'pan',
                'save',
                'hover',
                'resize',
                'reset',
                'tap',
                'wheel_zoom']

figCorrente = figure(plot_width=1000, 
                     plot_height=450,
                     x_axis_label='Data',
                     y_axis_label='Corrente [A]',
                     x_axis_type="datetime", 
                     title="Trafo C - Gráfico de Corrente", 
                     toolbar_location="below",
                    )



figCorrente.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )

figCorrente.line(x, y1, line_width=1, alpha=1, legend="Fase A", line_color="red")
figCorrente.line(x, y2, line_width=1, alpha=0.5, legend="Fase B", line_color="orange")
figCorrente.line(x, y3, line_width=1, legend="Fase C", line_color="navy")

figCorrente.yaxis[0].formatter = NumeralTickFormatter(format='00.0')

figCorrente.add_tools(HoverTool(
                        tooltips=[
                            ('Data', '@x{%F}'),
                            ("Fase A", "@y1{0.00} A"),
                            ("Fase B", "@y2{%0.2f} A"),
                            ("Fase C", '@y3{0.00%} A')
                        ],
                        formatters={
                            'x' : 'datetime',
                        }
                        ))
figCorrente.legend.click_policy = 'hide'

figPotencia = figure(plot_width=1000, 
                     plot_height=450,
                     x_axis_label='Data',
                     y_axis_label='Potência [kw]',
                     x_axis_type="datetime", 
                     title="Trafo C - Gráfico de Potência", 
                     toolbar_location="below",
                    )
figPotencia.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y"],
        days=["%d %B %Y"],
        months=["%d %B %Y"],
        years=["%d %B %Y"],
    )

figPotencia.line(x, y4, line_width=2, alpha=1, legend="Potência", line_color="red")
figPotencia.line(x, y5, line_width=2, alpha=1, legend="Desvio Padrão", line_color="orange")
figPotencia.line(x, y6, line_width=2, alpha=1, legend="Média", line_color="navy")

figPotencia.add_tools(HoverTool(
                        tooltips=[
                            ('Data', '@x{%F}'),
                            ("Potência", '@y4{0.00}'),
                            ('Desvio Padrão', '@y5{%F}'),
                            ('Média', '@y6{0.00}'),
                        ],
                        formatters={
                            'x' : 'datetime',
                        }
                        ))

figPotencia.legend.click_policy = 'hide'

painelCorrente = Panel(child=figCorrente, title='Gráfico Corrente')
painelPotencia = Panel(child=figPotencia, title='Gráfico Potência')

tabs = Tabs(tabs=[painelCorrente,
                  painelPotencia,
                 ])

show(tabs)
#iFrame(fig, width= 1300, height = 800 )