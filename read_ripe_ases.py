# Reads RIPE file ripe.db.aut-num and writes records to SQL database
import requests
import re

import os

import time
import sys

import mysql.connector
def sql_write(record_id,record,desc,imp4,exp4,imp6,exp6):
    print (record_id)
    print (record['asn'])
    #print (imp6)
    #time.sleep(5)
    

    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="ripe"
            )
    cursor = mydb.cursor()
    sql = "INSERT INTO ases(asn, asname, org, created,modified,source, default4, default6) VALUES (%s, %s, %s, %s, %s, %s,%s, %s);"
    val = (record['asn'], record['asname'], record['org'], record['created'], record['modified'], record['source'], record['default4'], record['default6'] )
    
    cursor.execute(sql,val)
    mydb.commit()
    
    for d in desc:
        #print (d)
        sql = "INSERT INTO descriptions(asn, descr) VALUES (%s, %s)"
        val = (record['asn'], d)
        cursor.execute(sql,val)
        mydb.commit()
    v = iter(imp4)
    
    for up,pol in zip(v,v):
        #print(pol,up)
        sql = "INSERT INTO import4(asn, policy, asn_up) VALUES (%s, %s,%s)"
        #print ("UPO is", up)
        val = (record['asn'], pol,up)
        #if record_id == 643:
            #print (pol)
        cursor.execute(sql,val)
        mydb.commit()
    v = iter(exp4)
    for down,pol in zip(v,v):
        #print(down,pol)
        sql = "INSERT INTO export4(asn, policy, asn_down) VALUES (%s, %s,%s)"
        val = (record['asn'], pol,down)
        #if record_id > 6142:
            #print (down, pol)
        cursor.execute(sql,val)
        mydb.commit()
    
    for pol in imp6:
        #print(pol)
        up = 0
        sql = "INSERT INTO import6(asn, policy, asn_up) VALUES (%s, %s,%s)"
        val = (record['asn'], pol,up)
        cursor.execute(sql,val)
        mydb.commit()
    
    for pol in exp6:
        #print(pol)
        down = 0
        sql = "INSERT INTO export6(asn, policy, asn_down) VALUES (%s, %s,%s)"
        val = (record['asn'], pol,down)
        cursor.execute(sql,val)
        mydb.commit()
     
    #print ("Record sent to sql ",record_id,record)
    #print ("desc ", desc)
    #print ("Import4 ", imp4)
    #print ("export4 ",exp4)
    #print ("import6 ", imp6)
    #print ("export6 ", exp6)
    #time.sleep(5)
    record = {}
    desc = []
    imp4 = []
    imp6 = []
    exp4 = []
    exp6 = []
def main():
    desc = []
    imp4 = []
    exp4 = []
    imp6 = []
    exp6 = []
    
    fields = ('asn', 'asname', 'org',desc, imp4, exp4, imp6, exp6, 'created','modified','source', 'default4', 'default6')
    record = {}
    record_id = 0
    last_record_id = 0

    record['asn']  = ""
    record['asname']  = ""
    record['org'] =  ""
    record['default4'] = ""
    record['default6'] = ""
    record['created']  = ""
    record['modified'] = ""
    record['source'] = ""
    asnum = ""
    policy = ""

    with open("../files/ripe.db.aut-num", "r", encoding="ISO-8859-1") as myfile:
        
        
        for line in myfile:
        
            #print (line)
            #time.sleep(2)
            if line.split(":")[0][0] == "%" or line.split(":")[0][0] == "#" or line.split(":")[0][0] == "\n" or line.split(":")[0][0] == " "  or line.split(":")[0][0] == "+":
                continue
            if line.split(":")[0] == "aut-num":
                if record_id != 0:
                    sql_write(record_id,record,desc,imp4,exp4,imp6,exp6)
                #print (record_id)
                record['asn'] = line.split(":")[1].upper().split("AS")[1].strip()
                record_id = record_id +1 
                record['asname']  = ""
                record['org'] =  ""
                record['default4'] = 0
                record['default6'] = ""
                record['created']  = ""
                record['modified'] = ""
                record['source'] = ""
                desc = []
                imp4 = []
                exp4 = []
                imp6 = []
                exp6 = []
                
                continue
            if line.split(":")[0] == "as-name":
                record['asname'] = line.split(":")[1].strip()
                continue
            if line.split(":")[0] == "org":
                record['org'] = line.split(":")[1].strip()
                continue
            if line.split(":")[0] == "descr":
                desc.append(line.split(":")[1].strip())
                continue
            if line.split(":")[0] == "import":
                values = line.split(":")[1].strip().upper()
                #print (values)
                #TODO : work out how to deal with policies contained within {}
                #TODO : lots of work required here to parse imports and exports better
                if "{" in values: 
                    continue
                if "AS" in values:
                    # add the as number that is announcing the policy
                    asnum = values.split("AS")[1].split(" ")[0]
                    # if AS and policy are on same line
                    if len(values.split("AS")[1].split(" ")) > 1:

                        # If value has an action statement add it to policy and add a 
                        # space because there must be an accept after it
                        if "ACTION " in values:
                            if len(values.split("ACTION")[1].split(";")) > 1:
                                policy = values.split("ACTION ")[1].split(";")[0]+ " "
                        # If value has an accept statement add it to policy        
                        if "ACCEPT" in values:
                            if len(values.split("ACCEPT")[1]) > 1:
                                policy = policy + values.split("ACCEPT ")[1]
                        

                    else:
                        # IF AS and Policy are on 2 different lines
                        p = next(myfile).upper()
                        #if action add a space because there must be an accept after it
                        if "ACTION" in p:
                            policy = p.split("ACTION ")[1].split(";")[0].strip() + " "
                        # if there is an Action add the accept to it otherwise just add accept
                        if "ACCEPT" in p:
                            policy = policy + p.split("ACCEPT ")[1].strip()
                        
                        #print (asnum,policy)
                        
                    
                    imp4.append(asnum)
                    imp4.append(policy)
                    # reset policy ready for next import
                    policy = ""
                    continue
                else:
                    continue
            if line.split(":")[0] == "export":
                values = line.split(":")[1].strip().upper()
                #print (values)
                #TODO : work out how to deal with policies contained within {}
                #TODO : lots of work required here to parse imports and exports better
                if "{" in values: 
                    continue
                if "AS" in values:
                    asnum = values.split("AS")[1].split(" ")[0]
                    # if AS and policy are on same line
                    if len(values.split("AS")[1].split(" ")) > 1:
                        #print (values)
                        if "ANNOUNCE" in values:
                            if len(values.split("ANNOUNCE")[1]) > 1:
                                policy = values.split("ANNOUNCE ")[1]
                        #if "ACTION" in values:
                            #if len(values.split("ACTION")[1].split(";")) > 1:
                                #policy = values.split("ACTION ")[1].split(";")[0]
                    else:
                        # IF AS and Policy are on 2 different lines
                        p = next(myfile).upper()
                        #print (p)
                        if "ANNOUNCE" in p:
                            policy = p.split("ANNOUNCE ")[1].strip()
                        #if "ACTION" in p:
                            #olicy = p.split("ACTION ")[1].strip()
                    
                        #print (asnum,policy)
                        
                    exp4.append(asnum)
                    exp4.append(policy)
                    # reset policy ready for next import
                    policy = ""
                    continue
                else:
                    continue
            if line.split(":")[0] == "mp-import":
                imp6.append(line.split(":")[1].strip())
                continue
            if line.split(":")[0] == "mp-export":
                exp6.append(line.split(":")[1].strip())
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
            #TODO : This variable needs to be changed to a list as there can be a few defaults per AS
            if line.split(":")[0] == "mp-default" :
                record['default6'] = line.split(":")[1].strip()
                continue
            #TODO : This variable needs to be changed to a list as there can be a few defaults per AS
            # also needs work on parsing the entire syntax
            if line.split(":")[0] == "default" :
                if "AS" in line.split(":")[1]:
                    record['default4'] = line.split(":")[1].split("AS")[1].split(" ")[0].strip()
                    #print (record['default4'])
                    continue

            #TODO : Ignore anything else for now 
            if line.split(":")[0] == "remarks":
                continue
            if line.split(":")[0] == "export-via":
                continue
            if line.split(":")[0] == "import-via":
                continue
            if line.split(":")[0] == "admin-c":
                continue
            if line.split(":")[0] == "tech-c":
                continue
            if line.split(":")[0] == "status":
                continue
            if line.split(":")[0] == "mnt-by":
                continue
            if line.split(":")[0] == "notify":
                continue
            if line.split(":")[0] == "sponsoring-org":
                continue
            if line.split(":")[0] == "member-of":
                continue
            if line.split(":")[0] == "abuse-c":
                continue
            if line == "":
                print ("this one got through ", line.split(":")[0])
                time.sleep(5)
    sql_write(record_id,record,desc,imp4,exp4,imp6,exp6)


            


    '''
    if record:
        # handle last record
        writer.writerow(record)
    '''

    

if __name__ == "__main__":
    main()