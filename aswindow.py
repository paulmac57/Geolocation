
import tkinter as tk
#from test5 import MultiListbox # A possible new windows type worth trying
from asn import As # my current AS Class
import framework # simple window framework in framework.py
import pprint
import os
from geopy.geocoders import Nominatim
import time
import collections
import sys

# Maybe use folium for version2
''' import pandas as pd
import datetime
import folium
from folium.map import *
from folium import plugins
from folium.plugins import MeasureControl
from folium.plugins import FloatImage
'''


class show_as_info(framework.Framework):

    def __init__(self,root):
        #super().__init__(root)
        self.root = root
        self.root.title = ('AS Geo-Location')           
        self.create_gui() 
    
    def create_gui(self):
        
        self.create_menu()
        #self.create_top_bar()
        #self.create_tool_bar()
        self.create_window()
        self.handle_focus_out('dummy')
        self.bind_menu_accelerator_keys()

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        menu_definitions = (
            'File- &New/Ctrl+N/self.on_new_file_menu_clicked, Save/Ctrl+S/self.on_save_menu_clicked, SaveAs/ /self.on_save_as_menu_clicked, sep, Exit/Alt+F4/self.on_close_menu_clicked',
            'Edit- Undo/Ctrl+Z/self.on_undo_menu_clicked, sep',
            'View- Zoom in//self.on_canvas_zoom_in_menu_clicked,Zoom Out//self.on_canvas_zoom_out_menu_clicked',
            'About- About/F1/self.on_about_menu_clicked'
        )
        self.build_menu(menu_definitions)  # here's our framework 

    def create_window(self):
        tk.Label(root, text="AS Number").grid(row=0)
        self.e1 = tk.Entry(root, fg='grey',state='disabled')
        self.e1.grid(row=0, column=1, columnspan=3)
        self.e1.insert(0,"8048")
        
        self.e1.bind("<FocusIn>",self.handle_focus_in)
        self.e1.bind("<FocusOut>", self.handle_focus_out)
        self.e1.bind("<Return>", self.handle_enter)

        
        self.var1 = tk.BooleanVar()
        tk.Checkbutton(root, text="test", variable=self.var1, command=self.activateCheck).grid(row=0, column=4, sticky=tk.W)
        self.handle_focus_in('dummy')
        self.var1.set(True)
        
        tk.Button(root, 
            text='Quit', 
            command=root.quit).grid(row=1, 
                                    column=0, 
                                    sticky=tk.W, 
                                    pady=4)
        tk.Button(root, 
            text='Show', command=self.show_entry_fields).grid(row=1, 
                                                        column=3, 
                                                        sticky=tk.W, 
                                                        pady=4)
            
        
    def bind_menu_accelerator_keys(self):
        self.root.bind('<KeyPress-F1>', self.on_about_menu_clicked)
        self.root.bind('<Control-N>', self.on_new_file_menu_clicked)
        self.root.bind('<Control-n>', self.on_new_file_menu_clicked)
        self.root.bind('<Control-s>', self.on_save_menu_clicked)
        self.root.bind('<Control-S>', self.on_save_menu_clicked)
        self.root.bind('<Control-z>', self.on_undo_menu_clicked)
        self.root.bind('<Control-Z>', self.on_undo_menu_clicked)    

    def on_new_file_menu_clicked(self, event=None):
        pass

    def on_save_menu_clicked(self, event=None):
        pass

    def on_save_as_menu_clicked(self):
        pass

    def on_canvas_zoom_out_menu_clicked(self):
        pass

    def on_canvas_zoom_in_menu_clicked(self):
        pass

    def on_close_menu_clicked(self):
        pass

    def on_undo_menu_clicked(self, event=None):
        pass

    def on_about_menu_clicked(self, event=None):
        pass

    def handle_focus_in(self,_):
        self.e1.config(state='normal')
        self.e1.delete(0, tk.END)
        self.e1.config(fg='black')

    def handle_focus_out(self,_):
        self.e1.delete(0, tk.END)
        self.e1.config(fg='grey')
        self.e1.insert(0, "8048")
        self.e1.config(state='disabled')

    def handle_enter(self,txt):
        print(self.e1.get())
        self.show_entry_fields()

    def activateCheck(self):
        
        if self.var1.get() == 1:          #whenever checked
            self.e1.config(state='normal')
            self.handle_focus_out('dummy')# using root.focus() might be better
        elif self.var1.get() == 0:        #whenever unchecked
            self.e1.config(state='normal')
            self.handle_focus_in('dummy') # using root.focus() might be better
  


    def show_entry_fields(self):
        

        # get asnumber to be searched
        asnumber = self.e1.get()
        # Create AS instance
        print('Check test: ' + str(self.var1.get()))
        thisas = As(asnumber,self.var1.get())

        # get AS company info
        try:
            geolocator = Nominatim(user_agent="aswindow")
            ascompany = thisas.get_company_info()
            location = None
            address = ""
            print(ascompany)


            
            if ascompany['lat'] != None:
                latitude = ascompany['lat']
                longitude = ascompany['lon']
            else:
                address = str(ascompany['address2'])+" "+str(ascompany['country'])
                location = geolocator.geocode(address)
                print(address)
                print(location)

                if location == None:
                    address = str(ascompany['address2'])
                    location = geolocator.geocode(address)
                    print(address)
                    print(location)
                if location == None:
                    address = str(ascompany['address1'])+" "+str(ascompany['country'])
                    location = geolocator.geocode(address)
                    print(address)
                    print(location)
        
                if location == None:
                    address = str(ascompany['address1'])+str(ascompany['address2'])+" "+str(ascompany['country'])
                    location = geolocator.geocode(address)
                    print(address)
                    print(location)
                if location == None:
                    address= str(ascompany['owner'])+" "+str(ascompany['country']) 
                    location = geolocator.geocode(address)
                    print(address)
                    print(location)
                if location == None:
                    raise TypeError
                latitude = location.latitude
                longitude = location.longitude
        except TypeError:
            print ("I can't find that As"+asnumber+" address and cordinates")
            sys.exit(1)  

        print(latitude, longitude)
        print ("Location is ", location, "Address is ", address)

        # write default head info to new file
        filename = 'ases/as'+str(asnumber)+'.html'
        cmd2 = 'chmod ' +'766 '+filename
        cmd = 'cp html/head.html '+ filename
                
        os.system(cmd)
        # Fix File Permisssions
        os.system(cmd2)
               
        # Write latitude and longitude to html file for zoom location
        # open file 
        ip = open(filename, 'a')
        ip.write(str(latitude)+", "+str(longitude)+'], 7);\n')
        ip.close()
        # TODO: work out a way of zooming to the correct distance
        
        # write tilelayer information to html file
        cmd = 'cat html/tilelayer.html >> '+ filename
        os.system(cmd)
        

        # show the AS on the map as a large red circle at correct coordinates
        ip = open(filename, 'a')
        string1 = "var circle = L.circle(["
        string2 = "], { \n        color: 'red',\n        fillColor: '#f03',\n        fillOpacity: 0.5,\n        radius: 50000\n        }).addTo(map);\n"
        ip.write(string1+str(latitude)+', '+str(longitude)+string2)
        ip.close()
        # show all ip locations on map
        result = {}
        ipinfo =thisas.get_ipinfo()

        # below was to create a file for test purposes (no longer needed)
        #filename = 'ases/'+'AS8048_ipinfo'+'.txt'
        #ipdata= open(filename, 'w')
        #ipdata.write(str(ipinfo))


        # reorganise ip addressses via latitudes so as not to duplicate points

        for ipaddress,values in ipinfo.items():
            print (values)
            print ("LAT is "+values['lat']) 
                        
            # create a point for the ipaddress
            if values['lat'] not in result:
                result[values['lat']] = {}
                result[values['lat']][ipaddress]            = {}
                #result[values['lat']][ipaddress]           = ipaddress
                result[values['lat']][ipaddress]['company'] = values['company']
                result[values['lat']][ipaddress]['lon']     = values['lon']
                result[values['lat']][ipaddress]['popup']   = ipaddress +"  "+ values['company']
                #print ('popup is ', result[values['lat']][ipaddress]['popup'] )
            # if an ipadress already exists at that location just add it to list, dont create another point 
            else:  
                result[values['lat']][ipaddress]            = {}
                #result[values['lat']][ipaddress]           = ipaddress
                result[values['lat']][ipaddress]['company'] = values['company']
                result[values['lat']][ipaddress]['lon']     = values['lon']
                         
                result[values['lat']][ipaddress]['popup'] = ipaddress +"  "+ values['company']
       
                #print ('popup is ',result[values['lat']][ipaddress]['popup']) 
                
            # TODO: ensure if values['lon'] != result[values['lat']]['lon']
        for lati,values in result.items():
            print(lati)
            print (values)
            tmpstring= ""
            lat_popup = {}
            for ipaddr, cmpinfo in values.items():
                tmpstring = tmpstring + cmpinfo['popup']+ "\n"
                #print ('tempstring is ',tmpstring)
            # This is the popup sign for each point
            lat_popup[lati] = tmpstring
            print ('LAT POPUP is ',lat_popup[lati])
        #pprint.pprint(result)
        # create a test file (no longer needed now that it is permanently created)
        # filename = 'ases/'+'AS8048_lats'+'.txt'
        # aslats= open(filename, 'w')
        # aslats.write(str(result))

        # create ipaddress points on map in green circles
        # also create popups

        number_of_points = len(result)
        string1 = "      // show the area of operation of the AS on the map\n      var polygon = L.polygon([\n"
        string2 = "], { color: 'green', fillColor: '#00ff4d', fillOpacity: 0.5, radius: 20000 }).addTo(map);"
        string3 = "        ]).addTo(map);\n"
        ip = open(filename, 'a')
        spacer1 = "        ["
        spacer2 = "],\n"
        ip.write(string1)
        
        #lat_list = result.items()
        #print ("LAT_LIST ", lat_list)

        
        # Sort Ip addresses via Latitude to tidy up area of operation

        sorted_lat_list = collections.OrderedDict(sorted(result.items()))
        
        # create polygon area of operation
        # TODO: this needs improvement.
        for lat, values in sorted_lat_list.items():
            for ipaddress, info in values.items():
                print ("LAT IS ",lat, "VALUES IS ",values)
            ip.write(spacer1+lat+ ','+info['lon']+spacer2)

        # add polygon ending   
        ip.write(string3)

        string4 = '      polygon.bindPopup("<b>AS'
        string5 = '</b><br />'
        string6 = '<br />Area of Operation");\n'
        ip.write(string4 +asnumber+string5+ascompany['owner']+string6)

        #Create circle to denote AS

        string7 = '      circle.bindPopup("<b>AS'
        string8 = ' ").openPopup();\n\n'
        ip.write(string7 +asnumber+string5+ascompany['owner']+string8)

        string9 = "    </script>\n  </body>\n</html>"
        
        ip.write (string9)
        ip.close()
        
        
        
        

        


        '''
        for lati, values in result.items():
            print (lati)
            for ipadr, longi in values.items():
                
                print (ipadr)
                print (longi)
                print (longi['company'])
                lat_popups[lati] = {}
                lat_popups[lati][ipadr] = longi['company']
        print(lat_popups)        
        '''        

            #ip.write(spacer1+str(lat)+', '+str(result[lat]['lon'])+spacer2)








        '''
        # write company info to file
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
        print (filename+ " Written Succesfully, copy it to your webserver")
        self.e1.delete(0, tk.END)
    

if __name__ == '__main__':
    os.chdir('/home/paul/Documents/geolocation')

    root = tk.Tk()
    app = show_as_info(root)
    root.mainloop()