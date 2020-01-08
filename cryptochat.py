import socket
import os

def clear():
	os.system('cls')

def encryptdata(data):
	return data[::-1]

def decryptdata(data):
	return data[::-1]

print("   _____                  _         _____ _           _   ")
print("  / ____|                | |       / ____| |         | |  ")
print(" | |     _ __ _   _ _ __ | |_ ___ | |    | |__   __ _| |_ ")
print(" | |    | '__| | | | '_ \| __/ _ \| |    | '_ \ / _` | __|")
print(" | |____| |  | |_| | |_) | || (_) | |____| | | | (_| | |_ ")
print("  \_____|_|   \__, | .__/ \__\___/ \_____|_| |_|\__,_|\__|")
print("               __/ | |                                    ")
print("              |___/|_|                                    ")

print("\n[1] Start a server.\n[2] Connect to a server.\n[3] Exit.\n")
ch = int(input("==> "))
if ch==1:
	clear()
	lhost=input("[+] Local IP address: ")
	lport=int(input("[+] Local port: "))
	try:
		s=socket.socket()
		s.bind((lhost,lport))
	except OSError:
		print("[-] Server creation failed at",lhost)
		exit()
	passcode=input("[+] Set Passcode: ")
	clear()
	print("[+] Listening for any connection on",lport)
	s.listen(1)
	c,addr=s.accept()
	print("[+] Connection from",addr[0])
	data = decryptdata(c.recv(1024)).decode('utf-8')
	if data!=passcode:
		print("[-] Incorrect Passcode was entered !!")
		c.send(encryptdata("Passcode Incorrect").encode('utf-8'))
		c.close()
		exit()
	else:
		key=len(passcode)
		print("[+] Authentication Successfull")
		c.send(encryptdata("Passcode Correct").encode('utf-8'))
	while True:
		data = decryptdata(c.recv(1024)).decode('utf-8')
		if not data:
			break
		print("[+] Received From",addr[0],"\n|--->",data)
		data = input("=>")
		print("[+] Sending:",data)
		c.send(encryptdata(data).encode('utf-8'))
	c.close()

elif ch==2:
	clear()
	rhost=input("[+] Remote IP address: ")
	rport=int(input("[+] Remote port: "))
	s = socket.socket()
	try:
		s.connect((rhost,rport))
	except ConnectionRefusedError:
		print("[-] Server Unavailable on",rhost)
		print("[-] Start the server first.")
		exit()
	msg=input("[+] Passcode: ")
	s.send(encryptdata(msg).encode('utf-8'))
	data=decryptdata(s.recv(1024)).decode('utf-8')
	if data=="Passcode Incorrect":
		print("[-] Incorrect Passcode was entered !!")
		s.close()
		exit()
	elif data=="Passcode Correct":
		print("[+] Authentication Successfull")
		key = len(msg)
	msg=input("=>")
	while msg!='QUIT':
		print("[+] Sending:",msg)
		s.send(encryptdata(msg).encode('utf-8'))
		data=decryptdata(s.recv(1024)).decode('utf-8')
		print("[+] Received from",rhost,"\n|--->",data)
		msg=input("=>")
	s.close()
elif ch==3:
	print("[-] Exiting.")