# Shodan ip search term scraper


from bs4 import BeautifulSoup
import requests
import sys
import re
import urllib2
from colorama import init
from colorama import Fore, Back, Style
init()
import sho
import re

class Search:

    def display_visible_html_using_re(self, text):             
        return(re.sub("(\<.*?\>)", "",text))

    def grabIPs(self, url):
        soup = BeautifulSoup(self.request.text, "html.parser")
        ips = soup.findAll("div", attrs={"class": "ip"})
        return ips
        
    def getSearchedIPS(self, search):
        self.session = requests.Session()
        URL = 'https://www.shodan.io/search?query=' + str(search)
        print(URL)
        self.request = self.session.get(URL)
        IPS = self.grabIPs(self.request)
        IPS = self.display_visible_html_using_re(str(IPS))
        return IPS
    #requestShodan = sho.Shodan(IP)

    def cleanIPS(self, ips):
        ips = ips.split('\\n,')
        ips = list(map(str.strip,ips))
        lastElement = ''
        results = ips[1:5]
        results = results + ips[8:10]
        for element in results:
            if "\\n" in str(element):
                elementHolder = element.strip("\\n]")
                lastElement = elementHolder
                lastElement = lastElement.split(' ')
        del results[5]
        results = results + lastElement
        return results

    def askSearch(self):
        search = raw_input("Enter the shodan search: ")
        search = search.replace(' ','+')
        return str(search)

    def checkIPS(self, ips):
        print("\n")
        print("\n")
        print("Checkings IPS: " , ips)
        print("\n")
        print("\n")
        for ip in ips:
            print("Start of services for IP: " + ip)
            print("----------------------------------")
            Shodan = sho.Shodan(ip)
            print("\nEnd of services for IP: " + ip)
            print("---------------------------------------")
            print("\n")
            print("\n")
            print("\n")
            print("\n")
            print("\n")
            print("\n")
    def main(self):
        try:
            search = self.askSearch()
            IPS = self.getSearchedIPS(search)
            IPS = self.cleanIPS(IPS)
            self.checkIPS(IPS)
        except Exception as e:
            print(e)
            pass

    def __init__(self):
        self.main()

search = Search()
