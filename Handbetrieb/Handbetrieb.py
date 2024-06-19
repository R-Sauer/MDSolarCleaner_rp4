import tkinter as tk
from gpiozero import Button
import RPi.GPIO as GPIO
from time import strftime
from tkinter import messagebox
from tkinter import PhotoImage, ttk
from SerialReadToDB_FSM import *
import CSVwriter
from multiprocessing.connection import Connection
#from ttkthemes import themed_tk as tkt # ttkthemes

import motor_steuerung

try:
 import RPi.GPIO as GPIO
except ImportError:
 import SimulRPi.GPIO as GPIO
#import RPi.GPIO as GPIO

#button array to store all the buttons created 
buttons=[]

# Function to toggle power of step motor
def disable_buttons():
    for button in buttons:
        button.config(state=tk.DISABLED)

def enable_buttons():
    for button in buttons:
        button.config(state=tk.NORMAL)

def toggle_power():
    global buttons_disabled
    if buttons_disabled:
        enable_buttons()
    else:
        disable_buttons()
    buttons_disabled = not buttons_disabled

buttons_disabled = True


def handbetrieb(databasePath: str, sensorColumns: list[str], readSerialcommandPipe: Connection):

    # GPIO-Pins für die SchrittMotorsteuerung
    motorY_step_pin = 17 # Step-Pin für Motor Y/1
    motorY_dir_pin = 27 # Richtungspin für Motor Y/1
    motorX_step_pin = 25 # Step-Pin für Motor X/2
    motorX_dir_pin = 8 # Richtungspin für Motor X/2
    #Endstoppspins
    endstop1_pin = 14
    endstop2_pin = 15
    
    # GPIO-Pins für die Bürstenmotorsteuerung
    motor_pwm_pin_1 = 18  # PWM-Pin für Motor 1 Geschwindigkeitssteuerung
    motor_pwm_pin_2 = 23  # PWM-Pin für Motor 2 Geschwindigkeitssteuerung

    # Function for emergency stop
    def emergency_stop():
        motorY.stop_motor()
        print('motor stop')
        brush_motor_1.stop()
        brush_motor_2.stop()

    #Implemetierung der SchrittMotor Klasse
    motorY = motor_steuerung.StepMotor(motorY_step_pin,motorY_dir_pin,endstop1_pin,endstop2_pin)
    motorX = motor_steuerung.StepMotor(motorX_step_pin,motorX_dir_pin,endstop1_pin,endstop2_pin)

    # Bürstenmotoren initialisieren
    brush_motor_1 = motor_steuerung.BrushMotor(motor_pwm_pin_1)
    brush_motor_2 = motor_steuerung.BrushMotor(motor_pwm_pin_2)

    def getTime(): #bearbeitet den Text vom Label "Zeit", indem der Inhalt auf die aktuelle Uhrzeit gesetzt wird
        zeit.config(text=strftime("%H:%M:%S %p"))
        zeit.after(1000, getTime)  #Nach 1000 Millisekunden (1 Sekunde) wird die Funktion "time" wieder aufgerufen

    ###################################################################################################
    ####################### Schrittmotor Funktionen Beginn ############################################
    ###################################################################################################


    # Function for Schrittmotor stop
    def Schrittmotor_stop():
            motorY.stop_motor()
            print('motor stop')

    ## Function to move step motor continuosus up (ARROW UP)
    def move_step_motor_Y_continuous_up():
        # Define the function for continuous motor movement
        def motor_Y_continuous_up():
            # Make one step up
            motorY.makeSteps(1, 0)
            print('motor Y continuous_up')
            # Check if the button is still pressed
            if btn_step_motor_Y_continuous_up_pressed.get():
                # Schedule the function to run again after 100 milliseconds
                root.after(1, motor_Y_continuous_up)

        # Call the inner function to start the continuous movement
        motor_Y_continuous_up()

    # Function to move step motor continuosus down (ARROW DOWN)
    def move_step_motor_Y_continuous_down():
            # Define the function for continuous motor movement
        def motor_Y_continuous_down():
            # Make one step up
            motorY.makeSteps(1, 1)
            print('motor Y continuous_down')
            # Check if the button is still pressed
            if btn_step_motor_Y_continuous_down_pressed.get():
                # Schedule the function to run again after 100 milliseconds
                root.after(1, motor_Y_continuous_down)

        # Call the inner function to start the continuous movement
        motor_Y_continuous_down()

    # Function to move step motor up with steps (DIRECTION UP WITH STEPS)
    def move_step_motor_Y_discrete_up():
    # Get the number of steps from the input field
        try:
            steps = int(entry_steps.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid number of steps")
            return

        # Define the function for discontinuous motor movement
        def motor_Y_up_discrete():
            # Make one step up
            motorY.start_steps(steps,0)
            print('motor Y up_discrete')

        # Call the inner function to start the movement
        motor_Y_up_discrete()
            
    # Function to move step motor down with steps (DIRECTION DOWN WITH STEPS)
    def move_step_motor_Y_discrete_down():
    # Get the number of steps from the input field
        try:
            steps = int(entry_steps.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid distance")
            return

        # Define the function for continuous motor movement
        def motor_Y_discrete_down():
            # Make one step down
            motorY.start_steps(steps, 1)
            print('motor Y discrete down')

        # Call the inner function to start the movement
        motor_Y_discrete_down()

    ##################################################################################################
    ####################### Schrittmotor Funktionen Ende ############################################
    ##################################################################################################
            
    #Konzept für Schrittmotor X
    #wenn für X Richtung auch ein Schrittmotor benutzt wird, kann die gleiche Konzepte von Y Richtung genutzt werden.

    ###################################################################
    ######### Bürstenmotoren Funtionen Beginn #########################
    ###################################################################

    # Function to control brushed motor	
    def move_brushmotor(BrushMotor , direction):
        if direction == 'Vorwärts':
            if(BrushMotor.getSpeedInPercent() < 0):
                BrushMotor.setSpeedPercent(-BrushMotor.getSpeedInPercent())
            BrushMotor.move()
            print("forward")
        elif direction == 'Ruckwärts':
            if(BrushMotor.getSpeedInPercent() > 0):
                BrushMotor.setSpeedPercent(-BrushMotor.getSpeedInPercent())
            BrushMotor.move()
            print("backward")
        else:	
            tk.messagebox.showerror("Invalid Input", "Please select a valid direction")

    # Function to stop brushed motor
    def stop_brush_motor(BrushMotor):
        if BrushMotor.is_active == True:
            BrushMotor.stop()
            print("stop")
            BrushMotor.is_active = False
    
    # Function to set speed of brush motor
    def set_brush_motor_speed1(speed):
        brush_motor_1.setSpeedPercent(speed)
        print('brush speed 1: ', speed)

    # Function to set speed of brush motor
    def set_brush_motor_speed2(speed):
        brush_motor_2.setSpeedPercent(speed)
        print('brush speed 2: ', speed)    
            
    # Function to set speed of step motor
    def set_step_motor_speed(speed):
        motorY.setSpeedInMPS(speed)
        print('step motor speed: ', speed)

    ##################################################################
    ######### Bürstenmotoren Funtionen Ende ##########################
    ##################################################################
        
    # Create GUI
    root = tk.Tk() 
    root.title("SandUp Handbetrieb")

    #start button mit Icon
    #os.chdir(os.path.dirname(os.path.abspath(__file__)))
    image = PhotoImage(file="power.png").subsample(6)
    startImage = ttk.Button(root,image = image,command = toggle_power)
    startImage.grid(column = 0, row = 0, rowspan=3, sticky="NSEW")

    # Button Emergency stop
    btn_emergency_stop = tk.Button(root, text="Emergency Stop", command=emergency_stop)
    btn_emergency_stop.grid(row=0, column=2)

    ######## Buttons for logging the Data and writing it in CSV File
    btn_start_logging = tk.Button(root, text="Start Logging", command=lambda:None)
    btn_start_logging.grid(row=17, column=0)
    btn_start_logging.bind('<ButtonPress-1>', lambda event: startSerialReceive(readSerialcommandPipe))
    buttons.append(btn_start_logging)

    btn_stop_logging = tk.Button(root, text="Stop Logging", command=lambda:None)
    btn_stop_logging.grid(row=17, column=1)
    btn_stop_logging.bind('<ButtonPress-1>', lambda event: stopSerialReceive(readSerialcommandPipe))
    buttons.append(btn_stop_logging)

    btn_writeToCSV = tk.Button(root, text="Write to CSV", command=lambda:None)
    btn_writeToCSV.grid(row=17, column=2)
    btn_writeToCSV.bind('<ButtonPress-1>', lambda event: CSVwriter.writeCSV(databasePath, sensorColumns))
    buttons.append(btn_writeToCSV)

    #Uhrzeit anzeigen
    zeit = ttk.Label(root, text="INIT")
    zeit.grid(row=17,column=3,sticky = "NSEW")
    getTime()

    ####################################################
    ########### Schrittmotor Buttons ###################
    ####################################################

    #labels
    lbl_motor_Y = tk.Label(root, text="Schrittmotor Y")
    lbl_motor_Y.grid(row=3, column=0)

    # Text input for number of steps for motor Y discontinous Up&Down
    lbl_steps = tk.Label(root, text="Abstand in cm eingeben:")
    lbl_steps.grid(row=3, column=2)
    entry_steps = tk.Entry(root)
    entry_steps.grid(row=3, column=3)
    buttons.append(entry_steps)

    #label for Schrittmotor speed
    lbl_M_speed = tk.Label(root, text="Step Motor Speed in m/s:")
    lbl_M_speed.grid(row=3, column=4)

    # Slider for speed selection
    var_speed_1 = tk.DoubleVar(value=0.1)
    speed_slider_1 = tk.Scale(root, variable=var_speed_1, from_=0.1, to=0.6, resolution=0.05, orient='horizontal')
    speed_slider_1.grid(row=3, column=5)
    buttons.append(speed_slider_1)

    # Button to set step motor speed
    btn_set_M_speed = tk.Button(root, text="Set Speed", command=lambda: set_step_motor_speed(float(var_speed_1.get())))
    btn_set_M_speed.grid(row=4, column=5)
    buttons.append(btn_set_M_speed)

    #Button Schrittmotor STOP
    btn_Schrittmotor_stop = tk.Button(root, text="Schrittmotor Stop", command= Schrittmotor_stop)
    btn_Schrittmotor_stop.grid(row=4, column=4)
    buttons.append(btn_Schrittmotor_stop)

    #function definition Buttons for Schrittmotor Continuous

    # Create a Tkinter variable to track button state
    btn_step_motor_Y_continuous_up_pressed = tk.BooleanVar()
    btn_step_motor_Y_continuous_up_pressed.set(False)

    btn_step_motor_Y_continuous_down_pressed = tk.BooleanVar()
    btn_step_motor_Y_continuous_down_pressed.set(False)

    # Button callback to set the button state to True when pressed
    def btn_step_motor_Y_continuous_up_pressed_callback():
        btn_step_motor_Y_continuous_up_pressed.set(True)
        # Start continuous motor movement
        move_step_motor_Y_continuous_up()

    def btn_step_motor_Y_continuous_down_pressed_callback():
        btn_step_motor_Y_continuous_down_pressed.set(True)
        # Start continuous motor movement
        move_step_motor_Y_continuous_down()

    # Button callback to set the button state to False when released
    def btn_step_motor_Y_continuous_up_released_callback():
        btn_step_motor_Y_continuous_up_pressed.set(False)

    def btn_step_motor_Y_continuous_down_released_callback():
        btn_step_motor_Y_continuous_down_pressed.set(False)

    # Define button callback functions
    def on_button_press_Y_continuous_up(event):
        btn_step_motor_Y_continuous_up_pressed_callback()

    def on_button_release_Y_continuous_up(event):
        btn_step_motor_Y_continuous_up_released_callback()

    def on_button_press(event):
        btn_step_motor_Y_continuous_down_pressed_callback()

    def on_button_release(event):
        btn_step_motor_Y_continuous_down_released_callback()    

    # Button Schrittmotor Y UP CONTINUOUS
    image1 = PhotoImage(file="Drehrichtung_vorwärts.png").subsample(6)
    btn_step_motor_Y_continuous_up = ttk.Button(root, image=image1, command=lambda: None)
    btn_step_motor_Y_continuous_up.grid(column=0, row=4, sticky="NSEW", padx=10, pady=10)
    buttons.append(btn_step_motor_Y_continuous_up)

    btn_step_motor_Y_continuous_up.bind('<ButtonPress-1>', on_button_press_Y_continuous_up)
    btn_step_motor_Y_continuous_up.bind('<ButtonRelease-1>', on_button_release_Y_continuous_up)
    
    # Button Schrittmotor Y DOWN CONTINUOUS
    image2 = PhotoImage(file="Drehrichtung_rückwärts.png").subsample(6)
    btn_step_motor_Y_continuous_down = ttk.Button(root, image=image2, command=lambda: None)
    btn_step_motor_Y_continuous_down.grid(column=1, row=4, sticky="NSEW", padx=10, pady=10)
    buttons.append(btn_step_motor_Y_continuous_down)

    btn_step_motor_Y_continuous_down.bind('<ButtonPress-1>', on_button_press)
    btn_step_motor_Y_continuous_down.bind('<ButtonRelease-1>', on_button_release)
    
    # Button Schrittmotor Y UP DISCRETE
    btn_step_motor_Y_discrete_up = ttk.Button(root, text="Schrittmotor Vorwärts", command= move_step_motor_Y_discrete_up)
    btn_step_motor_Y_discrete_up.grid(column=2, row=4, sticky="NSEW", padx=10, pady=10)
    buttons.append(btn_step_motor_Y_discrete_up)

    # Button Schrittmotor Y DOWN DISCRETE
    btn_step_motor_Y_discrete_down = ttk.Button(root, text="Schrittmotor Rückwärts",  command=move_step_motor_Y_discrete_down)
    btn_step_motor_Y_discrete_down.grid(column=3, row=4, sticky="NSEW", padx=10, pady=10)
    buttons.append(btn_step_motor_Y_discrete_down)

     # Call move_step_motor_Y_up function when the button is pressed
    btn_step_motor_Y_continuous_up.config(command=move_step_motor_Y_continuous_up)
    btn_step_motor_Y_continuous_down.config(command=move_step_motor_Y_continuous_down) 
    
    ################################################################################
    ##### Schrittmotor in  X Richtung  - gleiche Konzepte von Y Richtung ###########
    ################################################################################

    #folgende Zeile sind nur für Platzierung
    lbl_motor_X = tk.Label(root, text="Schrittmotor X")
    lbl_motor_X.grid(row=7, column=0)

    for i in range(8, 11):
        for j in range(6):
            label_X = tk.Label(root, text='X')
            label_X.grid(row=i, column=j)

    ###################################################
    ########### Bürstemotor Buttons ###################
    ###################################################

    # Brush Motor 1
    lbl_brush_motor_1 = tk.Label(root, text="Bürste 1")
    lbl_brush_motor_1.grid(row=12, column=2)

    lbl_motor_1_drehrichtung = tk.Label(root, text="Drehrichtung:")
    lbl_motor_1_drehrichtung .grid(row=13, column=3)

    # Brush Motor 2
    lbl_brush_motor_2 = tk.Label(root, text="Bürste 2")
    lbl_brush_motor_2.grid(row=14, column=2)

    lbl_motor_2_drehrichtung = tk.Label(root, text="Drehrichtung:")
    lbl_motor_2_drehrichtung .grid(row=16, column=3)

    # Brush Motor Speed
    lbl_B_speed = tk.Label(root, text="Bürste Motor Speed in percent:")
    lbl_B_speed.grid(row=11, column=0)

    # Text input for speed of step motor
    entry_B_speed1 = tk.DoubleVar(value=0)
    entry_B_speed_slider1 = tk.Scale(root, variable=entry_B_speed1, from_=0, to=100, resolution=10, orient='horizontal')
    entry_B_speed_slider1.grid(row=12, column=0)
    buttons.append(entry_B_speed_slider1)

    # Text input for speed of step motor
    entry_B_speed2 = tk.DoubleVar(value=0)
    entry_B_speed_slider2 = tk.Scale(root, variable=entry_B_speed2, from_=0, to=100, resolution=10, orient='horizontal')
    entry_B_speed_slider2.grid(row=14, column=0)
    buttons.append(entry_B_speed_slider2)

    # to select the direction of Bürste Motor 1
    var_direction_1 = tk.StringVar(value="Richtung wählen")
    direction_menu_1 = ttk.Combobox(root, textvariable=var_direction_1, values=["Vorwärts", "Ruckwärts"])
    direction_menu_1.grid(row=13, column=4)
    buttons.append(direction_menu_1)

    # to select the direction of Bürste Motor 2
    var_direction_2 = tk.StringVar(value="Richtung wählen")
    direction_menu_2 = ttk.Combobox(root, textvariable=var_direction_2, values=["Vorwärts", "Ruckwärts"])
    direction_menu_2.grid(row=16, column=4)
    buttons.append(direction_menu_2)

    # Button to set Bürste motor speed 1
    btn_set_B_speed1 = tk.Button(root, text="Set Speed 1", command=lambda: set_brush_motor_speed1(float(entry_B_speed1.get())))
    # btn_set_B_speed = tk.Button(root, text="Set Speed 1", command=lambda: none)
    btn_set_B_speed1.grid(row=12, column=1)
    buttons.append(btn_set_B_speed1)

    # Button to set Bürste motor speed 2
    btn_set_B_speed2 = tk.Button(root, text="Set Speed 2", command=lambda: set_brush_motor_speed2(float(entry_B_speed2.get())))
    # btn_set_B_speed2 = tk.Button(root, text="Set Speed 2", command=lambda: none)
    btn_set_B_speed2.grid(row=14, column=1)
    buttons.append(btn_set_B_speed2)

   #EIN und AUS Buttons für Bürste Motor 1
    btn_brush_motor_1 = tk.Button(root, text="EIN", command=lambda:None)
    btn_brush_motor_1.grid(row=12, column=3)
    btn_brush_motor_1.bind('<ButtonPress-1>', lambda event: move_brushmotor(brush_motor_1, var_direction_1.get()))
    buttons.append(btn_brush_motor_1)

    btn_brush_motor_1 = tk.Button(root, text="AUS", command=lambda:None)
    btn_brush_motor_1.grid(row=12, column=4)
    btn_brush_motor_1.bind('<ButtonPress-1>', lambda event: stop_brush_motor(brush_motor_1))
    buttons.append(btn_brush_motor_1)
    
    #EIN und AUS Buttons für Bürste Motor 2
    btn_brush_motor_2 = tk.Button(root, text="EIN", command=lambda:None)
    btn_brush_motor_2.grid(row=14, column=3)
    btn_brush_motor_2.bind('<ButtonPress-1>', lambda event: move_brushmotor(brush_motor_2, var_direction_2.get()))
    buttons.append(btn_brush_motor_2)

    btn_brush_motor_2 = tk.Button(root, text="AUS", command=lambda:None)
    btn_brush_motor_2.grid(row=14, column=4)
    btn_brush_motor_2.bind('<ButtonPress-1>', lambda event: stop_brush_motor(brush_motor_2))
    buttons.append(btn_brush_motor_2)

    
    # Start GUI
    disable_buttons()
    root.mainloop()





