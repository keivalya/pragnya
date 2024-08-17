from PIL import Image, ImageTk
import tkinter as tk
from customtkinter import *

from opcua import Server
import threading
import time

from speech_main import speak

import socket
hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

from itertools import cycle
colors = cycle(["red", "blue", "green"])

from dotenv import load_dotenv

# Load environment variables from the .env file and Access the variables
load_dotenv()
my_ip_address = os.getenv('MY_IP_ADDRESS')

# Define the server endpoint (IP address and port)
# server_url = "opc.tcp://"+IPAddr+":4840"
server_url = "opc.tcp://"+my_ip_address+":4840"

# Function to update the selected radio button
def update_radio_button(value):
    try:
        if 0 <= int(value) <= 8:
            selected_option.set(int(value))
    except:
        pass

global bearing_no
bearing_no = ""

def complete_speaking(stn_num, voice_control, sentence):
    time.sleep(0)
    if "success" in sentence:
        dict_of_stations_text[stn_num].configure(fg_color="#1b7e57", wrap="word") # green
    elif "sent" in sentence:
        dict_of_stations_text[stn_num].configure(fg_color="#010048", wrap="word") # blue 
    else:
        dict_of_stations_text[stn_num].configure(fg_color="#2e0f3d", wrap="word") #purple
    dict_of_stations_text[stn_num].insert("0.0", "> "+sentence+"\n")

    speak(voice_control, sentence)

# Function to run the OPC UA server
def run_opcua_server():
    server = Server()
    server.set_endpoint(server_url)
    server.register_namespace("https://www.keivalya.com")
    objects = server.get_objects_node()

    param = objects.add_variable("ns=2;i=2", "Parameter", 0)
    bearing_number = objects.add_variable("ns=2;i=3", "BearingNumber", 0)
    inner_dia = objects.add_variable("ns=2;i=4", "innerDia", 0)
    outer_dia = objects.add_variable("ns=2;i=5", "outerDia", 0)
    bearing_height = objects.add_variable("ns=2;i=6", "bearingHeight", 0)
    housing = objects.add_variable("ns=2;i=7", "Housing", 0)
    shaft = objects.add_variable("ns=2;i=8", "Shaft", 0)
    pallet = objects.add_variable("ns=2;i=9", "Pallet", 0)
    bearing_cell = objects.add_variable("ns=2;i=10", "bearingCell", 0)
    housing_cell = objects.add_variable("ns=2;i=11", "housingCell", 0)
    pallet_cell = objects.add_variable("ns=2;i=12", "palletCell", 0)
    shaft_cell = objects.add_variable("ns=2;i=13", "shaftCell", 0)

    param.set_writable()
    bearing_number.set_writable()
    inner_dia.set_writable()
    outer_dia.set_writable()
    bearing_height.set_writable()
    housing.set_writable()
    shaft.set_writable()
    bearing_cell.set_writable()
    housing_cell.set_writable()
    pallet_cell.set_writable()
    shaft_cell.set_writable()
    pallet.set_writable()
    try:
        server.start()
        print(f"Server started at {server_url}")
        while True:
            value = param.get_value()
            bearing_no = bearing_number.get_value()
            housing_type = housing.get_value()
            repeat_var = False
            if value != selected_option.get():
                print(f"Updating GUI with value: {value}")
                update_radio_button(value)
                if selected_option.get()==1 and repeat_var==False:
                    cst = selected_option.get()
                    complete_speaking(cst, "CS", f"Received an order for {bearing_no}, of {housing_type} type housing and a {shaft.get_value()} shaft from the customer.")
                    complete_speaking(cst, "CS", f"Message sent to A.S.R.S. - Bring {housing_type} housing from {housing_cell.get_value()} cell to the delivery platform.")
                    complete_speaking(cst, "CS", f"Message sent to A.M.R. - Go to A.S.R.S. to collect {housing_type} housing from {housing_cell.get_value()} cell.")
                    complete_speaking(cst, "CS", f"{bearing_no} bearing from {bearing_cell.get_value()} cell.")
                    complete_speaking(cst, "CS", f"{shaft.get_value()} bearing from {shaft_cell.get_value()} cell.")
                    complete_speaking(cst, "CS", f"{pallet.get_value()} pallet from {pallet_cell.get_value()} cell.")
                    complete_speaking(cst, "CS", f"Message sent to A.M.R. - collect the {housing_type} housing and take it to Mirac P.C.")
                    complete_speaking(cst, "ST", f"The {housing_type} housing has been successfully delivered to Mirac P.C.")
                    selected_option.set(2)
                if selected_option.get()==2 and repeat_var==False:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"AMR has reached to Mirac P.C. and oriented to load {housing_type} housing on the machine.")
                    complete_speaking(cst, "CS", f"Message sent to Mirac P.C. -  Open Chuck to load {housing_type} housing.")
                    complete_speaking(cst, "ST", f"the chuck in Mirac P.C. has been opened.")
                    complete_speaking(cst, "CS", f"Message sent to A.M.R. - Load the {housing_type} housing in the chuck.")
                    complete_speaking(cst, "ST", f"The {housing_type} housing is loaded into the chuck.")
                    complete_speaking(cst, "CS", f"Message sent to Mirac P.C. - close the chuck.")
                    complete_speaking(cst, "ST", f"The chuck in Mirac P.C. has been closed.")
                    complete_speaking(cst, "CS", f"Message sent to Mirac P.C. - Start the machining process.")
                    time.sleep(2)
                    complete_speaking(cst, "ST", f"Facing operation is successfully finished!")
                    time.sleep(2)
                    complete_speaking(cst, "ST", f"Drilling operation is successfully finished!")
                    complete_speaking(cst, "ST", f"Machining of the {housing_type} housing is done!")
                    complete_speaking(cst, "CS", f"Message sent to A.M.R. - Go to Mirac P.C. and to collect {housing_type} housing.")
                    complete_speaking(cst, "ST", f"The A.M.R. has positioned itself to collect the {housing_type} housing.")
                    complete_speaking(cst, "CS", f"Message sent to A.M.R. - Hold the {housing_type} housing to unload from Mirac P.C.")
                    complete_speaking(cst, "ST", f"The A.M.R. is holding the {housing_type} housing.")
                    complete_speaking(cst, "CS", f"Message sent to Mirac P.C. - Open the chuck.")
                    complete_speaking(cst, "ST", f"The chuck has been opened.")
                    complete_speaking(cst, "CS", f"Message sent to A.M.R. - unload the {housing_type} housing.")
                    complete_speaking(cst, "ST", f"The {housing_type} housing has been successfully unloaded. Moving to palletizing station!")
                    selected_option.set(3)
                if selected_option.get()==3:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"The A.M.R. has reached to the palletizing station with proper orientation.")
                    complete_speaking(cst, "CS", f"Message sent to the A.M.R. - load the pallet on palletizing station.")
                    complete_speaking(cst, "ST", f"The pallet has been loaded on palletizing station.")
                    complete_speaking(cst, "ST", f"Pallet has been received by the palletizing station.")
                    complete_speaking(cst, "CS", f"Message sent to the A.M.R. - load {housing_type} housing.")
                    complete_speaking(cst, "ST", f"The {housing_type} housing has been loaded on palletizing station.")
                    complete_speaking(cst, "ST", f"Command for palletizing has been sent to the palletizing station.")
                    complete_speaking(cst, "ST", f"The {housing_type} housing has been successfully mounted on the pallet.")
                    complete_speaking(cst, "CS", f"Message sent to the A.M.R. - Unload the pallet from the palletizing station.")
                    complete_speaking(cst, "ST", f"Pallet has been successfully unloaded. Moving to the Triac P.C.")
                    selected_option.set(4)
                if selected_option.get()==4:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"The A.M.R. has reached to the TRIAC P.C. with proper orientation.")
                    complete_speaking(cst, "CS", f"Message sent to TRIAC P.C. - Open the vice to unload the pallet.")
                    complete_speaking(cst, "ST", f"The vice has been opened.")
                    complete_speaking(cst, "ST", f"Pallet is received.")
                    complete_speaking(cst, "CS", f"Message sent to A.M.R. - Load pallet in the vice.")
                    complete_speaking(cst, "ST", f"The pallet has been loaded in the vice.")
                    complete_speaking(cst, "CS", f"Message sent to Triac P.C. - Close the vice.")
                    complete_speaking(cst, "ST", f"The vice has been closed.")
                    complete_speaking(cst, "CS", f"We are about to begin machining of housing.")
                    complete_speaking(cst, "ST", f"Facing operation is completed successfully.")
                    complete_speaking(cst, "ST", f"Boring operation is completed successfully.")
                    complete_speaking(cst, "ST", f"Centering operation is completed successfully.")
                    complete_speaking(cst, "ST", f"Drilling operation is completed successfully.")
                    complete_speaking(cst, "ST", f"Machining of the {housing_type} housing is successfully completed.")
                    repeat_var = True
                    selected_option.set(2)
                if selected_option.get()==2 and repeat_var==True:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"The A.M.R. has reached to Mirac P.C.")
                    complete_speaking(cst, "CS", f"Open the chuck to load the shaft.")
                    complete_speaking(cst, "ST", f"The chuck is opened.")
                    complete_speaking(cst, "CS", f"Load the shaft inside the chuck.")
                    complete_speaking(cst, "ST", f"Shaft has been loaded into the chuck.")
                    complete_speaking(cst, "CS", f"Close the chuck.")
                    complete_speaking(cst, "ST", f"The chuck has been closed.")
                    complete_speaking(cst, "CS", f"Start the machine of the shaft.")
                    complete_speaking(cst, "ST", f"The facing operation has been successfully completed.")
                    complete_speaking(cst, "ST", f"The turning operation has been successfully completed.")
                    complete_speaking(cst, "ST", f"Machining of the shaft has been successfully completed.")
                    complete_speaking(cst, "CS", f"A.M.R. will go to Mirac P.C. and unload the shaft.")
                    complete_speaking(cst, "ST", f"A.M.R. has held the shaft to unload.")
                    complete_speaking(cst, "CS", f"Mirac P.C. must Open the chuck.")
                    complete_speaking(cst, "ST", f"The chuck is opened.")
                    complete_speaking(cst, "ST", f"A.M.R. has unloaded the shaft from Mirac P.C.")
                    complete_speaking(cst, "CS", f"A.M.R. must collect the housing from Triac P.C. and move to Manual Inspection Station.")
                    selected_option.set(4)
                if selected_option.get()==4:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"(success) A.M.R. has collected the pallet from Triac P.C.")
                    selected_option.set(5)
                if selected_option.get()==5:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"The A.M.R. has reached the Manual Inspection station and oriented accordingly.")
                    complete_speaking(cst, "CS", f"A.M.R. must load the pallet to the manual station.")
                    complete_speaking(cst, "ST", f"The pallet has been loaded to the manual station.")
                    complete_speaking(cst, "CS", f"Now, load the shaft on the Manual Station.")
                    complete_speaking(cst, "ST", f"The shaft has been loaded to Manual Station.")
                    complete_speaking(cst, "CS", f"Start shaft inspection. Measure dimensions!")
                    complete_speaking(cst, "ST", f"Pallet inspection is completed successfully!")
                    complete_speaking(cst, "ST", f"Shaft inspection is completed successfully!")
                    complete_speaking(cst, "CS", f"Unload the pallet from the Manual Station.")
                    complete_speaking(cst, "ST", f"The pallet has been unloaded.")
                    complete_speaking(cst, "CS", f"Unload the shaft from the Manual Station.")
                    complete_speaking(cst, "ST", f"The shaft has been unloaded.")
                    complete_speaking(cst, "CS", f"Shaft has unloaded successfully now, go to the Assembly Station.")
                    selected_option.set(6)
                if selected_option.get()==6:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"A.M.R. has reached to Assembly Station and oriented accordingly.")
                    complete_speaking(cst, "CS", f"Load pallet on Assembly Station.")
                    complete_speaking(cst, "ST", f"The pallet has been loaded on Assembly Station.")
                    complete_speaking(cst, "ST", f"The pallet is received.")
                    complete_speaking(cst, "CS", f"Load the {bearing_number} bearing on Assembly Station.")
                    complete_speaking(cst, "ST", f"{bearing_number} bearing is loaded on Assembly Station.")
                    complete_speaking(cst, "CS", f"Load shaft on Assembly Station.")
                    complete_speaking(cst, "ST", f"The shaft has been loaded.")
                    complete_speaking(cst, "CS", f"Start the Assembly of components.")
                    complete_speaking(cst, "ST", f"The assembly is completed.")
                    complete_speaking(cst, "CS", f"A.M.R. must unload the pallet from Assembly Station.")
                    complete_speaking(cst, "ST", f"Pallet has been unloaded successfully. Now, Move to the Palletizing station.")
                    selected_option.set(7)
                if selected_option.get()==7:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"The A.M.R. has reached to the Palletizing Station.")
                    complete_speaking(cst, "CS", f"Load Pallet on Palletizing Station.")
                    complete_speaking(cst, "ST", f"The pallet has been loaded successfullt into the Palletizing Station.")
                    complete_speaking(cst, "ST", f"The pallet has been received by the station.")
                    complete_speaking(cst, "CS", f"Do unpalletizing.")
                    complete_speaking(cst, "ST", f"Unpalletizing has been successfully completed.")
                    complete_speaking(cst, "CS", f"Unload product from the palletizing station.")
                    complete_speaking(cst, "ST", f"Product has been unloaded from the station.")
                    complete_speaking(cst, "CS", f"Unload pallet from the palletizing station.")
                    complete_speaking(cst, "ST", f"Pallet has been successfully unloaded.")
                    complete_speaking(cst, "CS", f"Move to the Manual Station.")
                    selected_option.set(8)
                if selected_option.get()==8:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"The A.M.R. has reached to the Manual Station.")
                    complete_speaking(cst, "CS", f"Load the product on Palletizing Station.")
                    complete_speaking(cst, "ST", f"Product has been loaded on the Station.")
                    complete_speaking(cst, "CS", f"Put barcode on the finished product.")
                    complete_speaking(cst, "ST", f"Barcode has been successfully placed on the product.")
                    complete_speaking(cst, "CS", f"Unload the product from the Manual Station.")
                    selected_option.set(1)
                if selected_option.get()==1 and repeat_var==True:
                    cst = selected_option.get()
                    complete_speaking(cst, "ST", f"The A.M.R. has reached at the A.S.R.S. and oriented accordingly.")
                    complete_speaking(cst, "CS", f"Load product on A.S.R.S. delivery platform.")
                    complete_speaking(cst, "ST", f"Product is loaded on A.S.R.S. delivery platform.")
                    complete_speaking(cst, "CS", f"A.S.R.S must place the product in cell number.")
                    complete_speaking(cst, "CS", f"A.M.R. must load the pallet in cell number.")
                    complete_speaking(cst, "ST", f"Product is placed in Cell number.")
                    complete_speaking(cst, "CS", f"A.S.R.S. must place the pallet in Cell number.")
                    complete_speaking(cst, "ST", f"The pallet is successfully placed in cell number.")
                    selected_option.set(-1)
                    break
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.stop()

set_appearance_mode("Dark")
app = CTk()
# app.geometry("1080x400")
# app.wm_attributes('-fullscreen', True)
app.after(0, lambda:app.state('zoomed'))
app.title("Pragnya (प्रज्ञा) Software")
app.grid_columnconfigure((0, 1), weight=1)
# app.grid_rowconfigure(0, weight=1)
# app.grid_columnconfigure(0, weight=1)

# Variable to store the selected radio option
selected_option = tk.IntVar()
selected_option.set(0)

# Create radio buttons
radio_buttons = []

image = Image.open("CoDM.png")
title_font = CTkFont(family="Roboto", size=24, weight="bold")
logo_image = CTkImage(dark_image=image, size=(100, 50))
logo_label = CTkLabel(app, image=logo_image, text="प्रज्ञा \n Control Software", compound="left", font=title_font)
logo_label.grid(row=0, column=0, padx=20, pady=5, sticky="ew", columnspan=2)

main_frame = CTkFrame(master=app, width=200, height=800)
main_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)
main_frame.grid_columnconfigure((0, 1, 2, 3), weight=2)

def toggle_blink():
    if selected_option.get() == 1:
        ASRS.configure(fg_color=next(colors))
    if selected_option.get() == 2:
        CNC.configure(fg_color=next(colors))
    if selected_option.get() == 3:
        Pallet.configure(fg_color=next(colors))
    if selected_option.get() == 4:
        VMC.configure(fg_color=next(colors))
    if selected_option.get() == 5:
        manual_inspection.configure(fg_color=next(colors))
    if selected_option.get() == 6:
        assembly_station.configure(fg_color=next(colors))
    if selected_option.get() == 7:
        performance_station.configure(fg_color=next(colors))
    if selected_option.get() == 8:
        barcode_station.configure(fg_color=next(colors))
    app.after(500, toggle_blink)

global from_asrs_messages
from_asrs_messages= [
    f"The {bearing_no}  is brought to the delivery platform.",
]

from_cnc_messages = [
    "Chuck is opened",
    "Chuck is closed",
    "Machining is Started",
    "Facing operation is finished",
    "Drilling operation is finished",
]

# ASRS
asrs_img = CTkImage(light_image=Image.open("asrs.png"),
                    dark_image=Image.open("asrs.png"),
                    size=(50, 50))
# ASRS_btn = CTkButton(master=main_frame, text="Autonomous Storage and \n Retrieval System", image=asrs_img, corner_radius=32)
# ASRS_btn.grid(row=0, column=0, padx=20, pady=20)
asrs_image = Image.open("asrs.png").resize((160, 160))
ASRS_img = ImageTk.PhotoImage(asrs_image)
asrs_label = tk.Label(main_frame, image = ASRS_img, text = "", bg="#2E2E2E")
asrs_label.grid(row=0, column=0, padx=20, pady=20)
ASRS = CTkRadioButton(main_frame, text="Automated Storage and Retrieval System", variable=selected_option, value=1, fg_color="green")
ASRS.grid(row=1, column=0, padx=20, pady=20)
radio_buttons.append(ASRS)
global asrs_text
asrs_text = CTkTextbox(master=main_frame, width=400, height=80, corner_radius=5)
asrs_text.grid(row=2, column=0, padx=20, pady=5)
# asrs_text.insert("1.0", from_asrs_messages[0])

# CNC Turning Center
cnc_img = CTkImage(light_image=Image.open("cnc.png"),
                    dark_image=Image.open("cnc.png"),
                    size=(100, 100))
# CNC_btn = CTkButton(master=main_frame, text="CNC Turning Center", image=cnc_img, corner_radius=32)
# CNC_btn.grid(row=0, column=1, padx=20, pady=20)
cnc_image = Image.open("cnc.png").resize((160, 160))
CNC_img = ImageTk.PhotoImage(cnc_image)
CNC_label = tk.Label(main_frame, image = CNC_img, text = "", bg="#2E2E2E")
CNC_label.grid(row=0, column=1, padx=20, pady=20)
CNC = CTkRadioButton(main_frame, text="CNC Turning Center", variable=selected_option, value=2, fg_color="green")
CNC.grid(row=1, column=1, padx=20, pady=20)
radio_buttons.append(CNC)
global cnc_text
cnc_text = CTkTextbox(master=main_frame, width=400, height=80, corner_radius=5)
cnc_text.grid(row=2, column=1, padx=20, pady=5)

# Palletizing Station
pallet_img = CTkImage(light_image=Image.open("pallet.png"),
                    dark_image=Image.open("pallet.png"),
                    size=(100, 100))
# pallet_btn = CTkButton(master=main_frame, text="Palletizing Station", image=pallet_img, corner_radius=32)
# pallet_btn.grid(row=0, column=2, padx=20, pady=20)
pallet_image = Image.open("pallet.png").resize((160, 160))
pallet_img = ImageTk.PhotoImage(pallet_image)
pallet_label = tk.Label(main_frame, image = pallet_img, text = "", bg="#2E2E2E")
pallet_label.grid(row=0, column=2, padx=20, pady=20)
Pallet = CTkRadioButton(main_frame, text="Palletizing Station", variable=selected_option, value=3, fg_color="green")
Pallet.grid(row=1, column=2, padx=20, pady=20)
radio_buttons.append(Pallet)
global pallet_text
pallet_text = CTkTextbox(master=main_frame, width=400, height=80, corner_radius=5)
pallet_text.grid(row=2, column=2, padx=20, pady=5)

# VMC Machine
vmc_img = CTkImage(light_image=Image.open("vmc.png"),
                    dark_image=Image.open("vmc.png"),
                    size=(100, 100))
# vmc_btn = CTkButton(master=main_frame, text="VMC Machine", image=vmc_img, corner_radius=32).grid(row=0, column=3, padx=20, pady=20)
vmc_image = Image.open("vmc.png").resize((160, 160))
vmc_img = ImageTk.PhotoImage(vmc_image)
vmc_label = tk.Label(main_frame, image = vmc_img, text = "", bg="#2E2E2E")
vmc_label.grid(row=0, column=3, padx=20, pady=20)
VMC = CTkRadioButton(main_frame, text="VMC Machine", variable=selected_option, value=4, fg_color="green")
VMC.grid(row=1, column=3, padx=20, pady=20)
radio_buttons.append(VMC)
global vmc_text
vmc_text = CTkTextbox(master=main_frame, width=400, height=80, corner_radius=5)
vmc_text.grid(row=2, column=3, padx=20, pady=5)

# Manual Inspection
man_img = CTkImage(light_image=Image.open("manual.png"),
                    dark_image=Image.open("manual.png"),
                    size=(100, 100))
# man_btn = CTkButton(master=main_frame, text="Manual Inspection", image=man_img, corner_radius=32).grid(row=3, column=3, padx=20, pady=20)
man_image = Image.open("manual.png").resize((160, 160))
man_img = ImageTk.PhotoImage(man_image)
man_label = tk.Label(main_frame, image = man_img, text = "", bg="#2E2E2E")
man_label.grid(row=3, column=3, padx=20, pady=20)
manual_inspection = CTkRadioButton(main_frame, text="Manual Inspection", variable=selected_option, value=5, fg_color="green")
manual_inspection.grid(row=4, column=3, padx=20, pady=20)
radio_buttons.append(manual_inspection)
global man_text
man_text = CTkTextbox(master=main_frame, width=400, height=80, corner_radius=5)
man_text.grid(row=5, column=3, padx=20, pady=20)

# Assembly Station
asm_img = CTkImage(light_image=Image.open("assembly.png"),
                    dark_image=Image.open("assembly.png"),
                    size=(100, 100))
# asm_btn = CTkButton(master=main_frame, text="Assembly Station", image=asm_img, corner_radius=32).grid(row=3, column=2, padx=20, pady=20)
asm_image = Image.open("assembly.png").resize((160, 160))
asm_img = ImageTk.PhotoImage(asm_image)
asm_label = tk.Label(main_frame, image = asm_img, text = "", bg="#2E2E2E")
asm_label.grid(row=3, column=2, padx=20, pady=20)
assembly_station = CTkRadioButton(main_frame, text="Assembly Station", variable=selected_option, value=6, fg_color="green")
assembly_station.grid(row=4, column=2, padx=20, pady=20)
radio_buttons.append(assembly_station)
global asm_text
asm_text = CTkTextbox(master=main_frame, width=400, height=80, corner_radius=5)
asm_text.grid(row=5, column=2, padx=20, pady=20)

# Performance Testing Station
pts_img = CTkImage(light_image=Image.open("performance.png"),
                    dark_image=Image.open("performance.png"),
                    size=(100, 100))
# pts_btn = CTkButton(master=main_frame, text="Palletizing Station", image=pts_img, corner_radius=32).grid(row=3, column=1, padx=20, pady=20)
pts_image = Image.open("performance.png").resize((160, 160))
pts_img = ImageTk.PhotoImage(pts_image)
pts_label = tk.Label(main_frame, image = pts_img, text = "", bg="#2E2E2E")
pts_label.grid(row=3, column=1, padx=20, pady=20)
performance_station = CTkRadioButton(main_frame, text="Palletizing Station", variable=selected_option, value=7, fg_color="green")
performance_station.grid(row=4, column=1, padx=20, pady=20)
radio_buttons.append(performance_station)
global pts_text
pts_text = CTkTextbox(master=main_frame, width=400, height=80, corner_radius=5)
pts_text.grid(row=5, column=1, padx=20, pady=20)

# Barcoding Station
barcode_img = CTkImage(light_image=Image.open("barcoding.png"),
                    dark_image=Image.open("barcoding.png"),
                    size=(100, 100))
# barcode_btn = CTkButton(master=main_frame, text="Manual Station", image=barcode_img, corner_radius=32).grid(row=3, column=0, padx=20, pady=20)
barcode_image = Image.open("barcoding.png").resize((160, 160))
barcode_img = ImageTk.PhotoImage(barcode_image)
barcode_label = tk.Label(main_frame, image = barcode_img, text = "", bg="#2E2E2E")
barcode_label.grid(row=3, column=0, padx=20, pady=20)
barcode_station = CTkRadioButton(main_frame, text="Manual Barcoding Station", variable=selected_option, value=8, fg_color="green")
barcode_station.grid(row=4, column=0, padx=20, pady=20)
radio_buttons.append(barcode_station)
global barcode_text
barcode_text = CTkTextbox(master=main_frame, width=400, height=80, corner_radius=5)
barcode_text.grid(row=5, column=0, padx=20, pady=20)

foot_image = Image.open("kv_logo.png")
footer_font = CTkFont(family="Roboto", size=12, weight="bold")
kv_image = CTkImage(dark_image=foot_image, size=(80, 50))
foot_label = CTkLabel(app, image=kv_image, text=f"developed by Keivalya Pandya (www.keivalya.com)", compound="left", font=footer_font)
foot_label.grid(row=6, column=0, padx=20, pady=5, sticky="ew", columnspan=2)

toggle_blink()

# Function to select the next radio option
def select_next():
    current_value = selected_option.get()
    if current_value < 8:
        selected_option.set(current_value + 1)
    else:
        selected_option.set(0)

global dict_of_stations_text
dict_of_stations_text = {
    1: asrs_text,
    2: cnc_text,
    3: pallet_text,
    4: vmc_text,
    5: man_text,
    6: asm_text,
    7: pts_text,
    8: barcode_text
}

# next_button = CTkButton(app, text="Trigger", command=select_next).grid(row=3, column=0, padx=20, pady=20)

if __name__ == "__main__":
    # Start the OPC UA server in a separate thread
    opcua_thread = threading.Thread(target=run_opcua_server)
    opcua_thread.daemon = True
    opcua_thread.start()

    app.mainloop()