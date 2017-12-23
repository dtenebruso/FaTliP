## THINGS to do::::! -- must get sleep
## add a subnet validator == valid_ip method
## check performance of ipaddress module vs socket module for host scanning a network
## naming conventions???? clean up code????
## in time clean up by adding more functionality to existing functions, using real exception handling

import socket
import sys
import subprocess
import platform
import ipaddress
from ftplib import FTP


def main():
	if platform.system() == 'Windows':
		subprocess.call('cls', shell=True)
	elif platform.system() == 'Linux':
		subprocess.call('clear', shell=True)
	else:
		pass

	# get ip range from user ex.(192.168.1.1/24)
	usersTarget = input("What is the ip range you want to scan?\n(Example: 192.168.1.1/24)\n\n:/> ")
	ipAddress = usersTarget.split('/')

	if len(ipAddress) > 2:
		print("\nToo much info; What the hell did you type?\ntry something like 192.168.1.1/24 || a.k.a [IP address][backslash][subnet mask]")
	elif len(ipAddress) < 2:
		print("\nNot enough info; What the hell did you type?\ntry something like 192.168.1.1/24 || a.k.a [IP address][backslash][subnet mask]")
	else:
		if valid_ip(ipAddress[0]) == True:
			print("\nSeems to be a valid IP... let's have crack at it, eh?!\n\n")
			print("-"*120)
			print("  Please hold onto your panties because we are doing a scannies... shutup i was drunk while coding this,**buuerrerrrp*")
			print("-"*120)

			networkScan('/'.join(ipAddress))
		else:
			sys.exit()


def valid_ip(testADDR):
    try:
        socket.inet_aton(testADDR)
        return True
    except:
   		print('\n{} is not a valid IP address.\n\n*\\.*\\.*\\.*\\.Exiting./*./*./*./*'.format(testADDR))
   		return False

def networkScan(ipRange):
	targetNet = ipaddress.ip_network(ipRange)
	for node in targetNet.hosts():
		hostScan(str(node))


def hostScan(host):
	try:	
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# if connection returned value confirms port is open --> store IP address somewhere for later use
		# else continue to next node
		portState = sock.connect_ex((host, 21))
		print("Scanning {}.format(host)...")
		sock.close()

	except KeyboardInterrupt:
    	print "You pressed Ctrl+C"
    	sys.exit()

	except socket.gaierror:
    	print 'Hostname could not be resolved. Exiting'
    	sys.exit()

	except socket.error:
    	print "Couldn't connect to server"
    	sys.exit()


if __name__ == "__main__":
	main()