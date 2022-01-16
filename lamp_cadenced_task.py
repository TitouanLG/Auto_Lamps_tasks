# -*- coding:Utf8 -*-

#######################
#  Routine d'allumage #
#     des lampes      #
#     GALATRAVE       #
#######################

#######################
#       NOTES
#  weekday()
#


#######################
## Import externe
import RPi.GPIO as GPIO
from datetime import datetime
import time
import sqlite3

#######################
## Liste des DEFINE
#22 = P1
#24 = P3
LAMP_PIN = 22
NC = 1

#######################
## Fonctions locales
def day_to_sec(day_obj):
    sec = 0
    #sec = int(str(day_obj.hour)) + int(str(day_obj.min)) + int(str(day_obj.sec))
    sec = day_obj.hour*3600 +day_obj.minute*60 +day_obj.second
    return sec

#######################
## Init
#GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LAMP_PIN, GPIO.OUT)   #GPIO
time.sleep(3)

#######################
## Globals Variables
lamp_last_state = GPIO.input(LAMP_PIN)


#######################
## MAIN SCRIPT
print("__--  LAMP_CADENCED_TASK  --__")
current_date = datetime.now()
print("Current date is:" +str(current_date))
print("Last State is:" +str(lamp_last_state))

#Recuperation des horaires et init de la DB
conn_DB = sqlite3.connect('Tasks.db')
cursor_DB = conn_DB.cursor()
cursor_DB.execute("""
CREATE TABLE IF NOT EXISTS horairesLamp(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     day TEXT,
     start_h_morning INTERGER,
     start_m_morning INTERGER,
     stop_h_morning INTERGER,
     stop_m_morning INTERGER,
     start_h_evening INTERGER,
     start_m_evening INTERGER,
     stop_h_evening INTERGER,
     stop_m_evening INTERGER
)
""")
conn_DB.commit()

db.close()

#Allumage conditionel matin
if(day_to_sec(current_date) >= day_to_sec(morning_start_date)) \
    and (day_to_sec(current_date) <= day_to_sec(morning_stop_date)):
    print("Lamps ON")
    GPIO.output(LAMP_PIN, GPIO.HIGH)
    if(lamp_last_state == False):
        print("Setting Lamps ON !")
    lamp_last_state = True
    time.sleep(1)

#Allumage conditionel soir
elif(day_to_sec(current_date) >= day_to_sec(evening_start_date)) \
   and (day_to_sec(current_date) <= day_to_sec(evening_stop_date)):
    print("Lamps ON")
    GPIO.output(LAMP_PIN, GPIO.HIGH)
    if(lamp_last_state == False):
        print("Setting Lamps ON !")
    lamp_last_state = True
    time.sleep(1)

else:
    print("lamps OFF")
    GPIO.output(LAMP_PIN, GPIO.LOW)
    if(lamp_last_state == True):
        print("Setting Lamps OFF .. ")
    lamp_last_state = False
    time.sleep(1)

print("__                          __")
print("  --         END          --  ")


    

