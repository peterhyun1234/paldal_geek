# paldal_geek
Smart Locker - System Programming Team Project

## 1. Control Buttons Not Keypad
    make
    sudo insmod button_mod.ko
    sudo mknod -m 777 /dev/button_mod c 241 0
    gcc -o button_app button_app.c -lwiringPi
    ./button_app


## 2. Control LCD
    gcc -o lcd-test lcd-test.c -lwiringPi -lwiringPiDev
    ./lcd-test


## 3. Control Ultra Wave Sensor
    gcc -o ultra ultra.c -lwiringPi
    ./ultra

## 4. Control RFID
    python3 rfid.py
    
## 5. Server
    python3 server.py

![Capture](https://github.com/SiverPineValley/paldal_geek/blob/master/Capture.jpg?raw=true)
