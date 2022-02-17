# -*- coding:Utf8 -*-

#######################
#  Routine d'affectation#
#     de l'heure      #
#      solaire        #
#     GALATRAVE       #
#######################

#######################
#      DEV NOTES
# 
#


#######################
## Import externe
import RPi.GPIO as GPIO
from datetime import datetime
import time
import sqlite3
from suntime import Sun 
from geopy.geocoders import Nominatim 

#######################
## Liste des DEFINE
weekDays = ("Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche")

#######################
## Fonctions locales
geolocator = Nominatim(user_agent="geoapiExercises") 


#######################
## Init
#GPIO.setwarnings(False)

time.sleep(3)

#######################
## Globals Variables

#######################
## MAIN SCRIPT
print("__--  SET_SOLAR_TIME_TASK  --__")
#Getting current position latitude and longitude
home_location = geolocator.geocode("Rodez")
sun_info = Sun(home_location.latitude, home_location.longitude)

current_date = datetime.now()
current_day = current_date.weekday()
current_day_str = weekDays[current_day]

sun_rise = sun_info.get_local_sunrise_time(current_date)
sun_dusk = sun_info.get_local_sunset_time(current_date)

print("Current date is:" +str(current_date))
print("Today is a:" +current_day_str)
print("Sunrise = " +sun_rise.strftime('%H:%M'))
print("Sunset  = " +sun_dusk.strftime('%H:%M'))

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
    print('Erreur la table existe déjà')

except Exception as e:
    print("Erreur globale sur la Tasks.DB")

finally:
    print("..DB ouverte")


## Setting hours for sunrise
DB_request = """UPDATE horairesLamp 
    SET stop_h_morning = """ +"'" +sun_rise.hour +"'" """,
        stop_m_morning = """ +"'" +sun_rise.minute +"'" """,
        WHERE day = """ +"'" +current_day_str +"'"
cursor_DB.execute(DB_request)
print('Today Morning Stop date is :' +str(sun_rise))

## Setting hours for sunset
DB_request = """UPDATE horairesLamp 
    SET start_h_evening = """ +"'" +sun_dusk.hour +"'" """,
        start_m_evening = """ +"'" +sun_dusk.minute +"'" """,
        WHERE day = """ +"'" +current_day_str +"'"
cursor_DB.execute(DB_request)
print('Today evening Start date is :' +str(sun_dusk))

conn_DB.close()

print("__                          __")
print("  --         END          --  ")


    

