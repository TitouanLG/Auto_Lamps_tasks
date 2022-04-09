# -*- coding:Utf8 -*-

#######################
#  Routine d'allumage #
#     des lampes      #
#     GALATRAVE       #
#######################

#######################
#      DEV NOTES
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
weekDays = ("Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche")

#######################
## Fonctions locales
def day_to_sec(day_obj):
    sec = 0
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
current_day = current_date.weekday()
current_day_str = weekDays[current_day]
print("Current date is:" +str(current_date))
print("Today is a:" +current_day_str)
print("Last State is:" +str(lamp_last_state))

#Recuperation des horaires et init de la DB
conn_DB = sqlite3.connect('Tasks.db')
cursor_DB = conn_DB.cursor()

try:
    cursor_DB.execute("""
    CREATE TABLE IF NOT EXISTS horairesLamp(
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        day TEXT,
        start_h_morning INTEGER,
        start_m_morning INTEGER,
        stop_h_morning INTEGER,
        stop_m_morning INTEGER,
        start_h_evening INTEGER,
        start_m_evening INTEGER,
        stop_h_evening INTEGER,
        stop_m_evening INTEGER
    )
    """)
    conn_DB.commit()

except sqlite3.OperationalError:
    print('Erreur la table existe deja')

except Exception as e:
    print("Erreur globale sur la Tasks.DB")

finally:
    print("..DB ouverte")


## Getting hours for sunrise
DB_request = """SELECT day , morning , evening FROM joursLamp WHERE day = """ +"'" +current_day_str +"'"
cursor_DB.execute(DB_request)
raw_light_needed = cursor_DB.fetchone()
morning_light_needed = int(raw_light_needed[1])
evening_light_needed = int(raw_light_needed[2])

DB_request = """SELECT day, start_h_morning , start_m_morning FROM horairesLamp WHERE day = """ +"'" +current_day_str +"'"
cursor_DB.execute(DB_request)
raw_date = cursor_DB.fetchone()
morning_start_date = datetime(NC,NC,NC,raw_date[1],raw_date[2],0)
print('Today Morning Start date is :' +str(morning_start_date))

DB_request = """SELECT day, stop_h_morning , stop_m_morning FROM horairesLamp WHERE day = """ +"'" +current_day_str +"'"
cursor_DB.execute(DB_request)
raw_date = cursor_DB.fetchone()
morning_stop_date = datetime(NC,NC,NC,raw_date[1],raw_date[2],0)
print('Today Morning Stop date is :' +str(morning_stop_date))

## Getting hours for sunset
DB_request = """SELECT day, start_h_evening , start_m_evening FROM horairesLamp WHERE day = """ +"'" +current_day_str +"'"
cursor_DB.execute(DB_request)
raw_date = cursor_DB.fetchone()
evening_start_date = datetime(NC,NC,NC,raw_date[1],raw_date[2],0)
print('Today Evening Start date is :' +str(evening_start_date))

DB_request = """SELECT day, stop_h_evening , stop_m_evening FROM horairesLamp WHERE day = """ +"'" +current_day_str +"'"
cursor_DB.execute(DB_request)
raw_date = cursor_DB.fetchone()
evening_stop_date = datetime(NC,NC,NC,raw_date[1],raw_date[2],0)
print('Today Evening Stop date is :' +str(evening_stop_date))

conn_DB.close()

#Allumage conditionel matin
if(day_to_sec(current_date) >= day_to_sec(morning_start_date)) \
    and (day_to_sec(current_date) <= day_to_sec(morning_stop_date)):
    if(morning_light_needed):
        print("Lamps ON needed")
        GPIO.output(LAMP_PIN, GPIO.HIGH)
        if(lamp_last_state == False):
            print("Setting Lamps ON !")
        lamp_last_state = True
        time.sleep(1)
    else:
        print("Lamps not today")

#Allumage conditionel soir
elif(day_to_sec(current_date) >= day_to_sec(evening_start_date)) \
    and (day_to_sec(current_date) <= day_to_sec(evening_stop_date)):
    if(evening_light_needed):
        print("Lamps ON needed")
        PIO.output(LAMP_PIN, GPIO.HIGH)
        if(lamp_last_state == False):
            print("Setting Lamps ON !")
        lamp_last_state = True
        time.sleep(1)
    else:
        print("Lamps not today")

else:
    print("lamps OFF")
    GPIO.output(LAMP_PIN, GPIO.LOW)
    if(lamp_last_state == True):
        print("Setting Lamps OFF .. ")
    lamp_last_state = False
    time.sleep(1)

print("__                          __")
print("  --         END          --  ")


    

