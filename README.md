# GEOLOCATION

To Run: Python aswindow.py <br />
creates a HTMl file (<asnumber>.html) in ases folder which must be copied to webserver to display map. <br />
<br />
uses asn.py <br />
AS Class API <br />
  As(asn_number, test) <br />
  <br />
  .speed                  # Speed of ping from Manchester to AS <br />
  .download               # Speed of Download from AS to Manchester <br />
  .upload                 # Speed of Upload from Manchester to AS <br />
  <br />
  .getcompanyinfo()       # returns Dict of info {'owner', 'ownerid', 'responsible', 'address1', 'address2', 'country', 'phone', 'created', 'changed'} <br />
  .get_ipinfo()           # returns Dict of Prefix Details {Company,lat,lon} <br />
  .get_upstream()         # returns Dict of upstream ASnumber peers <br />
  .get_downstream()       # returns Dict of upstream ASnumber peers <br />
  .get_domains()          # has ability to return Dict of domains on this AS (not implemented) <br />
  .get_related_networks() # has ability to return Dict of related networks on this AS (not implemented) <br />
  
