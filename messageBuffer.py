
# Class for storing messages which are queued for serial

class MessageBuffer:
    def __init__(self):
        self.messageList = []
        self._messagesStored = 0

        self._sentList = []
        self.awaitingResponse = 0


    # Add a message to the storage array. Returns true if new val is added
    def addMessage(self, message, replaceSame=2):
        # Check if a message is stored with the same first two bytes
        if replaceSame > 0:
            for storedMessage in self.messageList:
                if storedMessage[0:replaceSame] == message[0:replaceSame]:
                    storedMessage[replaceSame:] = message[replaceSame:]
                    return False

        self.messageList.append(message)
        self.messagesStored += 1
        return True

    def retrieveMessage(self):
        retrievedMessage = []
        if len(self.messageList) > 0 :
            retrievedMessage = self.messageList[0]
            #Move message to sent list
            self._sentList.append(retrieveMessage)
            self.awaitingResponse += 1
            self.messageList = self.messageList[1:]
            self.messagesStored -= 1

        return retrievedMessage

#   Checks the awaiting response list and returns true if message is in list
    def checkResponse(self, message, removeFound = True):
        try:
            index=self._sentList.index(message)
            if removeFound:
                self._sentList.pop(index)
                self.awaitingResponse -=1
            return true
        except ValueError:
            pass
        return False
