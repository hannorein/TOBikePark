
import os
import urllib2
import urllib
import time
import xml.etree.ElementTree as ET
for fi in range(1,4):
    it = 0
    with open("Parking_Tags_Data_2015_%d.csv"%fi,"r") as f:
        for r in f:
            c = r.split(",")
            if c[3] == "STOP VEH OTR THN BCYCL-BYCL LN":
                ad = c[7]
                found = 0
                with open("locations.txt","r") as fl:
                    for ll in fl:
                        cl = ll.split(",")
                        if cl[0]==ad:
                            found = 1
                            break
                if found == 0:
                    time.sleep(0.2)
                    uad = urllib.urlencode({"address": ad+", Toronto"})
                    url = "http://maps.google.com/maps/api/geocode/xml?"+uad
                    response = urllib2.urlopen(url)
                    html = response.read()
                    root = ET.fromstring(html)
                    stars = root.findall(".//location/lat")
                    if len(stars)>0:
                       lat = float(stars[0].text)
                    stars = root.findall(".//location/lng")
                    if len(stars)>0:
                       lng = float(stars[0].text)
                    with open("locations.txt","a+") as fl:
                        print lat, lng
                        fl.write(ad+",%.9f,%.9f\n"%(lat,lng))
                it +=1 


for fi in range(0,4):
    with open("card%02d.kml"%fi,"w") as of:
        of.write( """
    <?xml version="1.0" encoding="UTF-8"?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document>
    """)
        chunk = 2000
        it = 0
        for i in range(1,4):
            with open("Parking_Tags_Data_2015_%d.csv"%i,"r") as f:
                for r in f:
                    c = r.split(",")
                    if c[3] == "STOP VEH OTR THN BCYCL-BYCL LN":
                        ad = c[7]
                        with open("locations.txt","r") as fl:
                            for ll in fl:
                                cl = ll.strip().split(",")
                                if cl[0]==ad:
                                    if it>=chunk*fi and it <chunk*(fi+1):
                                        date = c[1][0:4]+"/"+c[1][4:6]+"/"+c[1][6:8]
                                        if it==chunk*fi:
                                            print date
                                        of.write("""
                                        <Placemark>
                                        <name>""" + cl[0].title() + """</name>
                                        <description>Car in Bike Lane on """+date+"""</description>
                                        <Point>
                                        <coordinates>""" +cl[2]+","+cl[1]+"""</coordinates>
                                        </Point>
                                        </Placemark>
                                        """)
                                    it +=1


        of.write("""
        </Document>
        </kml>
        """
        )
    print it
