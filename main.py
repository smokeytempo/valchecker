import ctypes
import json
import os
import tkinter
from tkinter import filedialog

import time
import requests

import simple
from modules import auth, checkers, systems, validsort

check=checkers.checkers()
sys=systems.system()
authenticate=auth.auth()
scheck=simple.simplechecker()
valid=validsort.validsort()

class program():
    def __init__(self) -> None:
        self.count=0
        self.checked=0
        self.version='2.3.1'
        self.riotlimitinarow=0
        try:
            self.lastver=requests.get('https://lil-jaba.github.io/valchecker/system/lastver.html').text.replace(' ','').replace('\n','')
            if 'a' in self.lastver:
                self.lastver=self.version
        except:
            self.lastver=self.version

    def start(self):
        while True:
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
            print(sys.center(f'v{self.version}'))
            if self.lastver!=self.version:
                print(sys.center(f'update to the last version ({self.lastver}) on my GitHub'))
            print(sys.center('\nhttps://github.com/LIL-JABA/valchecker\n'))
            print('  [1] - START CHECKER')
            print('  [2] - EDIT SETTINGS')
            print('  [3] - SIMPLE CHECKER')
            print('  [4] - SORT VALID')
            print('  [5] - INFO')
            res=str(input('\n>>>'))
            if res=='1':
                os.system('cls')
                pr.main()
                break
            elif res=='2':
                sys.edit_settings()
            elif res=='3':
                self.main(redirect=True)
                break
            elif res=='4':
                valid.sort()
                print('done')
                return
            elif res=='5':
                os.system('cls')
                print('''

  [1] - check skins, rank, level, etc
  [2] - i think u understand
  [3] - check valid/invalid/ban and save them to files in simplefolder
  [4] - sorts all accounts from simplefolder\\valid.txt to simplefolder\\sorted\\...

  [~] - press ENTER to return
                ''')
                input()
                continue
            else:
                continue


    def get_accounts(self,filename):
        while True:
            os.system('cls')
            try:
                with open (str(filename), 'r', encoding='UTF-8') as file:
                    lines = file.readlines()
                    ret=[]
                    for logpass in lines:
                        self.count+=1
                        logpass=logpass.split(' - ')[0].replace('\n','').replace(' ','')
                        ret.append(logpass)
                    print(f'\ndetected {self.count} accounts\n')
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
        useproxy=sys.load_proxy()
        checkru=settings['checkru']
        fn=settings['default_file']
        tofile=''
        accounts=self.get_accounts(fn)
        if redirect==True:
            scheck.main(accounts,self.count)
            return
        for account in accounts:
            while True: # programm will check this account again if there is a riot limit
                ctypes.windll.kernel32.SetConsoleTitleW(f'ValChecker {self.version} by liljaba1337 | CHECKED {self.checked}/{self.count}')
                print('_____________')
                tofile+='_____________\n'
                print(account+'\n\n')
                tofile+=account+'\n\n'
                acctoken,enttoken,uid,mailverified=authenticate.auth(logpass=account)
                if enttoken==0:
                    print('incorrect')
                    tofile+=f'incorrect\n\n'
                    self.checked+=1
                    break
                elif enttoken==1:
                    if useproxy==True:
                        print('changing proxy')
                        continue
                    else:
                        if self.riotlimitinarow<3:
                            print('riot limit. waiting 30 seconds')
                            time.sleep(30)
                            self.riotlimitinarow+=1
                            continue
                        else:
                            print('3 riot limits in a row. skipping')
                            tofile+=f'riot limit\n\n'
                            self.riotlimitinarow=0
                            self.checked+=1
                            break
                        
                elif enttoken==3:
                    print('2FA')
                    tofile+=f'2FA\n\n'
                    self.checked+=1
                    break
                elif enttoken==4:
                    print('banned')
                    tofile+=f'banned\n\n'
                    self.checked+=1
                    break
                region,level=sys.get_region(acctoken)
                if region==False and level=='riotlimit':
                    if self.riotlimitinarow<3:
                        print('riot limit. waiting 30 seconds')
                        time.sleep(30)
                        self.riotlimitinarow+=1
                        continue
                    else:
                        print('3 riot limits in a row. skipping')
                        tofile+=f'riot limit\n\n'
                        self.riotlimitinarow=0
                        self.checked+=1
                        break
                elif region==False:
                    print(f"unable to check region")
                    tofile+='unable to check region\n\n'
                    self.checked+=1
                    break
                skins=check.skins_en(enttoken,acctoken,uid,region)
                print(skins)
                tofile+=skins+'\n'
                print('\n')
                tofile+='\n'
                if checkru=='True':
                    skinsru=check.skins_ru(enttoken,acctoken,uid,region)
                    print(skinsru)
                    tofile+=skinsru+'\n'
                rank=check.ranked(enttoken,acctoken,uid,region)
                print(f'{rank} ({level} lvl)')
                tofile+=f'{rank} ({level} lvl)\n'
                lp=check.lastplayed(uid,region)
                print(f'last game was on {lp}\n')
                tofile+=f'last game was on {lp}\n'
                self.checked+=1
                ctypes.windll.kernel32.SetConsoleTitleW(f'ValChecker {self.version} by liljaba1337 | CHECKED {self.checked}/{self.count}')
                break
        if settings['saveout']=='False':
            saveno=str(input('save output to "out.txt"? (y/n) >>>'))
        else:
            saveno='y'
        if saveno=='y' or settings['saveout']=='True':
            with open ('out.txt', 'w', encoding='UTF-8') as file:
                file.write(tofile)
            print('saved output to out.txt')
        else:
            pass
    
pr=program()
if __name__=='__main__':
    pr.start()
