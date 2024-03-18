import csv

import serial
import pymysql
import datetime
import datetime as dt

# Serielle Verbindung zum Arduino herstellen
ser = serial.Serial('COM5', 9600)  # 'COM4' an Ihre Umgebung anpassen

# Verbesserte Fehlerbehandlung bei der MySQL-Verbindung
try:
    db_rfid_cards = pymysql.connect(host='localhost', user='root', password='', database='rfid_cards')
    cursor = db_rfid_cards.cursor()

except pymysql.Error as e:
    print(f"Fehler bei der MySQL-Verbindung: {e}")
    exit(1)

try:
    while True:
        # Daten vom Arduino lesen und leere Zeilen ignorieren

        line1 = ''
        line2 = ''
        Pos_NR = ''
        rfid_uid2 = ''
        Vorname = ''
        Nachname = ''
        zeit = datetime.datetime.now()
        Uhrzeit = zeit.strftime('%H:%M:%S')  # Zeitstempel als String im aktuellen Format
        Status1 = ' KOMMEN '
        Status2 = ' GEHEN '
        Datum = str(dt.date.today())

        while not line1:
            line1 = ser.readline().decode().strip()
        while not line2:
            line2 = ser.readline().decode().strip()

        if line1 and line2:

            try:

                abfrage = """SELECT * FROM rfidcards WHERE rfid_uid1 = %s AND Datum = %s"""

                # Abfrage mit Variablen ausführen
                cursor.execute(abfrage, (line2, Datum))

                # Ergebnisse abrufen
                ergebnisse = cursor.fetchall()

                if not ergebnisse:
                    sql = f"""INSERT INTO rfidcards (Card_detected, rfid_uid1, Datum, Zeit, STATUS) Value(%s,%s,%s,%s,%s)"""
                    cursor.execute(sql, (line1, line2, Datum, Uhrzeit, Status1))
                    print(f"{Status1}: RFID-Karte mit Card detected:{line1} und UID: {line2} und Zeitstempel: {Datum} {Uhrzeit} erfolgreich gespeichert.")
                else:
                    letzter_status = ergebnisse[-1]
                    if letzter_status[4] == " KOMMEN ":
                        sql = f"""INSERT INTO rfidcards (Card_detected, rfid_uid1, Datum, Zeit, STATUS) Value(%s,%s,%s,%s,%s)"""
                        cursor.execute(sql, (line1, line2, Datum, Uhrzeit, Status2))
                        print(
                            f"{Status2}: RFID-Karte mit Card detected:{line1} und UID: {line2} und Zeitstempel: {Datum} {Uhrzeit} erfolgreich gespeichert.")
                    else:
                        sql = f"""INSERT INTO rfidcards (Card_detected, rfid_uid1, Datum, Zeit, STATUS) Value(%s,%s,%s,%s,%s)"""
                        cursor.execute(sql, (line1, line2, Datum, Uhrzeit, Status1))
                        print(
                            f"{Status1}: RFID-Karte mit Card detected:{line1} und UID: {line2} und Zeitstempel: {Datum} {Uhrzeit} erfolgreich gespeichert.")


                cursor.execute("SELECT * FROM mitarbeiter, rfidcards where rfid_uid1 = rfid_uid2 and rfidcards.rfid_uid1 = mitarbeiter.rfid_uid2")

                # CSV-Schreiber erstellen
                with open("rfid1.csv", "w", newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)

                    # Kopfzeile schreiben
                    csv_writer.writerow([i[0] for i in cursor.description])

                    # Datenzeilen schreiben
                    for row in cursor:
                        csv_writer.writerow(row)

                cursor.execute("SELECT * FROM mitarbeiter, rfidcards where Zeit >= ('8:00:00') and Zeit <= ('15:00:00')")

                # CSV - Pausen - Schreiber erstellen
                with open("Pausen.csv", "w", newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)

                    # Kopfzeile schreiben
                    csv_writer.writerow([i[0] for i in cursor.description])

                    # Datenzeilen schreiben
                    for row in cursor:
                        csv_writer.writerow(row)

                db_rfid_cards.commit()  # Änderungen comitten



            except (pymysql.Error, ValueError) as e:
                print(f"Fehler beim Speichern der RFID-Karte: {e}")



except KeyboardInterrupt:
    print("Programm beendet.")
finally:
    # Verbindung schließen, falls vorhanden
    if db_rfid_cards:
        db_rfid_cards.close()
