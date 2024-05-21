import tkinter as tk
from gpiozero import Button
import RPi.GPIO as GPIO
import time
from tkinter import messagebox
from tkinter import PhotoImage, ttk
#from ttkthemes import themed_tk as tkt # ttkthemes

import motor_steuerung

# GPIO-Pins für die SchrittMotorsteuerung
motorY_step_pin = 17 # Step-Pin für Motor Y/1
motorY_dir_pin = 27 # Richtungspin für Motor Y/1
motorX_step_pin = 25 # Step-Pin für Motor X/2
motorX_dir_pin = 8 # Richtungspin für Motor X/2

#Implemetierung der SchrittMotor Klasse
motorY = motor_steuerung.StepMotor(motorY_step_pin,motorY_dir_pin)
motorX = motor_steuerung.StepMotor(motorX_step_pin,motorX_dir_pin)

# GPIO-Pins für die Bürstenmotorsteuerung
motor_pwm_pin_1 = 18  # PWM-Pin für Motor 1 Geschwindigkeitssteuerung
motor_dir_pin_1_1 = 23  # Richtungspin 1 für Motor 1

motor_pwm_pin_2 = 26  # PWM-Pin für Motor 2 Geschwindigkeitssteuerung
motor_dir_pin_1_2 = 8   # Richtungspin 1 für Motor 2

# Bürstenmotoren Implementierung
brush_motor_1 = motor_steuerung.BrushMotor(motor_pwm_pin_1, motor_dir_pin_1_1, motor_dir_pin_2_1)
brush_motor_2 = motor_steuerung.BrushMotor(motor_pwm_pin_2, motor_dir_pin_1_2, motor_dir_pin_2_2)


# Function for emergency stop
def emergency_stop():
    brush_motor.stop()
    step_motor.stop()

    
# Function to toggle power of step motor
def toggle_step_motor():
    if step_motor.is_active:
        step_motor.stop()
    else:
        step_motor.forward()




# Function to move step motor continuosus up
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

# Function to move step motor continuosus down
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

# Function to move step motor up with steps
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
        motorY.makeSteps(steps, 0)
        print('motor Y up_discrete')

    # Call the inner function to start the movement
    motor_Y_up_discrete()
    	
# Function to move step motor down with steps
def move_step_motor_Y_discrete_down():
# Get the number of steps from the input field
    try:
        steps = int(entry_steps.get())
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter a valid number of steps")
        return

    # Define the function for continuous motor movement
    def motor_Y_discrete_down():
        # Make one step down
        motorY.makeSteps(steps, 1)
        print('motor Y discrete down')

    # Call the inner function to start the movement
    motor_Y_discrete_down()
	
def move_step_motor_X_up():
    # Define the function for continuous motor movement
    def motor_X_up():
        # Make one step up
        motorX.makeSteps(1, 0)
        print('motor X up')
        # Check if the button is still pressed
        if btn_step_motor_X_up_pressed.get():
            # Schedule the function to run again after 100 milliseconds
            root.after(100, motor_X_up)
    # Call the inner function to start the continuous movement
    motor_X_up()
	
def move_step_motor_X_down():
    # Define the function for continuous motor movement
    def motor_X_down():
        # Make one step up
        motorX.makeSteps(1, 1)
        print('motor X down')
        # Check if the button is still pressed
        if btn_step_motor_X_down_pressed.get():
            # Schedule the function to run again after 100 milliseconds
            root.after(100, motor_X_down)

    # Call the inner function to start the continuous movement
    motor_X_down()
    
# Function to control brushed motor	
def move_brushmotor(BrushMotor , direction):
		if direction == 'Vorwärts':
			BrushMotor.control
			print("forward")
		elif direction == 'Ruckwärts':
			print("backward")
		
	
# Function to stop brushed motor
def stop_brush_motor(BrushMotor):
    BrushMotor.stop()
    print("stop")

	
	    
# Function to set speed of step motor
def set_step_motor_speed(speed):
    step_motor.forward(speed=float(speed))

# Create GUI
root = tk.Tk()
root.title("SandUp Handbetrieb")

#start button mit Icon
#os.chdir(os.path.dirname(os.path.abspath(__file__)))
image = PhotoImage(file="power.png")
image = image.subsample(6)
startImage = ttk.Button(
    root,
    image = image,
)
startImage.grid(column = 0, row = 0, rowspan=3, sticky="NSEW")

# Buttons
btn_emergency_stop = tk.Button(root, text="Emergency Stop", command=emergency_stop)
btn_emergency_stop.grid(row=0, column=2)



# Text input for number of steps for motor Y discontinous Up&Down
lbl_steps = tk.Label(root, text="Schritte eingeben:")
lbl_steps.grid(row=3, column=2)
entry_steps = tk.Entry(root)
entry_steps.grid(row=3, column=3)

# Create a Tkinter variable to track button state
btn_step_motor_Y_continuous_up_pressed = tk.BooleanVar()
btn_step_motor_Y_continuous_up_pressed.set(False)

btn_step_motor_Y_continuous_down_pressed = tk.BooleanVar()
btn_step_motor_Y_continuous_down_pressed.set(False)

#btn_step_motor_Y_discrete_up_pressed = tk.BooleanVar()
#btn_step_motor_Y_discrete_up_pressed.set(False)

#btn_step_motor_Y_discrete_down_pressed = tk.BooleanVar()
#btn_step_motor_Y_discrete_down_pressed.set(False)

btn_step_motor_X_up_pressed = tk.BooleanVar()
btn_step_motor_X_up_pressed.set(False)

btn_step_motor_X_down_pressed = tk.BooleanVar()
btn_step_motor_X_down_pressed.set(False)

# Button callback to set the button state to True when pressed
def btn_step_motor_Y_continuous_up_pressed_callback():
    btn_step_motor_Y_continuous_up_pressed.set(True)
    # Start continuous motor movement
    move_step_motor_Y_continuous_up()

def btn_step_motor_Y_continuous_down_pressed_callback():
    btn_step_motor_Y_continuous_down_pressed.set(True)
    # Start continuous motor movement
    move_step_motor_Y_continuous_down()
    
#def btn_step_motor_Y_discrete_up_pressed_callback():
  #  btn_step_motor_Y_discrete_up_pressed.set(True)
    # Start discontinuous motor movement with steps
   # move_step_motor_Y_discrete_up()

#def btn_step_motor_Y_discrete_down_pressed_callback():
 #   btn_step_motor_Y_discrete_down_pressed.set(True)
    # Start discontinuous motor movement with steps
  #  move_step_motor_Y_discrete_down()

def btn_step_motor_X_up_pressed_callback():
    btn_step_motor_X_up_pressed.set(True)
    # Start continuous motor movement
    move_step_motor_X_up()
    
def btn_step_motor_X_down_pressed_callback():
    btn_step_motor_X_down_pressed.set(True)
    # Start continuous motor movement
    move_step_motor_X_down()

# Button callback to set the button state to False when released
def btn_step_motor_Y_continuous_up_released_callback():
    btn_step_motor_Y_continuous_up_pressed.set(False)
    
def btn_step_motor_Y_continuous_down_released_callback():
    btn_step_motor_Y_continuous_down_pressed.set(False)

#def btn_step_motor_Y_discrete_up_released_callback():
 #   btn_step_motor_Y_discrete_up_pressed.set(False)
    
#def btn_step_motor_Y_discrete_down_released_callback():
 #   btn_step_motor_Y_discrete_down_pressed.set(False)
    
def btn_step_motor_X_up_released_callback():
    btn_step_motor_X_up_pressed.set(False)

def btn_step_motor_X_down_released_callback():
    btn_step_motor_X_down_pressed.set(False)

lbl_motor_Y = tk.Label(root, text="Schrittmotor Y")
lbl_motor_Y.grid(row=3, column=0)

# Define button callback functions
#Motor Y Up cont.
def on_button_press_Y_continuous_up(event):
    btn_step_motor_Y_continuous_up_pressed_callback()

def on_button_release_Y_continuous_up(event):
    btn_step_motor_Y_continuous_up_released_callback()
    
#Motor Y Down cont.
def on_button_press(event):
    btn_step_motor_Y_continuous_down_pressed_callback()

def on_button_release(event):
    btn_step_motor_Y_continuous_down_released_callback()    

#Motor Y UP discont.
#def on_button_press_Y_discrete_up(event):
 #   btn_step_motor_Y_discrete_up_pressed_callback()

#def on_button_release_Y_discrete_up(event):
 #   btn_step_motor_Y_discrete_up_released_callback()

#Motor Y Down discont.
#def on_button_press_Y_discrete_down(event):
 #   btn_step_motor_Y_discrete_down_pressed_callback()

#def on_button_release_Y_discrete_down(event):
 #   btn_step_motor_Y_discrete_down_released_callback()
    
# Create button
#Schrittmotor Y UP CONTINUOUS
image1 = PhotoImage(file="Drehrichtung_vorwärts.png").subsample(6)
btn_step_motor_Y_continuous_up = ttk.Button(root, image=image1, command=lambda: None)
btn_step_motor_Y_continuous_up.grid(column=0, row=4, sticky="NSEW", padx=10, pady=10)

btn_step_motor_Y_continuous_up.bind('<ButtonPress-1>', on_button_press_Y_continuous_up)
btn_step_motor_Y_continuous_up.bind('<ButtonRelease-1>', on_button_release_Y_continuous_up)
  
#Schrittmotor Y DOWN CONTINUOUS
image2 = PhotoImage(file="Drehrichtung_rückwärts.png").subsample(6)
btn_step_motor_Y_continuous_down = ttk.Button(root, image=image2, command=lambda: None)
btn_step_motor_Y_continuous_down.grid(column=1, row=4, sticky="NSEW", padx=10, pady=10)

btn_step_motor_Y_continuous_down.bind('<ButtonPress-1>', on_button_press)
btn_step_motor_Y_continuous_down.bind('<ButtonRelease-1>', on_button_release)

#Schrittmotor Y UP STEPS
#title1 = ttk.Label(root, text="Schrittmotor Rückwärts", anchor="center")
#title1.grid(column=3, row=5, sticky="NSEW")

# Create button
btn_step_motor_Y_discrete_up = ttk.Button(root, text="Schrittmotor Vorwärts", command= move_step_motor_Y_discrete_up)
btn_step_motor_Y_discrete_up.grid(column=2, row=4, sticky="NSEW", padx=10, pady=10)

# Bind events to button
#btn_step_motor_Y_discrete_up.bind('<ButtonPress-1>', on_button_press_Y_discrete_up)
#btn_step_motor_Y_discrete_up.bind('<ButtonRelease-1>', on_button_release_Y_discrete_up)

#Schrittmotor Y DOWN STEPS
#title1 = ttk.Label(root, text="Schrittmotor Rückwärts", anchor="center")
#title1.grid(column=3, row=5, sticky="NSEW")

# Create button
btn_step_motor_Y_discrete_down = ttk.Button(root, text="Schrittmotor Rückwärts",  command=move_step_motor_Y_discrete_down)
btn_step_motor_Y_discrete_down.grid(column=3, row=4, sticky="NSEW", padx=10, pady=10)

# Bind events to button
#btn_step_motor_Y_discrete_down.bind('<ButtonPress-1>', on_button_press_Y_discrete_down)
#btn_step_motor_Y_discrete_down.bind('<ButtonRelease-1>', on_button_release_Y_discrete_down)

#-------------------------------------------------------------------------------------------------

lbl_motor_X = tk.Label(root, text="Schrittmotor X")
lbl_motor_X.grid(row=7, column=0)

btn_step_motor_X_up = tk.Button(root, text="")
#btn_step_motor_X_up = tk.Button(root, text="Schrittmotor X Vorwärts")
btn_step_motor_X_up.grid(row=8, column=0)
btn_step_motor_X_up.bind('<ButtonPress-1>', lambda event: btn_step_motor_X_up_pressed_callback())
btn_step_motor_X_up.bind('<ButtonRelease-1>', lambda event: btn_step_motor_X_up_released_callback())

btn_step_motor_X_down = tk.Button(root, text="")
#btn_step_motor_X_down = tk.Button(root, text="Schrittmotor X Rückwärts")
btn_step_motor_X_down.grid(row=9, column=0)
btn_step_motor_X_down.bind('<ButtonPress-1>', lambda event: btn_step_motor_X_down_pressed_callback())
btn_step_motor_X_down.bind('<ButtonRelease-1>', lambda event: btn_step_motor_X_down_released_callback())

for i in range(8, 11):
    for j in range(6):
        label_X = tk.Label(root, text='X')
        label_X.grid(row=i, column=j)

# Call move_step_motor_Y_up function when the button is pressed
btn_step_motor_Y_continuous_up.config(command=move_step_motor_Y_continuous_up)
btn_step_motor_Y_continuous_down.config(command=move_step_motor_Y_continuous_down)

#btn_step_motor_Y_discrete_up.config(command=move_step_motor_Y_discrete_up)
#btn_step_motor_Y_discrete_down.config(command=move_step_motor_Y_discrete_down)

btn_step_motor_X_up.config(command=move_step_motor_X_up)
btn_step_motor_X_down.config(command=move_step_motor_X_down)

#Step Motor Speed
# Text input for speed of step motor
lbl_M_speed = tk.Label(root, text="Step Motor Speed:")
lbl_M_speed.grid(row=3, column=4)
entry_M_speed = tk.Entry(root)
entry_M_speed.grid(row=3, column=5)

# Button to set step motor speed
btn_set_M_speed = tk.Button(root, text="Set Speed", command=lambda: set_step_motor_speed(entry_M_speed.get()))
btn_set_M_speed.grid(row=4, column=4)

#Brush Motor Speed
# Text input for speed of step motor
lbl_B_speed = tk.Label(root, text="Bürste Motor Speed:")
lbl_B_speed.grid(row=11, column=0)
entry_B_speed = tk.Entry(root)
entry_B_speed.grid(row=11, column=1)

# Button to set step motor speed
#btn_set_B_speed = tk.Button(root, text="Set Speed", command=lambda: set_step_motor_speed(entry_b_speed.get()))
btn_set_B_speed = tk.Button(root, text="Set Speed", command=lambda: none)
btn_set_B_speed.grid(row=12, column=0)



#Bürstenmotor control
# Brush Motor 1
lbl_motor_1_drehrichtung = tk.Label(root, text="Drehrichtung:")
lbl_motor_1_drehrichtung .grid(row=13, column=2)

var_direction_1 = tk.StringVar(value="Richtung wählen")
direction_menu_1 = ttk.Combobox(root, textvariable=var_direction_1, values=["Vorwärts", "Ruckwärts"])
direction_menu_1.grid(row=13, column=3)

btn_brush_motor_1 = tk.Button(root, text="Bürste 1", command=lambda:None)
btn_brush_motor_1.grid(row=12, column=2)
btn_brush_motor_1.bind('<ButtonPress-1>', lambda event: move_brushmotor(brush_motor_1, var_direction_1.get()))
btn_brush_motor_1.bind('<ButtonRelease-1>', lambda event: stop_brush_motor(brush_motor_1))

# Brush Motor 2
lbl_motor_2_drehrichtung = tk.Label(root, text="Drehrichtung:")
lbl_motor_2_drehrichtung .grid(row=15, column=2)

var_direction_2 = tk.StringVar(value="Richtung wählen")
direction_menu_2 = ttk.Combobox(root, textvariable=var_direction_2, values=["Vorwärts", "Ruckwärts"])
direction_menu_2.grid(row=15, column=3)

btn_brush_motor_2 = tk.Button(root, text="Bürste 2", command=lambda:None)
btn_brush_motor_2.grid(row=14, column=2)
btn_brush_motor_2.bind('<ButtonPress-1>', lambda event: move_brushmotor(brush_motor_2, var_direction_2.get()))
btn_brush_motor_2.bind('<ButtonRelease-1>', lambda event: stop_brush_motor(brush_motor_2))






#btn_brush_up = tk.Button(root, text="Bürstenmotor Vorwärts", command=move_brush_up)
#btn_brush_up.grid(row=12, column=2)

#btn_brush_down = tk.Button(root, text="Bürstenmotor Rückwärts", command=move_brush_down)
#btn_brush_down.grid(row=14, column=2)

# Text input for number of rotations of brush motor
#lbl_rotation = tk.Label(root, text="Number of rotations:")
#lbl_rotation.grid(row=16, column=2)

# Start GUI
root.mainloop()





