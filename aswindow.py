
import tkinter as tk
#from test5 import MultiListbox # A possible new windows type worth trying
from asn import As # my current AS Class
import framework # simple window framework in framework.py
import pprint
import os
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

        ascompany = thisas.get_company_info()
            
        print(ascompany)
        time.sleep(10)

        # Start writing the HTML FILE >>>>>

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
        ip.write(str(ascompany['lat'])+", "+str(ascompany['lon'])+'], 6);\n')
        ip.close()
        # TODO: work out a way of zooming to the correct distance
        
        # write tilelayer information to html file
        cmd = 'cat html/tilelayer.html >> '+ filename
        os.system(cmd)
        

        # show the AS on the map as a large red circle at correct coordinates
        ip = open(filename, 'a')
        string1 = "var circle = L.circle(["
        string2 = "], { \n        color: 'red',\n        fillColor: '#f03',\n        fillOpacity: 0.5,\n        radius: 50000\n        }).addTo(map);\n"
        ip.write(string1+str(ascompany['lat'])+', '+str(ascompany['lon'])+string2)
        ip.close()
        # show all ip locations on map
        result = {}
        ipinfo =thisas.get_ipinfo()

        # below was to create a file for test purposes 
        #pre_filename = 'ases/presorted_'+'AS' +asnumber+'_ipinfo'+'.json'
        #ipdata= open(pre_filename, 'w')
        #ipdata.write(str(ipinfo))


        # reorganise ip addressses via latitudes so as not to duplicate points

        for ipaddress,values in ipinfo.items():
            #print (values)
            #print ("LAT is "+str(values['lat']) )
                        
            # create a point for the ipaddress
            if values['lat'] not in result:
                result[values['lat']] = {}
                result[values['lat']][ipaddress]            = {}
                #result[values['lat']][ipaddress]           = ipaddress
                result[values['lat']][ipaddress]['company'] = values['company']
                result[values['lat']][ipaddress]['lon']     = values['lon']
                result[values['lat']][ipaddress]['popup']   = ipaddress +"  "+ values['company']
                #print ('popup is ', result[values['lat']][ipaddress]['popup'] )
            # if an ipadress already exists at that location just add it to the lat list, dont create another point 
            else:  
                result[values['lat']][ipaddress]            = {}
                #result[values['lat']][ipaddress]           = ipaddress
                result[values['lat']][ipaddress]['company'] = values['company']
                result[values['lat']][ipaddress]['lon']     = values['lon']
                         
                result[values['lat']][ipaddress]['popup'] = ipaddress +"  "+ values['company']
       
                #print ('popup is ',result[values['lat']][ipaddress]['popup']) 
              
            # TODO: ensure if values['lon'] != result[values['lat']]['lon']
        #print("RESULT IS ",result)
        # Create the popup values (not currently working)
        for lati,values in result.items():
            #print(lati)
            #print (values)
            tmpstring = ""
            lat_popup = {}
            for ipaddr, cmpinfo in values.items():
                tmpstring = tmpstring + cmpinfo['popup']+ "\n"
                #print ('tempstring is ',tmpstring)
            # This is the popup sign for each point
            lat_popup[lati] = tmpstring
            print ('LAT POPUP is ',lat_popup[lati])
        #pprint.pprint(result)
        
        # create ipaddress points on map in green circles
        stringa = "      var circle"
        stringb = " = L.circle(["
        string1 = "      // show the area of operation of the AS on the map\n      var polygon = L.polygon([\n"
        string2 = "], { color: 'green', fillColor: '#00ff4d', fillOpacity: 0.5, radius: 20000 }).addTo(map);"
        string3 = "        ]).addTo(map);\n"
        string4 = '      polygon.bindPopup("<b>AS'
        string5 = '</b><br />'
        string6 = '<br />Area of Operation");\n'
        string7 = '      circle.bindPopup("<b>AS'
        string7a ='      circle'
        string7b ='.bindPopup("<b>AS'
        string8 = ' ").openPopup();\n\n'
        spacer1 = "        ["
        spacer2 = "],\n"
        popup = {}
        
        #lat_list = result.items()
        #print ("LAT_LIST ", lat_list)

        # Test Purposes file creation
        #postlat_filename = 'ases/postlat_'+'AS' +asnumber+'_ipinfo'+'.json'
        #ipdata= open(postlat_filename, 'w')
        #ipdata.write(str(result))

        # Sort Ip addresses via Latitude to tidy up area of operation
        
 
        s = sorted(result.items())
        # Negative strings are not orderd correctly so need to fix
        
              
        #print (s)
        sorted_ipinfo = collections.OrderedDict(s)
        #print (sorted_ipinfo)

        # Test Purposes file creation
        #post_filename = 'ases/postsorted_'+'AS' +asnumber+'_ipinfo'+'.json'
        #ipdata= open(post_filename, 'w')
        #ipdata.write(str(sorted_ipinfo))


        ip = open(filename, 'a')
        ip_location_id = 0
        for lat, values in sorted_ipinfo.items():
            ip_location_id += 1
            popup[lat] = ""
            for ipaddress, info in values.items():
                print ("LAT IS ",lat, "VALUES IS ",values)
                #print (info['popup'])
                #popup[lat] = popup[lat]+info['popup']+"<br />"
                #print (popup[lat])

            # Create Green IP Address location Circles   
            ip.write(stringa + str(ip_location_id)+stringb+str(lat)+ ','+str(info['lon'])+string2+'\n')
            # Create Green circle Popup
            ip.write(string7a +str(ip_location_id)+string7b+asnumber + string5 + info['company']+"<br />" + ipaddress +string8)
        
            #print ("POPUP for ",lat," is ",popup[lat])


        # Create area of operation

        ip = open(filename, 'a')
        ip.write(string1)

        for lat, values in sorted_ipinfo.items():
            # popup[lat] = ""
            for ipaddress, info in values.items():
                print ("LAT IS ",lat, "VALUES IS ",values)
                
                #print (info['popup'])
                #popup[lat] = popup[lat]+info['popup']+"<br />"
                #print (popup[lat])
                
                
            ip.write(spacer1+str(lat)+ ','+str(info['lon'])+spacer2)
            #print ("POPUP for ",lat," is ",popup[lat])
        
        # add polygon ending   
        ip.write(string3)
        ip.write(string4 +asnumber+string5+ascompany['owner'])
        if ascompany['inetnum'] != "":
            ip.write("<br /" + ascompany['inetnum']+string6)
        else:
            ip.write(string6)

        #Create circle to denote AS
        ip.write(string7 +asnumber+string5+ascompany['owner']+string8)
        string9 = "    </script>\n  </body>\n</html>"
        ip.write (string9)
        ip.close()

 
        print (filename+ " Written Succesfully, copy it to your webserver")
        self.e1.delete(0, tk.END)
    

if __name__ == '__main__':
    os.chdir('/home/paul/Documents/geolocation')

    root = tk.Tk()
    app = show_as_info(root)
    root.mainloop()