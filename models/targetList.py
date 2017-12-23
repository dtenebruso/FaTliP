from targetDB import Database

__author__ = 'pr0c'

class Post(object):

    def __init__(self, ip_addr, mac_addr, hostname):
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr
        self.hostname = hostname


        # post = Post(ip_addr="123", title="a title", hostname = "some hostname", mac_addr = "FF:FF:FF:FF:FF:FF")


    def save_to_mongo(self):
        Database.insert(collection='targetHosts',
                        data=self.json())

    def json(self):
        return {
            'ip_addr': self.ip_addr,
            'mac_addr': self.mac_addr,
            'hostname': self.hostname,}

    @classmethod
    def from_mongo(cls, ip_addr):
        #Post.from_mongo('192.168.1.1')
        scan_data = Database.find_one(collection='targetHosts', query={'ip_addr': ip_addr})
        return cls(ip_addr=scan_data['ip_addr'],
                   mac_addr=scan_data['mac_addr'],
                   hostname=scan_data['hostname'])

    @staticmethod
    def from_blog(ip_addr):
        return [post for post in Database.find(collection='targetHosts', query={'ip_addr': ip_addr})]