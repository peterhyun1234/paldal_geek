# -*- coding: utf8 -*-

from socket import *
from select import select
import sys


HOST = '127.0.0.1'
PORT = 9000
BUFSIZE = 1024
ADDR = (HOST, PORT)


clientSocket = socket(AF_INET, SOCK_STREAM)


try: clientSocket.connect(ADDR)
except Exception as e:
    print('채팅 서버(%s:%s)에 연결 할 수 없습니다.' % ADDR)
    sys.exit()

print('채팅 서버(%s:%s)에 연결 되었습니다.' % ADDR)


def prompt():
    sys.stdout.write(" >> ")
    sys.stdout.flush()


while True:
    try:


        connection_list = [sys.stdin, clientSocket]
        read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

        for sock in read_socket:

     
            if sock == clientSocket:
               data = sock.recv(BUFSIZE)
               if not data:
                  print('채팅 서버(%s:%s)와의 연결이 끊어졌습니다.' % ADDR)
                  clientSocket.close()
                  sys.exit()
               else:
                  print "Server sock : "+str(sock)
                  print('%s' % data)  
                  prompt()

   
            else:
               message = sys.stdin.readline()
               print "What is this sock : "+str(sock)
               message = raw_input()
               clientSocket.send(message)
               prompt()

    except KeyboardInterrupt:
        clientSocket.close()
        sys.exit()
