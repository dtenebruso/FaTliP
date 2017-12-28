from lxml import etree
import sys
import ftp_knocker
from targetDB import Database
from models.storageCom import DataManage

__author__ = 'pr0c'

class Menu(object):

    def run_menu():
        getItRight = 0 #point system to make sure user uses an option given
        while getItRight == 0:
            menuChoice = input("\n\nHow shall we proceed?\n"+
                "Type (e) to start an exploit on the ftp servers found\n"+
                "Type (p) to print the database to a file in csv format\n"+
                "Type (a) to scan a network again\n"+
                "Type (x) to exit the program\n"+
                ":/>\t")
            if menuChoice.upper() == 'E' or 'EXPLOIT':
                # give the option to bruteforce ftp server username and password
                getItRight+=1
            elif menuChoice.upper() == 'P' or 'PRINT':
                _print_targets()
                getItRight+=1
            elif menuChoice.upper() == 'A' or 'AGAIN':
                ftp_knocker.main()
                getItRight+=1
            elif menuChoice.upper() == 'X' or 'EXIT':
                getItRight+=1
                sys.exit()
            else:
                x = 0

    def _print_targets():
        """
        print xml

        root of tree with each element just an icrement of the next|| childElementId == childElementId++
        childSubElement = IP or MAC or Hostname
        subElementText = IP.ip_addr or MAC.mac_addr or Hostname.hostname

        """
        x = 0
        entries = Database.find()
        #root = etree.Element('targets')
        #roo.append(etree.Element(str(x)))
        for entry in entries:
            print(entry)
            #print("IP: {}, Mac Address: {}, Hostname: {}".format(entry['ip_addr'], entry['mac_addr'], entry['hostname']))

    def _view_blog():
        blog_to_see = input("Enter the ID of the blog you'd like to read: ")
        blog = DataManage.from_mongo(blog_to_see)
        posts = blog.get_posts()
        for post in posts:
            print("Date: {}, Title: {}\n\n{}".format(post['created_date'], post['title'], post['content']))