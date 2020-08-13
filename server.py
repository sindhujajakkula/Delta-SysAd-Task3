import socket
import threading
from datetime import date, timedelta
PORT = 5000

IP = socket.gethostbyname(socket.gethostname()) 
ADDRESS = (IP, PORT)
FORMAT = 'utf-8'
 
clients={}
save=[]
army=[]
navy=[]
airforce=[]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
server.bind(ADDRESS) 

def startChat(): 
	
    print("server is working on " + IP) 
    server.listen() 
	
    while True:
        conn, addr = server.accept()
        conn.send("NAME".encode(FORMAT))
        name = conn.recv(1024).decode(FORMAT)
        clients[name]=conn
        print(clients)
        print(f"Name is :{name}")
        broadcastMessage(name, f"{name} has joined the chat!".encode(FORMAT))

        conn.send('Connection successful!'.encode(FORMAT))
        #sends messages which were sent when client was offline
        for i in range(1,51):
            army.append("Army"+str(i))

        
        for i in range(1,51):
            navy.append("Navy"+str(i))

        
        for i in range(1,51):
            airforce.append("Air Force"+str(i))

        for i in range(len(save)):
                  
            if save[i][0] == name:
                for j in range(i):

                    if name == "Chief":
                        conn.send(save[i-j-1][1].encode(FORMAT))

                    elif name == "Army General":
                        army_general_contact = ["Chief"]
                        for s in range(1,51):
                            army_general_contact.append("Army"+str(s))
                            
                        if save[i-j-1][0] in army_general_contact:
                            conn.send(save[i-j-1][1].encode(FORMAT))

                            
                    elif name == "Navy General":
                        navy_general_contact = ["Chief"]
                        for s in range(1,51):
                            navy_general_contact.append("Navy"+str(s))
                            
                        if save[i-j-1][0] in navy_general_contact:
                            conn.send(save[i-j-1][1].encode(FORMAT))

                    elif name == "Air Force General":
                        airforce_general_contact = ["Chief"]
                        for s in range(1,51):
                            airforce_general_contact.append("Air Force"+str(s))
                            
                        if save[i-j-1][0] in airforce_general_contact:
                            conn.send(save[i-j-1][1].encode(FORMAT))

                    elif name in army:
                        army_general_contact.append("Army General")
                        if save[i-j-1][0] in army_general_contact and save[i-j-1][0]!= "Chief":
                            conn.send(save[i-j-1][1].encode(FORMAT))
                            
                    elif name in navy:
                        navy_general_contact.append("Navy General")
                        if save[i-j-1][0] in navy_general_contact and save[i-j-1][0]!= "Chief":
                            conn.send(save[i-j-1][1].encode(FORMAT))

                    elif name in airforce:
                        airforce_general_contact.append("Air Force General")
                        if save[i-j-1][0] in airforce_general_contact and save[i-j-1][0]!= "Chief":
                            conn.send(save[i-j-1][1].encode(FORMAT))
                                                
                break
            elif i == (len(save)-1):
                for j in range(len(save)):
                    if name == "Chief":
                        conn.send(save[len(save)-j-1][1].encode(FORMAT))

                    elif name == "Army General":
                        army_general_contact = ["Chief"]
                        for s in range(1,51):
                            army_general_contact.append("Army"+str(s))
                            
                        if save[len(save)-j-1][0] in army_general_contact:
                            conn.send(save[len(save)-j-1][1].encode(FORMAT))

                            
                    elif name == "Navy General":
                        navy_general_contact = ["Chief"]
                        for s in range(1,51):
                            navy_general_contact.append("Navy"+str(s))
                            
                        if save[len(save)-j-1][0] in navy_general_contact:
                            conn.send(save[len(save)-j-1][1].encode(FORMAT))

                    elif name == "Air Force General":
                        airforce_general_contact = ["Chief"]
                        for s in range(1,51):
                            airforce_general_contact.append("Air Force"+str(s))
                            
                        if save[len(save)-j-1][0] in airforce_general_contact:
                            conn.send(save[len(save)-j-1][1].encode(FORMAT))

                    elif name in army:
                        armygroup_general_contact = ["Army General"]
                        for s in range(1,51):
                            armygroup_general_contact.append("Army"+str(s))
                        if save[len(save)-j-1][0] in armygroup_general_contact:
                            conn.send(save[len(save)-j-1][1].encode(FORMAT))
                            
                    elif name in navy:
                        navygroup_general_contact = ["Navy General"]
                        for s in range(1,51):
                            navygroup_general_contact.append("Navy"+str(s))
                        if save[len(save)-j-1][0] in navygroup_general_contact:
                            conn.send(save[len(save)-j-1][1].encode(FORMAT))

                    elif name in airforce:
                        airforcegroup_general_contact = ["Air Force General"]
                        for s in range(1,51):
                            airforcegroup_general_contact.append("Air Force"+str(s))
                        if save[len(save)-j-1][0] in airforcegroup_general_contact:
                            conn.send(save[len(save)-j-1][1].encode(FORMAT))




        thread = threading.Thread(target = handle, args = (name, conn, addr))
        thread.start()

        print(f"active connections {threading.activeCount()-1}")


def handle(name, conn, addr): 
	
    print(f"new connection {addr}") 
    connected = True
	
    while connected:
        message = conn.recv(1024)
        print(message)
        #when client sends message "Download", messages from past 7 days is sent to client
        if message.decode(FORMAT) == f"{name}: Download":
            present_date=date.today().strftime("%d/%m/%Y")
            from_date=(date.today() - timedelta(8)).strftime("%d/%m/%Y")
            print(from_date)
            req_index=0
            conn.send(f"Download Chat History {name} {(date.today() - timedelta(7)).strftime('%d/%m/%Y')} to {date.today().strftime('%d/%m/%Y')}".encode(FORMAT))
            for i in range(len(save)):
                if save[i][2] == from_date:
                    req_index = i
                    break
            #Incase no messages were sent on last last 7th day, messages of previous 6 days are sent
            if req_index ==0:
                req_index=len(save)
                for i in range(req_index):
                    if name == "Chief": 
                        conn.send(save[req_index-i-1][1].encode(FORMAT))
                    
                    elif name == "Army General":
                        army_general_contact = ["Chief",name]
                        for s in range(1,51):
                            army_general_contact.append("Army"+str(s))
                            
                        if save[req_index-i-1][0] in army_general_contact:
                            conn.send(save[req_index-i-1][1].encode(FORMAT))
                            
                    elif name == "Navy General":
                        navy_general_contact = ["Chief",name]
                        for s in range(1,51):
                            navy_general_contact.append("Navy"+str(s))
                            
                        if save[req_index-i-1][0] in navy_general_contact:
                            conn.send(save[req_index-i-1][1].encode(FORMAT))

                    elif name == "Air Force General":
                        airforce_general_contact = ["Chief",name]
                        for s in range(1,51):
                            airforce_general_contact.append("Air Force"+str(s))
                            
                        if save[req_index-i-1][0] in airforce_general_contact:
                            conn.send(save[req_index-i-1][1].encode(FORMAT))

                    elif name in army:
                        army.append("Army General")
                        if save[req_index-i-1][0] in army:
                            conn.send(save[req_index-i-1][1].encode(FORMAT))
                            
                    elif name in navy:
                        navy.append("Navy General")
                        if save[req_index-i-1][0] in navy:
                            conn.send(save[req_index-i-1][1].encode(FORMAT))

                    elif name in airforce:
                        airforce.append("Air Force General")
                        if save[req_index-i-1][0] in airforce:
                            conn.send(save[req_index-i-1][1].encode(FORMAT))

                
            #messaages of past 7 days are sent
            for i in range(req_index):
                
                if name == "Chief": 
                    conn.send(save[req_index-i-1][1].encode(FORMAT))
                        

                elif name == "Army General":
                    army_general_contact = ["Chief",name]
                    for s in range(1,51):
                        army_general_contact.append("Army"+str(s))
                            
                    if save[req_index-i-1][0] in army_general_contact:
                        conn.send(save[req_index-i-1][1].encode(FORMAT))

                            
                elif name == "Navy General":
                    navy_general_contact = ["Chief",name]
                    for s in range(1,51):
                        navy_general_contact.append("Navy"+str(s))
                            
                    if save[req_index-i-1][0] in navy_general_contact:
                        conn.send(save[req_index-i-1][1].encode(FORMAT))

                elif name == "Air Force General":
                    airforce_general_contact = ["Chief",name]
                    for s in range(1,51):
                        airforce_general_contact.append("Air Force"+str(s))
                            
                    if save[req_index-i-1][0] in airforce_general_contact:
                        conn.send(save[req_index-i-1][1].encode(FORMAT))

                elif name in army:
                    army.append("Army General")
                    if save[req_index-i-1][0] in army:
                        conn.send(save[req_index-i-1][1].encode(FORMAT))
                            
                elif name in navy:
                    navy.append("Navy General")
                    if save[req_index-i-1][0] in navy:
                        conn.send(save[req_index-i-1][1].encode(FORMAT))

                elif name in airforce:
                    airforce.append("Air Force General")
                    if save[req_index-i-1][0] in airforce:
                        conn.send(save[req_index-i-1][1].encode(FORMAT))
            conn.send(f"Reached chat history end : {name} {(date.today() - timedelta(7)).strftime('%d/%m/%Y')} to {date.today().strftime('%d/%m/%Y')}".encode(FORMAT))
        else:        
            s_message= message.decode(FORMAT)
            save.insert(0, [s_message[0:s_message.index(":")], s_message, date.today().strftime("%d/%m/%Y")])
            print(save)
            broadcastMessage(name, message)
    conn.close() 

def broadcastMessage(name, message):
#message is sent to all elgible people
#eligible clients list contains user names eligible to receive messages from name

    army_eligible_clients=["Chief","Army General"]
    for i in range(1,51):
        army_eligible_clients.append("Army"+str(i))
        
    navy_eligible_clients=["Chief","Navy General"]
    for i in range(1,51):
        navy_eligible_clients.append("Navy"+str(i))
        
    airforce_eligible_clients=["Chief","Air Force General"]
    for i in range(1,51):
        airforce_eligible_clients.append("Air Force"+str(i))
        
    
    if name == "Chief":
        eligible_clients = [name, "Army General", "Navy General", "AirForce General"]
        
        for i in clients:
            for j in eligible_clients:
                if i==j:
                    clients[i].send(message)
                    eligible_clients.remove(i)
                        
    elif name == "Army General":
        eligible_clients=[name, "Chief"]
        for i in range(1,51):
            eligible_clients.append("Army"+str(i))

        for i in clients:
            for j in eligible_clients:
                if i==j:
                    clients[i].send(message)
                    eligible_clients.remove(i)
                        
    elif name == "Navy General":
        eligible_clients=[name, "Chief"]
        for i in range(1,51):
            eligible_clients.append("Navy"+str(i))

        for i in clients:
            for j in eligible_clients:
                if i==j:
                    clients[i].send(message)
                    eligible_clients.remove(i)
                        
    elif name == "AirForce General":
        eligible_clients=[name, "Chief"]
        for i in range(1,51):
            eligible_clients.append("AirForce"+str(i))

        for i in clients:
            for j in eligible_clients:
                if i==j:
                    clients[i].send(message)
                    eligible_clients.remove(i)
                    
    elif name in army_eligible_clients:
        for i in clients:
            for j in army_eligible_clients:
                if i==j:
                    clients[i].send(message)
                    army_eligible_clients.remove(i)

    elif name in navy_eligible_clients:
        for i in clients:
            for j in navy_eligible_clients:
                if i==j:
                    clients[i].send(message)
                    navy_eligible_clients.remove(i)

    elif name in airforce_eligible_clients:
        for i in clients:
            for j in airforce_eligible_clients:
                if i==j:
                    clients[i].send(message)
                    airforce_eligible_clients.remove(i)
    
 
startChat() 
