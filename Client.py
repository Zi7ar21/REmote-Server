import socket
import sys
import time
import psutil
# Command Arguments Format: Host, Port, Protocol

#def updatescreen():
#	loading = "#"
#	loadingdec = " "
#	print("Memory state: \n")
#	for i in range (0, 10):
#		time.sleep(1)
#		sys.stdout.write("\rDoing thing: " + str(i))
#		sys.stdout.write("\r[" + loading + loadingdec + "]")
#		loadingdec = loadingdec[:-1]
#		loading += "#"
#		sys.stdout.flush()

# Dynamic Memory Display
#def memorystream():
#	while True:
#		for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
#			sys.stdout.write(f"\rCore {i}: {percentage}%")
#			sys.stdout.flush()

def main(argv):
	# Find the arguments
	if (len(sys.argv[1:]) == 3):
		if (str(sys.argv[3]) == "TCP"):
			#try: 
			host = str(sys.argv[1])
			port = int(sys.argv[2])
			commandlist = ['help', 'shutdown', 'cpustate', 'command4', 'command5', 'command6'] # Table of commands
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.connect((host, port))
				s.sendall(b'sysinfo')
				while True:
					# s.sendall(b'sysinfo')
					data = s.recv(1024) # Recieve data
					print('Received data: ', repr(data))
					command = input("SERVER>")
					if command in commandlist: # Check the variable exists
						if command == "shutdown":
							s.sendall(bytes(command, 'UTF-8')) 
							print("Disconnected from server...")
							break
						elif command == "help":
							print("Here is the help command:")
							s.sendall(bytes(command, 'UTF-8'))
						else:
							s.sendall(bytes(command, 'UTF-8'))
					else:
						print("Command not found.")
						continue
		#elif(str(sys.argv[3]) == "UDP"):
		#	#try:
		#	host = str(sys.argv[1])
		#	port = int(sys.argv[2])
		#	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		#		s.sendto(b'sysinfo', (host, port))
		#		print("Message sent as: %s" % host)
		#		print("On port: %s" % port)
		#	print("Work in progress...")
	else:
		print("Missing arguments in command.")

if __name__ == "__main__":
	main(sys.argv[1:])