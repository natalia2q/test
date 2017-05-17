# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 17:07:13 2016

@author: Natalia
"""

import sqlite3

import plotly.plotly as py
import plotly.graph_objs as go

# before to start you have to set the credential that the Plotly gives you when you are sing up in the website
# plotly.tools.set_credentials_file(username='natalia2q', api_key='yvtcs*****')

con = sqlite3.connect('dbworld')  
curs = con.cursor()

Menu = """
***Enter an option:
(1) Top 10 spoken languages
(2) Average life expectancy by Continent
(3) Top 10 countries with highest Gross National Product(GNP)
(x) Exit
->"""


while True:

    option= input(Menu).strip()   
    
    if option == 'x':                              # ***************Exit
        con.close()
        del con     
        break   
    
    elif option == '1':                            # Top 10 spoken languages
        
        query = """
        SELECT l.language, round(sum(co.population * (l.percentage/100))) population
        FROM countrylanguage l
        join Country co on l.CountryCode = co.code
        group by l.language
        order by sum(co.population * (l.percentage/100)) DESC Limit 10"""
        curs.execute(query)
        qdata = curs.fetchall()                    # data came in a list of tuples [('x','1'),('y','2'),..]
        
        lang = []
        popul = []
        for item in qdata:                         # setting the variables in separated lists 
            lang.append(item[0])
            popul.append(item[1])
            
        data = [go.Bar(
                       x = lang, 
                       y = popul,
                       marker=dict(
                                   color='rgb(158,202,225)',
                                    line=dict(color='rgb(8,48,107)',width=1.5)
                                    ),
                       opacity=0.6
        )]
                                    
        layout = go.Layout(            
            title = 'Top 10 Spoken Languages',    
            titlefont = dict(color='darkblue',size = 24),
            xaxis = dict(title='Language'),
            yaxis = dict(title='Population'),
            plot_bgcolor = 'whitesmoke')  
                                                           
        figure = go.Figure(data=data, layout=layout)
        plot_url = py.plot(figure, filename='Top 10 spoken languages')

    elif option == '2':                             # Average life expectancy by Continent

        query = """
                SELECT Continent, avg(GNP) 'Current GNP', count(name)
                FROM Country
                WHERE LifeExpectancy is not null
                GROUP BY Continent
                ORDER BY avg(LifeExpectancy) DESC"""
        curs.execute(query)
        qdata = curs.fetchall()                    # data came in a list of tuples [('x','1'),('y','2'),..]
        
        continent = []
        gnp = []
       

        for item in qdata:                         # setting the variables in separated lists 
            continent.append(item[0])
            gnp.append(item[1])   
           
        
        data = [go.Pie(
                  values = gnp,
                  labels = continent,
                  hoverinfo = "label+percent+name",
                  textposition = "outside",
                  marker=dict(
                                    colors=['rgb(255,255,219)',
                                  'rgb(189,229,202)',
                                  'rgb(82,149,197)',
                                  'rgb(122,204,214)',
                                  'rgb(102,113,180)',
                                  'rgb(107,165,205)'],
                                    line=dict(color='rgb(88,87,87)',width=1.5)
                                    ),
                  textfont=dict(size=18),
                  opacity=0.6,
                  pull = 0.05
                  
                  )]
        layout = go.Layout(            
                    title = "GNP by Continent",    
                    titlefont = dict(color='darkblue',size = 24),
                    plot_bgcolor = 'whitesmoke')  
                              
        
        figure = go.Figure(data=data, layout=layout)
        plot_url = py.plot(figure, filename='2')
     
    elif option == '3':   #Countries with highest and the lowest life expectancy
        query = """
            SELECT Name, Region, GNP 'Current GNP',GNPOld 'Last GNP', GNP-GNPOld Growth
            FROM Country
            order by GNP DESC Limit 10"""
        curs.execute(query)
        qdata = curs.fetchall()              
        
        country = []
        region = []
        gnp = []
        gnpold = []
        diff = []

        for item in qdata:                         
            country.append(item[0])
            region.append(item[1])    
            gnp.append(item[2])
            gnpold.append(item[3])
            diff.append(item[4])
      
        trace1 = go.Scatter(
            x=country,
            y=gnp,
            name = 'GNP',
            line = dict(
                color = ('rgb(80,139,249)'),
                )
        )
        trace2 = go.Scatter(
            x=country,
            y=gnpold,
            name = 'GNP Old',
            line = dict(
                color = ('rgb(249,150,80'),
                )
        )
        trace3 = go.Bar(
            x=country,
            y=diff,
            name = 'Difference',
            marker=dict(
                   color='rgb(246,240,153)',
                   line=dict(color='rgb(246,202,131)',width=1.5)
                   ),
            
        ) 
        data = [trace1,trace2,trace3]
        
        layout = go.Layout(            
            title = 'Top 10 countries with highest Gross National Product(GNP)',    
            titlefont = dict(color='rgb(80,139,249)',size = 24),
            xaxis = dict(title='Country'),
            
            )  

        figure = go.Figure(data=data, layout=layout)
        plot_url = py.plot(figure, filename='GNP')
        
