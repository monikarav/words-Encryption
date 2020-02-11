import socket
import threading
import socketserver
import sympy
from random import randint
import pickle
import messagestruct
from Crypto.Cipher import DES3

global g
global q


def gcd(a, b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def primitive_root(modulo):
    required_set = set(num for num in range(1, modulo) if gcd(num, modulo) == 1)
    for g in range(1, modulo):
        actual_set = set(pow(g, powers) % modulo for powers in range(1, modulo))
        if required_set == actual_set:
            return g


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    ip, port = "localhost", 8001
    sock.connect((ip, port))
    message = input("enter message")
    sock.sendall(bytes(message, 'ascii'))
    q = sympy.randprime(8693, 41603)

    g = primitive_root(q)

    secret_key = randint(999, 999999)
    y = (pow(g, secret_key)) % q

    m1 = messagestruct.Message(messagestruct.Hdr(10, None, None), messagestruct.Pubkey(q, g, y), None, None, None, None)
    m1 = pickle.dumps(m1)
    sock.sendall(m1)

    data = sock.recv(1024)
    m1 = pickle.loads(data)
    B = m1.publickey.y
    sharedkey1 = (pow(B, secret_key)) % q

    secret_key = randint(999, 999999)
    y = (pow(g, secret_key)) % q
    m1 = messagestruct.Message(messagestruct.Hdr(10, None, None), messagestruct.Pubkey(q, g, y), None, None, None, None)
    m1 = pickle.dumps(m1)
    sock.sendall(m1)
    data = sock.recv(1024)
    m1 = pickle.loads(data)
    B = m1.publickey.y
    sharedkey2 = (pow(B, secret_key)) % q

    secret_key = randint(999, 999999)
    y = (pow(g, secret_key)) % q
    m1 = messagestruct.Message(messagestruct.Hdr(10, None, None), messagestruct.Pubkey(q, g, y), None, None, None, None)
    m1 = pickle.dumps(m1)
    sock.sendall(m1)
    data = sock.recv(1024)
    m1 = pickle.loads(data)
    B = m1.publickey.y
    sharedkey3 = (pow(B, secret_key)) % q
    print("sharedkey1 ", sharedkey1)
    print("sharedkey2 ", sharedkey2)
    print("sharedkey3 ", sharedkey3)

    key = str(sharedkey1) + str(sharedkey2) + str(sharedkey3)
    key = f"{key:<24}"
    print("final key",key)
    while True:
        filename = input("Enter file to be downloaded")
        msg = messagestruct.Message(messagestruct.Hdr(20, None, None), None, messagestruct.ReqServ(filename), None,
                                    None, None)
        sentmsg = pickle.dumps(msg)
        sock.sendall(sentmsg)
        packrecv = sock.recv(1294)
        msgrecv = pickle.loads(packrecv)


        if msgrecv.hdr.opcode == 50:
            print("File not found error")
            break
        cipher = DES3.new(key)
        with open("client/" + filename, "wb") as file:
            counter = 1
            striped = 0
            while msgrecv.hdr.opcode != 40 :                
                decrypted_msg = cipher.decrypt(msgrecv.encmsg.encodedMessage)
                if msgrecv.hdr.opcode == 100 :
                     print("stripping")   
                     decrypted_msg = decrypted_msg.rstrip(b'\x00')
                     striped =1
                file.write(decrypted_msg)
                #recv_data = 0
                
                packrecv = sock.recv(1294)
                # if len(temp) == 0:
                #     break
                # packrecv += temp
                # recv_data += len(temp)


                print(counter)
                counter += 1     
                print("packet length",len(packrecv))
                print("opcode ",msgrecv.hdr.opcode)               
                msgrecv = pickle.loads(packrecv)
                                
        print("file recv")