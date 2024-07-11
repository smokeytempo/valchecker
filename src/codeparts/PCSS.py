import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
import ctypes
import requests
import os
from colorama import Fore, Back, Style, init

init(autoreset=True)

class ProxyChecker:
    def __init__(self):
        self.loaded_proxies = 0
        self.valid_proxies = 0
        self.dead_proxies = 0
        self.good_proxies = 0
        self.moderate_proxies = 0
        self.slow_proxies = 0
        self.THREADS_NUM = 0
        self.valid_proxy_list = []
        self.CHECK_URL = "http://api.ipify.org/"

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
    {Fore.CYAN}│{Style.RESET_ALL} Threads        {Fore.WHITE}>>: {Fore.CYAN}[{Fore.GREEN}{self.THREADS_NUM}{Fore.CYAN}]{' ' * (41 - len(str(self.THREADS_NUM)) - 21)}{Fore.CYAN}│
    {Fore.CYAN}└──────────────────────────────────────────┘{Style.RESET_ALL}'''
        print(gui)

    def get_num_threads(self):
        default_num_threads = 1
        prompt = f'> Enter Number of Threads (Leave Empty For Default: {default_num_threads}): '
        num_threads = input(prompt).strip()

        if not num_threads:
            num_threads = default_num_threads

        try:
            num_threads = int(num_threads)
            if num_threads > 50:
                print(Fore.YELLOW + 'Number of threads set to 50' + Style.RESET_ALL)
                num_threads = 50
        except ValueError:
            print(Fore.LIGHTRED_EX + 'Invalid number of threads, please enter an integer' + Style.RESET_ALL)
            return self.get_num_threads()

        print(Fore.YELLOW + 'Number of threads set to ' + str(num_threads) + Style.RESET_ALL)
        return num_threads

    def main(self, proxies: list) -> list:
        self.CMD_CLEAR_TERM = "cls" if os.name == 'nt' else 'clear'
        self.TIMEOUT = (3.05, 10)
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

    async def check_proxies(self) -> list:
        with ThreadPoolExecutor(max_workers=self.THREADS_NUM) as executor:
            loop = asyncio.get_event_loop()
            tasks = []
            for proxy in self.proxies:
                tasks.append(loop.run_in_executor(executor, self.check_proxy, proxy))
            await asyncio.gather(*tasks)

        self.update_gui()
        return self.valid_proxy_list

    def check_proxy(self, proxy):
        try:
            session = requests.Session()
            session.trust_env = False
            session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            session.max_redirects = 300

            start_time = time.time()
            response = session.get(self.CHECK_URL, proxies=proxy, timeout=self.TIMEOUT, allow_redirects=True)
            end_time = time.time()

            response_time = (end_time - start_time) * 1000  

            if response.status_code == 200:
                self.valid_proxies += 1
                self.valid_proxy_list.append(proxy['http'].split('//')[1])
                if response_time <= 100:
                    self.good_proxies += 1
                elif response_time <= 500:
                    self.moderate_proxies += 1
                else:
                    self.slow_proxies += 1
            else:
                self.dead_proxies += 1

        except Exception:
            self.dead_proxies += 1

        self.checked += 1
        if self.checked % 4 == 0:  
            self.update_gui()

        ctypes.windll.kernel32.SetConsoleTitleW(f"Proxy Checker | {self.checked}/{len(self.proxies)} | Threads: {self.THREADS_NUM}")

