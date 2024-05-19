import asyncio
import ctypes
import os
import random
import sys as s
from ctypes import windll
try:
    import tkinter
    from tkinter import filedialog
except ImportError:
    pass
from InquirerPy import inquirer
from InquirerPy.separator import Separator
from InquirerPy.validator import PathValidator
from clear import clear
import colorama

import requests

import checker
from codeparts import checkers, systems, validsort
from codeparts.systems import system

check = checkers.checkers()
sys = systems.system()
valid = validsort.validsort()

class program():
    def __init__(self) -> None:
        self.count = int(0)
        self.checked = int(0)
        with open("system/ver.txt", 'r') as r:
            self.version = r.read().strip()
        self.riotlimitinarow = int(0)
        path = str(os.getcwd())
        self.parentpath = str(os.path.abspath(os.path.join(path, os.pardir)))
        try:
            self.lastver = str(requests.get(
                'https://api.github.com/repos/lil-jaba/valchecker/releases').json()[0]['tag_name'])
        except Exception:
            self.lastver = self.version

    def start(self) -> None:
        try:
            print('internet check')
            requests.get('https://github.com')
        except requests.exceptions.ConnectionError:
            print('no internet connection')
            os._exit(0)

        print("checking certificates")
        if not sys.check_certificates():
            print("You don't have the required certificate installed\nPlease download and install it from https://crt.sh/?d=2835394")
            os._exit(0)
        clear()
        #kernel32 = ctypes.windll.kernel32
        #kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 128)
        codes = vars(colorama.Fore)
        colors = [codes[color] for color in codes if color not in ['BLACK']]
        colored_name = [random.choice(
            colors) + char for char in 'ValChecker by liljaba1337']
        print(sys.get_spaces_to_center('ValChecker by liljaba1337') +
              (''.join(colored_name))+colorama.Fore.RESET)
        print(sys.center(f'v{self.version}'))

        if self.lastver != self.version:
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
            input('finished checking. press ENTER or the power button on your PC to exit')
        elif res == menu_choices[2]:
            settings = sys.load_settings()
            slchecker = checker.singlelinechecker(settings["antipublic_token"] if settings["antipublic"] is True else "", settings["session"])
            asyncio.run(slchecker.main())
        elif res == menu_choices[3]:
            sys.edit_settings()
        elif res == menu_choices[4]:
            valid.customsort()
            input('done. press ENTER or the power button on your PC to exit')
        elif res == menu_choices[5]:
            sys.checkproxy()
        elif res == menu_choices[6]:
            clear()
            print(f'''
    valchecker v{self.version} by liljaba1337

    Cleaned and Modified by WeCanCodeTrust
    yo whatsup

  [~] - press ENTER to return
            ''')
            input()
            
        elif res == menu_choices[8]:
            os._exit(0)
        pr.start()

    def get_accounts(self) -> tuple:
        """
        Get accounts from a file or a .vlchkr file

        :return: tuple
        """
        filetypes = (("", (".txt", ".vlchkr")), ("All files", "."))
        if consolemode:
            print("Press Tab to show files in directory Press Enter to select file")
            file = inquirer.filepath(
                message="Select a file with combos OR .vlchkr ro continue checking:\n",
                default=os.getcwd(),
                validate=PathValidator(is_file=True, message="Input is not a file"),
                only_files=True,
            ).execute()
        elif not consolemode:
            root = tkinter.Tk()
            file = filedialog.askopenfile(
                parent=root,
                mode="rb",
                title="Select a file with combos OR .vlchkr to continue checking",
                filetypes=filetypes,
            )
            root.destroy()
        clear()
        if file is None:
            os._exit(0)
        filename = str(file).split("name='")[1].split("'>")[0]
        if ".vlchkr" in filename:
            valkekersource = systems.vlchkrsource(filename)
            return valkekersource, filename.split("/")[-1]

        ret = []
        seen = set()
        with open(str(filename), "r", encoding="UTF-8", errors="replace") as file:
            for logpass in file:
                logpass = str(logpass.strip())
                if logpass not in seen and len(logpass.split(':')) == 2:
                    self.count += 1
                    ret.append(logpass)
                    seen.add(logpass)
        
        sys.set_console_title(f"ValChecker {self.version} by liljaba1337 | Loading Accounts ({self.count})")
        return ret, filename.split("/")[-1]

    def main(self) -> None:
        sys.set_console_title(f'ValChecker {self.version} by liljaba1337 | Loading Settings')
        print('loading settings')
        settings = sys.load_settings()

        sys.set_console_title(f'ValChecker {self.version} by liljaba1337 | Loading Proxies')
        print('loading proxies')
        proxylist = sys.load_proxy()

        sys.set_console_title(f'ValChecker {self.version} by liljaba1337 | Loading Accounts')
        print('loading accounts')
        accounts, comboname = self.get_accounts()

        sys.set_console_title(f'ValChecker {self.version} by liljaba1337 | Loading Assets')
        print('loading assets')
        sys.load_assets()

        sys.set_console_title(f'ValChecker {self.version} by liljaba1337 | Loading Checker')
        print('loading checker')
        
        if proxylist is None:
            windll.user32.MessageBoxW(0, "You are trying to start the checker without using any proxies. "+
        "I strongly recommend you not to do that, since it can cause your IP to get banned by Riot. To buy good proxies, you can join my Discord server.", "PROXYLESS ALERT", 4144)
        scheck = checker.simplechecker(settings, proxylist, self.version, comboname)

        isvalkekersource = False
        if type(accounts) == systems.vlchkrsource:
            isvalkekersource = True
        asyncio.run(scheck.main(accounts, self.count, isvalkekersource))
        return


pr = program()
if __name__ == '__main__':
    args = s.argv
    if '-d' in args:
        slchecker = checker.singlelinechecker("", "_debug_session", True)
        asyncio.run(slchecker.main())
        os._exit(0)
    elif '-c' in args:
        consolemode = True
    elif ["-h", "--help"] in args:
        print('ValChecker by liljaba1337\n\n-h, --help: show this message\n-c: run in console mode\n-d: run in debug mode\n')
        os._exit(0)
    else:
        consolemode = False
    print('starting')
    if not consolemode:
        try:
            import tkinter
            from tkinter import filedialog
        except ImportError:
            raise ImportError('tkinter is not installed on your system. Please install it to use the GUI or use the console mode -c')
    pr.start()
