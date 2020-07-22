from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="aswindow")
location = geolocator.geocode("Tebet Timur Raya No. 53 Jakarta 12820, Indonesia")
print(location.address)
print((location.latitude, location.longitude))
