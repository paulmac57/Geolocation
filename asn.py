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

class As:
    def __init__(self, asnumber,test):
        self.name = asnumber
        self.handler = ipinfo.getHandler(access_token='5887e8b74e7139')
        self.geolocator = Nominatim(user_agent="aswindow")
        self.url_base = 'http://ipinfo.io/'
        self.as_base = 'AS'
        self.asn = self.as_base + str(self.name)
        self.test = test
        
        print ("this is the asn "+ self.asn)

        if self.test:
            #======== or work with static file during tests =====
            self.myfile = open('html/doc.html', 'r')
            self.html_doc = self.myfile.read()
        else:
            #======== download live data=========
            filename = 'html/'+self.asn.lower()+'_doc.html'
            output = open(filename, 'wb')
            page = requests.get(self.url_base+self.asn)
            self.html_doc = page.content
            output.write(self.html_doc)
        self.soup = BeautifulSoup(self.html_doc, 'html.parser')
        
        try:
            # Speed of connection
            _data =  self.soup.find_all("div", attrs={"class": "media-body mt-n1"})
            self.speed = _data[0].h5.get_text()
            #print ("SPEED is "+str(self.speed))
            self.download = _data[1].h5.get_text()
            #print ("DOWNLOAD is "+self.download)
            self.upload = _data[2].h5.get_text()
            #print ("UPLOAD is "+self.upload)
        except IndexError:
            print (self.asn+" ... Are you sure you typed a correct AS number ?")
            sys.exit(1)  

    class d():
        # used by test
        def __init__(self,ips,thedict):
            #print ('ips is ' + ips)
            self.latitude= thedict[ips]['lat']
            self.longitude= thedict[ips]['lon']
    
    def substring_after(self,s, delim):
        return s.partition(delim)[2]
    def substring_before(self,s, delim):
        return s.partition(delim)[1]
    def find_2nd(self,string, substring):
        return string.partition(substring, string.partition(substring) + 1)

    def get_company_info(self):
       
        
        company = self.soup.find(id='whois')
        #print ("COMPANY IS ",company)
        info = company.contents[3].pre.contents[0]

        # TODO: it looks like different RIR's have different field names
        # so might be worth creating templates for each one instead of using if statements.

        owner    = self.substring_after(info,'owner:').split('\n')[0].strip()
        if owner == "":
            owner = self.substring_after(info,'ASName:').split('\n')[0].strip()
        if owner == "":
            owner = self.substring_after(info,'descr:').split('\n')[0].strip()


        ownerid  = self.substring_after(info,'ownerid:').split('\n')[0].strip()
        if ownerid == "":
            ownerid = self.substring_after(info,'OrgID:').split('\n')[0].strip()
        responsible = self.substring_after(info,'responsible:').split('\n')[0].strip()
        if responsible == "":
            responsible = self.substring_after(info,'person:').split('\n')[0].strip()
        
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
        
        country  = self.substring_after(info,'country:').split('\n')[0].strip()
        if country == "":
            country  = self.substring_after(info,'Country:').split('\n')[0].strip()
        phone    = self.substring_after(info,'phone:').split('\n')[0].strip()
        created  = self.substring_after(info,'created:').split('\n')[0].strip()
        if created == "":
            created  = self.substring_after(info,'RegDate:').split('\n')[0].strip()

        changed  = self.substring_after(info,'changed:').split('\n')[0].strip()
        if changed == "":
            changed  = self.substring_after(info,'Updated:').split('\n')[0].strip()
        inetnum  = self.substring_after(info,'inetnum:').split('\n')[0].strip()
        
        
        
        #TODO work with more than 1 inetnum
        
        # build inetnum ip address to be sent to ipinfo geolocator

        if inetnum != "":
            l = len(inetnum.split('/')[0].split('.'))
            print ("Inetnum ",inetnum)
            print ("LENGTH is ",l)
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
            print ("INETNUM IS ", inetnum)
            coord = self.handler.getDetails(inetnum) # get coords from ipinfo
            # TODO: Note Not Currently in use
            i1_lat = float(coord.latitude)
            i1_lon = float(coord.longitude)

        #print ("INFO IS "+ info)
        lat = 0
        lon = 0
        lat,lon = self.get_coords(owner,address1,address2,country)

        this_company = {'owner' : owner, 'ownerid': ownerid, 'responsible' : responsible,
                        'address1' : address1, 'address2' : address2, 'country' : country,
                        'phone' : phone, 'created' : created, 'changed' : changed, 'inetnum' : inetnum,
                        'lat' : lat, 'lon' : lon, 'i1_lat': i1_lat, 'i1_lon' : i1_lon }
        #print ("OWNER IS " + thiscompany["owner"])
        
        #use nominatim to find coordinates
        
        

        return this_company
    
    def get_coords(self,o,a1,a2,c):
        try:
            location = None
            address = ""
            
            address = a2 + " " + c
            location = self.geolocator.geocode(address)
            
            if location == None:
                address = a2
                location = geolocator.geocode(address)
                
            if location == None:
                address = a1 + " " + c
                location = geolocator.geocode(address)
                
    
            if location == None:
                address = a1 + " " + a2 + " " + c
                location = geolocator.geocode(address)
               
            if location == None:
                address= o+" " + c 
                location = geolocator.geocode(address)
                
            if location == None:
                raise TypeError
            latitude = location.latitude
            longitude = location.longitude
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
    thisas = As(ASN,True)
    print (thisas.get_company_info())
    print (thisas.get_ipinfo())
    
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
    
   
    