import re
import json
from urllib import request

url = 'http://ipinfo.io/json'
response = request.urlopen(url)
data = json.load(response)

IP=data['ip']
org=data['org']
city = data['city']
country=data['country']
region=data['region']
geo=data['loc']
print ('Your IP detail\n ')
print ('IP : {4} \nRegion : {1} \nCountry : {2} \nCity : {3} \nOrg : {0}\nGeo: {5}'.format(org,region,country,city,IP,geo))