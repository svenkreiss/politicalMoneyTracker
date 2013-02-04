> This project is our team's entry for the [Bicoastal Datafest](http://www.bdatafest.computationalreporting.com). We had a great time working on this together in Columbia's School of Journalism. Thanks to all the organizers. All results were prepared in one weekend. Our project is documented on the [Bicoastel Datafest's Project Page](http://www.bdatafest.computationalreporting.com/distribitionpacs).

How do small and large donors contribute to candidate and interest group PACs; what is their ideology? Election campaigns and interest groups pour over their donor data, yet there is little public analysis of donor trends beyond the big donors and aggregates. Who are the millions of people donating; where do they live; how much do they donate; where do they fall on the political spectrum?  Find out in this heat map of political donors to the presidency, Senate and House races of 2012. 


# Team Members

* Michael Schwam-Baird, PhD Candidate Political Science, Columbia University 
* Jess Duda, freelance web producer for PBS Interactive
* [Sven Kreiss](http://www.svenkreiss.com), PhD Candidate, Particle Physics, New York University
* Ray Schwartz, Librarian, William Paterson University


# Project Idea

Ideology scores are DW-Nominate scores from congressional roll call votes developed by Poole and Rosenthal (1997) and available for all Congresses at [voteview.com](http://www.voteview.com).  DW-Nominate scores range from -1 (most liberal) to +1 (most conservative).  We used the 112th Congress scores and matched each House member and Senator to their score. We found that the amount of money donated is distributed over ideology as shown in this piture:<br />
![ideologyDistribution](http://www.bdatafest.computationalreporting.com/_/rsrc/1359920658926/distribitionpacs/Ideology%20Dist%20Few%20Bins.jpg)

Donations to members of Congress were then assigned the ideology score of their recipient.  The ideology of a particular zip code is then the dollar-weighted average of the ideology of the donations from that zip code.



# Proof-of-Concept

The map below shows all transactions from the [Inference Explorer's bulk data](http://data.influenceexplorer.com/bulk/) by zip code. The size of the circle corresponds to the size of the transaction and the color corresponds to the ideology score.

[![testMap](http://a.tiles.mapbox.com/v3/svenkreiss.test/-99.76,39.91000000000001,3/640x480.png)](http://tiles.mapbox.com/svenkreiss/map/test)
