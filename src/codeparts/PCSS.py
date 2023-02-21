#!/usr/bin/python3
import urllib3
import ctypes
import requests
import os
from colorama import Fore

class ProxyChecker:
    def main(self,proxies:list) -> list:
        ctypes.windll.kernel32.SetConsoleTitleW("Proxy Checker")

        self.URL = "https://api.ipify.org/"
        self.CMD_CLEAR_TERM = "cls"
        self.TIMEOUT = 20
        self.checked=0
        self.goods=[]
        self.bad=0

        cmd = 'mode 53,25'
        os.system(cmd)
        for proxy in proxies:
            ctypes.windll.kernel32.SetConsoleTitleW(f"Proxy Checker | {self.checked}/{len(proxies)}")
            try:
                if self.check_proxy(proxy):
                    print(Fore.LIGHTRED_EX, end='')
                else:
                    print(Fore.LIGHTGREEN_EX, end='')
                    if proxy not in self.goods:
                        self.goods.append(proxy.replace('\n',''))
                print(f'response: {self.code}')
            except KeyboardInterrupt:
                print(Fore.LIGHTGREEN_EX + '\nExit.')
                exit()
            self.checked+=1
        print(Fore.LIGHTGREEN_EX + 'Total ' + str(len(self.goods)) + ' GOOD Proxies Found')
        print(Fore.LIGHTRED_EX + 'And ' + str(len(proxies) - len(self.goods)) + ' are bad')
        return self.goods

    def check_proxy(self,proxy):
        self.code = -1
        try:
            session = requests.Session()
            session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            session.max_redirects = 300
            proxy = proxy.split('\n',1)[0]
            print(Fore.LIGHTYELLOW_EX + 'Checking...  ' + proxy)
            self.r = session.get(self.URL, proxies={'http':'http://' + proxy, 'https':'http://'+proxy}, timeout=self.TIMEOUT,allow_redirects=True)
            self.code = self.r.status_code
        # except requests.exceptions.ConnectTimeout as e:
        #     print(Fore.LIGHTRED_EX + 'ERROR,Timeout!')
        #     return e
        # except requests.exceptions.HTTPError as e:
        #     print(Fore.LIGHTRED_EX + 'HTTP ERROR!')
        #     return e
        # except requests.exceptions.Timeout as e:
        #     print(Fore.LIGHTRED_EX + 'ERROR! Connection Timeout!')
        #     return e
        # except urllib3.exceptions.ProxySchemeUnknown as e:
        #     print(Fore.LIGHTRED_EX + 'ERROR! Unknown Proxy Scheme!')
        #     return e
        # except requests.exceptions.TooManyRedirects as e:
        #     print(Fore.LIGHTRED_EX + 'ERROR! Too Many Redirects!')
        #     return e
        except Exception as e:
            return e