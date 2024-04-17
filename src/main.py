import asyncio
import ctypes
import json
import os
import random
import tkinter
import win32api
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
        self.version = '3.17.0.4'
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
        #kernel32 = ctypes.windll.kernel32
        #kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
        codes = vars(colorama.Fore)
        colors = [codes[color] for color in codes if color not in ['BLACK']]
        colored_name = [random.choice(
            colors) + char for char in f'ValChecker by liljaba1337']
        print(sys.get_spaces_to_center('ValChecker by liljaba1337') +
              (''.join(colored_name))+colorama.Fore.RESET)
        print(sys.center(f'v{self.version}'))

        self.CheckIfFirstStart()

        if 'beta' in self.version:
            print(sys.center(
                f'{Fore.YELLOW}You have downloaded the BETA version. It can work unstable and contain some bugs.'))
            print(sys.center(
                f'Visit https://github.com/LIL-JABA/valchecker/releases/latest to download the latest stable release{Fore.RESET}'))
        elif self.lastver != self.version:
            print(sys.center(
                f'\nnext version {self.lastver} is available!'))
            if inquirer.confirm(
                message="{}Would you like to download it now?".format(system.get_spaces_to_center('Would you like to download it now? (Y/n)')), default=True, qmark=''
            ).execute():
                os.system(f'{self.parentpath}/updater.bat')
                os._exit(0)
        menu_choices = [
            Separator(),
            'Start Checker',
            'Single-Line Checker',
            'Edit Settings',
            'Sort Valid',
            'Test Proxy',
            'Info',
            Separator(),
            'Exit'
        ]
        print(sys.center('\nhttps://github.com/LIL-JABA/valchecker\n'))
        print(sys.center('https://discord.gg/vapenation\n'))
        res = inquirer.select(
            message="\nUse arrow keys to select and ENTER to confirm\nPlease select an option:",
            choices=menu_choices,
            default=menu_choices[0],
            pointer='>',
            qmark=''
        ).execute()
        if res == menu_choices[1]:
            self.main()
            input('finished checking. press ENTER to exit')
            pr.start()
        elif res == menu_choices[2]:
            settings = sys.load_settings()
            slchecker = checker.singlelinechecker(settings["antipublic_token"] if settings["antipublic"] == "True" else "", settings["session"])
            slchecker.main()
            pr.start()
        elif res == menu_choices[3]:
            sys.edit_settings()
            pr.start()
        elif res == menu_choices[4]:
            valid.customsort()
            input('done. press ENTER to exit')
            pr.start()
        elif res == menu_choices[5]:
            sys.checkproxy()
            pr.start()
        elif res == menu_choices[6]:
            os.system('cls')
            print(f'''
    valchecker v{self.version} by liljaba1337

    yo whatsup

  [~] - press ENTER to return
            ''')
            input()
            pr.start()
        elif res == menu_choices[8]:
            os._exit(0)

    def get_accounts(self):
        filetypes = (
            ("", ("*.txt", "*.vlchkr")),
            ("All files", "*.*")
        )
        root = tkinter.Tk()
        file = filedialog.askopenfile(parent=root, mode='rb', title='Select a file with combos OR .vlchkr ro continue checking',
                                      filetypes=filetypes)
        root.destroy()
        os.system('cls')
        if file == None:
            os._exit(0)
        filename = str(file).split("name='")[1].split("'>")[0]
        if (".vlchkr" in filename):
            valkekersource = systems.vlchkrsource(filename)
            return valkekersource, filename.split('/')[-1]
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
                    return lines, filename.split('/')[-1]
            for logpass in lines:
                logpass = logpass.strip()
                # remove doubles
                if logpass not in ret and ':' in logpass:
                    self.count += 1
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f'ValChecker {self.version} by liljaba1337 | Loading Accounts ({self.count})')
                    ret.append(logpass)
            return ret, filename.split('/')[-1]

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

        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Accounts')
        print('loading accounts')
        accounts, comboname = self.get_accounts()

        print('loading assets')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Assets')
        sys.load_assets()

        print('loading checker')
        ctypes.windll.kernel32.SetConsoleTitleW(
            f'ValChecker {self.version} by liljaba1337 | Loading Checker')
        scheck = checker.simplechecker(settings, proxylist, self.version, comboname)

        isvalkekersource = False
        if type(accounts) == systems.vlchkrsource:
            isvalkekersource = True
        asyncio.run(scheck.main(accounts, self.count, isvalkekersource))
        return

    def CheckIfFirstStart(self) -> None:
        with open("system/xd.txt", 'r+') as r:
            if r.read() == '0':
                win32api.MessageBox(None,
                                             """Hello! Looks like it's your first start of ValChecker.
Although you can find the FAQ and the full guide in my discord, I will specify some things here.


What is a Rate Limit? When you send a lot of auth requests from one IP, riot blocks you for some time.
So that's why you should use proxies for checking. If riot bans your IP, you will not be able to login in their launcher or site for ~30 minutes.

Where can I find proxies? Any website you trust, just search for that in the internet. Or you can buy a cheap UHQ proxy method on my discord server.

Where can I find combos? Actually, the answer is the same as with proxies. The internet. But if you want to do combos yourself, you can buy a cheap and effective method on my discord server.


The link to my discord server can be found in the readme section of the github repository or on the ValChecker title screen.

Good luck!""", "Hello!", 0)
                r.write("1")


pr = program()
if __name__ == '__main__':
    print('starting')
    pr.start()
