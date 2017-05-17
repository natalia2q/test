# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 16:05:42 2016
@author: Natalia Dosque ndosquec
"""

import sqlite3
con = sqlite3.connect('dbworld')  

curs = con.cursor()
curs.execute('delete from City')
curs.execute('delete from Country')
curs.execute('delete from CountryLanguage')

data = []
fd = open('table_city.txt','r')

for line in fd:
     line = line[line.index('(')+1:line.rindex(')')]
     datacity = line.split(',')
     ID = int(datacity[0])
     Name = str(datacity[1]).strip('\'')
     CountryCode = str(datacity[2]).strip('\'')
     District = str(datacity[3]).strip('\'')
     Population = int(datacity[4])
     data.append([ID,Name,CountryCode,District,Population])
#inserting the data one row by one
for row in data:  
    curs.execute('insert into City values(?,?,?,?,?)', row) # row = [123,'Santiago','Chile',111,'Region Metropolitana',16008343]

""" If I want to print
curs.execute('select * from City')
row = curs.fetchall()
print(row)
"""

data = []
fd = open('table_country.txt','r')

for line in fd:
     line = line[line.index('(')+1:line.rindex(')')]
     datacountry = line.split(',')
     
     Code = str(datacountry[0]).strip('\'')
     Name = str(datacountry[1]).strip('\'')
     Continent = str(datacountry[2]).strip('\'')
     Region = str(datacountry[3]).strip('\'')
     SurfaceArea = str(datacountry[4]).strip('\'')
     if datacountry[5] == 'NULL':
         IndepYear = None
     else:
         IndepYear = int(datacountry[5])
     Population = int(datacountry[6])
     if datacountry[7] == 'NULL':
         LifeExpectancy = None
     else:
         LifeExpectancy = float(datacountry[7])
     if datacountry[8] == 'NULL':
         GNP = None
     else:
         GNP = float(datacountry[8])
     if datacountry[9] == 'NULL':
         GNPOld = None
     else:
         GNPOld = float(datacountry[9])
     LocalName = str(datacountry[10]).strip('\'')
     GovernmentForm = str(datacountry[11]).strip('\'')
     HeadOfState = str(datacountry[12]).strip('\'')
     if datacountry[9] == 'NULL':
         Capital = None
     else:
         Capital = int(datacountry[13])
     Code2 = str(datacountry[14]).strip('\'')
     
     data.append([Code,Name,Continent,Region,SurfaceArea,IndepYear,Population,LifeExpectancy,GNP,GNPOld,LocalName,GovernmentForm,HeadOfState,Capital,Code2])  
  
#inserting the data one row by one     
for row in data:  
    curs.execute('insert into Country values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', row)


""" If I want to print
curs.execute('select * from Country')
row = curs.fetchall()
print(row)
"""

data = []
fd = open('table_country_language.txt','r')

for line in fd:
     line = line[line.index('(')+1:line.rindex(')')]
     datalanguage = line.split(',')
     
     CountryCode = str(datalanguage[0]).strip('\'')
     Language = str(datalanguage[1]).strip('\'')
     IsOfficial = str(datalanguage[2]).strip('\'')
     Percentage = float(datalanguage[3])
     data.append([CountryCode,Language,IsOfficial,Percentage])
     
#other way to insert with .executemany doing it 
curs.executemany('insert into CountryLanguage values(?,?,?,?)', data)     
print("Elements in table CountryLanguage:",curs.rowcount)

con.commit() #**** Important to make the records visibles from others databases connections.

""" If I want to print
curs.execute('select * from CountryLanguage')
row = curs.fetchall()
print(row)
"""
        




