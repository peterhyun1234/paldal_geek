#-*- coding: utf-8 -*-

# socket 과 select 모듈 임포트
from socket import *
from select import *
import sys
import logging
import time
from time import sleep
from time import ctime
from cabinet import cabinet
import datetime
from gtts import gTTS
import os

# Variable Initialization
lcd = ""
tid = ""
tn = -1
lcdSock = 0
lcdState = 0

# Ultra Sonic Variable Initialization
ultra_sonic_value = 0
check_list = [0,0]
temp_cl = 0

c1Sock = 0
c2Sock = 0
# Speech  variable Initialize
tts = gTTS(text='안녕하세요. 스마트 사물함입니다. 학번과 비밀번호 입력해주세요.',lang='ko')
tts.save("hello.mp3")

cl = [ cabinet('201420999','1234',4,True,False), cabinet('','',5,False,False) ]

# log기록을 남기기 위한 변수
logger = logging.getLogger("Leni")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
logger.info("Start Server System")

# 호스트, 포트와 버퍼 사이즈를 지정
HOST = '192.168.1.134'
#HOST = '192.168.24.147'
#HOST = '127.0.0.1'
PORT = 9000 # 36789
BUFSIZE = 1024
ADDR = (HOST, PORT)

# 소켓 객체를 만들고..
serverSocket = socket(AF_INET, SOCK_STREAM)

# 서버 정보를 바인딩
serverSocket.bind(ADDR)

# 요청을 기다림(listen)
serverSocket.listen(10)
connection_list = [serverSocket]
print('==============================================')
print(' 서버를 시작합니다. %s 포트로 접속을 기다립니다.' % str(PORT))
print('==============================================')

# 무한 루프를 시작
while connection_list:
    try:

        # select 로 요청을 받고, 10초마다 블럭킹을 해제하도록 함
        read_socket, write_socket, error_socket = select(connection_list, [], [], 10)

        for sock in read_socket:
            # 새로운 접속
            if sock == serverSocket:
                clientSocket, addr_info = serverSocket.accept()
                connection_list.append(clientSocket)
                # Cabinet 1
                if clientSocket.fileno() == 4:
                    c1Sock = len(connection_list) - 1
                # Cabinet 2
                elif clientSocket.fileno() == 5:
                    c2Sock = len(connection_list) - 1
                #LCD Socket Assignment
                if clientSocket.fileno() == 7:
                    lcdSock = len(connection_list) - 1

                logger.debug("INFO : [%s] 클라이언트(%s)가 새롭게 연결 되었습니다." % (ctime(), addr_info[0]))
                # 서버소켓이 아닌 경우 방문을 환영한다는 message를 전송한다 - - - - - - - - - - - - - My Part
                if connection_list[-1] != serverSocket:
                    print("Client Socket Connected")
                    #connection_list[-1].send("[%s] 방문을 환영합니다. 반가워요 ^u^" %ctime()) 
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - My Part

                # 전체 클라이언트로 응답을 돌려줌 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Original
                '''for socket_in_list in connection_list:
                    if socket_in_list != serverSocket and socket_in_list != sock:
                        try:
                            socket_in_list.send('[%s] 새로운 방문자가 대화방에 들어왔습니다. 반가워요~ 짝짝짝!' % ctime())
                        except Exception as e:
                            socket_in_list.close()
                            connection_list.remove(socket_in_list)'''
                # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Original

            # 접속한 사용자(클라이언트)로부터 새로운 데이터 받음
            # O: 사물함 열기, C: 닫기, N: LED 키기, F: 끄기
            else:
                data = sock.recv(BUFSIZE)
                data = data.decode()
                ds = sock.fileno()
                if cl[1].isUse == True:
                    if cl[1].checkTimeout() == True:
                        cl[1].isUse = False
                        cl[1].isOpen = True
                        cl[1].id = ''        
                        cl[1].pwd = ''
                        # 사물함 열고 LED 끄고 반납
                        connection_list[c2Sock].send('O'.encode('utf-8'))
                        connection_list[c2Sock].send('F'.encode('utf-8'))
                if data:
                    if data.find('201420999') != -1:
                        data = '201420999'
                    elif data.find('0') != -1:
                        data = '0'
                    elif data.find('1') != -1:
                        data = '1'
                    elif data.find('2') != -1:
                        data = '2'
                    elif data.find('3') != -1:
                        data = '3'
                    elif data.find('4') != -1:
                        data = '4'
                    elif data.find('5') != -1:
                        data = '5'
                    elif data.find('6') != -1:
                        data = '6'
                    elif data.find('7') != -1:
                        data = '7'
                    elif data.find('C') != -1:
                        data = 'C'
                    # Cabinet
                    #if ds == 4 || ds == 5:
                    #    print "Cabinet"
                    # Button
                    if ds == 6:
                        print("Data: " + data + ", LCD: " + lcd + ", LCD Len: " + str(len(lcd)) + ", Status: " + str(lcdState))
                        # LCD First Display
                        if lcdState == 0:
                            if (data.find('1') != -1 or data.find('2') != -1) and lcd == '':
                                lcd += data
                                connection_list[lcdSock].send(lcd.encode('utf-8'))
                            elif data.find('6') != -1 and lcd.find('1') != -1:
                                lcdState = 1
                                lcd = ''
                                connection_list[lcdSock].send('Input cabinet\nNum:'.encode('utf-8'))
                            elif data.find('6') != -1 and lcd.find('2') != -1:
                                lcdState = 2
                                lcd = ''
                                connection_list[lcdSock].send('Input cabinet\nNum:'.encode('utf-8'))
                            elif data.find('7') != -1 and len(lcd) != 0:
                                lcd = ''
                                connection_list[lcdSock].send(data.encode('utf-8'))
                        # Enroll LCD
                        elif lcdState == 1:
                            if data.find('6') != -1 and len(lcd) != 0:
                                target = int(lcd)
                                for c in cl:
                                    print(str(c.num) + " " + str(c.id))
                                    if target == c.num:
                                        if c.isUse == True:
                                            connection_list[lcdSock].send('Already Using'.encode('utf-8'))
                                            sleep(1)
                                            lcdState = 0
                                            lcd = ''
                                            connection_list[lcdSock].send('7'.encode('utf-8'))
                                            break
                                        else:
                                            connection_list[lcdSock].send('Input Nine Length ID'.encode('utf-8'))
                                            lcdState = 11
                                            lcd = ''
                                            break
                                    elif c == cl[-1]:
                                        connection_list[lcdSock].send('There is no such Number'.encode('utf-8'))
                                        sleep(1)
                                        lcdState = 0
                                        lcd = ''
                                        connection_list[lcdSock].send('D'.encode('utf-8'))
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ''
                                    connection_list[lcdSock].send('7'.encode('utf-8'))
                                else:
                                   lcd = lcd[:-1]
                                   connection_list[lcdSock].send(lcd.encode('utf-8'))
                            else:
                                if len(lcd) <= 32:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                                else:
                                    connection_list[lcdSock].send('Overflow!!'.encode('utf-8'))
                                    sleep(1)
                                    lcdState = 0
                                    lcd = ''
                                    connection_list[lcdSock].send('7'.encode('utf-8'))
                        # Input ID
                        elif lcdState == 11:
                            if data.find('6') != -1:
                                if len(lcd) == 9:
                                    connection_list[lcdSock].send('Please Four Length PWD'.encode('utf-8'))
                                    tid = lcd
                                    lcdState = 12
                                    lcd = ""
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ""
                                    connection_list[lcdSock].send('7'.encode('utf-8'))
                                else:
                                    lcd = lcd[:-1]
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                            else:
                                if len(lcd) == 9:
                                    connection_list[lcdSock].send('No Longer than 9 Letters'.encode('utf-8'))
                                    sleep(1)
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                                else:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                        # Input Password
                        elif lcdState == 12:
                            if data.find('6') != -1:
                                if len(lcd) == 4:
                                    connection_list[lcdSock].send('Enroll Complete!!'.encode('utf-8'))
                                    sleep(1)
                                    cl[1].pwd = lcd
                                    cl[1].isUse = True
                                    cl[1].id = tid
                                    cl[1].isOpen = False
                                    cl[1].enrollt = datetime.datetime.now()
                                    connection_list[c2Sock].send('N'.encode('utf-8'))
                                    lcd = ""
                                    lcdState = 0
                                    tid = ""
                                    connection_list[lcdSock].send('D'.encode('utf-8'))
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ""
                                    connection_list[lcdSock].send('7'.encode('utf-8'))
                                else:
                                    lcd = lcd[:-1]
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                            else:
                                if len(lcd) == 4:
                                    connection_list[lcdSock].send('No Longer than 4 Letters'.encode('utf-8'))
                                    sleep(1)
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                                else:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                        # Open Cabinet
                        elif lcdState == 2:
                            if data.find('6') != -1 and len(lcd) != 0:
                                connection_list[lcdSock].send('Please Four Length PWD'.encode('utf-8'))
                                tn = int(lcd)
                                lcdState = 21
                                lcd = ""
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ""
                                    connection_list[lcdSock].send('7'.encode('utf-8'))
                                else:
                                    lcd = lcd[:-1]
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                            else:
                                if len(lcd) == 3:
                                    connection_list[lcdSock].send('No Longer than 3 Letters'.encode('utf-8'))
                                    sleep(1)
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                                else:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                        # Input Password
                        elif lcdState == 21:
                            if data.find('6') != -1:
                                if len(lcd) == 4:
                                    for c in cl:
                                        if tn == c.num:
                                            # Open Success!
                                            if c.pwd == lcd:
                                                connection_list[lcdSock].send('Open Success!!'.encode('utf-8'))
                                                connection_list[c2Sock].send('O'.encode('utf-8'))
                                                c.isOpen = True
                                                sleep(1)
                                                lcd = ""
                                                lcdState = 0
                                                tn = -1
                                                connection_list[lcdSock].send('D'.encode('utf-8'))
                                            else:
                                                connection_list[lcdSock].send('Password is not correct!!'.encode('utf-8'))
                                                sleep(1)
                                                lcd = ""
                                                connection_list[lcdSock].send('7'.encode('utf-8'))
                                        elif c == cl[-1]:
                                            connection_list[lcdSock].send('There is no number like that!'.encode('utf-8'))
                                            sleep(1)
                                            lcd = ""
                                            lcdState = 0
                                            tn = -1
                                            connection_list[lcdSock].send('D'.encode('utf-8'))
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ""
                                    connection_list[lcdSock].send('7'.encode('utf-8'))
                                else:
                                    lcd = lcd[:-1]
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                            else:
                                if len(lcd) == 4:
                                    connection_list[lcdSock].send('No Longer than 4 Letters'.encode('utf-8'))
                                    sleep(1)
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                                else:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd.encode('utf-8'))
                               
                    # 초음파
                    # 8
                    elif ds == 8:
                        if data.find('1') != -1:
                            check_list[0]= check_list[1]
                            check_list[1]= 1
                            #print("가까워짐")
                            if check_list[0] == 2 and check_list[1] == 1:
                                os.system("mpg321 hello.mp3")
                        if data.find('2') != -1:
                            check_list[0]= check_list[1]
                            check_list[1]= 2
                            #print("멀어짐")
                    # RFID
                    # 9
                    elif ds == 9:
                        for c in cl:
                            # print("Data: " + data)
                            # print(len(data))
                            if str(c.id) == data:
                                if c.isUse == True:
                                    c.isOpen = True
                                    print("RFID로 사물함 열기")
                                    connection_list[c1Sock].send('O'.encode('utf-8'))
                    # Cabinet 1
                    elif ds == c1Sock:
                        if data.find('C') != -1:
                            print("4th Cabinet Closed")
                            cl[0].isOpen = False
                    # Cabinet 2
                    elif ds == c2Sock:
                        if data.find('C') != -1:
                            print("5th Cabinet Closed")
                            cl[1].isOpen = False
                    # 서버소켓이 아니며 자기자신이닌 연결 소켓들에게 메시지를 전체 전송하는 부분 - - - - - - - - - - - - - - - - - - - - - - - - - - - - Original
                    '''for socket_in_list in connection_list:
                        if socket_in_list != serverSocket and socket_in_list != sock:
                            try:
                                socket_in_list.send('[%s] %s' % (ctime(), data))
                                print('[INFO][%s] 클라이언트로 데이터를 전달합니다.' % ctime())
                            except Exception as e:
                                print(e.message)
                                socket_in_list.close()
                                connection_list.remove(socket_in_list)
                                continue'''
                    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - Original
                       
                else:
                    connection_list.remove(sock)
                    sock.close()
                    logger.debug("INFO : [%s] 사용자와의 연결이 끊어졌습니다." % ctime())
                    
    except KeyboardInterrupt:
        # 부드럽게 종료하기
        serverSocket.close()
        sys.exit()
