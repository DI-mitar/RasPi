import urllib3

URL = 'https://api.thingspeak.com/update?api_key=C25HX6MCDL1M429U'

http = urllib3.PoolManager()
r = http.urlopen('GET',URL+'&field1=55')


