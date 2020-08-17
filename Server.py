import socket 
import sys
import psutil
import threading
import _thread 
import time

# CPU Info
def cpustream(ThreadName):
	print("="*5, " CPU Info ", "="*5)
	while True:
		# CPU Cores
		sys.stdout.write(f"\rPhysical cores:" + str(psutil.cpu_count(logical=False)))
		sys.stdout.write(f"\rTotal cores:" + str(psutil.cpu_count(logical=True)))

		# CPU Clockspeed
		cpufreq = psutil.cpu_freq()
		sys.stdout.write(f"\rMax Frequency:  {cpufreq.max:.2f}Mhz")

		# CPU Utilization
		sys.stdout.write(f"\rCPU Usage per Core: ")
		for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):

			sys.stdout.write(f"\rCore: {i} === Memory Usage: {percentage}% ===")
			sys.stdout.flush()

def cpustreamvalue():
	physical_core = psutil.cpu_count(logical=False)
	total_core = psutil.cpu_count(logical=True)
	return(physical_core, total_core)

def diskinformation():
	print("="*5, " Disk Info ", "="*5)
	print("Partitions and Usage: \n")
	partitions = psutil.disk_partitions()
	for partition in partitions:
		print(f"=== Device: {partition.device} ===")
		print(f" Mountpoint: {partition.mountpoint}")
		print(f" File system type: {partition.fstype}")
		try:
			partition_usage = psutil.disk_usage(partition.mountpoint)
		except PermissionError:
			print("Error, access denied.")
			return(0)

# Manage new threads
class Threadsystem(threading.Thread):
	def __init__(self, Clientaddr, Clientsocket):
		threading.Thread.__init__(self)
		self.csocket = Clientsocket
		print("New client connected: ", Clientaddr)
	# Execute thread
	def run(self):
		# Disk Information()
		print("Connection from: ", self.csocket)
		self.csocket.send(bytes("Server informations here: ", 'UTF-8'))
		commandstatement = ""
		while True:
			data = self.csocket.recv(2048)
			commandstatement = data.decode()
			if(commandstatement=="shutdown"): # Stop the thread if the client disconnects to prevent memory yeeting
				break
			elif(commandstatement=="cpustate"): # Check the order and return what the client requests
				self.csocket.send(bytes(str(cpustreamvalue()), 'UTF-8'))
			elif(commandstatement=="diskinfo"): # Disk info
				self.csocket.send(bytes(str(diskinformation()), 'UTF-8'))
			print("From client: ", commandstatement)
			self.csocket.send(bytes(commandstatement, 'UTF-8'))
		print ("Client at ", self.csocket, "disconnected...")

# Port and Protocol Argument
def main(argv):
	if (len(sys.argv[1:]) == 2):
		if (str(sys.argv[2]) == "TCP"):
			host = ''
			port = int(sys.argv[1])
			with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
				s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				s.bind((host, port))
				while True:
					s.listen(1)
					clientsock, cliendAddress = s.accept()
					newthread = Threadsystem(cliendAddress, clientsock)
					# Start a new thread if neccesary
					newthread.start()
		#elif (str(sys.argv[2] == "UDP")):
		#	host = '127.0.0.1'
		#	port = int(sys.argv[1])
		#	with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
		#		s.bind((host, port))
		#		while True:
		#			data, addr = s.recvfrom(1024)
		#			print("Received message: %s" % data)
	else:
		print("Failed to start the server.")

if __name__ == "__main__":
	main(sys.argv[1:])