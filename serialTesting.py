
import serial
from serialCom import SerialProtocol
import time
from messageBuffer import MessageBuffer
import logging

logging.basicConfig(level=logging.DEBUG)

ser = serial.Serial('COM5', 9600 )

manager = SerialProtocol(ser, 8)
sendBuffer = MessageBuffer()

messageLen = 8
hueVal = 0
delayBetweenChange = 100

hueSent = False


ardReady = False

def encodeMessage(message):
    for i in range(len(message)):
        message[i]=message[i].encode('ascii')
    return message

def fillMessage(message, fillLen):
    return message + [0]*(fillLen-len(message))


while not ardReady:
    if manager.readSerial():
        recievedMessage = manager.getMessage()
        manager.resetMessage()
        if recievedMessage[0] == 1 and recievedMessage[1] == 2 : #Device sending ID
            deviceID=inString=''.join(str(recievedMessage[2:6]))
            logging.debug("Connected to device with ID: {} ".format(deviceID))
            ardReady = True
    else:
        logging.debug("Sending request for ID")
        message = fillMessage([1,3],messageLen)
        logging.debug(message)
        manager.writeSerial(message)
        time.sleep(1)


def sendHue(hue):
    hue  = int(hue)
    sendBuffer.addMessage(fillMessage([2,2,hue,255,255], messageLen))

sendHue(hueVal)
hueSent = True
startTime = time.time()

try:
    while True:
        #Handle complete messages
        if manager.readSerial():
            recievedMessage = manager.getMessage()
            manager.resetMessage()
            if recievedMessage[0] == 3 and recievedMessage[1] == 2:
                if hueSent:
                    logging.debug("Hue confirmation recieved after {:5.1f} ms"\
                    .format((time.time()-startTime)*1000))
                    hueSent = False
        if not hueSent and (time.time()-startTime)*1000 > delayBetweenChange:
            hueVal = hueVal + 1
            if hueVal > 255: hueVal = 0
            logging.debug("Setting hue to {}".format(hueVal))
            sendHue(hueVal)
            hueSent = True
            startTime = time.time()

        for waitingMessage in sendBuffer:
            manager.writeSerial(waitingMessage)


except KeyboardInterrupt:
    ser.close()
    logging.debug("Closing")
