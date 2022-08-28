import ctypes
import json
import os
import random
import tkinter
from tkinter import filedialog
from InquirerPy import inquirer
from InquirerPy.separator import Separator

import time
import requests

import checker
from codeparts import auth, checkers, systems, validsort

check=checkers.checkers()
sys=systems.system()
valid=validsort.validsort()

class program():
    def __init__(self) -> None:
        self.count=0
        self.checked=0
        self.version='3.2'
        self.riotlimitinarow=0
        try:
            self.lastver=requests.get('https://lil-jaba.github.io/valchecker/src/system/lastver.html').text.replace(' ','').replace('\n','')
            if 'a' in self.lastver:
                self.lastver=self.version
        except:
            self.lastver=self.version

    def start(self):
        while True:
            secret=''
            if random.randint(0,50)==0:
                secret='\n\ncapybaras ontop!\n\n'
            ctypes.windll.kernel32.SetConsoleTitleW(f'ValChecker {self.version} by liljaba1337')
            os.system('cls')
            print(sys.center(f'''

██╗░░░██╗░█████╗░██╗░░░░░░█████╗░██╗░░██╗███████╗░█████╗░██╗░░██╗███████╗██████╗░
██║░░░██║██╔══██╗██║░░░░░██╔══██╗██║░░██║██╔════╝██╔══██╗██║░██╔╝██╔════╝██╔══██╗
╚██╗░██╔╝███████║██║░░░░░██║░░╚═╝███████║█████╗░░██║░░╚═╝█████═╝░█████╗░░██████╔╝
░╚████╔╝░██╔══██║██║░░░░░██║░░██╗██╔══██║██╔══╝░░██║░░██╗██╔═██╗░██╔══╝░░██╔══██╗
░░╚██╔╝░░██║░░██║███████╗╚█████╔╝██║░░██║███████╗╚█████╔╝██║░╚██╗███████╗██║░░██║
░░░╚═╝░░░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝░╚════╝░╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝
            '''))
            print(sys.center(f'v{self.version}{secret}'))
            if self.lastver!=self.version:
                print(sys.center(f'update to the last version ({self.lastver}) on my GitHub'))
            menu_choices=[
                Separator(),
                'Start Checker',
                'Edit Settings',
                'Sort Valid',
                'Info/Help',
                Separator(),
                'Exit'
            ]
            print(sys.center('\nhttps://github.com/LIL-JABA/valchecker\n'))
            res = inquirer.select(
                message="Please select an option:",
                choices=menu_choices,
                default=menu_choices[0],
                pointer='>'
            ).execute()
            if res==menu_choices[1]:
                self.main(redirect=True)
                break
            elif res==menu_choices[2]:
                sys.edit_settings()
            elif res==menu_choices[3]:
                valid.customsort()
                input('done. press ENTER to exit')
            elif res==menu_choices[4]:
                os.system('cls')
                print(f'''
    valchecker v{self.version} by liljaba1337

    discord: LIL JABA#1895
    server: https://discord.gg/r3Y5KhM7kP

  [1] - check valid/invalid/ban and save them to valid.txt in output folder
  [2] - i think u understand
  [3] - sorts all accounts from valid.txt which match your requirements to output\\sorted\\custom.txt

  [~] - press ENTER to return
                ''')
                input()
                continue
            elif res==menu_choices[6]:
                os._exit(0)


    def get_accounts(self,filename):
        while True:
            os.system('cls')
            try:
                with open (str(filename), 'r', encoding='UTF-8') as file:
                    lines = file.readlines()
                    ret=[]
                    for logpass in lines:
                        logpass=logpass.split(' ')[0].replace('\n','').replace(' ','')
                        # remove doubles
                        if logpass not in ret:
                            self.count+=1
                            ret.append(logpass)
                    return ret
            except:
                print(f"can't find the default file ({filename})\nplease select a new one")
                root = tkinter.Tk()
                file = filedialog.askopenfile(parent=root, mode='rb', title='select file with accounts (login:password)',
                    filetype=(("txt", "*.txt"), ("All files", "*.txt")))
                root.destroy()
                if file==None:
                    print('u chose nothing')
                    input('press ENTER to choose again')
                    continue
                filename=str(file).split("name='")[1].split("'>")[0]
                with open('system\\settings.json','r+') as f:
                    data = json.load(f)
                    data['default_file']=filename
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    f.truncate()
                continue


    def main(self,redirect=False):
        settings=sys.load_settings()
        proxylist=sys.load_proxy()
        fn=settings['default_file']
        accounts=self.get_accounts(fn)
        if redirect==True:
            scheck=checker.simplechecker(settings,proxylist)
            scheck.main(accounts,self.count)
            return
    
pr=program()
if __name__=='__main__':
    pr.start()
