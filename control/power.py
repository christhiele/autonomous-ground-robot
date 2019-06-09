import RPi.GPIO as gpio
import time
import os

def powercheck():
    try:
        f = open("powerstatus.txt", "r")
    except:
        return True #assume Power Transfer is on if unknown

    fl = f.readlines()
    for idx, value in enumerate(fl):
        # print(idx, value)
        if idx == 1:
            powerstatus = value.rstrip()  # strip to remove /n and other ending spaces in string
            powerstatus = powerstatus.replace("Power Transfer = ","")
            powerstatus = int(powerstatus)
            break

    if powerstatus == 1:
        return True # Power Transfer is On from RPi 3.7V -> External 7.4.V  (Maximized)
    elif powerstatus == 0:
        return False

def poweroff():
    # power saving - turn off idle services
    os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/unbind")  # turn off usb + ethernet
    os.system("sudo /opt/vc/bin/tvservice -o")  # turnoff hdmi
    os.system("sudo rfkill block bluetooth")

    #writing file
    f = open("powerstatus.txt", "w+")
    f.write("# Status of Power Transfer b/t 3.7V RPi & 7.4V External Batteries. Wise to have on during recharging but off during use. Else RPi gets drained quickly. 1 = On, 0 = Off\n")
    f.write("Power Transfer = 0\n")


def poweron():
    #restart idle services
    os.system("echo '1-1' |sudo tee /sys/bus/usb/drivers/usb/bind") #usb + ethernet
    os.system("sudo /opt/vc/bin/tvservice -p") #hdmi
    os.system("sudo rfkill unblock bluetooth") #bluetooth

    #writing file
    f = open("powerstatus.txt", "w+")
    f.write("# Status of Power Transfer from 3.7V RPi & 7.4V External Batteries. Wise to have on during recharging but off during use. Else RPi gets drained quickly. 1 = On, 0 = Off\n")
    f.write("Power Transfer = 1\n")

def main():
    print("Control Power:")
    print("0 - Power Status USB/Ethernet/HDMI/Bluetooth")
    print("1 - Power Off USB/Ethernet/HDMI/Bluetooth")
    print("2 - Power On USB/Ethernet/HDMI/Bluetooth")
    print("x - Exit")
    choice = input()
    if choice == "1":
        poweroff()
    elif choice == "2":
        poweron()
    elif choice == "0":
        result = powercheck()
        # print (result)
        if result is False:
            result2 = "OFF"
        elif result is True:
            result2 = "ON"
        print("Power Transfer from 3.7V RPi -> 7.4V External is %s" % result2)
    elif choice == "x":
        return
    else:
        print("Invalid Input; try again")
        main()

if __name__ == "__main__":
    main()