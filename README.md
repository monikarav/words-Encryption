# File-Encryption
## Commands to Run :
*  for server : python3 server.py
*  for client : python3 client.py
## Packet structure :
/*A general message */


typedef struct {


Hdr hdr; /* Header for a message */
typedef union {
PubKey pubkey;
ReqServ reqserv;
ReqCom reqcom;
EncMsg encmsg;
Disconnect disconnect;
} AllMsg;
} Msg;
    
