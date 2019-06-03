# -*- coding: utf8 -*-

from socket import *
from select import select
import sys
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from cabinet import cabinet

HOST = '192.168.1.134'
PORT = 9000
BUFSIZE = 1024
ADDR = (HOST, PORT)


clientSocket = socket(AF_INET, SOCK_STREAM)

# Initialize RFID
reader = SimpleMFRC522()

# Initialize Cabinet
# cl = [ cabinet('201420974','1234',4,True), cabinet('201420999','1234',5,False) ]

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

        while 1:
            id, text = reader.read()
            # print(text)
            text = text[0:9]
            msg = text
            clientSocket.send(msg.encode('utf-8'))
                 


    except KeyboardInterrupt:
        GPIO.cleanup()
        clientSocket.close()
        sys.exit()
