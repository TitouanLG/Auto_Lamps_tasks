# -*- coding:Utf8 -*-

#######################
#  Routine d'affectation#
#     de l'heure      #
#      solaire        #
#     GALATRAVE       #
#######################

#######################
#      DEV NOTES
#  Rajouter des lignes (ou autre)
#  pour activer le matin / soir
#  par des booleans


#######################
## Import externe
from datetime import datetime, timedelta
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

time.sleep(3)

#######################
## Globals Variables

#######################
## Globals Functions
def sql_create_horairesLamp_table(conn, cursor):
    try:
        cursor.execute("""
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
        conn.commit()

    except sqlite3.OperationalError:
        print('Info: la table hoariresLamp existe déjà')
        return True

    except Exception as e:
        print(e)
        print("Erreur globale sur la Tasks.DB")
        return False

    finally:
        print("..DB ouverte")
        return True

def sql_create_joursLamp_table(conn, cursor):
    #creating table joursLamp..
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS joursLamp(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            day TEXT,
            morning INTEGER,
            evening INTEGER
        )
        """)
        conn.commit()

    except sqlite3.OperationalError:
        print('Info: la table joursLamp existe deja')
        return True

    except Exception as e:
        print(e)
        print("Erreur globale sur la Tasks.DB")
        return False

    finally:
        print("..table joursLamp newly created !")
        try:
            cursor.execute("""
            INSERT INTO joursLamp (day,morning,evening)
                VALUES
                    (Lundi,1,1),
                    (Mardi,1,1),
                    (Mercredi,1,1),
                    (Jeudi,1,1),
                    (Vendredi,1,1),
                    (Samedi,1,1),
                    (Dimanche,1,1);
            """)
            conn.commit()

        except sqlite3.OperationalError:
            print('Info: la table joursLamp est deja peuplee')

        except Exception as e:
            print("Erreur globale sur la Tasks.DB")

        finally:
            print("..7 lines added into joursLamp!")


#######################
## MAIN SCRIPT
print("__--  SET_SOLAR_TIME_TASK  --__")
# Getting current position latitude and longitude
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

# Recuperation des horaires et init de la DB
conn_DB = sqlite3.connect('Tasks.db')
cursor_DB = conn_DB.cursor()

# Only for the DB creation :
#sql_create_horairesLamp_table(conn_DB, cursor_DB)
#sql_create_joursLamp_table(conn_DB, cursor_DB)

## Setting hours for sunrise
time_offset = timedelta(hours = 0, minutes = 0)
sun_rise = sun_rise + time_offset
DB_request = """UPDATE horairesLamp
    SET stop_h_morning = """ +str(sun_rise.hour) +""",
        stop_m_morning = """ +str(sun_rise.minute) +"""
    WHERE day = """ +"'" +current_day_str +"'"
print(DB_request)
print(cursor_DB.execute(DB_request))
print('Today Morning Stop date is :' +str(sun_rise))

## Setting hours for sunset
time_offset = timedelta(hours = 0, minutes = 20)
sun_dusk = sun_dusk + time_offset
DB_request = """UPDATE horairesLamp 
    SET start_h_evening = """ +str(sun_dusk.hour) +""",
        start_m_evening = """ +str(sun_dusk.minute) +"""
    WHERE day = """ +"'" +current_day_str +"'"
print(DB_request)
print(cursor_DB.execute(DB_request))
print('Today evening Start date is :' +str(sun_dusk))

conn_DB.commit()
conn_DB.close()

print("__                          __")
print("  --         END          --  ")
