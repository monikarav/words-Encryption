import socket
import threading
import socketserver
import sympy
from random import randint
import pickle
import messagestruct
from Crypto.Cipher import DES3


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def serveRequest(self, key):
        key = f"{key:<24}"
        print("final key ", key)
        msg = self.request.recv(1024)
        msg = pickle.loads(msg)
        requestedFile = msg.reqserv.filename
        try:

            filepath = "files/" + requestedFile
            with open(filepath, "rb") as file:
                data = file.read(1024)
                cipher = DES3.new(key)
                completed = True
                counter = 1
                while len(data) > 0:
                    blockLength = len(data)
                    rem = blockLength % 1024
                    if rem:
                        data += bytes(1024 - rem)
                        print("adjusted: ", len(data))
                    encrypted_text = cipher.encrypt(data)
                    if rem:

                        sentpacket = messagestruct.Message(messagestruct.Hdr(100, None, None), None, None, None,
                                                       messagestruct.EncMsg(encrypted_text),
                                                       None)
                    else :

                        sentpacket = messagestruct.Message(messagestruct.Hdr(30, None, None), None, None, None,
                                                       messagestruct.EncMsg(encrypted_text),
                                                       None)
                    sentmsg = pickle.dumps(sentpacket)
                    print(counter)
                    counter = counter + 1
                    print("sent message size :",len(sentmsg))
                    self.request.sendall(sentmsg)
                    data = file.read(1024)
                lastpacket = messagestruct.Message(messagestruct.Hdr(40, None, None), None, None,
                                                   messagestruct.ReqServ(completed), None, None)
                lastmsg = pickle.dumps(lastpacket)
                self.request.sendall(lastmsg)
                print("file sent")
        except FileNotFoundError:
            print("file not found")
            sentpacket = messagestruct.Message(messagestruct.Hdr(50, None, None), None, None, None, None,
                                               messagestruct.Disconnect(completed))
            sentmsg = pickle.dumps(sentpacket)
            self.request.sendall(sentmsg)

    def handle(self):
        secret_key = randint(999, 999999)
        data = str(self.request.recv(1024), 'ascii')
        print(data)
        data = self.request.recv(1024)
        m1 = pickle.loads(data)
        m1pubkeyq = m1.publickey.q
        m1pubkeyalpha = m1.publickey.alpha
        A = m1.publickey.y
        y = (pow(m1pubkeyalpha, secret_key)) % m1pubkeyq
        m1 = messagestruct.Message(messagestruct.Hdr(10, None, None), messagestruct.Pubkey(m1pubkeyq, m1pubkeyalpha, y),
                                   None, None, None,
                                   None)
        m1 = pickle.dumps(m1)
        self.request.sendall(m1)
        sharedkey1 = (pow(A, secret_key)) % m1pubkeyq

        secret_key = randint(999, 999999)
        y = (pow(m1pubkeyalpha, secret_key)) % m1pubkeyq
        data = self.request.recv(1024)
        m1 = pickle.loads(data)
        A = m1.publickey.y
        sharedkey2 = (pow(A, secret_key)) % m1pubkeyq
        m1 = messagestruct.Message(messagestruct.Hdr(10, None, None), messagestruct.Pubkey(m1pubkeyq, m1pubkeyalpha, y),
                                   None, None, None,
                                   None)
        m1 = pickle.dumps(m1)
        self.request.sendall(m1)

        secret_key = randint(999, 999999)
        y = (pow(m1pubkeyalpha, secret_key)) % m1pubkeyq
        data = self.request.recv(1024)
        m1 = pickle.loads(data)
        A = m1.publickey.y
        sharedkey3 = (pow(A, secret_key)) % m1pubkeyq
        m1 = messagestruct.Message(messagestruct.Hdr(10, None, None), messagestruct.Pubkey(m1pubkeyq, m1pubkeyalpha, y),
                                   None, None, None,
                                   None)
        m1 = pickle.dumps(m1)
        self.request.sendall(m1)

        print("sharedkey1 ", sharedkey1)
        print("sharedkey2 ", sharedkey2)
        print("sharedkey3 ", sharedkey3)
        while True:
            self.serveRequest(str(sharedkey1) + str(sharedkey2) + str(sharedkey3))
        


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


ip, port = "localhost", 8001
server = ThreadedTCPServer((ip, port), ThreadedTCPRequestHandler)
server.serve_forever()
