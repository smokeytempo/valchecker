import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
import ctypes
import requests
import os
from colorama import Fore, Style, init
from requests.exceptions import RequestException
import socket

init(autoreset=True)

class ProxyChecker:
    def __init__(self):
        self.loaded_proxies = 0
        self.valid_proxies = 0
        self.dead_proxies = 0
        self.good_proxies = 0
        self.moderate_proxies = 0
        self.slow_proxies = 0
        self.http_proxies = 0
        self.https_proxies = 0
        self.socks4_proxies = 0
        self.socks5_proxies = 0
        self.THREADS_NUM = 0
        self.valid_proxy_list = []
        self.CHECK_URL = "http://httpbin.org/ip"
        self.TIMEOUT = 5
        self.checked = 0

    def update_gui(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        gui = f'''
    {Fore.CYAN}┌─ Proxy Stats ────────────────────────────┐
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} Loaded proxies {Fore.WHITE}>>: {Fore.CYAN}[{Fore.WHITE}{self.loaded_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.loaded_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} Valid proxies  {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.valid_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.valid_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} Dead proxies   {Fore.WHITE}>>: {Fore.CYAN}[{Fore.YELLOW}{self.dead_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.dead_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}├──────────────────────────────────────────┤
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} Good           {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.good_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.good_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} Moderate       {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.moderate_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.moderate_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} Slow           {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.slow_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.slow_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}├──────────────────────────────────────────┤
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} HTTP           {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.http_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.http_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} HTTPS          {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.https_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.https_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} SOCKS4         {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.socks4_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.socks4_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}│{Style.RESET_ALL}{Fore.WHITE} SOCKS5         {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.socks5_proxies}{Fore.CYAN}]{' ' * (41 - len(str(self.socks5_proxies)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}├──────────────────────────────────────────┤
    {Fore.CYAN}│{Style.RESET_ALL} Threads        {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.THREADS_NUM}{Fore.CYAN}]{' ' * (41 - len(str(self.THREADS_NUM)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}└──────────────────────────────────────────┘{Style.RESET_ALL}'''
        print(gui)

    def get_num_threads(self):
        default_num_threads = 100
        prompt = f'> Enter Number of Threads (Leave Empty For Default: {default_num_threads}): '
        num_threads = input(prompt).strip()

        if not num_threads:
            num_threads = default_num_threads

        try:
            num_threads = int(num_threads)
            if num_threads > 1000:
                print(Fore.YELLOW + 'Number of threads set to 1000' + Style.RESET_ALL)
                num_threads = 1000
        except ValueError:
            print(Fore.LIGHTRED_EX + 'Invalid number of threads, please enter an integer' + Style.RESET_ALL)
            return self.get_num_threads()

        print(Fore.YELLOW + 'Number of threads set to ' + str(num_threads) + Style.RESET_ALL)
        return num_threads

    def main(self, proxies: list) -> list:
        self.CMD_CLEAR_TERM = "cls" if os.name == 'nt' else 'clear'
        self.checked = 0
        self.proxies = proxies
        self.loaded_proxies = len(proxies)

        ctypes.windll.kernel32.SetConsoleTitleW("ValChecker | Proxy Checker")

        self.THREADS_NUM = 0
        while self.THREADS_NUM == 0:
            self.THREADS_NUM = self.get_num_threads()
        print()

        print("Starting checking...")
        time.sleep(1)
        self.update_gui()

        with ThreadPoolExecutor(max_workers=self.THREADS_NUM) as executor:
            executor.map(self.check_proxy, self.proxies)

        self.update_gui()
        return self.valid_proxy_list

    def check_proxy(self, proxy):
        proxy_types = ['socks5', 'socks4', 'https', 'http']
        proxy_address = proxy['http'].split('//')[1]
        
        for proxy_type in proxy_types:
            try:
                proxy_url = f"{proxy_type}://{proxy_address}"
                proxies = {'http': proxy_url, 'https': proxy_url}

                start_time = time.time()
                with requests.Session() as session:
                    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    session.proxies = proxies
                    response = session.get(self.CHECK_URL, timeout=self.TIMEOUT, allow_redirects=True)
                end_time = time.time()

                response_time = (end_time - start_time) * 1000  

                if response.status_code == 200:
                    self.valid_proxies += 1
                    self.valid_proxy_list.append((proxy_address, proxy_type))
                    
                    if proxy_type == 'http':
                        self.http_proxies += 1
                    elif proxy_type == 'https':
                        self.https_proxies += 1
                    elif proxy_type == 'socks4':
                        self.socks4_proxies += 1
                    elif proxy_type == 'socks5':
                        self.socks5_proxies += 1

                    if response_time <= 100:
                        self.good_proxies += 1
                    elif response_time <= 500:
                        self.moderate_proxies += 1
                    else:
                        self.slow_proxies += 1
                    
                    break  
            except (RequestException, socket.error):
                pass
        else:
            self.dead_proxies += 1

        self.checked += 1
        if self.checked % 5 == 0:  
            self.update_gui()

        ctypes.windll.kernel32.SetConsoleTitleW(f"Proxy Checker | {self.checked}/{len(self.proxies)} | Threads: {self.THREADS_NUM}")