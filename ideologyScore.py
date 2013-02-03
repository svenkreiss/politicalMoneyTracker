#!/usr/bin/env python

#  Created on: February 2, 2013

__author__ = "Sven Kreiss <sk@svenkreiss.com>"
__version__ = "0.1"


import csv

ideologyScore = {}

def getIS( comId ):
   if comId in ideologyScore:
      return ideologyScore[comId]
   else:
      #print( "WARNING: ideology score for "+comId+" not found. Setting to 0.0." )
      return (0.0,0.0)

def readCSVFile( filename ):
   with open(filename, 'rb') as csvfile:
      reader = csv.reader(csvfile)
      next(reader) # skips header
      for row in reader:
         print( row )
         if len(row) > 10 and row[8]:
            ideologyScore[ row[8] ] = ( float(row[9]), float(row[10]) )

def __init__():
   print( "Initializing ideology score ... " )

   readCSVFile( "HouseTable.csv" )
   readCSVFile( "SenateTable.csv" )
      
   print( "Done getting ideology score." )

__init__()
