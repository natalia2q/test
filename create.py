# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 18:25:22 2016
@author: Natalia Dosque ndosquec
"""

import sqlite3

con = sqlite3.connect('dbworld')   # Connexion could be in memory :memory:

curs = con.cursor()

tcity = """
CREATE TABLE IF NOT EXISTS City (
  ID INTEGER,
  Name VARCHAR(35),
  CountryCode VARCHAR(3),
  District VARCHAR(20),
  Population INTEGER,
  PRIMARY KEY  (ID)
);
"""
curs.execute(tcity)

tcountry = """
CREATE TABLE IF NOT EXISTS Country (
  Code VARCHAR(3) ,
  Name VARCHAR(52) ,
  Continent VARCHAR(30),
  Region VARCHAR(26) ,
  SurfaceArea REAL ,
  IndepYear INTEGER,
  Population INTEGER,
  LifeExpectancy REAL,
  GNP REAL,
  GNPOld REAL,
  LocalName VARCHAR(45),
  GovernmentForm VARCHAR(45),
  HeadOfState VARCHAR(60),
  Capital INTEGER,
  Code2 VARCHAR(2),
  PRIMARY KEY  (Code)
) ;"""

curs.execute(tcountry)

tcolang = """
CREATE TABLE IF NOT EXISTS CountryLanguage (
  CountryCode VARCHAR(3),
  Language VARCHAR(30),
  IsOfficial VARCHAR(1), 
  Percentage REAL
  
) ;"""

curs.execute(tcolang)
con.commit()