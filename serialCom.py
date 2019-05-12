import serial
from enum import Enum
import time
import logging

logger = logging.getLogger('serialCom')


class SerialProtocol:
    # Class is given an open serial object
    def __init__(self, serialObject, message_len, start_char = 0x13, end_char = 0x15, esc_char = 0x17 ):
        self.ser = serialObject
        self.start_char = start_char.to_bytes(1,'little')
        self.end_char = end_char.to_bytes(1,'little')
        self.esc_char = esc_char.to_bytes(1,'little')

        self.max_message_len = message_len

        self.message_state_enum = Enum('message_state', 'WAIT_HEADER IN_MSG AFTER_ESC')
        self.current_message_state = self.message_state_enum.WAIT_HEADER

        self.read_buffer = []  #Blank list for input
        self.message_recieved = False

    def resetMessage(self):
        self.message_recieved = False
        self.read_buffer = []
        self.current_message_state = self.message_state_enum.WAIT_HEADER

    def getMessage(self):
        if self.message_recieved:
            return self.read_buffer
        return []

    def readSerial(self):
        while self.ser.in_waiting > 0:
            inByte = self.ser.read()
            # print(inByte)
            if self.current_message_state == self.message_state_enum.WAIT_HEADER and inByte == self.start_char :
                self.current_message_state = self.message_state_enum.IN_MSG
            elif self.current_message_state == self.message_state_enum.IN_MSG:
                if inByte == self.esc_char:
                     self.current_message_state = self.message_state_enum.AFTER_ESC
                elif inByte == self.end_char:
                    # print("Message complete")
                    self.message_recieved = True
                    return True
                elif inByte == self.start_char:
                    self.resetMessage()
                    logger.error("Recieved unescaped start char in message")
                else:
                    if len(self.read_buffer) < self.max_message_len:
                        self.read_buffer.append(int.from_bytes(inByte, byteorder='little'))
                    else: #Message is too long
                        self.resetMessage()
                        logger.error("Message is too long.")
            elif self.current_message_state == self.message_state_enum.AFTER_ESC:
                self.current_message_state = self.message_state_enum.IN_MSG
                if len(self.read_buffer) < self.max_message_len:
                    self.read_buffer.append(int.from_bytes(inByte, byteorder='little'))
                else: #Messgae is too long
                    self.resetMessage()
                    logger.error("Message is too long.")

        return False

    def writeSerial(self, message):
        #Make message the correct length
        if len(message) < self.max_message_len:
            message =  message + [0]*(self.max_message_len-len(message))
        self.ser.write(self.start_char)
        for byte in message:
            currentByte=byte.to_bytes(1,'little',signed=False)
            if currentByte == self.start_char or  currentByte == self.end_char or currentByte == self.esc_char:
                self.ser.write(self.esc_char)
            #print("Writing byte {}".format(currentByte))
            self.ser.write(currentByte)
        self.ser.write(self.end_char)
