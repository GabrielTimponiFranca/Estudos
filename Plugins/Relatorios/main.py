# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4  #
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.units import *
from datetime import datetime           #biblioteca para comando com data e tempo
from reportlab.pdfgen import *
import os
import Plugins as ep
import numpy as np
### Plugins EPM Studio - Dataset Analysis ###
@ep.DatasetFunctionPlugin('Consumo',1)
def Cons():
    d1=ep.EpmDatasetPens.SelectedPens[0].Values
    ultimo=d1.size - 1 
    Consumo=(d1['Value'][ultimo]-d1['Value'][0])/1000
    ultimomes=d1['Timestamp'][ultimo].strftime('%m')
    numero_pagina = 1                                             #numero inicial de paginas
    nome_relatorio="Consumo"                             #nome de relatorio
    nome_relatorio_pdf = 'D:\Relatorios\Consumo ' + ep.DatasetFunctionPlugin.SelectedPens[0].Name +' ' + datetime.now().strftime('%d%m%Y%H%M%S') + '.pdf'         #nome do arquivo gerado
    c = canvas.Canvas(nome_relatorio_pdf,pagesize=A4)
    c.setFont('Helvetica',28,leading = None)
    c.drawCentredString(300,710,'Consumo')
    c.drawCentredString(300,640,'de')
    c.drawCentredString(300,590,'Energia Elétrica')
    c.setFont('Helvetica',18,leading = None)
    c.drawCentredString(300,420,'Dados do Medidor')
    aux1=u"%s" % d1['Timestamp'][0].strftime('%d-%m-%Y %H:%M:%S')
    dati= 'Data Inicial: ' + aux1
    aux1=u"%s" % d1['Timestamp'][ultimo].strftime('%d-%m-%Y %H:%M:%S')
    datf= 'Data Final: ' + aux1
    aux1=u"%s" % (d1['Value'][0]/1000)
    vali= 'Valor: ' + aux1 + ' Kw/h'
    aux1=u"%s" % (d1['Value'][ultimo]/1000)
    valf= 'Valor: ' + aux1 + ' Kw/h'
    aux1=u"%s" % Consumo
    con= 'Consumo: ' + aux1 + ' Kw/h'
    tab=[[dati,vali],[datf,valf],[con,'']]
    t=Table(tab,9.1*cm,0.6*cm,style=[('LINEABOVE',(0,0),(-1,-1),1,colors.black),
                                     ('BOX',(0,0),(-1,-1),2,colors.black),
                                     ('ALIGN',(1,0),(-1,-1),'RIGHT')])
    t.wrapOn(c,450,590)
    t.drawOn(c,40,340)  
    '''c.drawString(110,450,dati)
    c.drawString(110,420,datf)
    c.drawString(425,450,vali)
    c.drawString(425,420,valf)
    c.drawString(110,390,con)'''
    c.setFont('Helvetica',9,leading = None)
    data_atual=datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    c.setFont('Helvetica',12,leading = None)
    c.drawString(425,30,data_atual)  
    c.showPage()
    c.save()
    """os.startfile(nome_relatorio_pdf)"""
    print '\n Consumo:'
    print Consumo
    print ' Kw/h'
    return 0



### Plugins EPM Studio - Dataset Analysis ###
@ep.DatasetFunctionPlugin('Todos os Dados',1)
def TodDados():
    tab=ep.DatasetFunctionPlugin.SelectedPens[0].Values
    numero_pagina = 1                                              #numero inicial de paginas
    nome_relatorio=" Todos os dados"                             #nome de relatorio
    nome_relatorio_pdf = 'D:\Relatorios\Relatorio' + nome_relatorio + ' ' + datetime.now().strftime('%d%m%Y%H%M%S') + '.pdf'                    #nome do arquivo gerado
    c = canvas.Canvas(nome_relatorio_pdf,pagesize=A4)               
    valores=tab['Value'].tolist()
    tstamp=tab['Timestamp'].tolist()
    tab1=np.column_stack((tab['Value'],tab['Timestamp'])).tolist()
    linhas=tab.size-(tab.size/40)*40
    numeropagina=tab.size/40+1
    capa(c)
    for x in range(numeropagina):
        grid(c,x,numeropagina,nome_relatorio,linhas,tab1)
    c.save()
    """os.startfile(nome_relatorio_pdf)"""
    return 0

def grid(c,numeropagina,numero_pagina,nome_relatorio,linhas,tab1):
    rodape(c,numeropagina)
    cabecalho(c,nome_relatorio)
    corpo(c)
    c.setFont('Helvetica', 5 , leading = None)
    if (numero_pagina-1) == numeropagina:
        tabela(c,tab1,numeropagina,linhas)
    else:
        tabela(c,tab1,numeropagina,40)
    c.showPage()
    numero_pagina += numero_pagina
    return 0

def logo(c):                                                    #desenha um logo no topo da pagina a direita
    logo = 'images.jpg'
    c.drawImage(logo,525,782,width=20 , height = 35)            #arquivo da imagem,coordenada x, coordenada y, largura None(original), altura None(original)
    c.setFont('Helvetica', 8, leading = None)                   #fonte usada no comando drawString
    c.drawString(480,800,"Logo CAMG")                           #Escreve uma string no pdf (coordenada x, coordenada y, texto)

def cabecalho(c,nome_relatorio):                                #Escreve o cabecalho, sendo o nome do relatorio a esquerda e o logo a direita
    c.setFont('Helvetica',12,leading = None)
    c.drawString(35,800,ep.DatasetFunctionPlugin.SelectedPens[0].Name)
    #logo(c)

def rodape(c,numero_pagina):
    #data_atual=str(datetime.now())              data e tempo no formato do sql
    """if numero_pagina> 0:"""
    data_atual=datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    c.setFont('Helvetica',12,leading = None)
    c.drawString(50,30,data_atual)
    c.drawString(550,30,u"%s" %(numero_pagina+1))

def corpo(c):
    xi=50
    yi=750
    c.setFont('Helvetica',12,leading = None)
    c.drawString(75,yi,'Valor')
    c.drawString(480,yi,'Data')
def tabela(c,data,pag,numlinha):    #maximo de linha por pagina = 40
    altura_linha=17.5
    yajustado=758-numlinha*17.5       #trocar o 40 pelo numero de linhas
    t=Table(data[pag*40:pag*40+numlinha],9.1*cm,0.6*cm,style=[('LINEABOVE',(0,0),(-1,-1),1,colors.black),
                                     ('BOX',(0,0),(-1,-1),2,colors.black),
                                     ('ALIGN',(1,0),(-1,-1),'RIGHT')])
    t.wrapOn(c,450,750)
    t.drawOn(c,40,yajustado)
def capa(c):
    c.setFont('Helvetica',28,leading = None)
    c.drawCentredString(300,700,'Dados')
    c.drawCentredString(300,640,'da')
    c.drawCentredString(300,580,'Variável')
    c.setFont('Helvetica',24,leading = None)
    c.drawCentredString(300,520,ep.DatasetFunctionPlugin.SelectedPens[0].Name)
    c.showPage()

"""### Plugins EPM Studio - Dataset Analysis ###
@ep.DatasetFunctionPlugin('Alarmes',1)
def Alarmes():
    quantidade=len(ep.DatasetFunctionPlugin.SelectedPens)
    for x in range(quantidade):
        c=0
        var=np.column_stack((ep.DatasetFunctionPlugin.SelectedPens[x].Values['Value'],ep.DatasetFunctionPlugin.SelectedPens[x].Values['Timestamp'])).tolist()
        for i in range(ep.DatasetFunctionPlugin.SelectedPens[x].Values.size):
            var[i]=[0,0]
        for y in range (ep.DatasetFunctionPlugin.SelectedPens[x].Values.size):
            if y>0:
                if var[y-1] == 0 and var[y]==1:
                    var[c]=[ep.DatasetFunctionPlugin.SelectedPens[x].Values['Value'][y],ep.DatasetFunctionPlugin.SelectedPens[x].Values['Timestamp'][y]]
                    c+=c
        print var
    return 0"""
