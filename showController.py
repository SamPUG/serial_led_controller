import serialCom as sc
import time
import logging
import messageBuffer

logger=logging.getLogger('ShowController')


# Main link between hardware and UI
class ShowController():
    def __init__(self):
        self.messageLen=8

        self.deviceType=0
        self.deviceID = [0,0,0]
        self.connected=False
        self.comHandler=None

#       Max number of messages which should be sent to the arduino at once.
#       Really this should depend on the buffer size and message length.
#       Arduino nano serial buffer is 64 bytes, so theoretically we could send 8
        self.maxMessageSend=4
        self.sendBuffer = messageBuffer.MessageBuffer()

        print("I love beth")

#   Connect to led strip device using request for ID
    def connectDevice(self, serialObject, maxAttempts=3, timeBetweenRetries=0.5):
        logger.info("Attempting to connect to device.")
        attempts = 0
        tempComHandler = sc.SerialProtocol(serialObject, self.messageLen)
        tempComHandler.writeSerial([1,3])
        lastAttempt=time.time()
        time.sleep(1)
        while attempts < maxAttempts:
            if (time.time()-lastAttempt) > timeBetweenRetries:
                logger.info("Connect attempt {} on Serial port: {}".format(attempts,serialObject.port))
                if tempComHandler.readSerial():
                    logger.info("Got message from port: {}".format(serialObject.port))
                    # Check if it is an id reply message
                    if tempComHandler.getMessage()[0] == 1 and tempComHandler.getMessage()[1] == 2:
                        logger.info("Device found on port: {}".format(serialObject.port))
                        self.connected=True
                        self.deviceType=tempComHandler.getMessage()[2]
                        self.deviceID=tempComHandler.getMessage()[3:7]
                        tempComHandler.resetMessage()
                        self.comHandler=tempComHandler
                        return True
                    else:
                        logger.info("Recieved an unexpected reply.")
                        tempComHandler.resetMessage()
                attempts+=1
                tempComHandler.writeSerial([1,3])
                lastAttempt=time.time()

        logger.info("No device found on port: {}".format(serialObject.port))
        return False

    def disconnectDevice(self):
        self.deviceType=0
        self.deviceID = [0,0,0]
        self.connected=False
        self.comHandler=None

#   Queue methods add a message to the handler so they are sent next time
#   a send is called

    def queueRequestStatus(self):
        pass

    def queueRequestShow(self):
        pass

    def queueSendShow(self, showNo, vals):
        pass

    def queueSendStatus(self, **kwargs):
        # Default all to false
        sendOnOff = 0
        onOffVal = 0
        sendBrighness = 0
        brightnessVal=0
        sendPlayPause = 0
        playPauseVal=0

        for key, value in kwargs.items():
            if key == 'onOff':
                sendOnOff=1
                onOffVal=value
            elif key == 'brightness':
                sendBrighness=1
                brightnessVal=value
            elif key == 'playPause':
                sendPlayPause=1
                playPauseVal=value

        # Need more advanced logic for checking the send buffer



    def queueRequestId(self):


#   Get info from the Arduino
    def getInfo(self):
        self.queueRequestStatus()
        self.queueRequestShow()
