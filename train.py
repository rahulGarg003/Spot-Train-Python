import urllib2
import re
from bs4 import BeautifulSoup
import datetime
import json

stncodes = []

train_no = '19019'
station_code = 'GGC'
date_non = str(datetime.date.today())
def date(x):
    splitted=x.split("-")
    formatdate = str(splitted[2]+'-'+splitted[1]+'-'+splitted[0])
    return formatdate
url=urllib2.urlopen('https://www.confirmtkt.com/train-running-status/{0}?StationName={1}&Date={2}'.format(train_no,station_code,date(date_non)))

soup = BeautifulSoup(url.read(), 'lxml')

###################################################livedata json file#######################################################
data = soup.find_all('script')
#print(type(data))
data = str(data)
p = re.findall('var livedata = (.*?);',data)
jsonfile = json.loads(p[0])
##########################################################################################################################
#####################################################station name define#######################################################

for option in soup.find_all('option'):
    split=option['value'].split(' ')
    stncodes.append(split[-1])
###########################################################current status###########################################################################
curstnname = jsonfile['curStnName']
lastupdate = jsonfile['lastUpdated']
####################################################
i = 0
for code in stncodes:
    if (code == station_code):
        break
    i = i+1
stnname = jsonfile['stations']

finalvar =  ("Current Station: {}, Jounery Station: {},Delay: {} min, Schedule Arrival: {}, Expected Arrival: {}, Schedule Depature: {}, Expected Departure: {}, Last Updated: {}"
       .format(curstnname,stnname[i]['stnCodeName'],stnname[i]['delayArr'],stnname[i]['schArrTime'],stnname[i]['actArr'],stnname[i]['schDepTime'],stnname[i]['actDep'],lastupdate))

