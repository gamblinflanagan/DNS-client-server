'''
Joseph Flanagan
jcf29
004
'''
#! /usr/bin/env python3
# Echo Server
import sys 
import struct
import struct 
import time
import json
#import socket
from socket import *

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
returnCode = 1
fileName = 'dns-master.txt'
ansLen = 0
mType = 1

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(1024)
    data = json.loads(data.decode())
    #data = struct.unpack_from('!hhihh', data, 12)
    print("Receive data from client " + address[0] + ", " + str(address[1])) # + ": " + data.decode())
    
    question = data.get('question')
    questLen = data.get('questLen')
    iD = data.get('iD')
    
    fileObj = open(fileName, 'r')
    for line in fileObj:
        if question in line:
            ans = line
            break
    fileObj.close()
    
    if len(ans) > 0:
        ansLen = len(ans)
        returnCode = 0
    else:
        returnCode = 1
        
    #serverSocket.sendto(data2,address)
    print("Sending Data to client " + address[0] + ", " + str(address[1])) # + ": " + data.decode())
    dDict = {'mType': mType, 'returnCode': returnCode, 'ans': ans, 'ansLen': ansLen}
    data = json.dumps(dDict)
    #data = struct.pack('HHIHH', mType, returnCode, ansLen)+ans
    serverSocket.sendto(str(data).encode(),address)
    
#struct.pack/unpack for ints
#encode/decode for strings

