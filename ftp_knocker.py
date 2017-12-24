## THINGS to do::::! -- must get sleep
## add a subnet validator == valid_ip method
## check performance of ipaddress module vs socket module for host scanning a network
## naming conventions???? clean up code????
## in time clean up by adding more functionality to existing functions, using real exception handling
## scanning is super slow.. need to make it faster, so much faster

import socket
import threading
import sys
import subprocess
import platform
import ipaddress
from targetDB import Database
from models.targetList import Post
from ftplib import FTP

__author__ = 'pr0c'

usersPlatform = platform.system()

def main():
	global usersPlatform

	if usersPlatform == 'Windows':
		subprocess.call('cls', shell=True)
	elif usersPlatform == 'Linux':
		subprocess.call('clear', shell=True)
	else:
		pass

	# get ip range from user ex.(192.168.1.1/24)
	usersTarget = input("What is the ip range you want to scan?\n(Example: 192.168.1.1/24)\n\n:/> ")
	ipAddress = usersTarget.split('/')

	if len(ipAddress) > 2:
		print("\nToo much info; What the hell did you type?\ntry something like 192.168.1.0/24 || a.k.a [IP address][backslash][subnet mask]")
	elif len(ipAddress) < 2:
		print("\nNot enough info; What the hell did you type?\ntry something like 192.168.1.0/24 || a.k.a [IP address][backslash][subnet mask]")
	else:
		if valid_ip(ipAddress[0]) == True:
			print("\nSeems to be a valid IP... let's have a crack at it, eh?!\n\n")
			print("-"*120)
			print("  Please hold onto your panties because we are doing a scannies... shhhhhhh *buuerrerrrp*")
			print("-"*120)

			network_scan('/'.join(ipAddress))
		else:
			sys.exit()


def valid_ip(testADDR):
    try:
        socket.inet_aton(testADDR)
        return True
    except:
   		print('\n{} is not a valid IP address.\n\n*\\.*\\.*\\.*\\.Exiting./*./*./*./*'.format(testADDR))
   		return False

def network_scan(ipRange):
	targetNet = ipaddress.ip_network(ipRange, strict=False)
	for node in targetNet.hosts():
		host_scan(str(node))

######################################################################
def get_hdwInfo(ip):
	global usersPlatform
	if usersPlatform == "Linux":
		# ping the target host to get entry in arp table
		probe = subprocess.Popen(['ping', ip, '-c1'], stdout=subprocess.PIPE,
		        stderr=subprocess.PIPE)
 
		out, err = probe.communicate()
 
		# arp list
		probe = subprocess.Popen(['arp', '-n'], stdout=subprocess.PIPE,
		        stderr=subprocess.PIPE)
 
		out, err = probe.communicate()
 
		try:
			arp = [x for x in out.split('\n') if ip in x][0]
		except IndexError:
		    sys.exit(1)     # no arp entry found
		else:
		    # get the mac address from arp list
		    # bug: when the IP does not exists on the local network
		    # this will print out the interface name
		    return ' '.join(arp.split()).split()[2]

	elif usersPlatform == "Windows":
		# ping the target host to get entry in arp table
		probe = subprocess.Popen(['ping', ip, '-n 1'], stdout=subprocess.PIPE,
		        stderr=subprocess.PIPE)
 
		out, err = probe.communicate()
 
		# arp list
		probe = subprocess.Popen(['arp', '-a'], stdout=subprocess.PIPE,
		        stderr=subprocess.PIPE)
 
		out, err = probe.communicate()
 
		try:
			arp = [x for x in out.split('\n') if ip in x][0]
		except IndexError:
		    sys.exit(1)     # no arp entry found
		else:
		    # get the mac address from arp list
		    # bug: when the IP does not exists on the local network
		    # this will print out the interface name
		    return ' '.join(arp.split()).split()[2]
######################################################################

def host_scan(host):
	try:	
		sock = socket.socket(2,1) # socket.AF_INET, socket.SOCK_STREAM
		sock.settimeout(0.5)
		# if connection returned value confirms port is open --> store IP address somewhere for later use
		# else continue to next node
		print('Scanning {}...'.format(host))
		
		portState = sock.connect_ex((host, 21))

		if portState == 0:
			print("\n{} has port 21 open!\n".format(host))
			print("Grabbing MAC address and hostname...")

			get_hdwInfo(host)

		sock.close()

	except KeyboardInterrupt:
		print("You pressed Ctrl+C")
		sys.exit()

	except socket.gaierror:
		print('Hostname could not be resolved. Exiting')
		sys.exit()

	except socket.error:
		print("Couldn't connect to server")
		sys.exit()


if __name__ == "__main__":
	main()