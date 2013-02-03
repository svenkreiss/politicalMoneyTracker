#!/usr/bin/env python

#  Created on: February 2, 2013

__author__ = "Sven Kreiss <sk@svenkreiss.com>"
__version__ = "0.1"



import optparse
parser = optparse.OptionParser(version="0.1")
parser.add_option("-i", "--input", help="input files", type="string", dest="input",
                  default="/scratch/sk3253/bicoastaldatafest/bulkdata_influenceexplorer/contributions.fec.2012.csv")
parser.add_option("-o", "--output", help="output", type="string", dest="output", default="test.csv")
parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, 
                  help="Quiet output.")
(options, args) = parser.parse_args()


import csv

import numpy


import zipcode
# print( zipcode.zipcode )

import ideologyScore
# print( ideologyScore.ideologyScore )
# print( len(ideologyScore.ideologyScore) )


def main():
   filename = options.input.replace(".zip","")[options.input.rfind("/")+1:]
   if ".zip" in options.input:
      f = zipfile.ZipFile( options.input, "r" ).open( filename, "r" )
   else:
      f = open( options.input, "r" )
   print( f )
   lineCount = 0
   zipCodes = {}
   
   with open(options.input, 'rb') as csvfile:
      reader = csv.reader(csvfile)
      next(reader) # skips header
      for row in reader:
         lineCount += 1

         #print( "amount=$%.0f \t zip=%s \t committee_ext_id=%s" % (float(row[8]),row[19],row[33]) )
         
         # filter by transaction type: 15=contribution, 
         if row[5] not in [15]: continue

         zc = row[19]
         if zc == "": zc = "00000"
         
         if zc in zipCodes:
            # do not include refunds
            if float(row[8]) > 0.0 and float(row[8])+zipCodes[ zc ]["amount"] > 0.0:
               if zipCodes[ zc ]["amount"]+float(row[8]) == 0.0:
                  print( "WTF?? "+str(zipCodes[ zc ]["amount"])+", "+str(float(row[8])) )
               weight = float(row[8]) / (zipCodes[ zc ]["amount"]+float(row[8]))
               zipCodes[ zc ]["ideologyScore"] = (1.-weight)*zipCodes[ zc ]["ideologyScore"]  +  weight*ideologyScore.getIS(row[33])[0]
               
            # include refunds
            zipCodes[ zc ]["amount"] += float(row[8])

         else:
            zipCodes[ zc ] = { "amount":float(row[8]), "ideologyScore":ideologyScore.getIS(row[33])[0] }

         if options.verbose:            
            if zc == "00000":
               print( "" )
               print( row )
               print( "city: "+row[17]+", "+row[18] )
   
   zipLatLonInfo = [ (zc,zipcode.zipcode[zc],info) for zc,info in zipCodes.iteritems() if zc in zipcode.zipcode ]
   if options.verbose: print( zipLatLonInfo )
      
   sum = 0.0
   for zc,latLon,info in zipLatLonInfo:
      if zc: sum += info["amount"]
   print( "Amount with zipcode: $"+str(sum) )
   
   
   fOut = open( options.output, "w" )
   fOut.write( "lat,lon,amount,ideologyScore\n" )
   for zc,latLon,info in zipLatLonInfo:
      fOut.write( str(latLon[0])+","+str(latLon[1])+","+str(info["amount"])+","+str(info["ideologyScore"])+"\n" )
   fOut.close()

   print( "Processsed %d records." % lineCount )

   return

if __name__ == "__main__":
   main()
   
   

