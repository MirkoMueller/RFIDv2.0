import csv
import time
from tkinter import ttk


import customtkinter
import customtkinter as ctk
from PIL import ImageTk, Image
from tkcalendar import Calendar
import tkinter as tk

root = customtkinter.CTk()
root.title(' ZEITERFASSUNG ')
root.geometry('950x650')
root.resizable(False, False)

# CSV DATEI
def fill_textbox_from_csv():
    # Annahme: Die CSV-Datei hat Spalten "spalte1", "spalte2" und "spalte3"
    with open('rfid1.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            spalte0 = row.get('Pos_NR', '')  # Wert aus der 'spalte0'
            spalte1 = row.get('Datum', '')  # Wert aus der 'spalte1'
            spalte2 = row.get('Zeit', '')  # Wert aus der 'spalte2'
            spalte3 = row.get('Vorname', '')  # Wert aus der 'spalte3'
            spalte4 = row.get('Nachname', '')  # Wert aus der 'spalte4'
            spalte5 = row.get('STATUS', '')  # Wert aus der 'spalte5'
            text_data = f"{spalte0} |{spalte1} | {spalte2} | {spalte3} | {spalte4} | {spalte5}"  # Kombiniere die Werte
            textbox.insert( 'end', text_data + '\n')  # Füge den Wert in das Textfeld ein


# TEXTBOX + Button
textbox = customtkinter.CTkTextbox(root, width=600, height=320, border_width=6, border_color="black", corner_radius=12)
button_fill = customtkinter.CTkButton(root, text=" LOGIN ABFRAGEN", command=fill_textbox_from_csv)
textbox.grid(row=1, column=6, padx=(15, 15), pady=(20, 20))
button_fill.grid(row=0, column=0, padx=(15, 15), pady=(20, 20))


# Pausenzeiten abfragen

def fill_textbox1_from_csv():
    # Annahme: Die CSV-Datei hat Spalten "spalte1", "spalte2" und "spalte3"
    with open('Pausen.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            spalte0 = row.get('Pos_NR', '')  # Wert aus der 'spalte0'
            spalte1 = row.get('Vorname', '')  # Wert aus der 'spalte1'
            spalte2 = row.get('Nachname', '')  # Wert aus der 'spalte2'
            spalte3 = row.get('Zeit', '')  # Wert aus der 'spalte3'

            text_data = f"{spalte0} |{spalte1} |{spalte2} |{spalte3}"  # Kombiniere die Werte
            textbox1.insert('end', text_data + '\n')  # Füge den Wert in das Textfeld ein


# TEXTBOX + Button
textbox1 = customtkinter.CTkTextbox(root, width=500, height=100, border_width=6, border_color="black", corner_radius=12)
button_fill = customtkinter.CTkButton(root, text=" PAUSEN ABFRAGEN", command=fill_textbox1_from_csv)
textbox1.grid(row=2, column=6, padx=(15, 15), pady=(20, 20))
button_fill.place(x=45, y=90)


# Kalender
frame = ctk.CTkFrame(root, width=200, height=150, border_width=6, border_color="black", corner_radius=12)
frame.place(x=10, y=460)
style = ttk.Style(root)
style.theme_use("default")
cal = Calendar(frame, selectmode='day', locale='de_DE', disabledforeground='red',
               cursor="hand2", background=ctk.ThemeManager.theme["CTkFrame"]["fg_color"][1],
               selectbackground=ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
cal.grid(row=1, column=0, padx=(15, 15), pady=5)

def digital_clock():
    time_live = time.strftime("%H:%M:%S")
    label = customtkinter.CTkLabel(root, width=350, height=30, corner_radius=6, text="",
                                   fg_color="dodgerblue", font=("Arial", 25))
    label.grid(row=0, column=6, padx=(15, 15), pady=(20, 20))

    label.configure(width=100, height=40,text=time_live)
    label.after(200, digital_clock)

# Uhr
text_font = ("Boulder", 68, 'bold')
background = "#f2e750"
foreground = "#363529"

# Image SFZ
# Initialize the file name in a variable
path = "SFZ200x200.jpg"
# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("./SFZ200x200.jpg"))
# Breite und Höhe festlegen
new_width = 350
new_height = 350

label = customtkinter.CTkLabel(root, width=20, height=20, text='', image=img)
label.grid(row=1, column=0, padx=(15, 15), pady=(70,20))

digital_clock()
root.mainloop()


