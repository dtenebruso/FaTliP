from targetDB import Database

class DataManage(object):
	def __init__(self, ip_addr, mac_addr, hostname):
		self.ip_addr = ip_addr
		self.mac_addr = mac_addr
		self.hostname = hostname


	def postTargets(self):
		json = {
            'ip_addr': self.ip_addr,
            'mac_addr': self.mac_addr,
            'hostname': self.hostname,}

		Database.insert(collection='targetHosts', data=json)




	#pullData(self):
	#use ip_addr to pull all relevant info from the database to use with hack attacks

	#printData():
	#take everything from databse and place it into json format and output to file



