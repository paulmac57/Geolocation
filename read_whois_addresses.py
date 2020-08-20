# Reads RIPE file ripe.db.organisation and writes records to SQL database
import requests
import re

import subprocess
import os

import time
import sys

import mysql.connector
import whois
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

def sql_write(record_id,record):
    #print (record_id)
    print (record['organisation'])
    print (record['org_name'])
    #print (imp6)
    #time.sleep(5)
    

    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="ripe"
            )
    cursor = mydb.cursor()
    sql = "INSERT INTO asorganisations(organisation, org_name, org_type, created,modified,source) VALUES ( %s, %s, %s, %s,%s, %s);"
    val = (record['organisation'], record['org_name'], record['org_type'], record['created'], record['modified'], record['source'] )
    
    cursor.execute(sql,val)
    mydb.commit()
    
    record = {}
    
def main():
       
    fields = ('organisation', 'org_name', 'org_type','created','modified','source')
    record = {}
    record_id = 0
    last_record_id = 0

    record['organisation']  = ""
    record['org_name']  = ""
    record['org_type'] =  ""
    record['modified'] = ""
    record['source'] = ""
    
    with open("../files/ripe.db.organisation", "r", encoding="ISO-8859-1") as myfile:
        
        
        for line in myfile:
        
            #print (line)
            #time.sleep(2)
            #if line.split(":")[0][0] == "%" or line.split(":")[0][0] == "#" or line.split(":")[0][0] == "\n" or line.split(":")[0][0] == " "  or line.split(":")[0][0] == "+":
                #continue
            if line.split(":")[0] == "organisation":
                #if record_id != 0:
                #    sql_write(record_id,record,desc,imp4,exp4,imp6,exp6)
                #print (record_id)
                record['organisation'] = line.split(":")[1].strip()
                
                continue
            if line.split(":")[0] == "org-name":
                record['org_name'] = line.split(":")[1].strip()
                continue
            if line.split(":")[0] == "org-type":
                record['org_type'] = line.split(":")[1].strip()
                continue

            if line.split(":")[0] == "created":
                dat = line.split("created:")[1].split("T")[0].strip()
                tim = line.split("created:")[1].split("T")[1].split("Z")[0].strip()
                record['created'] = dat + " " + tim
                continue
            if line.split(":")[0] == "modified" or line.split(":")[0] == "last-modified":
                dat = line.split("modified:")[1].split("T")[0].strip()
                tim = line.split("modified:")[1].split("T")[1].split("Z")[0].strip()
                
                record['modified'] = dat + " " + tim
                continue
            if line.split(":")[0] == "source" :
                record['source'] = line.split(":")[1].strip()
                continue
            if line == "\n" :
                #skip first record as its just remarks
                record_id = record_id +1 
                if record_id == 1:
                    continue
                print (record_id)
                #print (record)
                #time.sleep(5)
                sql_write(record_id,record)

                record['organisation']  = ""
                record['org_name']  = ""
                record['org_type'] =  ""
                record['created']  = ""
                record['modified'] = ""
                record['source'] = ""
                continue

            #TODO : Ignore anything else for now 
            if line.split(":")[0] == "remarks":
                continue
            # Address is only a dummy address, need to get proper one from whois
            if line.split(":")[0] == "address":
                continue
            if line.split(":")[0] == "e-mail":
                continue
            if line.split(":")[0] == "admin-c":
                continue
            if line.split(":")[0] == "tech-c":
                continue

            if line.split(":")[0] == "mnt-by":
                continue
            if line.split(":")[0] == "mnt-ref":
                continue
            if line.split(":")[0] == "abuse-c":
                continue
            if line.split(":")[0] == "member-of":
                continue
            if line.split(":")[0] == "abuse-c":
                continue
            if line == "":
                print ("this one got through ", line.split(":")[0])
                time.sleep(5)
    sql_write(record_id,record)


            


    '''
    if record:
        # handle last record
        writer.writerow(record)
    '''

    

if __name__ == "__main__":
    #for id in range(2,126618)
    org = sql_read(2)[0]
    print ("ORG IS ",org)
    #org = "ORG-BPIS1-RIPE"
    bt = "whois -Br --sources RIPE ORG-BPIS1-RIPE"
    address = []
    info = os.popen(bt).read()
    #print ("this is it ",info)
    i = len(info.split("address:"))
    
    for add in range(1,i):
        address.append(info.split("address:")[add].split("\n")[0].strip())  
        print ( "Address is ",add-1,address[add-1].strip())
    

