# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 18:36:30 2016
@author: Natalia Dosque ndosquec
"""
import sqlite3

con = sqlite3.connect('dbworld')  
curs = con.cursor()

country = ''
countries = []
mainMenu = """
***Enter an option:
(1) Country Data 
(2) City Data 
(3) Update Country Data 
(4) Compare Two Countries 
(5) General Stats
(z) Rollback 
(x) Exit
->"""
updateMenu = """
***Enter column number to update:
(1) Name 
(2) Surface Area 
(3) Population 
(4) Government Form 
(5) Head of state
(6) Return to Main Menu
->"""
statsMenu = """
***Enter an option:
(1) Top 10 spoken languages
(2) Top 10 countries with highest life expectancy
(3) Average life expectancy by Continent
(4) Top 10 countries with lowest life expectancy
(5) Top 10 most populous countries
(6) Top 10 most populous cities
(7) Top 10 countries with highest Gross National Product(GNP)
(8) Return to Main Menu
->"""
tempCountryData ="""    
Code            : {}
Name            : {}
Continent       : {}
Region          : {}
Surface Area    : {:,} Km2
Population      : {:,}
Government Form : {}
Head Of State   : {} """


#print all the rows in the table Country
#curs.execute('select * from Country')
#print(curs.fetchall())

def FindTheCountry(country):
    query = "SELECT count(1) from country where name = ?"
    curs.execute(query,[country])
    return curs.fetchone()[0]

def SelectCountry():
    global country
    country = input("Enter a country: ").strip()    
    while FindTheCountry(country) == 0: 
        print("Country no found!")
        country = input("Enter a country: ").strip()
    return True

def optionToColumn(option):
    options = {1:'Name', 2: 'SurfaceArea',3:'Population',4:'GovernmentForm',5:'HeadOfState'}
    return options[int(option)]

def Select2Country():
    global countries
    prompt = "Enter two countries to compare in this format country1,country2 -> "
    countries = input(prompt).strip().split(',')    
    
    while FindTheCountry(str(countries[0]).strip()) == 0:
        print("First country no found!")
        countries = input(prompt).strip().split(',')
        
    while FindTheCountry(str(countries[1]).strip()) == 0:
        print("Second country no found!")
        countries = input(prompt).strip().split(',')
    return True
    

while True:

    option= input(mainMenu).strip()   
    
    if option == 'x':                                #***************Exit
        con.commit()  
        con.close()
        del con                          
        break
    
    elif option == 'z':                            #***************Rollback
        con.rollback()
        pass
               
    if option == '1' and SelectCountry() is True:  #****************Country Data
        
        query = """
        SELECT co.Code, co.Name, co.Continent, co.Region, co.SurfaceArea, co.Population, co.GovernmentForm, co.HeadOfState
        FROM Country co
        WHERE co.Name = ?"""

        curs.execute(query,[country])
        Code,Name,Continent,Region,SurfaceArea,Population,GovernmentForm,HeadOfState = curs.fetchone()
        print(tempCountryData.format(Code,Name,Continent,Region,SurfaceArea,Population,GovernmentForm,HeadOfState))
                  
    elif option == '2' and SelectCountry() is True:  #***************Cities Data
        
        temp_head = "{:4s} {:30s} {:6s} {:20s} {:9s}"
        print(temp_head.format('ID','Name','C Code','District','Population'))
        print('-'*75)

        query = """
        SELECT ci.ID,ci.Name,ci.CountryCode,ci.District,ci.Population 
        FROM Country co
        JOIN City ci ON co.Code = ci.CountryCode
        WHERE co.Name = ?"""

        curs.execute(query,[country])
        temp_body = "{:4d} {:30s} {:6s} {:20s} {:>9,}"
        for ID,Name,CountryCode,District,Population in curs.fetchall():
            print(temp_body.format(ID,Name,CountryCode,District,Population))
    
    elif option == '3' and SelectCountry() is True:  #***************Update Country Data
        optionUpdate = '0'
        while optionUpdate not in ['1','2','3','4','5','6']:  #select a valid option
            optionUpdate = input(updateMenu).strip()  
        
        if optionUpdate not in '6':   #case is not return
            newValue = input("Enter New Value:").strip()
            query = """
            UPDATE Country
            SET """+optionToColumn(optionUpdate)+ """= ?
            WHERE name = ?"""
           
            curs.execute(query,[newValue,country])
            print("Updated!")
        #con.commit()
    
    elif option == '4' and Select2Country() is True:    #***************Compare two Countries
        
        query = """
        SELECT  co.Name, co.Code, co.Continent, co.SurfaceArea, co.Population, co.IndepYear, co.LifeExpectancy, co.GNP, Co.GovernmentForm, co.HeadOfState
        FROM Country co
        WHERE co.Name = ? or co.Name = ?"""

        curs.execute(query,[countries[0].strip(),countries[1].strip()])
        country1 = curs.fetchone()
        country2 = curs.fetchone()

        i = 0
        for line in open('tempCountriesData.txt','r'):
            line = line.strip()
            if line.startswith('-') is False:
                print(line.format(country1[i],country2[i]))
                i += 1
            else:
                print(line)
                
    elif option == '5':                                #***************Generar Stats
        optionStats = '0'
        while optionStats not in ['1','2','3','4','5','6','7','8']:  #select a valid option
            optionStats = input(statsMenu).strip()  
            
        if optionStats not in '8':
            
            if optionStats == '1':
                temp = "{:4s} {:12s} {:15s}"
                print(temp.format("Rank", "Language","Population"))               
                print('-'*35)
                
                query = """
                SELECT l.language, round(sum(co.population * (l.percentage/100))) population
                FROM CountryLanguage l
                join Country co on l.CountryCode = co.code
                group by l.language
                order by sum(co.population * (l.percentage/100)) DESC Limit 10"""
                curs.execute(query)
            
                temp = "{:>4d} {:12s} {:,}"
                i = 1
                for x,y in curs.fetchall():
                    print(temp.format(i,x,int(y)))
                    i += 1
       
            
            if optionStats == '2':
                temp = "{:4s} {:12s} {:25s} {}"
                print(temp.format("Rank","Country", "Region","Life Expectancy"))               
                print('-'*60)
                
                query = """
                SELECT Name, Region, LifeExpectancy
                FROM Country
                order by LifeExpectancy DESC Limit 10"""
                curs.execute(query)
            
                temp = "{:>4d} {:12s} {:25s} {:4d} years"
                i = 1
                for x,y,z in curs.fetchall():
                    print(temp.format(i,x,y,int(z)))
                    i += 1
                    
            if optionStats == '3':
                temp = "{:4s} {:17s} {:15s}"
                print(temp.format("Rank", "Continent","Life Expectancy Avg."))               
                print('-'*42)
                
                query = """
                SELECT Continent, avg(LifeExpectancy)
                FROM Country
                WHERE LifeExpectancy is not null
                GROUP BY Continent
                ORDER BY avg(LifeExpectancy) DESC"""
                curs.execute(query)
            
                temp = "{:>4d} {:17s} {:^20}"
                i = 1
                for x,y in curs.fetchall():
                    print(temp.format(i,x,int(y)))
                    i += 1
            
            if optionStats == '4':
                temp = "{:4s} {:12s} {:25s} {}"
                print(temp.format("Rank","Country", "Region","Life Expectancy"))               
                print('-'*60)
                
                query = """
                SELECT  Name, Region, LifeExpectancy
                FROM Country
                where LifeExpectancy is not null
                order by LifeExpectancy ASC Limit 10"""
                curs.execute(query)
            
                temp = "{:>4d} {:12s} {:25s} {:4d} years"
                i = 1
                for x,y,z in curs.fetchall():
                    print(temp.format(i,x,y,int(z)))
                    i += 1
                    
            if optionStats == '5':
                temp = "{:4s} {:18s} {:26s} {}"
                print(temp.format("Rank","Country", "Region","Population"))               
                print('-'*65)
                
                query = """
                SELECT Name, Region, population
                FROM Country
                order by population DESC Limit 10"""
                curs.execute(query)
            
                temp = "{:>4d} {:18s} {:26s} {:,} "
                i = 1
                for x,y,z in curs.fetchall():
                    print(temp.format(i,x,y,int(z)))
                    i += 1
            
            if optionStats == '6':
                temp = "{:4s} {:18s} {:17s} {:11} {}"
                print(temp.format("Rank","Country", "City","Population","Life Expectancy"))               
                print('-'*72)
                
                query = """
                SELECT co.Name Country, ci.Name City, ci.population, co.lifeExpectancy
                FROM Country co
                join City ci on ci.countrycode = co.code
                where LifeExpectancy is not null
                order by ci.population DESC Limit 10"""
                curs.execute(query)
            
                temp = "{:>4d} {:18s} {:17s} {:>10,} {:>7d} years "
                i = 1
                for x,y,z,a in curs.fetchall():
                    print(temp.format(i,x,y,int(z),int(a)))
                    i += 1
            
            if optionStats == '7':
                temp = "{:4s} {:15s} {:15s} {:11} {:11} {}"
                print(temp.format("Rank","Country", "Region","Current GNP","Last GNP", "GNP Difference"))               
                print('-'*75)
                
                query = """
                SELECT Name, Region, GNP 'Current GNP',GNPOld 'Last GNP', GNP-GNPOld Growth
                FROM Country
                order by GNP DESC Limit 10"""
                curs.execute(query)
            
                temp = "{:>4d} {:15s} {:15s} {:>10,} {:>10,} {:>10,} "
                i = 1
                for x,y,z,a,b in curs.fetchall():
                    print(temp.format(i,x,y,int(z),int(a),int(b)))
                    i += 1
                
             
            
            
