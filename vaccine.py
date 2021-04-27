'''
copied from : https://github.com/burgamacha/CVS-covid-vaccine-checker

This is a python script that requires you have python installed, or in a cloud environment.

This script scrapes the CVS website looking for vaccine appointments in the cities you list.
To update for your area, update the locations marked with ### below.

If you receive an error that says something is not install, type

pip install beepy

in your terminal.
'''

import urllib2
import time
import json
from twilio.rest import Client

def findAVaccine():
    hours_to_run = 16 ###Update this to set the number of hours you want the script to run.
    max_time = time.time() + hours_to_run*60*60
    while time.time() < max_time:
        try:
            state = 'CA'
            request = urllib2.Request("https://www.cvs.com/immunizations/covid-19-vaccine.vaccine-status.{}.json?vaccineinfo".format(state.lower()),
                            headers={"Referer":"https://www.cvs.com/immunizations/covid-19-vaccine"})
            r = urllib2.urlopen(request, timeout=20)
            payload = json.load(r)

            mappings = {}
            for item in payload["responsePayloadData"]["data"][state]:
                mappings[item.get('city')] = item.get('status')

            cities = ['ALAMEDA', 'ALBANY', 'BERKELEY', 'CONCORD', 'EMERYVILLE','FREMONT','OAKLAND', 'PLEASANT HILL', 'SAN LEANDRO','WALNUT CREEK']

            account_sid = 'XXXXXXXXXXX'
            auth_token = 'XXXXXXXXXXX'
            client = Client(account_sid, auth_token)

            open_appointments = []
            for key in mappings.keys():
                if key in cities:
                    if (mappings[key] != 'Fully Booked'):
                        open_appointments.append(key)

            if len(open_appointments) > 0 :
                message = client.messages \
                    .create(
                    body=str(open_appointments),
                    from_='+XXXXXXXXXXX', XXXXXXXXXXX
                    to='+XXXXXXXXXXX'
                )
                print('twilio message.sid: ' + str(message.sid))
                print(open_appointments)
                break
            else:
                print 'no slots: ' + str(time.localtime())
        except Exception as e:
            print(e)

        time.sleep(60*2) ##This runs every 60 seconds. Update here if you'd like it to go every 10min (600sec)

findAVaccine() ###this final line runs the function. Your terminal will output the cities every 60seconds
