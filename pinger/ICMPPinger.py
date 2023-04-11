from socket import *
import os
import sys
import struct
import time
import select
import binascii  

ICMP_ECHO_REQUEST = 8

def checksum(string): 
	csum = 0
	countTo = (len(string) // 2) * 2
	count = 0
	while count < countTo:
		thisVal = string[count+1] * 256 + string[count] 
		csum = csum + thisVal 
		csum = csum & 0xffffffff  
		count = count + 2
	
	if countTo < len(string):
		csum = csum + string[len(string) - 1]
		csum = csum & 0xffffffff 
	
	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum 
	answer = answer & 0xffff 
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer
	
def receiveOnePing(mySocket, ID, timeout, destAddr):
	timeLeft = timeout
	
	while 1: 
		startedSelect = time.time()
		whatReady = select.select([mySocket], [], [], timeLeft)
		howLongInSelect = (time.time() - startedSelect)
		if whatReady[0] == []: # Timeout
			return "Request timed out."
	
		timeresponses = time.time() 
		recPacket, addr = mySocket.recvfrom(1024)
	       
	    #Fill in start
		icmp_header = recPacket[20:28]	
		icmp_type, code, checksum, id, sequence = struct.unpack("bbHHh", icmp_header)
		(sent_time,) = struct.unpack_from("d", recPacket, offset=28)
		# print(f"ICMP type: {icmp_type}, Code: {code}, Checksum: {checksum}")
		# print(f"ID: {id}, Sequence: {sequence}, Sent time: {sent_time}" )
		(address, _) = addr
		if address == destAddr and id == ID:
			return timeresponses - sent_time 
       	#Fill in end

		timeLeft = timeLeft - howLongInSelect
		if timeLeft <= 0:
			print(f"ICMP type: {icmp_type}, Code: {code}")
			return "Request timed out."
	
def sendOnePing(mySocket, destAddr, ID):
	# Header is type (8), code (8), checksum (16), id (16), sequence (16)
	
	myChecksum = 0
	# Make a dummy header with a 0 checksum
	# struct -- Interpret strings as packed binary data
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	data = struct.pack("d", time.time())
	# Calculate the checksum on the data and the dummy header.
	myChecksum = checksum(header + data)
	
	# Get the right checksum, and put in the header
	if sys.platform == 'darwin':
		# Convert 16-bit integers from host to network  byte order
		myChecksum = htons(myChecksum) & 0xffff		
	else:
		myChecksum = htons(myChecksum)
		
	header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
	packet = header + data
	
	mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
	# Both LISTS and TUPLES consist of a number of objects
	# which can be referenced by their position number within the object.
	
def doOnePing(destAddr, timeout): 
	icmp = getprotobyname("icmp")
	# SOCK_RAW is a powerful socket type. For more details:   
	#    http://sock-raw.org/papers/sock_raw

	mySocket = socket(AF_INET, SOCK_RAW, icmp)
	myID = os.getpid() & 0xFFFF  # Return the current process i
	sendOnePing(mySocket, destAddr, myID)
	rtt = receiveOnePing(mySocket, myID, timeout, destAddr)
	
	mySocket.close()
	return rtt
	
def ping(host, timeout=1):
	# timeout=1 means: If one second goes by without a reply from the server,
	# the client assumes that either the client's ping or the server's pong is lost
	dest = gethostbyname(host)
	print("Pinging " + dest + " using Python:")
	print("")
	round_trip_times = []
	# Send ping requests to a server separated by approximately one second
	try:
		while 1 :
			rtt = doOnePing(dest, timeout)
			round_trip_times.append(rtt)
			if not rtt or rtt == "Request timed out.":
				print(rtt)
			else:
				print(f"{round(float(rtt)*1000.0, 1)} ms")
			time.sleep(1) # one second
	except KeyboardInterrupt:
		attempts = len(round_trip_times)
		lost = round_trip_times.count("Request timed out.")
		responses = attempts - lost
		packet_loss = float(lost)/float(attempts)
		valid_values = [time for time in round_trip_times if time != "Request timed out."]
		print();
		print(f"{attempts} ping attempts, {responses} responses, {round(packet_loss*100, 2)}% packet loss")
		if (len(valid_values) > 0):
			print(f"min rtt: {round(min(valid_values)*1000.0,1)} ms, max rtt: {round(max(valid_values)*1000.0,1)} ms, avg rtt: {round(sum(valid_values)*1000.0/len(valid_values), 1)} ms")
		return
	
ping("uschicago-hostzealot.metercdn.net")
#ping("uk-hostzealot.metercdn.net")
#ping("hk-hostzealot.metercdn.net")
#ping("br-euforta.metercdn.com")
