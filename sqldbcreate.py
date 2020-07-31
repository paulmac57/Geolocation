import mysql.connector
import csv
import time

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="brindle7",
    database="asgeo"
)

print(mydb)

dbexist = False


cursor = mydb.cursor()
if not dbexist:
    #cursor.execute("CREATE TABLE asorganisations (id INT AUTO_INCREMENT PRIMARY KEY, owner VARCHAR(40), ownerid VARCHAR(15), responsible VARCHAR(30), address1 VARCHAR(40), address2 VARCHAR(40), country_code VARCHAR(3), region VARCHAR(12), phone VARCHAR(20), created DATE, changed DATE, lat DECIMAL(10, 8), lon DECIMAL(11, 8))")
    #cursor.execute("CREATE TABLE inetnums (id INT AUTO_INCREMENT PRIMARY KEY, inetnum VARCHAR(20), ownerid INT UNSIGNED, region VARCHAR(12), lat DECIMAL(10, 8), lon DECIMAL(11, 8))")
    cursor.execute("CREATE TABLE asnumber(id INT PRIMARY KEY, asorg INT, ipaddresses INT, region VARCHAR(12))")
    cursor.execute("CREATE TABLE ipaddresses(id INT AUTO_INCREMENT PRIMARY KEY, ipaddress VARCHAR(20), region VARCHAR(12))")
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall() ## it returns list of tables present in the database

    ## showing all the tables one by one
    for table in tables:
        print(table)

'''
# Define Region Code and Colour

RIPE    = "#ffcc32"
APNIC   = "#b00000"
AFRINIC = "#d15e13"
LACNIC  = "#00b000"
ARIN    = "#009ac7"
WHITE   = (255,255,255)


# delegated-ripencc-extended-latest.txt

global countries

prefixes = []
countries = []
allocations = []
numbers = []
net = []
net_country = []
ripe_countries = []
apnic_countries = []
afrinic_countries = []
lacnic_countries = []
arin_countries = []

def Add_info(index):
    
    theCountry = countries[index]
    theDate = allocations[index]
    theNumber = numbers[index]
    tday = list(theDate)
    year = tday[0:4]
    thisyear = "".join(year)
    month = tday[4:6]
    thismonth = "".join(month)
    day = tday[6:8]
    thisday = "".join(day)
    td = thisyear + '-'+thismonth + '-'+ thisday 
    return theCountry, td, theNumber


with open('countries-regions.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    
    for row in csv_reader:
        country_name   = row[0]
        country_code   = row[1]
        country_region = row[2]
        if country_region == "RIPE NCC":
            ripe_countries.append(country_code)
            ripe_countries.append(country_name)
        if country_region == "APNIC":
            apnic_countries.append(country_code)
            apnic_countries.append(country_name)
        if country_region == "AFRINIC":
            afrinic_countries.append(country_code)
            afrinic_countries.append(country_name)
        if country_region == "LACNIC":
            lacnic_countries.append(country_code)
            lacnic_countries.append(country_name)
        if country_region == "ARIN":
            arin_countries.append(country_code)
            arin_countries.append(country_name)
#print(arin_countries)

#time.sleep(10) 

with open('delegated-ripencc-extended-latest.txt') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter='|')
    line_count = 0
    
    for row in csv_reader:
        # print(f'\t{row[0]} belongs in the {row[7]} region')
        if row[2]=="ipv4":
            prefix = row[3]
            country = row[1]
            date_alloc = row[5]
            no_allocated = row[4]
            prefixes.append(prefix)
            countries.append(country)
            allocations.append(date_alloc)
            numbers.append(no_allocated)
        


network = 0
a = 0
b = 0
    

for prefix in prefixes:
    try:
        #print('The net is'+ str(net))
        #print('prefix is ' + str(prefix))
        byte1 = prefix.split('.')[0]
        network = byte1
        #print('Network is ' + str(network))
        #byte2 = prefix.split('.')[1] 
        #byte3 = prefix.split('.')[2]
        #byte4 = prefix.split('.')[3]
        #print("Country index is "+str(b))
        thiscountry,thisdate,thisno = Add_info(b)
        #print(thiscountry, thisdate)cat
        #time.sleep(10)

    # Country to Region Codes from
    #  https://www.ripe.net/participate/member-support/list-of-members/list-of-country-codes-and-rirs
    # Procedure: Remove first 4 lines from each file change flags below and change name of file above
    # flag = 0 means correct RIR, flag = 1 means Ripe issued, flag  =2 means apnic issued, flag =4 means afrinic issued
    # flag =8 means lacnic issued, flag =16 means arin issued
        if thiscountry in ripe_countries:
            thisregion = "RIPE"
            flag = 0
        elif thiscountry in apnic_countries:
            thisregion = "APNIC"
            flag = 1
        elif thiscountry in afrinic_countries:
            thisregion = "AFRINIC"
            flag = 1
        elif thiscountry in lacnic_countries:
            thisregion = "LACNIC"
            flag = 1
        elif thiscountry in arin_countries:
            thisregion = "ARIN"
            flag = 1

        #print("Country is "+thiscountry)

        # Date format = Network, prefix, country, region, sub-prefix, subprefix-country, region, sub-prefix,subprefix-country ......
        # example     = 2, 2.0.0.0, EU, 2.1.0.0, GB, 2.2.0.0, GE, ...... 
        # net = [[2,....],[3,......],[4,.....],........]]

        #if byte2 == '0' and byte3 == '0' and byte4 == '0':
            #print(net,a)
            #net.append([network, prefix, thisno, thiscountry, thisregion]) 
            #net_country[a].append(Country(prefixes.index))
            #print("network is "+net[a][0])
            #print("prefix is "+net[a][1])
            #print("country is "+net[a][2])
            #print("region is "+net[a][3])
            #a += 1

        #else:
            #print(net,a-1)
            #net[a-1].append(prefix)
            #net[a-1].append(thiscountry)
            #net[a-1].append(thisregion)
        print (b, network, thisdate, prefix, thisno, thiscountry, thisregion, flag)
        sql = "INSERT INTO networks (network, date, prefix, number, country_code, region, flag) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (network,thisdate,prefix,thisno, thiscountry, thisregion, flag)
        b +=1
        cursor.execute(sql,val)
        print(b, cursor.rowcount," ", prefix, " !record inserted.")
        mydb.commit()
    except:
        pass


#time.sleep(10)
'''