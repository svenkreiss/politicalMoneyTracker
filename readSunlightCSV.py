#!/usr/bin/env python

#  Created on: February 2, 2013

__author__ = "Sven Kreiss <sk@svenkreiss.com>"
__version__ = "0.1"



import optparse
parser = optparse.OptionParser(version="0.1")
parser.add_option("-i", "--input", help="input files", type="string", dest="input",
                  default="/scratch/sk3253/bicoastaldatafest/bulkdata_influenceexplorer/contributions.fec.2012.csv")
parser.add_option("-o", "--output", help="output", type="string", dest="output", default="test.csv")
parser.add_option(      "--ideologyDistribution", help="output", type="string", dest="ideologyDistributionOutput", default="ideologyDistribution.csv")
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
   
   ideologyDistribution = numpy.zeros( 1000 )
   ideologyDistributionId = numpy.linspace( -1,1,1000 )
   
   with open(options.input, 'rb') as csvfile:
      reader = csv.reader(csvfile)
      next(reader) # skips header
      for row in reader:
         lineCount += 1

         #print( "amount=$%.0f \t zip=%s \t committee_ext_id=%s" % (float(row[8]),row[19],row[33]) )
         
         # contributor type I
         if row[12] != "I": continue
         
         # filter by transaction type: 15=contribution, 22Y=refund to individual
         if row[5] not in ["15","22Y"]: continue

         zc = row[19]
         if zc == "": zc = "00000"
         
         # prepare entry in result
         if zc not in zipCodes: zipCodes[ zc ] = {
            "amount":0.0,
            "ideologyScore":0.0,
            "plot1":0.0,
            "plot2":0.0,
            "plot3":0.0,
            "plot4_M":0.0,
            "plot4_F":0.0,
            "plot4_FM":0.0,
            "plot10":0.0,
            "plot10_amount":0.0,
         }


         # do not include refunds
         if float(row[8]) > 0.0 and float(row[8])+zipCodes[ zc ]["amount"] > 0.0:
            if zipCodes[ zc ]["amount"]+float(row[8]) == 0.0:
               print( "WTF?? "+str(zipCodes[ zc ]["amount"])+", "+str(float(row[8])) )
            weight = float(row[8]) / (zipCodes[ zc ]["amount"]+float(row[8]))
            zipCodes[ zc ]["ideologyScore"] = (1.-weight)*zipCodes[ zc ]["ideologyScore"]  +  weight*ideologyScore.getIS(row[33])[0]
            
            # ideologyDistribution entry number in array
            idEntry = int(  (ideologyScore.getIS(row[33])[0]+1.0)/2.0  *  len(ideologyDistribution)  )
            ideologyDistribution[ idEntry ] += float(row[8])
            
            # include refunds
            zipCodes[ zc ]["amount"] += float(row[8])
            
            #print( row[28]+","+row[38] )
            
            ### Plots
            # 1)
            # recipient_type=O,P; seat=federal:senate,federal:house,federal:president
            if row[28] in ["C","O","P"] and row[38] in ["federal:senate","federal:house","federal:president"]:
               zipCodes[ zc ]["plot1"] += 1.0

            # 2)
            # recipient_type=O,P; seat=federal:senate,federal:house,federal:president
            if row[28] in ["C","O","P"] and row[38] in ["federal:senate","federal:house","federal:president"]:
               zipCodes[ zc ]["plot2"] += float(row[8])
#                
#             # 2)
#             # recipient_type=O,P; seat=federal:senate,federal:house,federal:president
#             if row[28] in ["C","O","P"] and row[38] in ["federal:senate","federal:house","federal:president"]:
#                weight = float(row[8]) / (zipCodes[ zc ]["plot2"]+float(row[8]))
#                zipCodes[ zc ]["plot2"] = (1.-weight)*zipCodes[ zc ]["plot2"]  +  weight*ideologyScore.getIS(row[33])[0]
# 
            # 3)
            # recipient_type=O
            if row[28] in ["C","O"]:
               zipCodes[ zc ]["plot3"] += 1.0
                
            # 4)
            # recipient_type=O
            if row[28] in ["C","O"]:
               if row[15] == "M": zipCodes[ zc ]["plot4_M"] += 1.0
               elif row[15] == "F": zipCodes[ zc ]["plot4_F"] += 1.0
               else: zipCodes[ zc ]["plot4_FM"] += 1.0
               
            # 10)
            # recipient_type=P; seat=federal:senate,federal:house
            if row[28] in ["P"] and row[38] in ["federal:senate","federal:house"]:
               weight = float(row[8]) / (zipCodes[ zc ]["plot10_amount"]+float(row[8]))
               zipCodes[ zc ]["plot10"] = (1.-weight)*zipCodes[ zc ]["plot10"]  +  weight*ideologyScore.getIS(row[33])[0]
               zipCodes[ zc ]["plot10_amount"] += float(row[8])
               #print( str(zipCodes[ zc ]["plot10"])+","+str(zipCodes[ zc ]["plot10_amount"]) )


         if options.verbose:            
            if zc == "00000":
               print( "" )
               print( row )
               print( "city: "+row[17]+", "+row[18] )
   
   zipLatLonInfo = [ (zc,zipcode.zipcode[zc],info) for zc,info in zipCodes.iteritems() if zc in zipcode.zipcode ]
   if options.verbose: print( zipLatLonInfo )
      
   sum = 0.0
   sumWithZipCodes = 0.0
   for zc,latLon,info in zipLatLonInfo:
      sum += info["amount"]
      if zc: sumWithZipCodes += info["amount"]
   print( "Amount with valid zipcodes: $%.2fB out of $%.2fB." % (sumWithZipCodes/1000000000,sum/1000000000) )
   
   
   infoKeys = sorted( zipLatLonInfo[0][2].keys() )
   fOut = open( options.output, "w" )
   fOut.write( "lat,lon," )
   fOut.write( ",".join(infoKeys)+"\n" )
   for zc,latLon,info in zipLatLonInfo:
      fOut.write( str(latLon[0])+","+str(latLon[1]) )
      for ik in infoKeys: fOut.write( ","+str(info[ik]) )
      fOut.write( "\n" )
   fOut.close()

   for iK in infoKeys:
      if "_amount" in iK: continue
      fOut = open( options.output.replace(".csv",iK+".csv"), "w" )
      fOut.write( "lat,lon,"+iK )
      if iK+"_amount" in infoKeys:
         fOut.write( ","+iK+"_amount" )
      fOut.write( "\n" )
      for zc,latLon,info in zipLatLonInfo:
         if info[ik] != 0.0:
            fOut.write( str(latLon[0])+","+str(latLon[1])+","+str(info[ik]) )
            if iK+"_amount" in infoKeys:
               fOut.write( ","+str( info[iK+"_amount"] ) )
            fOut.write( "\n" )
            if iK == "plot10":
               print( str(info[iK])+","+str(info[iK+"_amount"]) )
      fOut.close()

   # write ideologyDistribution
   fOut = open( options.ideologyDistributionOutput, "w" )
   fOut.write( "ideologyScore,amount\n" )
   for id,amount in zip(ideologyDistributionId,ideologyDistribution):
      fOut.write( str(id)+","+str(amount)+"\n" )
   fOut.close()


   print( "Processsed %d records." % lineCount )

   return

if __name__ == "__main__":
   main()
   
   

