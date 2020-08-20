import requests
import re

import os

import time
import sys
from geopy.geocoders import Nominatim
import mysql.connector

def main():
    desc = []
    imp4 = []
    exp4 = []
    imp6 = []
    exp6 = []
    
    fields = ('asn', 'asname', 'org',desc, imp4, exp4, imp6, exp6, 'created','modified','source')
    record = []
    record_id = 0
    last_record_id = 0

    with open("../files/ripe.db.aut-num", "r") as myfile:
        value = ""
        try:
            for line in myfile:
                
                    #time.sleep(2)
                    value = line.split(":")[0]
                    print (value)
                    
                    if value[0] == "%" or value[0] == "#" or value[0] == "\n":
                        continue
                    if value not in record:
                        record.append(line.split(":")[0])
                        print (record)
                        time.sleep(2)
        except UnicodeDecodeError:
                print ("BAH")
                           
       
        
    

if __name__ == "__main__":
    main()