from ast import excepthandler
import requests
import systems
import checkers
import ctypes
import os

check=checkers.checkers()
sys=systems.system()

class program():
    def __init__(self) -> None:
        self.count=0
        self.checked=0
        self.version='2.0.1'
        try:
            self.lastver=requests.get('https://lil-jaba.github.io/valchecker/lastver.html').text.replace(' ','').replace('\n','')
        except:
            self.lastver='err'

    def start(self):
        while True:
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
            print(sys.center('\nhttps://github.com/LIL-JABA\n'))
            print('  [1] - START CHECKER')
            print('  [2] - EDIT SETTINGS')
            res=str(input('\n>>>'))
            if res=='1':
                os.system('cls')
                pr.main()
                break
            elif res=='2':
                sys.edit_settings()
            else:
                pr.main()
                break


    def get_accounts(self,filename):
        try:
            with open (str(filename)+'.txt', 'r', encoding='UTF-8') as file:
                lines = file.readlines()
                ret=[]
                for logpass in lines:
                    self.count+=1
                    logpass=logpass.split(' - ')[0].replace('\n','').replace(' ','')
                    ret.append(logpass)
                print(f'detected {self.count} accounts\n')
                return ret
        except:
            return 0

    def main(self):
        checkru=sys.load_settings()
        tofile=''
        fn='accounts'
        accounts=self.get_accounts(fn)
        if accounts==0:
            print('file "accounts.txt" was not found')
            return
        for account in accounts:
            ctypes.windll.kernel32.SetConsoleTitleW(f'ValChecker {self.version} by liljaba1337 | CHECKED {self.checked}/{self.count}')
            print('_____________')
            tofile+='_____________\n'
            print(account+'\n\n')
            tofile+=account+'\n\n'
            acctoken,enttoken,uid=sys.auth(logpass=account,response=4)
            if enttoken=='err':
                print(acctoken)
                tofile+=f'{acctoken}\n\n'
                self.checked+=1
                continue
            region,level=sys.get_region(acctoken)
            if region==False:
                print(f"unable to check region\nyou can check it using {level} and type region below\n(leave it empty if u wanna skip this account)")
                region=input('>>>').replace(' ','')
                if region=='':
                    tofile+='SKIPPED\n\n'
                    self.checked+=1
                    continue
                level=None
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
        saveno=str(input('save output to "out.txt"? (y/n) >>>'))
        if saveno=='y':
            with open ('out.txt', 'w', encoding='UTF-8') as file:
                file.write(tofile)
        else:
            pass
    
pr=program()
if __name__=='__main__':
    pr.start()