import os
from PIL import Image, ImageTk
import tkinter as tk
from customtkinter import CTkImage, CTkRadioButton, CTkTextbox, CTkFrame, CTkFont, CTkLabel, CTkButton, set_appearance_mode, CTk
from opcua import Server, Client, ua
import threading
import time
from speech_main import speak
# import socket
from itertools import cycle
from dotenv import load_dotenv

# Load environment variables from the .env file and Access the variables
load_dotenv()
my_ip_address = os.getenv('MY_IP_ADDRESS')
my_port = os.getenv('MY_PORT')
st1_ip_address = os.getenv('ST1_IP_ADDRESS')
st1_port = os.getenv('ST1_PORT')
st2_ip_address = os.getenv('ST2_IP_ADDRESS')
st2_port = os.getenv('ST2_PORT')
st3_ip_address = os.getenv('ST3_IP_ADDRESS')
st3_port = os.getenv('ST3_PORT')
st4_ip_address = os.getenv('ST4_IP_ADDRESS')
st4_port = os.getenv('ST4_PORT')
st5_ip_address = os.getenv('ST5_IP_ADDRESS')
st5_port = os.getenv('ST5_PORT')
st6_ip_address = os.getenv('ST6_IP_ADDRESS')
st6_port = os.getenv('ST6_PORT')
st7_ip_address = os.getenv('ST7_IP_ADDRESS')
st7_port = os.getenv('ST7_PORT')
st8_ip_address = os.getenv('ST8_IP_ADDRESS')
st8_port = os.getenv('ST8_PORT')

class MachineStation:
    def __init__(self, master, name, image_path, variable, value, row, column):
        self.master = master
        self.name = name
        self.image_path = "assets/"+image_path
        self.variable = variable
        self.value = value
        self.row = row
        self.column = column
        self.create_widgets()
    
    def create_widgets(self):
        # Load and resize the image
        self.image = Image.open(self.image_path).resize((160, 160))
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.label_image = self.tk_image
        
        # Create and place the label with the image
        self.label = tk.Label(self.master, image=self.label_image, text="", bg="#2E2E2E")
        self.label.grid(row=self.row, column=self.column, padx=20, pady=20)
        
        # Create and place the radio button
        self.radio_button = CTkRadioButton(self.master, text=self.name, variable=self.variable, value=self.value, fg_color="green")
        self.radio_button.grid(row=self.row + 1, column=self.column, padx=20, pady=20)
        
        # Create and place the textbox
        self.textbox = CTkTextbox(self.master, width=400, height=80, corner_radius=5)
        self.textbox.grid(row=self.row + 2, column=self.column, padx=20, pady=5)

class OPCUAServer:
    def __init__(self, server_url, selected_option, gui_app):
        self.server_url = server_url
        self.selected_option = selected_option
        self.gui_app = gui_app
        self.server = Server()
        self.server.set_endpoint(self.server_url)
        self.server.register_namespace("https://www.keivalya.com")
        self.objects = self.server.get_objects_node()
        self.setup_variables()
    
    def setup_variables(self):
        self.param = self.objects.add_variable("ns=2;i=2", "Parameter", 0)
        self.bearing_number = self.objects.add_variable("ns=2;i=3", "BearingNumber", 0)
        self.inner_dia = self.objects.add_variable("ns=2;i=4", "innerDia", 0)
        self.outer_dia = self.objects.add_variable("ns=2;i=5", "outerDia", 0)
        self.bearing_height = self.objects.add_variable("ns=2;i=6", "bearingHeight", 0)
        self.housing = self.objects.add_variable("ns=2;i=7", "Housing", 0)
        self.shaft = self.objects.add_variable("ns=2;i=8", "Shaft", 0)
        self.pallet = self.objects.add_variable("ns=2;i=9", "Pallet", 0)
        self.bearing_cell = self.objects.add_variable("ns=2;i=10", "BearingCell", 0)
        self.housing_cell = self.objects.add_variable("ns=2;i=11", "HousingCell", 0)
        self.pallet_cell = self.objects.add_variable("ns=2;i=12", "PalletCell", 0)
        self.shaft_cell = self.objects.add_variable("ns=2;i=13", "shaftCell", 0)

        self.param.set_writable()
        self.bearing_number.set_writable()
        self.inner_dia.set_writable()
        self.outer_dia.set_writable()
        self.bearing_height.set_writable()
        self.housing.set_writable()
        self.shaft.set_writable()
        self.bearing_cell.set_writable()
        self.housing_cell.set_writable()
        self.pallet_cell.set_writable()
        self.shaft_cell.set_writable()
        self.pallet.set_writable()

    def run_server(self):
        try:
            self.server.start()
            print(f"Server started at {self.server_url}")
            while True:
                value = self.param.get_value()
                # bearing_no = self.bearing_number.get_value()
                # housing_type = self.housing.get_value()
                # shaft_type = self.shaft.get_value()
                repeat_var = False
                if value != self.selected_option.get():
                    print(f"Updating GUI with value: {value}")
                    self.update_radio_button(value)
                    if self.selected_option.get()==1 and repeat_var==False:
                        print(f"+-+-+- Received an order for -+-+-+-+-+-+-+-+ \
                              \n Brearing: \t {self.bearing_number.get_value()} \t {self.bearing_cell.get_value()} \
                              \n Housing:  \t {self.housing.get_value()} \t\t {self.housing_cell.get_value()} \
                              \n Shaft:    \t {self.shaft.get_value()} \t {self.shaft_cell.get_value()} \
                              \n+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+")
                        cst = self.selected_option.get()
                        # self.gui_app.station_1_demo()
                time.sleep(1)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.server.stop()

    def update_radio_button(self, value):
        try:
            if 0 <= int(value) <= 8:
                self.selected_option.set(int(value))
        except:
            pass

class GUIApp:
    def __init__(self):
        set_appearance_mode("Dark")
        self.app = CTk()
        self.selected_option = tk.IntVar()
        self.selected_option.set(0)
        self.colors = cycle(["red", "blue", "green"])
        self.radio_buttons = []
        self.dict_of_stations_text = {}
        self.image_refs = []
        self.setup_ui()
        self.opcua_server = OPCUAServer(server_url, self.selected_option, self)
    
    def setup_ui(self):
        self.app.after(0, lambda: self.app.state('zoomed'))
        self.app.title("Pragnya (प्रज्ञा) Software")
        self.app.grid_columnconfigure((0, 1), weight=1)

        image = Image.open("CoDM.png")
        title_font = CTkFont(family="Roboto", size=24, weight="bold")
        logo_image = CTkImage(dark_image=image, size=(100, 50))
        self.image_refs.append(logo_image)  # Store reference
        logo_label = CTkLabel(self.app, image=logo_image, text="प्रज्ञा \n Control Software", compound="left", font=title_font)
        logo_label.grid(row=0, column=0, padx=20, pady=5, sticky="ew", columnspan=2)

        main_frame = CTkFrame(master=self.app, width=200, height=800)
        main_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew", columnspan=2)
        main_frame.grid_columnconfigure((0, 1, 2, 3), weight=2)

        stations = [
            ("Automated Storage and Retrieval System", "asrs.png", 1, 0, 0),
            ("Triac PC", "cnc.png", 2, 0, 1),
            ("Palletizing Station", "pallet.png", 3, 0, 2),
            ("Mirac PC", "vmc.png", 4, 0, 3),
            ("Manual Inspection", "manual.png", 5, 3, 3),
            ("Assembly Station", "assembly.png", 6, 3, 2),
            ("Performance Testing Station", "performance.png", 7, 3, 1),
            ("Manual Barcoding Station", "barcoding.png", 8, 3, 0),
        ]

        for name, image_path, value, row, column in stations:
            station = MachineStation(main_frame, name, image_path, self.selected_option, value, row, column)
            self.radio_buttons.append(station.radio_button)
            self.dict_of_stations_text[value] = station.textbox
            self.image_refs.append(station.tk_image)  # Store reference

        foot_image = Image.open("kv_logo.png")
        footer_font = CTkFont(family="Roboto", size=12, weight="bold")
        kv_image = CTkImage(dark_image=foot_image, size=(80, 50))
        self.image_refs.append(kv_image)  # Store reference
        foot_label = CTkLabel(self.app, image=kv_image, text=f"developed by Keivalya Pandya (www.keivalya.com) \n currently at {server_url}", compound="left", font=footer_font)
        foot_label.grid(row=12, column=0, padx=20, pady=5, sticky="ew", columnspan=2)

        self.app.after(500, self.toggle_blink)
    
    def toggle_blink(self):
        current_value = self.selected_option.get()
        if current_value in range(1, 9):
            for button in self.radio_buttons:
                if button.cget('value') == current_value:
                    button.configure(fg_color=next(self.colors))
        self.app.after(500, self.toggle_blink)

    def complete_speaking(self, stn_num, voice_control, sentence):
        if "success" in sentence:
            self.dict_of_stations_text[stn_num].configure(fg_color="#1b7e57", wrap="word") # green
        elif "sent" in sentence:
            self.dict_of_stations_text[stn_num].configure(fg_color="#010048", wrap="word") # blue 
        else:
            self.dict_of_stations_text[stn_num].configure(fg_color="#2e0f3d", wrap="word") # purple
        self.dict_of_stations_text[stn_num].insert("0.0", "> " + sentence + "\n")
        speak(voice_control, sentence)

    def station_1_demo(self):
        client = Client("opc.tcp://"+st1_ip_address+":"+st1_port+"/")
        print(f"Attempting to Connect to opc.tcp://{st1_ip_address}:{st1_port}/")
        client.connect()
        word_var = client.get_node("ns=4;s=|var|Turck/ARM/WinCE TV.Application.PLC_PRG.MSG")
        word_value = ua.DataValue(ua.Variant("This is an OPCUA Demo!", ua.VariantType.String))
        word_var.set_value(word_value)
        speak("CS", f"Welcome to the O.P.C.U.A. Demo by Kayvi and Jay.")
        for led in range(1, 5):
            # ns=4;s=|var|Turck/ARM/WinCE TV.Application.PLC_PRG.ASRS_CMD
            this_var = client.get_node("ns=4;s=|var|Turck/ARM/WinCE TV.Application.PLC_PRG.ASRS_CMD")
            n_value = ua.DataValue(ua.Variant(led, ua.VariantType.Int16))
            this_var.set_value(n_value)
            time.sleep(0.5)
            if led == 1:
                ack_var = client.get_node("ns=4;s=|var|Turck/ARM/WinCE TV.Application.PLC_PRG.Ack_yellow")
                if ack_var.get_value() == True:
                    word_var.set_value(ua.DataValue(ua.Variant("Yellow glows!", ua.VariantType.String)))
                    speak("CS", f"The value of {led} bulb is set to GLOW!")
                    time.sleep(0.5)
                    speak("ST", "Confirmation received from system, the Yellow light is Glowing brightly!")
            elif led == 2:
                ack_var = client.get_node("ns=4;s=|var|Turck/ARM/WinCE TV.Application.PLC_PRG.Ack_red")
                if ack_var.get_value() == True:
                    word_var.set_value(ua.DataValue(ua.Variant("Red glows!", ua.VariantType.String)))
                    speak("CS", f"The value of {led} bulb is set to GLOW!")
                    time.sleep(0.5)
                    speak("ST", "Confirmation received from system, the Red light is Glowing brightly!")
            elif led == 3:
                ack_var = client.get_node("ns=4;s=|var|Turck/ARM/WinCE TV.Application.PLC_PRG.Ack_blue")
                if ack_var.get_value() == True:
                    word_var.set_value(ua.DataValue(ua.Variant("Blue glows!", ua.VariantType.String)))
                    speak("CS", f"The value of {led} bulb is set to GLOW!")
                    time.sleep(0.5)
                    speak("ST", "Confirmation received from system, the Blue light is Glowing brightly!")
            elif led == 4:
                ack_var = client.get_node("ns=4;s=|var|Turck/ARM/WinCE TV.Application.PLC_PRG.Ack_green")
                if ack_var.get_value() == True:
                    word_var.set_value(ua.DataValue(ua.Variant("Green glows!", ua.VariantType.String)))
                    speak("CS", f"The value of {led} bulb is set to GLOW!")
                    time.sleep(0.5)
                    speak("ST", "Confirmation received from system, the Green light is Glowing brightly!")
            elif led == 5:
                ack_var = client.get_node("ns=4;s=|var|Turck/ARM/WinCE TV.Application.PLC_PRG.Ack_final")
                if ack_var.get_value() == True:
                    speak("ST", "Confirmation received from system, the All the lights are Glowing brightly!")
        this_var.set_value(ua.DataValue(ua.Variant(0, ua.VariantType.Int16)))
        word_var.set_value(ua.DataValue(ua.Variant("Welcome to the DARK SIDE!", ua.VariantType.String)))
        speak("CS", "If only you knew the power of the dark side!")
        word_var.set_value(ua.DataValue(ua.Variant("OPCUA Demo Finished :) !", ua.VariantType.String)))
        client.disconnect()
        exit()
    
    def run(self):
        opcua_thread = threading.Thread(target=self.opcua_server.run_server)
        opcua_thread.daemon = True
        opcua_thread.start()
        self.app.mainloop()

if __name__ == "__main__":
    # server_url = "opc.tcp://10.10.14.77:4840"
    server_url = "opc.tcp://"+my_ip_address+":"+my_port
    gui_app = GUIApp()
    gui_app.run()
