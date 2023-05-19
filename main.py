import psycopg2
import urllib.request, json
from DataFetcher import DataFetcher

try:
    conn = psycopg2.connect(  # making a connection to the server
            host="localhost",
            database="racing",
            user="postgres",
            password="")
except:
    print("Unable to connect to database")

cur = conn.cursor()

fetcher = DataFetcher(host="localhost", database="racing", user="postgres", password="")
fetcher.fetchCircuits()
fetcher.fetchDrivers()
fetcher.fetchRace()
fetcher.fetchRaceresults()


# tabelle grandprix in circuits umbennen
conn.commit()
cur.close()
conn.close()
    # Get the json data from the website: drivers,grand prix,Rennergebnis
    # fetch it in the database
