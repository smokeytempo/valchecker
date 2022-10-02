#!/usr/bin/python3
import urllib3
import ctypes
import requests
import os
from colorama import Fore

class ProxyChecker:
    def main(self,proxies:list) -> list:
        ctypes.windll.kernel32.SetConsoleTitleW("PCSS by skyx#7043")

        self.URL = "http://auth.riotgames.com/api/v1/authorization/"
        self.CMD_CLEAR_TERM = "cls"
        self.TIMEOUT = (3.05,27)
        self.checked=0
        self.goods=[]
        self.bad=0

        cmd = 'mode 53,25'
        os.system(cmd)
        print(Fore.LIGHTMAGENTA_EX + '=========================SkyX========================')
        for proxy in proxies:
            ctypes.windll.kernel32.SetConsoleTitleW(f"PCSS by skyx#7043 | {self.checked}/{len(proxies)}")
            try:
                if self.check_proxy(proxy):
                    print(Fore.LIGHTRED_EX + 'BAD PROXY : ' + proxy)
                else:
                    print(Fore.LIGHTGREEN_EX + 'GOOD PROXY : ' + proxy)
                    if proxy not in self.goods:
                        self.goods.append(proxy.replace('\n',''))
                print(Fore.LIGHTMAGENTA_EX + '=========================SkyX========================')
            except KeyboardInterrupt:
                print(Fore.LIGHTGREEN_EX + '\nExit.')
                exit()
            self.checked+=1
        print(Fore.LIGHTGREEN_EX + 'Total ' + str(len(self.goods)) + ' GOOD Proxies Found')
        print(Fore.LIGHTRED_EX + 'And ' + str(len(proxies) - len(self.goods)) + ' are bad')
        print(Fore.LIGHTYELLOW_EX + 'Made with <3')
        return self.goods

    def check_proxy(self,proxy):
        try:
            session = requests.Session()
            session.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
            session.max_redirects = 300
            proxy = proxy.split('\n',1)[0]
            print(Fore.LIGHTYELLOW_EX + 'Checking...  ' + proxy)
            session.get(self.URL, proxies={'http':'http://' + proxy}, timeout=self.TIMEOUT,allow_redirects=True)
        except requests.exceptions.ConnectTimeout as e:
            print(Fore.LIGHTRED_EX + 'ERROR,Timeout!')
            return e
        except requests.exceptions.HTTPError as e:
            print(Fore.LIGHTRED_EX + 'HTTP ERROR!')
            return e
        except requests.exceptions.Timeout as e:
            print(Fore.LIGHTRED_EX + 'ERROR! Connection Timeout!')
            return e
        except urllib3.exceptions.ProxySchemeUnknown as e:
            print(Fore.LIGHTRED_EX + 'ERROR! Unknown Proxy Scheme!')
            return e
        except requests.exceptions.TooManyRedirects as e:
            print(Fore.LIGHTRED_EX + 'ERROR! Too Many Redirects!')
            return e
        except Exception as e:
            print(Fore.LIGHTRED_EX + 'UNKNOWN ERROR!')
            return e