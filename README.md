# paldal_geek
Smart Locker - System Programming Team Project

## 1. Control LCD
    gcc -o lcd-test lcd-test.c -lwiringPi -lwiringPiDev
    ./lcd-test


## 2. Control Buttons Not Keypad
    make
    sudo insmod button_mod.ko
    sudo mknod -m 777 /dev/button_mod c 241 0
    gcc -o button_app button_app.c -lwiringPi
    ./button_app

## 3. Communication between rasp

