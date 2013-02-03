#!/usr/bin/env python

#  Created on: February 2, 2013

__author__ = "Sven Kreiss <sk@svenkreiss.com>"
__version__ = "0.1"



import optparse
parser = optparse.OptionParser(version="0.1")
parser.add_option("-i", "--input", help="input files", type="string", dest="input",
                  default="/scratch/sk3253/bicoastaldatafest/bulkdata_influenceexplorer/contributions.fec.2012.csv")
parser.add_option("-o", "--output", help="output", type="string", dest="output", default="pacIdeology.csv")
parser.add_option("-q", "--quiet", dest="verbose", action="store_false", default=True, 
                  help="Quiet output.")
(options, args) = parser.parse_args()


import csv


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
   
   pacIdeology = {}

   with open(options.input, 'rb') as csvfile:
      reader = csv.reader(csvfile)
      next(reader) # skips header
      for row in reader:
         #print( "amount=$%.0f \t zip=%s \t committee_ext_id=%s" % (float(row[8]),row[19],row[33]) )

         # contributor_type=C
         if row[12] != "C": continue
         
         # recipient_type=P
         if row[28] != "P": continue

         

         # filter by transaction type: 15=contribution, 17Z=refund from candidate and committee, 22Y=refund to individual
         if row[5] not in ["15","24a","24e"]: continue
         
         score = ideologyScore.getIS(row[33])[0]
         # flip sign for contributions made "against"
         if row[5] in ["24a"]: score *= -1.0

         # contributor_ext_id
         pacCode = row[11]

         # prepare entry in result
         if pacCode not in pacIdeology: pacIdeology[ pacCode ] = {
            "amount":0.0,
            "ideologyScore":0.0,
         }


         # do not include refunds
         if float(row[8]) > 0.0:
            if pacIdeology[ pacCode ]["amount"]+float(row[8]) == 0.0:
               print( "WTF?? "+str(pacIdeology[ pacCode ]["amount"])+", "+str(float(row[8])) )
            weight = float(row[8]) / (pacIdeology[ pacCode ]["amount"]+float(row[8]))
            pacIdeology[ pacCode ]["ideologyScore"] = (1.-weight)*pacIdeology[ pacCode ]["ideologyScore"]  +  weight*score
            
            pacIdeology[ pacCode ]["amount"] += float(row[8])
            
   
   fOut = open( options.output, "w" )
   fOut.write( "pacCode,ideologyScore\n" )
   for pacCode,info in pacIdeology.iteritems():
      fOut.write( str(pacCode)+","+str(info["ideologyScore"])+"\n" )
   fOut.close()

   return


if __name__ == "__main__":
   main()
   
   

