'''
Joseph Flanagan
jcf29
004
'''
#! /usr/bin/env python3
# Echo Client
import sys 
import struct 
import time
import random
import json
#import socket
from socket import *

'''include pythons socket library'''
# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
hostname = sys.argv[3]

question = hostname + ' A IN'
#question = quest.encode('utf-8')
questLen = len(question)

'''create socket UDP socket for server'''
# Create UDP client socket. Note the use of SOCK_DGRAM
clientSocket = socket(AF_INET, SOCK_DGRAM)


counter = 0
mType = 1
returnCode = 0
ansLen = 0
iD = random.randint(0,100)

# Send data to server
clientSocket.settimeout(1)
#data = struct.pack("!II", 1, counter)# Initialize data to be sent
print("Sending Request to\t" + host + ", " + str(port) + ":")
print("Message ID:\t\t" + str(iD))
print("Question Length:\t" + str(questLen) + " bytes")
print("Answer Length\t\t0 bytes")
print("Question:\t\t" + str(question))

while counter < 3: 
    
    dDict = ({'mType': mType, 'returnCode': returnCode, 'iD': iD, 'questLen': questLen , 'question': question, 'ansLen': ansLen})
    data = json.dumps(dDict)
    #data = struct.pack('HHIHH', mType, returnCode, iD, questLen, ansLen)+question  
    #clientSocket.sendto(str(data).encode(),(host, port))
    clientSocket.sendto(data.encode(),(host, port))
    time.sleep(1)
          
    try:          
        
        dataEcho, address = clientSocket.recvfrom(1024)
        #dataEcho = struct.unpack(dataEcho.decode())
        dataEcho = json.loads(dataEcho.decode())
        
        if int(dataEcho.get('returnCode')) == 0:
            print("Received Responce from\t" + host + ", " + str(port) + ":")
            print("Return Code:\t\t0 (No errors)")
            print("Message ID:\t\t" + str(iD))
            print("Question Length:\t" + str(questLen) + " bytes")
            print("Answer Length:\t\t" + str(dataEcho.get('ansLen')) + " bytes")
            print("Question:\t\t" + str(question))
            print("Answer:\t\t\t" + str(dataEcho.get('ans')))
    
        elif int(dataEcho.get('returnCode')) == 1:
            print("Received Responce from\t" + host + ", " + str(port) + ":")
            print("Return Code:\t\t1 (Name does not exist)")
            print("Message ID:\t\t" + str(iD))
            print("Question Length:\t" + str(questLen))
            print("Answer Length\t\t0 bytes")
            print("Question:\t\t" + str(question))
        break
        
        
    except timeout:
        print("Request timed out ...")
        if counter < 2:
            print("Sending Request to\t" + host + ", " + str(port) + ":")
    counter += 1

#Close the client socket
clientSocket.close()

