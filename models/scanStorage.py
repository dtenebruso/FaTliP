from targetDB import Database
from models.targetList import Post

class Store(object):
    def __init__(self, ip_addr, mac_addr, hostname):
        self.ip_addr = ip_addr
        self.mac_addr = mac_addr
        self.hostname = hostname

    def new_post(self):
        post = Post(
        			ip_addr=self.ip_addr,
                    mac_addr=mac_addr,
                    hostname=hostname)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self.ip_addr)

    def save_to_mongo(self):
        Database.insert(collection='targetHosts',
                        data=self.json())

    def json(self):
        return {
            'ip_addr': self.ip_addr,
            'mac_addr': self.mac_addr,
            'hostname': self.hostname,
        }

    @classmethod
    def from_mongo(cls, ip_addr):
        discovered_targets = Database.find_one(collection='targetHosts',
                                      query={'ip_addr': ip_addr})
        return cls(ip_addr=blog_data['ip_addr'],
                    mac_addr=blog_data['mac_addr'],
                    hostname=blog_data['hostname'])