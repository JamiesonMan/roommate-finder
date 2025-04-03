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