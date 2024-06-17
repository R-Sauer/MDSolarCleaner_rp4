import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage, ttk
from ttkthemes import themed_tk as tkt # ttkthemes
from tkinter import filedialog
import csv
import random
import string
from time import strftime
import os

# Kommunikation
import sqlite3

def send_to_topic(topic, message):
    conn = sqlite3.connect('cloud.db')
    c = conn.cursor()
    c.execute(f"INSERT INTO {topic} (message) VALUES (?)", (message,))
    conn.commit()
    conn.close()

#Methoden
def time(): #bearbeitet den Text vom Label "Zeit", indem der Inhalt auf die aktuelle Uhrzeit gesetzt wird
    zeit.config(text=strftime("%H:%M:%S %p"))
    zeit.after(1000, time)  #Nach 1000 Millisekunden (1 Sekunde) wird die Funktion "time" wieder aufgerufen

def sendConfig(export=False):   #sends config to chip
    output = markeB1Var.get()+";"+materialB1Var.get()+";"+durchmesserB1Var.get()+";"+drehzahlB1Var.get()+";"+markeB2Var.get()+";"+materialB2Var.get()+";"+durchmesserB2Var.get()+";"+drehzahlB2Var.get()+";"+staubInputVar.get()+";"+probeInputVar.get()+";"+verfahrwegInput.get()+";"+drehRichtung1.get()+";"+drehRichtung2.get()+";"+str(nullHoehe.get())+";"+str(aktuelleHoehe.get())
    if (export == False):
        print(output)
        send_to_topic("gui", output)
    else:
        return output

def variableTracing(*args):
    a = markeB1Var.get()
    b = materialB1Var.get()
    c = durchmesserB1Var.get()
    d = drehzahlB1Var.get()
    e = markeB2Var.get()
    f = materialB2Var.get()
    g = durchmesserB2Var.get()
    h = drehzahlB2Var.get()
    i = staubInputVar.get()
    j = probeInputVar.get()
    k = verfahrwegInput.get()
    l = drehRichtung1.get()
    m = drehRichtung2.get()
    n = nullHoehe.get()
    o = aktuelleHoehe.get()

    if a and b and c and d and e and f and g and h and i and j and k and l and m and n and o:
        start.config(state="normal")
        download.config(state="normal")
    else:
        start.config(state="disabled")
        download.config(state="disabled")

    if n:
        inputLabelNullHoehe = tk.Label(window, text=f"{nullHoehe.get()}" + "cm").grid(row=1,column=3,sticky="NSEW")
        hoehe1.config(state="disabled")
    else:
        hoehe1.config(state="normal")
    if o:  
        inputLabelAktuelleHoehe = tk.Label(window, text=f"{aktuelleHoehe.get()}"+ "cm").grid(row=2,column=3,sticky="NSEW")

    if n and o:
        labelDifferenz = ttk.Label(window, text = "Differenzhoehe: "+ f"{aktuelleHoehe.get() - nullHoehe.get()}"+ "cm").grid(row=3,column=1,sticky="NSEW")

def click(button, num):
    verfahrwegInput.set(num)
    button.state(['pressed'])

    if num != 1:
        first.state(["!pressed"])
    if num != 2:
        second.state(["!pressed"])
    if num != 3:
        third.state(["!pressed"])
    if num != 4:
        fourth.state(["!pressed"])

def export_file(): # DOWNLOAD
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        # Generate a 2D array of random characters
        rows = 5
        cols = 5
        random_data = [[random.choice(string.ascii_uppercase) for _ in range(cols)] for _ in range(rows)]

        #config_array = sendConfig(export=True)

        # Write the array to a CSV file
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(random_data)

        print(f"Data exported to {file_path}")

def is_number(input_value):
    try:
        float_value = float(input_value)
        return True
    except ValueError:
        return False

def check_input():
    labels_test = [durchmesserB1Var.get(), drehzahlB1Var.get(), durchmesserB2Var.get(), drehzahlB2Var.get(), staubInputVar.get(), nullHoehe.get(), aktuelleHoehe.get()]
    
    for label in labels_test:
        user_input = label

        if is_number(user_input):
            True
        else:
            messagebox.showerror("Error", "Input is not a number.")
            return False
    
    sendConfig()

#window setup
window = tkt.ThemedTk(theme="arc",background="white")
window.title('GUI TEST')

style = ttk.Style()
style.configure("Bold.TLabel", font=("bold"))

start = ttk.Button(
    window,
    text = "START",
    command = check_input,   #add sendConfig after proofing
    state = "disabled"
)

download = ttk.Button(
    window,
    text="DOWNLOAD",
    state="disabled",
    command=export_file
)

#Variablendeklarationen
markeB1Var= tk.StringVar(window)
materialB1Var = tk.StringVar(window)
durchmesserB1Var = tk.StringVar(window)
drehzahlB1Var = tk.StringVar(window)

markeB2Var = tk.StringVar(window)
materialB2Var = tk.StringVar(window)
durchmesserB2Var = tk.StringVar(window)
drehzahlB2Var = tk.StringVar(window)

staubInputVar = tk.StringVar(window)
probeInputVar = tk.StringVar(window)

verfahrwegInput = tk.StringVar(window)

drehRichtung1 = tk.StringVar(window)
drehRichtung2 = tk.StringVar(window)

optionDrehrichtung = [
    "Links",
    "Rechts"
]

kopplungOptionen = [
    "Moeglichkeit 1",
    "Moeglichkeit 2",
    "Moeglichkeit 3",
    "Moeglichkeit 4"
]

nullHoehe = tk.IntVar(window)
aktuelleHoehe = tk.IntVar(window)
kopplung = tk.StringVar(window)
#Variable tracing to catch changes in entries
markeB1Var.trace("w",variableTracing)
materialB1Var.trace("w",variableTracing)
durchmesserB1Var.trace("w",variableTracing)
drehzahlB1Var.trace("w",variableTracing)

markeB2Var.trace("w",variableTracing)
materialB2Var.trace("w",variableTracing)
durchmesserB2Var.trace("w",variableTracing)
drehzahlB2Var.trace("w",variableTracing)

staubInputVar.trace("w",variableTracing)
probeInputVar.trace("w",variableTracing)

verfahrwegInput.trace("w",variableTracing)

drehRichtung1.trace("w",variableTracing)
drehRichtung2.trace("w",variableTracing)
#Grid configuration
for i in range(10):
    tk.Grid.rowconfigure(window,i,weight=1)
    tk.Grid.columnconfigure(window,i,weight=1)

#start button mit Icon
os.chdir(os.path.dirname(os.path.abspath(__file__)))
image = PhotoImage(file="power.png")
image = image.subsample(6)
startImage = ttk.Button(
    window,
    image = image,
)
startImage.grid(column = 0, row = 0, rowspan=4, sticky="NSEW")

#verfahrwege buttons
title1 = ttk.Label(window, text= "U-Vertikal", anchor="center").grid(column=0,row=4,sticky = "NSEW")
image1 = PhotoImage(file="Bahn1.png").subsample(6)
first = ttk.Button(
    window,
    image = image1,
    command=lambda : click(first,1),
)
first.grid(column=0,row=5,sticky = "NSEW", padx=10,pady=10)


title2 = ttk.Label(window, text= "U-Horizontal", anchor="center").grid(column=1,row=4,sticky = "NSEW")
image2 = PhotoImage(file="Bahn2.png").subsample(6)
second = ttk.Button(
    window,
    image = image2,
    command=lambda : click(second,2),
)
second.grid(column=1,row=5, sticky = "NSEW", padx=10,pady=10)

title3 = ttk.Label(window, text= "Straight Vertikal", anchor="center").grid(column=2,row=4,sticky = "NSEW")
image3 = PhotoImage(file="Bahn3.png").subsample(6)
third = ttk.Button(
    window,
    image = image3,
    command=lambda : click(third,3),
)
third.grid(column=2,row=5,sticky = "NSEW", padx=10,pady=10)

title4 = ttk.Label(window, text= "Straight Horizontal", anchor="center").grid(column=3,row=4,sticky = "NSEW")
image4 = PhotoImage(file="Bahn4.png").subsample(6)
fourth = ttk.Button(
    window,
    image = image4,
    command=lambda : click(fourth,4),
)
fourth.grid(column=3,row=5,sticky = "NSEW", padx=10,pady=10)

#Parameter Staub
staubLabel = ttk.Label(window, text= "Staub").grid(column=4,row=1,sticky = "NSEW")
staubInput = ttk.Entry(window, textvariable=staubInputVar)
staubInput.grid(column=5,row=1,sticky = "NSEW")
staubLabelUnit = ttk.Label(window,text="g/m^2").grid(column=6,row=1,sticky = "NSEW")

probetyp = ttk.Label(window, text="Probetyp").grid(column=4,row=2,sticky = "NSEW")
probeInput = ttk.Entry(window, textvariable=probeInputVar)
probeInput.grid(column=5,row=2,sticky = "NSEW")

#Buerste 1
labelB1 = ttk.Label(window, text="Buerste 1").grid(row=6, column=0,sticky = "NSEW")
labelM1 = ttk.Label(window, text="Material").grid(row=7, column=0,sticky = "NSEW")
labelD1 = ttk.Label(window, text= "Durchmesser [mm]").grid(row=8, column=0,sticky = "NSEW")
labeln1 = ttk.Label(window, text="Drehzahl [1/min]").grid(row=9, column=0,sticky = "NSEW")
labelDrop1 = ttk.Label(window, text="Drehrichtung").grid(row=10,column=0,sticky="NSEW")

markeB1 = ttk.Entry(window, textvariable=markeB1Var)
markeB1.grid(row=6, column=1,sticky = "NSEW")
materialB1 = ttk.Entry(window, textvariable=materialB1Var)
materialB1.grid(row=7, column=1,sticky = "NSEW")
durchmesserB1 = ttk.Entry(window, textvariable=durchmesserB1Var)
durchmesserB1.grid(row=8, column=1,sticky = "NSEW")
drehzahlB1 = ttk.Entry(window, textvariable=drehzahlB1Var)
drehzahlB1.grid(row=9, column=1,sticky = "NSEW")

drop1 = tk.OptionMenu(window,drehRichtung1,*optionDrehrichtung)
drop1.grid(row=10,column=1,sticky="NSEW")
#Buerste 2
labelB2 = ttk.Label(window, text="Buerste 2").grid(row=6, column=2,sticky = "NSEW")
labelM2 = ttk.Label(window, text="Material").grid(row=7, column=2,sticky = "NSEW")
labelD2 = ttk.Label(window, text= "Durchmesser [mm]").grid(row=8, column=2,sticky = "NSEW")
labeln2 = ttk.Label(window, text="Drehzahl [1/min]").grid(row=9, column=2,sticky = "NSEW")
labelDrop2 = ttk.Label(window, text="Drehrichtung").grid(row=10,column=2,sticky="NSEW")

markeB2 = ttk.Entry(window, textvariable=markeB2Var)
markeB2.grid(row=6, column=3,sticky = "NSEW")
materialB2 = ttk.Entry(window, textvariable=materialB2Var)
materialB2.grid(row=7, column=3,sticky = "NSEW")
durchmesserB2 = ttk.Entry(window, textvariable=durchmesserB2Var)
durchmesserB2.grid(row=8, column=3,sticky = "NSEW")
drehzahlB2 = ttk.Entry(window, textvariable=drehzahlB2Var)
drehzahlB2.grid(row=9, column=3,sticky = "NSEW")

drop2 = tk.OptionMenu(window,drehRichtung2,*optionDrehrichtung)
drop2.grid(row=10,column=3,sticky="NSEW")
# Label Placeholders
_l1 = ttk.Label(window).grid(row=0, column=2,columnspan=3,sticky="NSEW")
_l2 = ttk.Label(window).grid(row=3, column=2,columnspan=3,sticky="NSEW")

#Hoehenabstaende
labelNullHoehe = ttk.Label(window, text="Nullhoehe:").grid(row=1,column=1,sticky="NSEW")
labelAktuelleHoehe = ttk.Label(window,text="Aktuelle Hoehe:").grid(row=2, column=1,sticky="NSEW")

hoehe1 = ttk.Entry(window, textvariable=nullHoehe)
hoehe1.grid(row=1, column=2, sticky="NSEW")
hoehe2 = ttk.Entry(window, textvariable=aktuelleHoehe)
hoehe2.grid(row=2,column=2,sticky="NSEW")
#start und export button
start.grid(column=1,row=11,rowspan=2,padx=10,pady=10,sticky = "NSEW")
download.grid(column=2,row=11,rowspan=2,padx=10,pady=10,sticky = "NSEW")

#Uhrzeit anzeigen
zeit = ttk.Label(window, text="INIT")
zeit.grid(column=4,row=11,sticky = "NSEW")
time()

#kopplungen
kopplungLabel = ttk.Label(window,text="Kopplungseinstellungen").grid(row=3,column=4,sticky="NSEW")

drop = tk.OptionMenu(window,kopplung,*kopplungOptionen)
drop.grid(row=3,column=5,sticky="NSEW")
   
window.mainloop()



