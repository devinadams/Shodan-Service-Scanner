#The MIT License (MIT)

# Copyright (c) 2018 Devin Adams <github.com/devinatoms/>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from bs4 import BeautifulSoup
import requests
import sys
import re
import urllib2
from colorama import init
from colorama import Fore, Back, Style
init()

class Shodan:

    def getServiceDetails(self, url):
        soup = BeautifulSoup(self.request.text, "html.parser")
        openPorts = soup.find("meta", attrs={"name": "twitter:description"})["content"]
        print(Fore.GREEN + (openPorts))
        serviceDetails = iter(soup.findAll("div", attrs={"class": "service-details"}))
        serviceMains = soup.findAll("div", attrs={"class": "service-main"})
        return serviceDetails, serviceMains

    def display_visible_html_using_re(self, text):             
        return(re.sub("(\<.*?\>)", "",text))

    def checkResponse(self, serviceDetails, serviceMains):
        for serviceMain in serviceMains:
            currentService = next(serviceDetails)
            port = str(currentService.find("div", attrs={"class": "port"}).contents[0])
            serviceMains = ''.join(str(x) for x in serviceMains)
          #  print("\n")
            print(Fore.GREEN + ("Port: " + currentService.find("div", attrs={"class": "port"}).contents[0]))
            print(Fore.GREEN + ("Protocol: " + currentService.find("div", attrs={"class": "protocol"}).contents[0]))
            print(Fore.GREEN + ("State: " + currentService.find("div", attrs={"class": "state"}).contents[0]))
            print(Fore.GREEN + ("\nService: " +  self.display_visible_html_using_re(str(serviceMains))))
            print(Fore.GREEN + ("------"))
        print(Fore.GREEN + '[*] Header Done.')
        print(Fore.GREEN + '[*] SSL info response can sometimes be limited.')
        print(Style.RESET_ALL)

    def __init__(self, IP):
       # print("\n")
        print(Style.RESET_ALL)
        self.shodanURL = IP
        self.session = requests.Session()
        self.request = self.session.get('https://www.shodan.io/host/' + self.shodanURL)
        self.request.status_code = ('Shodan Status: ' + str(self.request.status_code))
        try:
            self.serviceDetails, self.serviceMains = self.getServiceDetails(self.request)
            self.checkResponse(self.serviceDetails, self.serviceMains)
        except Exception as e:
            print(e)
            print(Fore.GREEN + "[*] If you get the following error: TypeError: 'NoneType' object has no attribute '__getitem__'")
            print(Fore.GREEN + "[*] This error means that your target is not on Shodan.")
            return
