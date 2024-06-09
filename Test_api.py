import requests


uriBase                = "https://www.space-track.org"
requestLogin           = "/ajaxauth/login"
requestTLE             = "/basicspacedata/query/class/gp/EPOCH/%3Enow-30/MEAN_MOTION/%3E11.25/format/3le"

configUsr =  'batmansgrob@yandex.ru'
configPwd = 'Terraria2005!!!'

siteCred = {'identity': configUsr, 'password': configPwd}

def get_tle_data():
    with open("TLE_data.txt", 'w') as file:
        with requests.Session() as session:
            response = session.post(uriBase + requestLogin, data = siteCred)

            response = session.get(uriBase + requestTLE)

            file.write(response.text.replace('\r', ''))

get_tle_data()