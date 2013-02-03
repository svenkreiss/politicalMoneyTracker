#!/usr/bin/env python

#  Created on: February 2, 2013

__author__ = "Sven Kreiss <sk@svenkreiss.com>"
__version__ = "0.1"


import csv

zipcode = {}

def __init__():
   print( "Initializing zipcodes ... " )

   with open("zipcode.csv", 'rb') as csvfile:
      reader = csv.reader(csvfile)
      next(reader) # skips header
      for row in reader:
         #print( row )
         if len(row) > 3:
            zipcode[ row[0] ] = ( float(row[3]), float(row[4]) )
         
      
   print( "Done getting zipcodes." )


__init__()

