import requests
from bs4 import BeautifulSoup
import re
import ipinfo # uses ipinfo.io to get  ip location data and asinfo at same time
import pprint
import os
import json
import time
import sys
from geopy.geocoders import Nominatim
import mysql.connector

class As:
    def __init__(self, asnumber):
        self.name = asnumber
        self.handler = ipinfo.getHandler(access_token='5887e8b74e7139')
        self.geolocator = Nominatim(user_agent="aswindow")
        self.url_base = 'http://ipinfo.io/'
        self.as_base = 'AS'
        self.asn = self.as_base + str(self.name)
        
        print ("this is the asn "+ self.asn)

        if self.as_exists(asnumber):
            print ("asNumber exists in database")
            self.get_info_from_db()
            
        else:
            print ("asNumber does not exist in database")
            self.get_info_from_ipinfo()
            
            
        #except IndexError:
            #print (self.asn+" ... Are you sure you typed a correct AS number ?")
            #sys.exit(1)  

    class d():
        # used by test
        def __init__(self,ips,thedict):
            #print ('ips is ' + ips)
            self.latitude= thedict[ips]['lat']
            self.longitude= thedict[ips]['lon']

    def as_exists(self, asnumber):
        
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="asgeo"
            )
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM ases WHERE id = %s",(asnumber,))

        results = cursor.fetchone()  
        print ("RESULTS ARE ", results)
        
        if results == None:
            exists =False
        else:
            exists = True

        return exists

    def org_exists(self, owner, address1, address2):

        
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="asgeo"
            )
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM asorganisations WHERE owner = %s AND address1 = %s AND address2 = %s",(owner,address1,address2,))

        results = cursor.fetchone() 
        print ("RESULTS from DB are ",results) 
        if results == None:
            exists =False
            r = None
        else:
            exists = True
            r = results[0]

        return r, exists
        
    def inetnum_exists(self, asnumber):
        
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="asgeo"
            )
        cursor = mydb.cursor()
        cursor.execute("SELECT id FROM inetnums WHERE inetnum = %s",(self.inetnum,))

        results = cursor.fetchone()  
        print ("INETNUM RESULTS ARE ", results)
        
        if results == None:
            exists =False
        else:
            exists = True

        return exists
    
    def substring_after(self,s, delim):
        return s.partition(delim)[2]
    def substring_before(self,s, delim):
        return s.partition(delim)[1]
    def find_2nd(self,string, substring):
        return string.partition(substring, string.partition(substring) + 1)



    def get_info_from_ipinfo(self):

        #======== download live data=========
        filename = 'html/'+self.asn.lower()+'_doc.html'
        output = open(filename, 'wb')
        page = requests.get(self.url_base+self.asn)
        html_doc = page.content
        output.write(html_doc)
        soup = BeautifulSoup(html_doc, 'html.parser')
    
        company = soup.find(id='whois')
        #print ("COMPANY IS ",company)
        info = company.contents[3].pre.contents[0]

        
        # TODO: it looks like different RIR's have different field names
        # so might be worth creating templates for each one instead of using if statements.

        owner    = self.substring_after(info,'owner:').split('\n')[0].strip()
        if owner == "":
            owner = self.substring_after(info,'ASName:').split('\n')[0].strip()
        if owner == "":
            owner = self.substring_after(info,'descr:').split('\n')[0].strip()
        if owner == "":
            owner = self.substring_after(info,'Orgname:').split('\n')[0].strip()
        
        self.owner = owner

        ownerid  = self.substring_after(info,'ownerid:').split('\n')[0].strip()
        if ownerid == "":
            ownerid = self.substring_after(info,'OrgID:').split('\n')[0].strip()
        self.ownerid = ownerid

        responsible = self.substring_after(info,'responsible:').split('\n')[0].strip()
        if responsible == "":
            responsible = self.substring_after(info,'person:').split('\n')[0].strip()
        if responsible == "":
            responsible = self.substring_after(info,'FirstName:').split('\n')[0].strip()+self.substring_after(info,'LastName:').split('\n')[0].strip()
        self.responsible = responsible
        address1 = self.substring_after(info,'address1:').split('\n')[0].strip()
        address2 = self.substring_after(info,'address2:').split('\n')[0].strip()
        # if no address1 and address2 info then try just Street
        if address1 == "":
            address1 = info.partition("Street:")[2].split('\n')[0].strip()
            address2 = info.partition("Street:")[2].partition("Street:")[2].split('\n')[0].strip()
        
        if info.partition("City:")[2].split('\n')[0].strip() != "":
                address2 = address2 + " " + info.partition("City:")[2].split('\n')[0].strip()
        if info.partition("State\Prov:")[2].split('\n')[0].strip() != "":
                address2 = address2 + " " + info.partition("State\Prov:")[2].split('\n')[0].strip()
        # if still no address info the try address 
        if address1 == "":
            address1 = info.partition("address:")[2].split('\n')[0].strip()
            address2 = info.partition("address:")[2].partition("address:")[2].split('\n')[0].strip()
        self.address1 = address1
        self.address2 = address2
        
        country  = self.substring_after(info,'country:').split('\n')[0].strip()
        if country == "":
            country  = self.substring_after(info,'Country:').split('\n')[0].strip()
        self.country = country
        
        
        
        phone    = self.substring_after(info,'phone:').split('\n')[0].strip()
        self.phone = phone
        created  = self.substring_after(info,'created:').split('\n')[0].strip()
        if created == "":
            created  = self.substring_after(info,'RegDate:').split('\n')[0].strip()
        self.created = created
        changed  = self.substring_after(info,'changed:').split('\n')[0].strip()
        if changed == "":
            changed  = self.substring_after(info,'Updated:').split('\n')[0].strip()
        self.changed = changed
        
        self.region = self.substring_after(info,'Source:').split('\n')[0].strip()
        if self.region == "":
            self.region = self.get_region(country)

        inetnum  = self.substring_after(info,'inetnum:').split('\n')[0].strip()
        
        
        
        #TODO work with more than 1 inetnum
        
        # build inetnum ip address to be sent to ipinfo geolocator

        if inetnum != "":
            l = len(inetnum.split('/')[0].split('.'))
            #print ("Inetnum ",inetnum)
            #print ("LENGTH is ",l)
            i1 = inetnum.split('/')[0].split('.')[0]
            i2 = inetnum.split('/')[0].split('.')[1]
            
            if l == 2:
                i3 = '0' 
                i4 = '0'
            if l == 3:
                i3 = inetnum.split('/')[0].split('.')[2]
                i4 = '0'
            if l == 4: 
                i3 = inetnum.split('/')[0].split('.')[2]
                i4 = inetnum.split('/')[0].split('.')[3]
            inetnum = i1+'.'+i2+'.'+i3+'.'+i4
            #print ("INETNUM IS ", inetnum)
            coord = self.handler.getDetails(inetnum) # get coords from ipinfo
            self.inetnum = inetnum
            # TODO: Note Not Currently in use
            i1_lat = 0
            i1_lat = float(coord.latitude)
            i1_lon = float(coord.longitude)
        else:
            i1_lat = 0
            i1_lon = 0
            

        #print ("INFO IS "+ info)
        #lat = i1_lat
        #lon = i1_lon

        
        
        #if ipinfo didnt fine location then use nominatim to find company lat and lon coordinates
        #if lat == 0.00:
        lat,lon = self.get_coords(owner,address1,address2,country)

        self.lat = lat
        self.lon = lon  

        # Speed of connection
        _data =  soup.find_all("div", attrs={"class": "media-body mt-n1"})
        self.speed = _data[0].h5.get_text()
        #print ("SPEED is "+str(self.speed))
        self.download = _data[1].h5.get_text()
        #print ("DOWNLOAD is "+self.download)
        self.upload = _data[2].h5.get_text()
        #print ("UPLOAD is "+self.upload) 
        '''
        this_company = {'owner' : owner, 'ownerid': ownerid, 'responsible' : responsible,
                        'address1' : address1, 'address2' : address2, 'country' : country,
                        'phone' : phone, 'created' : created, 'changed' : changed, 'inetnum' : inetnum,
                        'lat' : lat, 'lon' : lon, 'i1_lat': i1_lat, 'i1_lon' : i1_lon }
        '''
        #print ("OWNER IS " + thiscompany["owner"])

        # write all Data to local Database for easier retrieval next time
        
        asorg_id, org_exist = self.org_exists(self.owner, self.address1, self.address2)
        if not org_exist:
            asorg_id = self.add_org_to_db()
        print ("ASORG_ID ",asorg_id)
        as_exist = self.as_exists(self.name)
        if not as_exist:
            self.add_as_to_db(self.name,asorg_id)
        inetnum_exist = self.inetnum_exists(self.inetnum)
        if not inetnum_exist:
            self.add_inetnums_to_db(asorg_id)

            #add_prefixes_to_db(asorg_id)

        return #this_company

    def get_region(self,c):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="asgeo"
            )
        cursor = mydb.cursor()
        print ("AS IS ",self.name)
        cursor.execute("SELECT region FROM ctor WHERE code = %s",(c,))

        region = cursor.fetchone()  
        # results[0] = asnumber, results[1] = org-id
        print ("REGION Results are ", region)
        r = region[0]
        return r


    def get_info_from_db(self):
    
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="asgeo"
            )
        cursor = mydb.cursor()
        print ("AS IS ",self.name)
        cursor.execute("SELECT * FROM ases WHERE id = %s",(self.name,))

        results = cursor.fetchone()  
        # results[0] = asnumber, results[1] = org-id
        print ("Results are ", results)

        return 


    def add_org_to_db(self):

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="brindle7",
        database="asgeo"
    )



        cursor = mydb.cursor()
        sql = "INSERT INTO asorganisations (owner, ownerid, responsible, address1, address2, country_code, region, phone, created,changed, lat,lon) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (self.owner, self.ownerid,self.responsible,self.address1, self.address2, self.country, self.region, self.phone, self.created, self.changed,self.lat,self.lon)
        cursor.execute(sql,val)
        print(cursor.rowcount," ", self.owner, " !record inserted.")
        mydb.commit()
        sql = "SELECT id FROM asorganisations WHERE owner = '" + self.owner + "' AND address1 = '"+ self.address1+"'"
        print ("SQL is ",sql)
        cursor.execute(sql)
        id = cursor.fetchone()
        print ( "ID is ",id)
        id = id[0]
        return id

    def add_as_to_db(self,name,org_id):

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="asgeo"
            )
        cursor = mydb.cursor()
        sql = "INSERT INTO ases(id, asorg_id,region ) VALUES (%s, %s, %s)"
        val = (name, org_id, self.region, )
        cursor.execute(sql,val)

        mydb.commit()
    
    def add_inetnums_to_db(self,org_id):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="brindle7",
            database="asgeo"
            )
        cursor = mydb.cursor()
        sql = "INSERT INTO inetnums(inetnum,owner,region, lat, lon ) VALUES (%s, %s, %s, %s, %s)"
        val = (self.inetnum, org_id , self.region, self.lat, self.lon )
        cursor.execute(sql,val)

        mydb.commit()
    
    def get_coords(self,o,a1,a2,c):
        try:
            print("os ",o,"a1 ",a1,"a2 ",a2,"c ",c)
            location = None
            address = ""
            
            address = a2 + " " + c
            location = self.geolocator.geocode(address)
            #print ("Address is ",address,"Location is ",location)
            
            if location == None:
                address = a2
                location = self.geolocator.geocode(address)
                
            if location == None:
                address = a1 + " " + c
                location = self.geolocator.geocode(address)
                
    
            if location == None:
                address = a1 + " " + a2 + " " + c
                location = self.geolocator.geocode(address)
               
            if location == None:
                address= o + " " + c 
                location = self.geolocator.geocode(address)
                
            if location == None:
                raise TypeError
            latitude = location.latitude
            longitude = location.longitude
            print ("lat is ", location.latitude)
            print ("lon is ", location.longitude)
        except TypeError:
            print ("I can't find that As"+asnumber+" address and cordinates")
            sys.exit(1)  

        print(latitude, longitude)
        print ("Location is ", location, "Address is ", address)
        return latitude, longitude
       
    def get_ipinfo(self):
        ip_info = {}

        if self.test:
            #======== or work with static file during tests =====
            filename = 'html/'+self.asn+'_ipinfo.txt'
            ipdata= open(filename, 'r')
            details_string = ipdata.read()
            details_dict = json.loads(details_string)

        
        # Get all the IP info belonging to this AS
        ip_table = self.soup.find("table", attrs={"class": "table table-striped table-sm table-borderless"})
        ip_table_data = ip_table.tbody.find_all("tr") 
        # number of separate ip Addresses belonging to this AS
        ipdata_length = len(ip_table_data) 
        prefix_details = {}
        for i in range(ipdata_length):
            for td in ip_table_data[i].find_all("td"):
                
                #print (str(i) + " td "+str(td))
                # Get each separate Ip information
                subn = ip_table_data[i].find('a').get_text()
                subn = subn.strip()
                subnet = subn.split('/')[0]
                cidr = subn.split('/')[1]
                # Get company information that belongs to this IP
                comp = ip_table_data[i].find('span').get_text()
                ip_company = comp.strip()

                print ("SUBNET " +subnet)
        
                print ("CIDR " +cidr)

                print ("company "+ ip_company)
                ips = subnet+"/"+cidr
                ip_info[ips] = ip_company
                
                if self.test:
                    #======== or work with static file during tests =====
                    print ("IPS is ",ips)
                    print ("DICT is ",details_dict)

                    details = self.d(ips,details_dict)
                    print ("lat is"+ str(details.latitude))
                    print ("lat is"+ str(details.longitude))


                else:
                    #======== download live data=========
                    details = self.handler.getDetails(subnet)               
                lat = float(details.latitude)
                lon = float(details.longitude)
                print ("COORDS ARE ",lat,lon)

                prefix_details[ips] = {}
                prefix_details[ips]['company'] = ip_company
                prefix_details[ips]['lat'] = lat
                prefix_details[ips]['lon'] = lon
                
                #pprint.pprint(str(prefix_details))
                #print('=======================')
                #time.sleep(5)
        return prefix_details

    
    def get_upstream(self):

        # Upstream peers
        upstream = {}
        data =  self.soup.find("div", attrs={"id": "upstreams"})
        upstreams = data.find_all("li", attrs={"class": "list-inline-item w-100 w-md-50 mb-4"})
        upstream_number = len(upstreams)
        #print (upstream_number)
        for i in range(upstream_number):
            upstream[upstreams[i].a.get_text()]= upstreams[i].p.get_text()
        return upstream
    def get_downstream(self):

        # Downstream peers 
        downstream = {}
        data =  self.soup.find("div", attrs={"id": "downstreams"})
        downstreams = data.find_all("li", attrs={"class": "list-inline-item w-100 w-md-50 mb-4"})
        downstream_number = len(downstreams)
        #print (downstream_number)
        for i in range(downstream_number):
            downstream[downstreams[i].a.get_text()]= downstreams[i].p.get_text()
        return downstream
    def get_domains(self):
        #TODO: Do We need this ASes Hosted Domains ? ipinfo.io has separate API
        pass   
    def get_related_networks(self):
        #TODO: Do We need this ASes related networks , frtom ipinfo.io
        pass
    


if __name__ == "__main__":
    os.chdir('/home/paul/Documents/geolocation')
    ASN = 8048
    result = {}
    thisas = As(ASN)
    #print (thisas.get_company_info())
    #print (thisas.get_ipinfo())
    
    #ipinfo=thisas.get_ipinfo()
    '''
    ip = open(str(ASN)+'.csv', 'w')
    thisas = As(ASN)
    
    ascompany = thisas.get_company_info()
    ip.write("Companyinfo\n") 
    ip.write(str(ascompany))
    print("Companyinfo") 
    pprint.pprint(ascompany)
    ip.write("\nspeed ") 
    ip.write(thisas.speed)
    ip.write("\ndownload ") 
    ip.write(thisas.download)
    ip.write("\nupload ") 
    ip.write(thisas.upload) 
    print(thisas.speed,thisas.download,thisas.upload)  
    as_ipinfo=thisas.get_ipinfo()
    ip.write("\nipinfo \n")
    ip.write(str(as_ipinfo))
    print("ipinfo ")
    pprint.pprint(as_ipinfo) 

   
    as_down = thisas.get_downstream()
    as_up = thisas.get_upstream()
    
    ip.write("\ndownstream ")
    ip.write(str(as_down))
    ip.write("\nupstream ")
    ip.write(str(as_up))
    
    print("\ndownstream ")
    pprint.pprint(as_down)
    print("\nupstream ")
    pprint.pprint(as_up)
    '''
    
    '''
    for key,value in ipinfo.items():
            if value[lat] not in result.values():
                result[key] = value
    '''
    
   
    