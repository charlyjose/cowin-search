from datetime import datetime, timedelta
import winsound
import requests
import time
import sys
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def disp(item):
    print('name: ', item['name'])
    print('address: ', item['address'])
    print('block_name: ', item['block_name'])
    print('pincode: ', item['pincode'])
    print('fee_type:', item['fee_type'])
    print('date:', item['date'])
    print('available_capacity_dose1: ', item['available_capacity_dose1'])
    print('available_capacity_dose2: ', item['available_capacity_dose2'])
    print('min_age_limit: ', item['min_age_limit'])
    print('vaccine: ', item['vaccine'])
    print()
    avail = {}
    avail['name'] = item['name']
    avail['address'] = item['address']
    avail['block_name'] = item['block_name']
    avail['pincode'] = item['pincode']
    avail['fee_type'] = item['fee_type']
    avail['date'] = item['date']
    avail['available_capacity_dose1'] = item['available_capacity_dose1']
    avail['available_capacity_dose2'] = item['available_capacity_dose2']
    avail['min_age_limit'] = item['min_age_limit']
    avail['vaccine'] = item['vaccine']
    return avail

def make_sound():
    frequency = 2500
    duration = 1000
    winsound.Beep(frequency, duration)
    frequency = 1000
    duration = 1000
    winsound.Beep(frequency, duration)

def check_conditions(item):
    if item['vaccine'] == 'COVISHIELD':
        if item['available_capacity_dose2'] > 0:
            if item['fee_type'] == 'Free':
                return True
    return False

def get_weeks_dates():
    one_weeks_date = []
    this_date = datetime.now()
    for _ in range(16):
        date = this_date.strftime("%d-%m-%Y")
        one_weeks_date.append(date)
        this_date += timedelta(1)
    return(one_weeks_date)

def file_write(item, date):
    file = open(f'{date}.txt', 'a')
    print(item)
    file.write(str(item)+'\n\n')
    file.close()

def search_vaccine(date):
    # date = sys.argv[1] # '08-06-2021'
    resp = requests.get(f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id=307&date={date}')
    if resp.status_code != 200:
        print('Error')
    for item in resp.json()['sessions']:
        # disp(item)
        if check_conditions(item):
            # make_sound()
            winsound.MessageBeep(type=winsound.MB_ICONHAND)
            avail = disp(item)
            file_write(item=avail, date=date)
    # time.sleep(1)
    cls()

def conwinator():
    dates = get_weeks_dates()
    i = 0
    while True:
        print('Searching for Date: ', dates[i])
        date = dates[i]
        search_vaccine(date=date)
        i+=1
        if i == 16:
            i = 0

while True:
    try:
        conwinator()
    except KeyboardInterrupt:
        break
    except:
        continue
