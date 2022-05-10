import os, threading, time, psutil, socket
from tkinter import messagebox
from tkinter import *
from util.log import *
from datetime import timedelta 

# store IP Address in use
ip_addr = ""

# store exit var status
exit_status = False

# func: get_ip_address
# args: none
# desc: returns the IPV4 adress of the device to verify network connectivity
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    global ip_addr
    ip_addr = s.getsockname()[0]
    return s.getsockname()[0]

    ##with open(os.path('./logs/'),(get_date()+".txt"), 'a') as the_file:
    ##    the_file.write(get_12time() + " - " + string  + "\n")

# func: check_connectivity
# args: none
# desc: returns the true/false to verify network connectivity
def check_connectivity():
    ip = get_ip_address()
    if(ip):
        return True
    else: 
        return False

# func: exit_on_click
# args: none
# desc: used to exit the program "cleanly" closing all active resources
# uses: used in Exit button and window exit button (X)
def exit_on_click(): 
    log("Exit command recieved")
    global exit_status
    global clock_thread
    exit_status = TRUE
    time.sleep(1)
    clock_thread.join()
    batt_thread.join()
    window.destroy()
    log("Closing Application\n\n")
    exit()

# func: set_time
# args: none
# desc: update clock element
def set_stime():

    clock.config(text = get_12time(), foreground="white")


# func: update_bat_stats
# args: none
# desc: update clock element
def update_bat_stats():
    #check battery status
    power_status = get_battery_info()
    batt_percent = power_status.percent
    seconds_left = power_status.secsleft
    plugged_in = power_status.power_plugged
    
    #update battery info
    battery_percent.config(text = str(batt_percent) + "% remaining")
    
    if(str(seconds_left) == "BatteryTime.POWER_TIME_UNLIMITED"):
        battery_secs.pack_forget()
    else:
        battery_secs.config(text = str(timedelta(seconds=seconds_left))+" of battery left")
        battery_secs.pack()
        
    if(plugged_in):
        battery_plugged.config(text = "PC is connected to power supply.")
    else:
        battery_plugged.config(text = "Connect PC to power supply to charge.")


# func: update_time
# args: none
# desc: Thread dedicated to updating the apllication clock every second (exits on application exit)
def update_time():
    try:
        while(True):
            global exit_status
            #log.log(exit_status)
            
            if(exit_status):
                log("Clock Thread Closed")
                break
            else:
                set_stime()
                time.sleep(1)
    except NameError:
        log("Clock Thread Closed With Error: " + NameError.name)
        return    

# func: update_battery
# args: none
# desc: Thread dedicated to updating the apllication battery info every second (exits on application exit)
def update_battery():
    try:
        while(True):
            global exit_status
            
            if(exit_status):
                log("Battery Thread Closed")
                break
            else:
                update_bat_stats()
                time.sleep(1)
    except NameError:
        log("Battery Thread Closed With Error: " + NameError.name)
        return   

# func: get_battery_info
# args: none
# desc: checks for battery information (Charging, time left, and percent)
def get_battery_info():
    return psutil.sensors_battery()

######################################################
############### Main Start Section ###################
######################################################

import os
directory = "./logs/"
if not os.path.exists(directory):
    os.makedirs(directory)

#main startup process
log("Prcoess Started")

# log user 
log("Active User: " + os.getlogin())

#start UI
window = Tk()
window.title(str(os.getlogin()))
window.config(background='black')
window.geometry('400x200')
log("UI Window Created")    

# Clock
clock = Label(text=get_12time())
clock.config(background='black',foreground="white", font=("Arial", 30))
clock.pack(side=TOP, anchor="c", padx=8, pady=20)

#create clock thread
log("Starting clock thread")
clock_thread = threading.Thread(target = update_time)
clock.daemon = True;
clock_thread.start()

#check if on a network
if(check_connectivity()):
    log("Connected to: " + str(ip_addr))
    #set title to IP
    window.title(str(os.getlogin())+"@"+ip_addr)
else: # Exit here on Error
    log("Failed to verify network connection")
    messagebox.showerror('Connection Error', 'A network connection is required to run this applicaiton. Please connect to a network and try again.')
    #set title to User
    window.title(str(os.getlogin())+"@Offline")

#network check cleared and IPv4 Saved for use in sensor ports. 

#check battery status
power_status = get_battery_info()
batt_percent = power_status.percent
seconds_left = power_status.secsleft
plugged_in = power_status.power_plugged

#post battery info
battery_percent = Label(text="Battery Percentage = " + str(batt_percent))
battery_percent.config(background='black',foreground="white", font=("Arial",15))
battery_percent.pack()
battery_plugged = Label(text="Connected to Powersupply: " + str(plugged_in))
if(plugged_in):
    battery_plugged.config(text = "PC is connected to power supply.")
else:
    battery_plugged.config(text = "Connect PC to power supply to charge.")
battery_plugged.config(background='black',foreground="white", font=("Arial",15))
battery_plugged.pack()
battery_secs = Label(text="Battery Time Left: " + str(timedelta(seconds=seconds_left)))
if(seconds_left == "BatteryTime.POWER_TIME_UNLIMITED"):
    battery_secs.pack_forget()
else:
    battery_secs.config(text = str(timedelta(seconds=seconds_left))+" of battery left")
    battery_secs.pack()
battery_secs.config(background='black',foreground="white", font=("Arial",15))
battery_secs.pack()

#create battery thread
log("Starting battery thread")
batt_thread = threading.Thread(target = update_battery)
batt_thread.daemon = True;
batt_thread.start()

#button
#b = Button(window, text="Exit", command=exit_on_click)
#b.config(background='cyan',foreground="black")
#b.pack(side=BOTTOM, anchor="e", padx=8, pady=20)

#main loop (disable X button on toolbar)
window.protocol("WM_DELETE_WINDOW", exit_on_click)
window.mainloop()