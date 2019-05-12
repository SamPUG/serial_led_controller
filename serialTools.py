import serial
import serial.tools.list_ports as serialtools

ignorePorts=['COM1'] #Make this controlled by some kind of settings file

def getSerialDevices():
    ports=serialtools.comports()
    portDevices=[]

    for port in ports:
        if ignorePorts.count(port.device) == 0:
            try:
                serial.Serial(port.device).close()
                portDevices.append(port.device)
            except serial.SerialException:
                pass

    portDevices.reverse()
    return portDevices
