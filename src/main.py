import asyncio
import ctypes
import json
import os
import random
import tkinter
from tkinter import filedialog
from InquirerPy import inquirer
from InquirerPy.separator import Separator
import colorama

import requests
from colorama import Fore, Style

import checker
from codeparts import checkers, systems, validsort
from codeparts.systems import system

check = checkers.checkers()
sys = systems.system()
valid = validsort.validsort()


class program():
    def __init__(self) -> None:
        self.count = 0
        self.checked = 0
        self.version = '3.14.2 beta'
        self.riotlimitinarow = 0
        path = os.getcwd()
        self.parentpath = os.path.abspath(os.path.join(path, os.pardir))
        try:
            self.lastver = requests.get(
                'https://api.github.com/repos/lil-jaba/valchecker/releases').json()[0]['tag_name']
        except:
            self.lastver = self.version

    def start(self):
        try:
            print('internet check')
            requests.get('https://github.com')
        except requests.exceptions.ConnectionError:
            print('no internet connection')
            os._exit(0)
        os.system('cls')
        codes = vars(colorama.Fore)
        colors = [codes[color] for color in codes if color not in ['BLACK']]
        colored_name = [random.choice(colors) + char for char in f'ValChecker by liljaba1337']
        print(sys.get_spaces_to_center('ValChecker by liljaba1337')+(''.join(colored_name))+colorama.Fore.RESET)
        print(sys.center(f'v{self.version}'))
        if self.lastver != self.version and 'beta' not in self.version:
            print(sys.center(
                f'\nnext version {self.lastver} is available!'))
            if inquirer.confirm(
                message="{}Would you like to download it now?".format(system.get_spaces_to_center('Would you like to download it now? (Y/n)')), default=True,qmark=''
            ).execute():
                os.system(f'{self.parentpath}/updater.bat')
                os._exit(0)
        if 'beta' in self.version:
            print(sys.center(f'{Fore.YELLOW}You have downloaded the BETA version. It can work unstable and contain some bugs.'))
            print(sys.center(f'Follow https://github.com/LIL-JABA/valchecker/releases/latest to download the latest stable release{Fore.RESET}'))
        menu_choices = [
            Separator(),
            'Start Checker',
            'Edit Settings',
            'Sort Valid',
            'Test Proxy',
            'Info/Help',
            Separator(),
            'Exit'
        ]
        print(sys.center('\nhttps://github.com/LIL-JABA/valchecker\n'))
        res = inquirer.select(
            message="Please select an option:",
            choices=menu_choices,
            default=menu_choices[0],
            pointer='>',
            qmark=''
        ).execute()
        if res == menu_choices[1]:
            self.main()
        elif res == menu_choices[2]:
            sys.edit_settings()
            pr.start()
        elif res == menu_choices[3]:
            valid.customsort()
            input('done. press ENTER to exit')
        elif res == menu_choices[4]:
            sys.checkproxy()
            pr.start()
        elif res == menu_choices[5]:
            os.system('cls')
            print(f'''
    valchecker v{self.version} by liljaba1337

    server: https://discord.gg/r3Y5KhM7kP

  [1] - check valid/invalid/ban and save them to valid.txt in output folder
  [2] - i think u understand
  [3] - sorts all accounts from valid.txt which match your requirements to output\\sorted\\custom.txt
  [4] - test your proxies

  [~] - press ENTER to return
            ''')
            input()
            pr.start()
        elif res == menu_choices[7]:
            os._exit(0)

    def get_accounts(self, filename):
        while True:
            try:
                with open(str(filename), 'r', encoding='UTF-8', errors='replace') as file:
                    lines = file.readlines()
                    ret = []
                    if len(lines) > 100000:
                        if inquirer.confirm(
                            message=f"You have more than 100k accounts ({len(lines)}). Do you want to skip the sorting part? (it removes doubles and bad logpasses but can be long)",
                            default=True,
                            qmark='!',
                            amark='!'
                        ).execute():
                            self.count = len(lines)
                            return lines

                    for logpass in lines:
                        logpass = logpass.strip()
                        # remove doubles
                        if logpass not in ret and ':' in logpass:
                            self.count += 1
                            ctypes.windll.kernel32.SetConsoleTitleW(
                                f'ValChecker {self.version} by liljaba1337 | Loading Accounts ({self.count})')
                            ret.append(logpass)
                    return ret
            except FileNotFoundError:
                print(
                    f"can't find the default file ({filename})\nplease select a new one")
                root = tkinter.Tk()
                file = filedialog.askopenfile(parent=root, mode='rb', title='select file with accounts (login:password)',
                                              filetype=(("txt", "*.txt"), ("All files", "*.txt")))
                root.destroy()
                os.system('cls')
                if file == None:
                    print('you chose nothing')
                    input('press ENTER to choose again')
                    continue
                filename = str(file).split("name='")[1].split("'>")[0]
                with open('system\\settings.json', 'r+') as f:
                    data = json.load(f)
                    data['default_file'] = filename
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                continue

    def main(self):
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Settings')
        print('loading settings')
        settings = sys.load_settings()

        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Proxies')
        print('loading proxies')
        proxylist = sys.load_proxy()

        if proxylist == None:
            path = os.getcwd()
            file_path = f"{os.path.abspath(os.path.join(path, os.pardir))}\\proxy.txt"

            print(Fore.YELLOW, end='')
            response = input('No Proxies Found, Do you want to scrape proxies? (y/n): ')
            print(Style.RESET_ALL, end='')

            if response.lower() == 'y':
                f = open('system\\settings.json', 'r+')
                data = json.load(f)
                proxyscraper = data['proxyscraper']
                f.close()

                # Scrape proxies
                url = proxyscraper
                proxies = requests.get(url).text.split('\r\n')

                # Save proxies to file
                with open(file_path, 'w') as f:
                    f.write("\n".join(proxies))

                # Print number of proxies saved
                num_proxies = len(proxies)
                print(f'{num_proxies} Proxies saved to "proxy.txt" file.')
                proxylist = sys.load_proxy()
            else:
                print('Running Proxy Less...')

        fn = settings['default_file']
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Accounts')
        print('loading accounts')
        accounts = self.get_accounts(fn)

        print('loading assets')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Assets')
        sys.load_assets()

        print('loading checker')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Checker')
        scheck = checker.simplechecker(settings, proxylist, self.version)
        asyncio.run(scheck.main(accounts, self.count))
        return


pr = program()
if __name__ == '__main__':
    print('starting')
    pr.start()
