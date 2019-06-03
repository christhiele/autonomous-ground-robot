import RPi.GPIO as gpio
import time
import os

def poweroff():
    # power saving - turn off idle services
    os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind")  # turn off usb + ethernet
    os.system("sudo /opt/vc/bin/tvservice -o")  # turnoff hdmi
    os.system("sudo rfkill block bluetooth")

def poweron():
    #restart idle services
    os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/bind") #usb + ethernet
    os.system("sudo /opt/vc/bin/tvservice -p") #hdmi
    os.system("sudo rfkill unblock bluetooth") #bluetooth

def main():
    print("Control Power:")
    print("1 - Power Off USB/Ethernet/HDMI/Bluetooth")
    print("2 - Power On USB/Ethernet/HDMI/Bluetooth")
    print("x - Exit")
    choice = input()
    if choice == "1":
        poweroff()
    elif choice == "2":
        poweron()
    elif choice == "x":
        pass
    else:
        print("Invalid Input; try again")
        main()

if __name__ == "__main__":
    main()