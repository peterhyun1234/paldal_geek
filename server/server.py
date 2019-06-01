#-*- coding: utf-8 -*-

# socket 과 select 모듈 임포트
from socket import *
from select import *
import sys
import logging
from time import sleep
from time import ctime
from cabinet import cabinet
import datetime

# Variable Initialization
lcd = ""
tid = ""
tn = -1
lcdSock = 0
lcdState = 0

cl = [ cabinet('201420999','1234',4,True), cabinet('','',5,False) ]

# log기록을 남기기 위한 변수
logger = logging.getLogger("Leni")
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)
logger.info("Start Server System")

# 호스트, 포트와 버퍼 사이즈를 지정
HOST = '127.0.0.1'
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
print('영화 서버를 시작합니다. %s 포트로 접속을 기다립니다.' % str(PORT))
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
                # LCD Socket Assignment
                if clientSocket.fileno() == 5: #7
                    lcdSock = len(connection_list) - 1
                logger.debug("INFO : [%s] 클라이언트(%s)가 새롭게 연결 되었습니다." % (ctime(), addr_info[0]))
                # 서버소켓이 아닌 경우 방문을 환영한다는 message를 전송한다 - - - - - - - - - - - - - My Part
                if connection_list[-1] != serverSocket:
                    print "Client Socket Connected"
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
            else:
                data = sock.recv(BUFSIZE)
                ds = sock.fileno()
                if data:
                    if data.find('1') != -1:
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
                    # Cabinet
                    #if ds == 4 || ds == 5:
                    #    print "Cabinet"
                    # Button
                    if ds == 4:
                        print "Data: " + data + ", LCD: " + lcd + ", LCD Len: " + str(len(lcd)) + ", Status: " + str(lcdState)
                        # LCD First Display
                        if lcdState == 0:
                            if (data.find('1') != -1 or data.find('2') != -1) and lcd == '':
                                lcd += data
                                connection_list[lcdSock].send(lcd)
                            elif data.find('6') != -1 and lcd.find('1') != -1:
                                lcdState = 1
                                lcd = ''
                                connection_list[lcdSock].send('Input cabinet\nNum:')
                            elif data.find('6') != -1 and lcd.find('2') != -1:
                                lcdState = 2
                                lcd = ''
                                connection_list[lcdSock].send('Input cabinet\nNum:')
                            elif data.find('7') != -1 and len(lcd) != 0:
                                lcd = ''
                                connection_list[lcdSock].send(data)
                        # Enroll LCD
                        elif lcdState == 1:
                            if data.find('6') != -1:
                                target = int(lcd)
                                for c in cl:
                                    print str(c.num) + " " + str(c.id)
                                    if target == c.num:
                                        if c.isUse == True:
                                            connection_list[lcdSock].send('Already Using')
                                            sleep(1)
                                            lcdState = 0
                                            lcd = ''
                                            connection_list[lcdSock].send('7')
                                            break
                                        else:
                                            connection_list[lcdSock].send('Input Nine Length ID')
                                            lcdState = 11
                                            lcd = ''
                                            break
                                    elif c == cl[-1]:
                                        connection_list[lcdSock].send('There is no such Number')
                                        sleep(1)
                                        lcdState = 0
                                        lcd = ''
                                        connection_list[lcdSock].send('D')
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ''
                                    connection_list[lcdSock].send('7')
                                else:
                                   lcd = lcd[:-1]
                                   connection_list[lcdSock].send(lcd)
                            else:
                                if len(lcd) <= 32:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd)
                                else:
                                    connection_list[lcdSock].send('Overflow!!')
                                    sleep(1)
                                    lcdState = 0
                                    lcd = ''
                                    connection_list[lcdSock].send('7')
                        # Input ID
                        elif lcdState == 11:
                            if data.find('6') != -1:
                                if len(lcd) == 9:
                                    connection_list[lcdSock].send('Please Four Length PWD')
                                    tid = lcd
                                    lcdState = 12
                                    lcd = ""
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ""
                                    connection_list[lcdSock].send('7')
                                else:
                                    lcd = lcd[:-1]
                                    connection_list[lcdSock].send(lcd)
                            else:
                                if len(lcd) == 9:
                                    connection_list[lcdSock].send('No Longer than 9 Letters')
                                    sleep(1)
                                    connection_list[lcdSock].send(lcd)
                                else:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd)
                        # Input Password
                        elif lcdState == 12:
                            if data.find('6') != -1:
                                if len(lcd) == 4:
                                    connection_list[lcdSock].send('Enroll Complete!!')
                                    sleep(1)
                                    cl[1].pwd = lcd
                                    cl[1].isUse = True
                                    cl[1].id = tid
                                    cl[1].enrollt = datetime.datetime.now()
                                    lcd = ""
                                    lcdState = 0
                                    tid = ""
                                    connection_list[lcdSock].send('D')
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ""
                                    connection_list[lcdSock].send('7')
                                else:
                                    lcd = lcd[:-1]
                                    connection_list[lcdSock].send(lcd)
                            else:
                                if len(lcd) == 4:
                                    connection_list[lcdSock].send('No Longer than 4 Letters')
                                    sleep(1)
                                    connection_list[lcdSock].send(lcd)
                                else:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd)
                        # Open Cabinet
                        elif lcdState == 2:
                            if data.find('6') != -1:
                                connection_list[lcdSock].send('Please Four Length PWD')
                                tn = int(lcd)
                                lcdState = 21
                                lcd = ""
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ""
                                    connection_list[lcdSock].send('7')
                                else:
                                    lcd = lcd[:-1]
                                    connection_list[lcdSock].send(lcd)
                            else:
                                if len(lcd) == 3:
                                    connection_list[lcdSock].send('No Longer than 3 Letters')
                                    sleep(1)
                                    connection_list[lcdSock].send(lcd)
                                else:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd)
                        # Input Password
                        elif lcdState == 21:
                            if data.find('6') != -1:
                                if len(lcd) == 4:
                                    for c in cl:
                                        if tn == c.num:
                                            # Open Success!
                                            if c.pwd == lcd:
                                                connection_list[lcdSock].send('Open Success!!')
                                                sleep(1)
                                                lcd = ""
                                                lcdState = 0
                                                tn = -1
                                                connection_list[lcdSock].send('D')
                                            else:
                                                connection_list[lcdSock].send('Password is not correct!!')
                                                sleep(1)
                                                lcd = ""
                                                connection_list[lcdSock].send('7')
                                        elif c == cl[-1]:
                                            connection_list[lcdSock].send('There is no number like that!')
                                            sleep(1)
                                            lcd = ""
                                            lcdState = 0
                                            tn = -1
                                            connection_list[lcdSock].send('D')
                            elif data.find('7') != -1:
                                if len(lcd) == 0:
                                    lcd = ""
                                    connection_list[lcdSock].send('7')
                                else:
                                    lcd = lcd[:-1]
                                    connection_list[lcdSock].send(lcd)
                            else:
                                if len(lcd) == 4:
                                    connection_list[lcdSock].send('No Longer than 4 Letters')
                                    sleep(1)
                                    connection_list[lcdSock].send(lcd)
                                else:
                                    lcd += data
                                    connection_list[lcdSock].send(lcd)
                               
                    # LCD
                    #elif ds == 7:
                    # RFID
                    elif ds == 8:
                        print "RFID"
                    # Ultra Wave
                    elif ds == 9:
                        print "Ultra Wave"
                    # 초음파센서
                    #if data.find('U') != -1:
                    # Enroll
                    #if data.find('1') != -1:
                    # Open
                    #elif data.find('2') != -1:
                    # Closed
                    #elif data.find('C') != -1:
                        

                    # 접속한 Client에게 서버가 메시지를 전송한다 - - - - - - - - - - - - - My Part
                    sock.send("Hi Client?")
                    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - My Part


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
