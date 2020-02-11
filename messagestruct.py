class Hdr:
    def __init__(self, opcode, s_addr, d_addr):
        self.opcode = opcode
        self.s_addr = s_addr
        self.d_addr = d_addr


class Pubkey:
    def __init__(self, q, alpha, y):
        self.q = q
        self.alpha = alpha
        self.y = y


class ReqServ:
    def __init__(self, filename):
        self.filename = filename


class ReqCom:
    def __init__(self):
        self.status = False


class EncMsg:
    def __init__(self, encodedMessage):
        self.encodedMessage = encodedMessage


class Disconnect:
    def __init__(self):
        self.disconnectstatus = False


class Message:
    def __init__(self, hdr, publickey, reqserv, requestcompleted, encmsg, disconnect):
        self.hdr = hdr
        self.publickey = publickey
        self.reqserv = reqserv
        self.requestcompleted = requestcompleted
        self.encmsg = encmsg
        self.disconnect = disconnect
