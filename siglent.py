#!/usr/bin/env python
# Based heavily on code from: https://siglentna.com/application-note/programming-example-sds-oscilloscope-screen-capture-python/?pdf=8354
#-*- coding:utf-8 –*-
#-----------------------------------------------------------------------------
#The short script is a example that open a socket, sends a query #and closes the socket.
#-----------------------------------------------------------------------------
import socket # for sockets
import sys # for exit
import time # for sleep
#-----------------------------------------------------------------------------
 
remote_ip = "192.168.0.135" # should match the instrument’s IP address
port = 5025 # the port number of the instrument service
SOCKET_CLOSE_DELAY = 5
SOCKET_QUERY_DELAY = 1
SOCKET_RECEIVE_DELAY = 0.01

def SocketConnect():
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print ('Failed to create socket.')
        sys.exit();
    try:
        #Connect to remote server
        s.connect((remote_ip , port))
        s.setblocking(0) # non-blocking mode, an exception occurs when no data is detected by the receiver
        #s.settimeout(3) 
    except socket.error:
        print ('failed to connect to ip ' + remote_ip)
    return s
 
def SocketQuery(Sock, cmd):
    try :
        #Send cmd string
        Sock.sendall(cmd)
        Sock.sendall(b'\n') #Command termination
        time.sleep(SOCKET_QUERY_DELAY)
    except socket.error:
        #Send failed
        print ('Send failed')
        sys.exit()
 
    data_body = bytes() 
    while True:
        try:
            time.sleep(SOCKET_RECEIVE_DELAY)
            server_replay = Sock.recv(8000)
            #print(len(server_replay))
            data_body += server_replay
        except BlockingIOError:
            print("data received complete..")
            break
    return data_body
 
def SocketClose(Sock):
    #close the socket
    Sock.close()
    time.sleep(SOCKET_CLOSE_DELAY)
 
def main():
    global remote_ip
    global port
    global count
 
    # Open a socket, query the scope, save and close socket
#    s = SocketConnect()
    for i in range(100):
        s = SocketConnect()
        print("iteration: " + str(i))
        #qStr = SocketQuery(s, b'*IDN?') #Request ID info
        qStr = SocketQuery(s, b'SCDP') #Request screen image
        SocketClose(s)
        print(len(qStr))
        if len(qStr) == 0:
            break
    #SocketClose(s)
 
    sys.exit
 
if __name__ == '__main__':
    proc = main()
