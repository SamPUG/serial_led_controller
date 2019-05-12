import tkinter as tk
from tkinter import ttk
import logging
import showController
import serialTools
import globals
import serial

logger = logging.getLogger('mainWindow')

#Main window for program
class MainWindow(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__ (parent, *args, **kwargs)
        self.parent=parent

        self.grid(column=0, row=0)

        self.ledStrip=showController.ShowController()
        self.serialObject=None

        self.generalBar=GeneralBar(self)
        self.generalBar.grid(column=0,row=1)

    def connectDevice(self, serialDeviceName):
        try:
            self.serialObject=serial.Serial(serialDeviceName, globals.baudRate)
            if self.ledStrip.connectDevice(self.serialObject):
                self.generalBar.connectDevice("".join([str(val) for val in self.ledStrip.deviceID])) #Want to allow user to save a name

            else: raise serial.SerialException

        except serial.SerialException:
            logger.warning("Could not connect to device at port {}".format(serialDeviceName))
            self.disconnectDevice()

    def disconnectDevice(self, finalClose = False):
        if self.serialObject != None:
            self.serialObject.close()
            
        if self.ledStrip.connected: self.ledStrip.disconnectDevice()
        self.generalBar.disconnectDevice(finalClose)



class GeneralBar(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__ (parent, *args, **kwargs)
        self.parent=parent
        self.grid(column=0, row=0)
        self.ledStrip=parent.ledStrip

        # Initialise power button
        ttk.Label(self, text="Power:").grid(column=0, row=0, sticky='E')
        self.bt_power = ttk.Button(self)
        self.bt_power.grid(column=1, row=0, sticky='W')

        # Initialise play/pause button
        ttk.Label(self, text="Play/Pause:").grid(column=0, row=1, sticky='E')
        self.bt_playPause = ttk.Button(self)
        self.bt_playPause.grid(column=1, row=1, sticky='W')

        #Initialise brightness
        ttk.Label(self, text="Brightness:").grid(column=0, row=2, sticky='E')
        self.sc_brightness = ttk.Scale(self, orient="horizontal", \
            length=150, from_=0, to=100)
        self.sc_brightness.grid(column=1, row=2)

        #Add a middle frame for a bit of padding
        self.columnconfigure(2, minsize=100)
        self.rowconfigure(3, minsize=10)

        #Device name
        ttk.Label(self, text="Device Name:").grid(column=0, row=4, sticky='E')
        self.lb_deviceName = ttk.Label(self)
        self.lb_deviceName.grid(column=1,row=4, sticky='W')

        #Initialise serial
        ttk.Label(self, text="Serial Port:").grid(column=3, row=0, sticky="W")
        self.cb_serialport=ttk.Combobox(self,state=['disabled'])
        self.cb_serialport['values'] = ('Test1', 'Test2', 'Test3')
        self.cb_serialport.grid(column=4, row=0, columnspan=2)
        self.bt_serialportReferesh=ttk.Button(self,text="Refresh",command=self.populatePorts)
        self.bt_serialportReferesh.grid(column=4, row=1)
        self.bt_serialport=ttk.Button(self, command=self.serialConnect_cb)
        self.bt_serialport.grid(column=5, row=1, sticky="E")

        #Show name
        ttk.Label(self, text="Show Name:").grid(column=3, row=4, sticky="W")
        self.cb_showName=ttk.Combobox(self)
        self.cb_showName.grid(column=4, row=4, columnspan=2)

        for child in self.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.disconnectDevice() #Initialise UI for disconnected device

    # Find which ports are valid led strips
    def populatePorts(self):
        devices=serialTools.getSerialDevices()
        validPorts=[]

        for device in devices:
            with serial.Serial(device, globals.baudRate) as serialObj:
                if self.ledStrip.connectDevice(serialObj):
                    logger.info("Valid device found on port: {}".format(device))
                    validPorts.append(device)
                    self.ledStrip.disconnectDevice()

        if len(validPorts) > 0:
            self.cb_serialport.state(['readonly', '!disabled'])
            self.bt_serialport.state(['!disabled'])
            self.cb_serialport['values'] = tuple(validPorts)
            self.cb_serialport.set(validPorts[0])
        else:
            logger.info("No valid ports found")
            self.bt_serialport.state(['disabled'])
            self.cb_serialport.state(['disabled'])
            self.cb_serialport.set("No valid devices")

    def disconnectDevice(self, finalClose=False):
        # Power defaults
        self.bt_power.state(['disabled'])
        self.bt_power['text']="Unknown"
        #Playpause defaults
        self.bt_playPause.state(['disabled'])
        self.bt_playPause['text']="Unknown"
        #Brightness slider
        self.sc_brightness.state(['disabled'])
        #Device name
        self.lb_deviceName['text']="No device connected"
        #Show
        self.cb_showName.state(['disabled'])
        #Serial port
        self.bt_serialportReferesh.state(['!disabled'])
        self.bt_serialport['text']="Connect"
        if not finalClose: self.populatePorts() #Repopulate lists if not exit

    def connectDevice(self, deviceName):
        self.lb_deviceName['text']=deviceName
        self.bt_serialportReferesh.state(['disabled'])
        self.bt_serialport['text']="Disconnect"

    def serialConnect_cb(self):
        if self.bt_serialport['text'] == "Connect":
            self.parent.connectDevice(self.cb_serialport.get())
        else:
            self.parent.disconnectDevice()
