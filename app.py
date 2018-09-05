from flask import Flask, jsonify, request
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
import datetime
import json

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def main():
    return '<h1>deployed to Heroku</h1>'
@app.route('/<trainno>/<stncode>', methods=['GET'])
def index(trainno,stncode):
    stncodes = []
    train_no = trainno
    station_code = stncode
    date_non = str(datetime.date.today())
    def date(x):
        splitted=x.split("-")
        formatdate = str(splitted[2]+'-'+splitted[1]+'-'+splitted[0])
        return formatdate
    url=urlopen('https://www.confirmtkt.com/train-running-status/{0}?StationName={1}&Date={2}'.format(train_no,station_code,date(date_non)))
    soup = BeautifulSoup(url.read(), 'lxml')
    ###################################################livedata json file#######################################################
    data = soup.find_all('script')
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
    ########################################################################################################################
    i = 0
    for code in stncodes:
        if (code == station_code):
            break
        i = i+1
    stnname = jsonfile['stations']
    finalvar =  {"Train No": train_no,
                 "Current Station": curstnname,
                 "Jounery Station": stnname[i]['stnCodeName'],
                 "Delay": stnname[i]['delayArr'],
                 "Schedule Arrival": stnname[i]['schArrTime'],
                 "Expected Arrival": stnname[i]['actArr'],
                 "Schedule Depature": stnname[i]['schDepTime'],
                 "Expected Departure": stnname[i]['actDep'],
                 "Last Updated": lastupdate}

    return jsonify(finalvar)

if __name__ == '__main__':
    app.run()
