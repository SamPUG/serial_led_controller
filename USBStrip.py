import tkinter as tk
import tkinter.ttk as ttk


root = tk.Tk()

mainFrame = ttk.Frame(root)
mainFrame.grid(column = 0, row=0)

generalFrame = ttk.Frame(mainFrame, borderwidth=5, width=500, height=200, relief='sunken')
generalFrame.grid(column = 0, row=0)

def testCb():
    print(generalFrame.bbox())

serialFrame = ttk.Frame(generalFrame)
serialFrame.grid(column=1,row=0, sticky="e", rowspan = 2)
generalFrame.columnconfigure(1, minsize=250)

cbSerialPorts = ttk.Combobox(serialFrame, state = 'readonly')
cbSerialPorts.grid(column=0, row=0, padx=5, pady=5, columnspan=2)
cbSerialPorts['values'] = ("Test com1", "test com2", "test com 3")

bConnect = ttk.Button(serialFrame, text='Connect', command = testCb)
bConnect.grid(column=0, row = 1, padx=5, pady=5)

bDisconnect = ttk.Button(serialFrame, text='Disconnect')
bDisconnect.grid(column=1, row = 1, padx=5, pady=5)

bOnOff = ttk.Button(generalFrame, text='on')
bOnOff.grid(column=0, row=0, padx=5, pady=5, sticky="w")

bPause = ttk.Button(generalFrame, text='pause')
bPause.grid(column=0, row=1, padx=5, pady=5, sticky="w")

brightnessFrame = ttk.Frame(generalFrame)
brightnessFrame.grid(column=0, row=2, padx=5, pady = 5, sticky= "w")


ttk.Label(brightnessFrame, text="Brightness:").grid(column=0, row=0, sticky="w")
scBrightness = ttk.Scale(brightnessFrame, orient="horizontal", length=100, from_ = 0, to = 255)
scBrightness.grid(column=1, row = 0, sticky = "w")

generalFrame.columnconfigure(0, minsize=250)

showFrame = ttk.Frame(generalFrame, borderwidth=5, relief='sunken', width=500, height=300)
showFrame.grid(column = 0, row=100, columnspan=100)


class value_slider():
    # Returns the frame object which contains the slider and value
    def __init__(self, parent, label, sliderLen, minVal, maxVal, sliderValCallback=None, callbackTimeout = 200):
        self.sliderValCallback=sliderValCallback
        self.callbackTimeout = callbackTimeout
        self.containerFrame = ttk.Frame(parent)
        self.label=ttk.Label(self.containerFrame, text=label).grid(column=0, row=0, sticky="w")
        self.slider=ttk.Scale(self.containerFrame, orient="horizontal", length=sliderLen, from_ = minVal, to = maxVal)

        self.callbackId=0

        if(self.sliderValCallback != None):
            self.slider.configure(command=self.callback)
        self.slider.grid(column=1, row=0, sticky="w")

    def callback(self, *args):
        if(self.callbackId  != 0):
            root.after_cancel(self.callbackId)

        self.callbackId=root.after(self.callbackTimeout, self.end_timeout)

    def get_slider_val(self):
        print("In class callback")
        return self.slider.get()

    def end_timeout(self):
        self.sliderValCallback(self)


valueSliders = []

rgbCanvas = tk.Canvas(showFrame, width = 90, height = 90)
rgbCanvas.grid(column=1, row=0, padx=5, pady = 5, sticky= "ne", rowspan = 2 )
bgRec = rgbCanvas.create_rectangle(0,0,90,90, fill="red")


def rgb_callback(sliderObject):
    print("Red: {}".format(valueSliders[0].get_slider_val()))
    print("Green: {}".format(valueSliders[1].get_slider_val()))
    print("Blue: {}".format(valueSliders[2].get_slider_val()))




valueSliders.append(value_slider(showFrame, "R:", 100, 0, 255, rgb_callback))
valueSliders.append(value_slider(showFrame, "G:", 100, 0, 255, rgb_callback))
valueSliders.append(value_slider(showFrame, "B:", 100, 0, 255, rgb_callback))

showFrame.columnconfigure(0, minsize=400)
showFrame.columnconfigure(1, minsize=100)

for i in range(len(valueSliders)):
    valueSliders[i].containerFrame.grid(row=i,padx=5, pady = 5, sticky= "w")






root.mainloop()
