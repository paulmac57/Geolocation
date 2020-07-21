# GEOLOCATION

To Run: Python aswindow.py

uses asn.py
AS Class API
  As(asn_number, test)
  
  .speed                  # Speed of ping from Manchester to AS
  .download               # Speed of Download from AS to Manchester
  .upload                 # Speed of Upload from Manchester to AS
  
  .getcompanyinfo()       # returns Dict of info {'owner', 'ownerid', 'responsible', 'address1', 'address2', 'country', 'phone', 'created', 'changed'}
  .get_ipinfo()           # returns Dict of Prefix Details {Company,lat,lon}
  .get_upstream()         # returns Dict of upstream ASnumber peers
  .get_downstream()       # returns Dict of upstream ASnumber peers
  .get_domains()          # has ability to return Dict of domains on this AS (not implemented)
  .get_related_networks() # has ability to return Dict of related networks on this AS (not implemented)
  
