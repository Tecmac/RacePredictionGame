import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="racing",
        user="postgres",
        password="")
except:
    print("Unable to connect to database")
cur = conn.cursor()

try:
    cur.execute("Create Table Spieler(test int)")
except:
    a = 1
    print(f"{a}Table " + " konnte NICHT erstellt werden bzw. bereits vorhanden")

conn.commit()
