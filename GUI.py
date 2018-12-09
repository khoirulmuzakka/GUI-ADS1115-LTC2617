"""
Created on Tue Dec  4 00:20:30 2018

@author: khoirul_muzakka
"""

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from ADS1115 import *
from LTC2617 import *

########## LTC2617 Frame #############
class LTC2617_Interface :
    def __init__(self,master):
        self.master=master
        
    def create_widget_DAC(self) :              
        self.DAC_frame = tk.LabelFrame(self.master, text= "LTC2617 DAC", labelanchor="n", borderwidth=1)
        self.DAC_frame.pack(fill="both", expand=True,  side="top", pady=10)
        #####Configuration Section####
        self.config_section=tk.LabelFrame(self.DAC_frame, text = "Configuration", borderwidth=0)#configuration section
        self.config_section.pack(fill="both", expand=True, pady=5)
        
        #Vref
        self.V_ref=tk.Label(self.config_section, text = "V_ref :") #Vref
        self.V_ref.grid(row=0, column=0, sticky='E', padx=3, pady=3)
        
        self.V_ref_var=tk.DoubleVar()
        self.V_ref_var.set(5.0)
        self.V_ref_entry= tk.Entry(self.config_section, width=10, textvariable=self.V_ref_var)
        self.V_ref_entry.grid(row=0, column=1, sticky='E', padx=5, pady=3)
        
        #Vreflo
        self.V_reflo=tk.Label(self.config_section, text = "V_reflo :") #Vreflo
        self.V_reflo.grid(row=0, column=2, sticky='E', padx=3, pady=5)
        
        self.V_reflo_var=tk.DoubleVar()
        self.V_reflo_var.set(0.0)
        self.V_reflo_entry= tk.Entry(self.config_section, width=10, textvariable=self.V_reflo_var)
        self.V_reflo_entry.grid(row=0, column=3, sticky='E', padx=5, pady=5)
        
        #####Conversion Section#####
        self.conver_section= tk.LabelFrame(self.DAC_frame, text = "Conversion to Analog", borderwidth=0)#conversion section
        self.conver_section.pack(fill="both", expand=True, pady=5)
        
        #self.chnlA=tk.Label(self.conver_section, text = "Channel A")
        #self.chnlA.grid(row=0, column=1, sticky='E', padx=5, pady=5)
        
        self.btnA_var = tk.IntVar()
        self.btnA_var.set(1)        
        self.cbA = tk.Checkbutton(self.conver_section, text= "Channel A", var=self.btnA_var)#checkbox for channel A
        self.cbA.grid(row=0, column=0, padx=10)
        
        self.chnA_entry_var = tk.DoubleVar()
        self.chnA_entry_var.set(0.0)
        self.chnA_entry= tk.Entry(self.conver_section, textvariable=self.chnA_entry_var) #channelA entry value
        self.chnA_entry.grid(row=0, column = 1)
        
        self.btnA=tk.Button(self.conver_section, text="CONVERT", command = self.convert_A_pressed) #convertbuttonA
        self.btnA.grid(row=0, column=2, padx=10)
        
        #self.chnlB=tk.Label(self.conver_section, text = "Channel B")
        #self.chnlB.grid(row=1, column=1, sticky='E', padx=5, pady=5)
        self.btnB_var = tk.IntVar()
        self.btnB_var.set(1)  
        self.cbB = tk.Checkbutton(self.conver_section, text="Channel B", var = self.btnB_var)#checkbox for channel B
        self.cbB.grid(row=1, column=0)
        
        self.chnB_entry_var = tk.DoubleVar()
        self.chnB_entry_var.set(0.0)
        self.chnB_entry= tk.Entry(self.conver_section, textvariable= self.chnB_entry_var ) #channelB entry value
        self.chnB_entry.grid(row=1, column = 1)
        
        self.btnB=tk.Button(self.conver_section, text="CONVERT")
        self.btnB["command"]= self.convert_B_pressed   
        self.btnB.grid(row=1, column=2, padx=10)
        
        #Create an instance based on the above input
        self.LTC2617 = LTC2617(0x41)
    
    def convert_A_pressed(self) :
        V_REF = self.V_ref_var.get()
        V_REFLO = self.V_reflo_var.get()
        if self.btnA_var.get()==1:
            self.LTC2617.write(self.chnA_entry_var.get(), self.btnA_var.get(), self.btnB_var.get())
        else :
            self.write(0, self.btnA_var.get(), self.btnB_var.get())
    def convert_B_pressed(self):
        if self.btnB_var.get()==1 :
            self.LTC2617.write(self.chnB_entry_var.get(), self.btnA_var.get(), self.btnB_var.get())
        else :
            self.write(0, self.btnA_var.get(), self.btnB_var.get())
            
            
            
        
    
  
        
        
 
################ ADS1115 Frame #############      
class ADS1115_Interface:
    def __init__(self, master):
        self.master=master
        #MessageBar.__init__(self, master)
                
    def create_widget_ADC(self):
        
        self.ADC_frame = tk.LabelFrame(self.master, text = "ADS1115 ADC",labelanchor="n",  borderwidth=1)
        self.ADC_frame.pack(fill="both", side="top", expand =True, pady =5)
        
        
        ########Configuration Section#####
        self.config_section1=tk.LabelFrame(self.ADC_frame, text = "Configuration", borderwidth=0)#configuration section
        self.config_section1.pack(fill="both", expand=True, pady=5)
        
        # Address
        self.address=tk.Label(self.config_section1, text="Address :")
        self.address.grid(row=0, column=0, padx=2, sticky="E")

        self.address_cbbx=ttk.Combobox(self.config_section1, width= 10)
        self.address_cbbx["values"] = ("0x48", "0x49", "0x4A", "0x4B")
        self.address_cbbx.current(0)
        self.address_cbbx.grid(row=0, column =1, padx=5, sticky="W")
        
        #mode
        self.mode=tk.Label(self.config_section1, text="mode :")
        self.mode.grid(row=0, column=2, padx=2, sticky="E")

        self.mode_cbbx=ttk.Combobox(self.config_section1, width= 10)
        self.mode_cbbx["values"] = ("Single", "Continuous")
        self.mode_cbbx.current(0)
        self.mode_cbbx.grid(row=0, column =3, padx=5, pady=5, sticky="E")
        
        #FSR
        self.FSR=tk.Label(self.config_section1, text="FSR :")
        self.FSR.grid(row=1, column=0, padx=2, sticky="E")

        self.FSR_cbbx=ttk.Combobox(self.config_section1, width= 10)
        self.FSR_cbbx["values"] = (4.096, 2.048, 1.024)
        self.FSR_cbbx.current(0)
        self.FSR_cbbx.grid(row=1, column =1, padx=5, pady=5, sticky="W")
        
        #Datarate
        self.DR=tk.Label(self.config_section1, text="Data Rate :")
        self.DR.grid(row=1, column=2, padx=2, sticky="E")

        self.DR_cbbx=ttk.Combobox(self.config_section1, width= 10)
        self.DR_cbbx["values"] = (8, 16, 32, 64, 128, 250, 475, 860)
        self.DR_cbbx.current(0)
        self.DR_cbbx.grid(row=1, column =3, padx=5, pady=5, sticky="E")
        
        # Channel
        self.channel=tk.Label(self.config_section1, text="Channel :")
        self.channel.grid(row=2, column=0, padx=2, sticky="E")

        self.channel_cbbx=ttk.Combobox(self.config_section1, width= 25)
        self.channel_cbbx["values"] = ("AINP = AIN0 and AINN = GND", "AINP = AIN1 and AINN = GND", 
                    "AINP = AIN2 and AINN = GND", "AINP = AIN3 and AINN = GND")
        self.channel_cbbx.current(0)
        self.channel_cbbx.grid(row=2,column=1, columnspan =2, padx=5, pady=5)
        
        #######Functionality Section#######
        self.funct_section=tk.LabelFrame(self.ADC_frame, text = "Functionality", borderwidth=0)#configuration section
        self.funct_section.pack(fill="both", expand=True, pady=5)
        
        #read
        self.read_ADC=tk.Button(self.funct_section, text= "READ ", command =self.read_button)
        self.read_ADC.grid(row=0, column=0, sticky='W', padx=5, pady=5)
        
        #Value
        self.value=tk.Label(self.funct_section, text= "Value :")
        self.value.grid(row=0, column=1, sticky='W', padx=10, pady=5)
        
        #Read Entry
        self.read_var = tk.StringVar()
        self.read_var.set("some random")
        self.read_entry=tk.Entry(self.funct_section,  textvariable = self.read_var)
        self.read_entry.grid(row=0, column=2, sticky='W', padx=10, pady=5)
        #read_entry.configure(state="readonly")
        
        #lastread
        self.last_read_ADC=tk.Button(self.funct_section, text= "LAST READ", command = self.last_read_button)
        self.last_read_ADC.grid(row=1, column=0, sticky='W', padx=5, pady=5)
        
        #lastValue
        self.last_value=tk.Label(self.funct_section, text= "Value :")
        self.last_value.grid(row=1, column=1, sticky='W', padx=10, pady=5)
        
        #LAstRead Entry
        self.last_read_var = tk.StringVar()
        self.last_read_var.set("some random")
        self.last_read_entry=tk.Entry(self.funct_section,  textvariable = self.last_read_var)
        self.last_read_entry.grid(row=1, column=2, sticky='W', padx=10, pady=5)

        #Create an instance based on the above input
        self.full_config()
        self.ADS1115= Ads1115(self.address, self.channel, self.FSR, self.mode, self.DR)
     
    def full_config(self):
        def get_address() :
            return int(self.address_cbbx.get()[2:], 16)
        def get_channel() :
            for key, value in channel_list.items():
                if value == self.channel_cbbx.get():
                    return key
        def get_DR():
            for key, value in data_rate_list.items():
                if value == int(self.DR_cbbx.get()):
                    return key
        def get_FSR():
            for key, value in FSR_list.items():
                if value == float(self.FSR_cbbx.get()):
                    return key
        def get_mode():
            if self.mode_cbbx.get() == "Single":
                return 1
            if self.mode_cbbx.get() =="Continuous":
                return 0
        self.address = get_address()
        self.channel = get_channel()
        self.FSR = get_FSR()
        self.mode = get_mode()
        self.DR = get_DR()
        
    def read_button(self):
        #self.full_config()
        def read_ADC():#update ADC configuration based on the laest input
            self.full_config() #update config
            return self.ADS1115.read()
        self.read_var.set(read_ADC())
        '''def read_raw_ADC():
            return self.ADS1115.raw_data()
        
        MessageBar.message_entry.insert(tk.INSERT, "oke")'''
        
    def last_read_button(self):
        def last_read_ADC():#update ADC configuration based on the laest input
            self.full_config() #update config
            return self.ADS1115.last_read()
        self.last_read_var.set(last_read_ADC())
        
        
        
        
###########Init Button##########
       
class InitButton(object):
    def __init__(self, master):
        self.master=master
    def create_widget_init(self):
        self.init_frame=tk.Frame(self.master)
        self.init_frame.pack()
        self.initbtn=tk.Button(self.init_frame, text="REINIT")
        self.initbtn.grid(column=0,row=0, sticky="n", pady=5)
        
        self.quitbtn=tk.Button(self.init_frame, text="QUIT", command=main_window.quit)
        self.quitbtn.grid(column=1,row=0, sticky="n", pady=5)
        
 
#####################Status and message bar##############       
class MessageBar ():
    def __init__(self, master) :
        self.master=master
        
        
        
    def create_widget_MB(self):      
        self.message_bar = tk.LabelFrame(self.master, text = "Message", borderwidth=1)
        self.message_bar.pack(fill="y", side="bottom")
        
        #entry
        #self.message_entry_var = tk.StringVar()
        #self.message_entry_var.set("So far so good")
        self.message_entry = scrolledtext.ScrolledText(self.message_bar)
        self.message_entry.insert(tk.INSERT, "So far so good")
        self.message_entry.pack(fill="both", expand=True)
        
        
        

        
        
        




main_window = tk.Tk()
main_window.maxsize(410, 580)
#main_window.geometry("500x600")
main_window.title("ADS1115 & LTC2617")

DAC_section = LTC2617_Interface(main_window)
DAC_section.create_widget_DAC()

ADS_section = ADS1115_Interface(main_window)
ADS_section.create_widget_ADC()

init = InitButton(main_window)
init.create_widget_init()

message_bar= MessageBar(main_window)
message_bar.create_widget_MB()
main_window.mainloop()
    
    

