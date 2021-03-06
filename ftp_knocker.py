## THINGS to do::::! -- must get sleep
## add a subnet validator == valid_ip method ... test for built-in function with pre-existing solution
## check performance of ipaddress module vs socket module for host scanning a network
## naming conventions???? clean up code????
## in time clean up by adding more functionality to existing functions, using real exception handling
## set scan timeout 
## multi thread the scanning process.... takes way too long
## flush Mongo DB before adding entries to avoid adding to old collections

import sys
import nmap
import socket
import platform
from multiprocessing.dummy import Pool as ThreadPool
#import threading
import ipaddress
import subprocess
import menu
#from ftplib import FTP
from targetDB import Database
from models.storageCom import DataManage

__author__ = 'pr0c'

# set userplatform to global variable to avoid repetitive checking of OS
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
	# split the input to checck and make sure the user avoid wasting time and making sure input follows "###.###.###.##/##"
	if len(ipAddress) > 2:
		print("\nToo much info; What the hell did you type?"+
			"\nTry something like 192.168.1.0/24 || a.k.a [IP address][backslash][subnet mask]")

	elif len(ipAddress) < 2:
		print("\nNot enough info; What the hell did you type?"+
			"\nTry something like 192.168.1.0/24 || a.k.a [IP address][backslash][subnet mask]")

	else:
		if valid_ip(ipAddress[0]) == True:
			print("\nSeems to be a valid IP... let's have a crack at it, eh?!\n\n")
			print("-"*120)
			print("\t\t\tPlease hold onto your panties because we are doing a scannies")
			print("-"*120)
			# after successful validation of the IP range we begin the scan process joining the accepted input into cidr notation
			network_scan('/'.join(ipAddress))
		else:
			sys.exit()

	# after the scan we'll pop a menu up to allow thw user to either hack, print, scan again...etc. More to come
	menu.Menu.run_menu()

def valid_ip(testADDR):
	# validate that the IP address given is truly an IP address
    try:
        socket.inet_aton(testADDR)
        return True
    except:
   		print('\n{} is not a valid IP address.\n\n*\\.*\\.*\\.*\\.Exiting./*./*./*./*'.format(testADDR))
   		return False


def network_scan(ipRange):
	pool = ThreadPool(16)
	targetNet = ipaddress.ip_network(ipRange, strict=False) # strict=False will allow 192.168.1.34; ip_network doesn't like the host bit
	nodes = []
	for node in targetNet.hosts():
		nodes.append(str(node))
	pool.map(host_scan, nodes)
	pool.close()
	pool.join()


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
			nmap_hdwInfo(host)
		else:
			pass

		sock.close()

	except KeyboardInterrupt:
		print("You pressed Ctrl+C")
		sys.exit()

	except socket.gaierror:
		print('{} could not be resolved. Exiting'.format(host))
		sys.exit()

	except socket.error:
		print("Couldn't connect to server")
		sys.exit()
"""
######################################################################
#################KEEPING THIS HERE JUST IN CASE#######################
# perhaps python-nmap would be of greater benefit here?
# will have to check the docs
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
"""
######################################################################
# NMAP 	NMAP 	NMAP 	NMAP 	NMAP 	NMAP 	NMAP 	NMAP 	NMAP #
######################################################################

def nmap_hdwInfo(ip):
	scanner = nmap.PortScanner()
	scanResults = scanner.scan(arguments='-sS -p 21', hosts=ip)
	macAddr = scanResults['scan'][ip]['addresses']['mac']
	hostname = scanResults['scan'][ip]['hostnames'][0]['name']
	pushToDB = DataManage(ip, macAddr, hostname)
	pushToDB.postTargets()

######################################################################

if __name__ == "__main__":

	Database.initialize()

	main()