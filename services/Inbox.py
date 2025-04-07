from datetime import datetime
import csv

class Message:
    def __init__(self, messageID, chatID, messageContents, sender, receiver, timeSent):
        self.messageContents = messageContents
        self.sender = sender
        self.receiver = receiver
        self.timeSent = timeSent
        self.messageID = messageID
        self.chatID = chatID

    def to_dict(self):
        return {
            'messageID': self.messageID,
            'chatID': self.chatID,
            'messageContents': self.messageContents,
            'sender': self.sender,
            'receiver': self.receiver,
            'timeSent': self.timeSent.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            int(data['messageID']),
            int(data['chatID']),
            data['messageContents'],
            data['sender'],
            data['receiver'],
            datetime.strptime(data['timeSent'], '%Y-%m-%d %H:%M:%S')
        )

class RoommateAgreement:
    def __init__(self, rmaID, user1, user2, user1Signature, user2Signature):
        self.rmaID = rmaID
        self.user1 = user1
        self.user2 = user2
        self.user1Signature = user1Signature
        self.user2Signature = user2Signature

    @classmethod
    def from_dict(cls, data):
        return cls(
            int(data['rmaID']),
            data['user1'],
            data['user2'],
            data['party1Signature'],
            data['party2Signature']
        )

# False means we are accepting the request, true means we deny it.
# Code 0 - Accepting request.
# Code 1 - Signed by both.
# Code 2 - Person requesting (user1) has already signed.
# Code 3 - Person requesting (user2) has already signed.
# Code 4 - Person requesting hasn't signed an already existing pending agreement between this individual.

def checkForExists(agreements, username, recipient):
    if not agreements:
        return {"val": False, "code": 0, "rmaID" : "DNE"} # No agreements so no chance for it already existing.
    else:
        for agreement in agreements.values():
            rmaID = agreement.rmaID
            if ((agreement.user1 == username and agreement.user2 == recipient) or
                    (agreement.user1 == recipient and agreement.user2 == username)):

                # Check if both signatures exist (truthy)
                if agreement.user1Signature == 'True' and agreement.user2Signature == 'True':
                    return {"val": True, "code": 1, "rmaID" : rmaID}  # Fully signed by both users
                elif username == agreement.user1 and agreement.user1Signature == 'True':
                    return {"val": True, "code": 2, "rmaID" : rmaID} # Person requesting it has already signed.
                elif username == agreement.user2 and agreement.user2Signature == 'True':
                    return {"val": True, "code": 3, "rmaID" : rmaID} # Same thing but incase requester is cataloged as user2 in cvs.
                else:
                    return {"val": True, "code": 4, "rmaID" : rmaID} # Since the agreement already exists, this is the recipient who is unaware there is a RMA waiting for there signature with this person already.
                
            else:
                return {"val": False, "code": 0, "rmaID" : rmaID} # There exist agreements, however this particular one doesn't exist yet.
        

class Chat:
    def __init__(self, chatID, user1, user2, messages):
        self.user1 = user1
        self.user2 = user2
        self.messages = messages or []
        self.chatID = chatID

    def getNextID(self):
       if not self.messages:
           return 1
       return max(message.messageID for message in self.messages) + 1
    
    def newMessage(self, messageContents, sender):
        if sender == self.user1:
            receiver = self.user2
        else:
            receiver = self.user1

        message = Message(self.getNextID(), self.chatID, messageContents, sender, receiver, datetime.now())

        self.messages.append(message)

        return message

def load_agreements_from_csv(filename='agreements.csv', agreements=[]):
    agreements.clear()
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['rmaID'].lower() == 'rmaid':
                continue
            agreement = RoommateAgreement.from_dict(row)
            agreements[agreement.rmaID] = agreement

def save_agreements_to_csv(filename='agreements.csv', agreements={}):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['rmaID', 'user1', 'user2', 'party1Signature', 'party2Signature']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for agreement in agreements.values():
            writer.writerow({
                'rmaID': agreement.rmaID,
                'user1': agreement.user1,
                'user2': agreement.user2,
                'party1Signature': agreement.user1Signature,
                'party2Signature': agreement.user2Signature
            })


def load_messages_from_csv(filename='messages.csv', chats=[]):
    chats.clear()
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['messageID'].lower() == 'messageid':  
                    continue 
                msg = Message.from_dict(row)
                if msg.chatID not in chats:
                    chats[msg.chatID] = Chat(msg.chatID, msg.sender, msg.receiver, messages=[])
                chats[msg.chatID].messages.append(msg)