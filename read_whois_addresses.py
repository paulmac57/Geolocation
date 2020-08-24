# Reads SQL organisations, executes a whois cmd and writes address to SQL database linked to as organisation
import requests
import re

import subprocess
import os

from ipwhois import IPWhois
import time
import sys

import mysql.connector

def sql_read(id):
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="ripe"
            )
    cursor = mydb.cursor(buffered=True)
    sql = "select organisation from asorganisations where id = %s;"
    val = (id,)
    cursor.execute(sql,val)
    record = cursor.fetchone()
    #print ( "organisation is ",record)
    return record


    

if __name__ == "__main__":
    
   
    for id in range(2,126618):
        org = sql_read(id)[0]
        #print ("ORG IS ",org)
        #org = "ORG-BPIS1-RIPE"
        cmd = "whois -Br --sources RIPE "+org + " > temp.txt"
        address = []
        info = os.system(cmd)
        #print ("this is it ",info)
        with open("temp.txt", "r", encoding="ISO-8859-1") as myfile:

            for line in myfile:
                if line.split(":")[0] == "address":
                    address = line.split("address:")[1].split("\n")[0].strip() 
                    #print ( "Address is ",address)
                    #print ("org is ",org)
                    #time.sleep(2)
                    sql_address_write(address,org)
 