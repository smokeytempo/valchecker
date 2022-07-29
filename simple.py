import ctypes
import os
import time

from colorama import Fore, Style

from modules import auth, checkers, systems

check=checkers.checkers()
sys=systems.system()
authenticate=auth.auth()

class simplechecker():
    def __init__(self) -> None:
        self.checked=0
        self.valid=0
        self.banned=0
        self.skins=0
        self.unverifiedmail=0
        self.err=0
        self.rlimits=0
        self.riotlimitinarow=0

        self.ranks={'unranked':0,'iron':0,'bronze':0,'silver':0,'gold':0,'platinum':0,'diamond':0,
        'ascendant':0,'immortal':0,'radiant':0,'unknown':0}
        self.locked=0

        self.regions={'eu':0,'na':0,'ap':0,'br':0,'kr':0,'latam':0,'unknown':0}

        self.useproxy=sys.load_proxy()

    def main(self,accounts,count):
        os.system(f'mode con: cols=60 lines=40')
        for account in accounts:
            while True:
                ctypes.windll.kernel32.SetConsoleTitleW(f'ValChecker by liljaba1337 | Checked {self.checked}/{count}')
                os.system('cls')
                print(f'''
        {sys.center('https://github.com/LIL-JABA/valchecker')}
        {sys.center(f'checking {account}')}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   checked              >[{Fore.YELLOW}{self.checked}/{count}{Style.RESET_ALL}]<
    >                   valid                >[{Fore.GREEN}{self.valid}{Style.RESET_ALL}]<
    >                   banned               >[{Fore.LIGHTRED_EX}{self.banned}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   skins                >[{Fore.GREEN}{self.skins}{Style.RESET_ALL}]<
    >                   unverified mail      >[{Fore.GREEN}{self.unverifiedmail}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   competitive locked  >[{Fore.LIGHTRED_EX}{self.locked}{Style.RESET_ALL}]<
    >                   unranked            >[{Fore.LIGHTGREEN_EX}{self.ranks['unranked']}{Style.RESET_ALL}]<
    >                   iron                >[{Fore.LIGHTBLACK_EX}{self.ranks['iron']}{Style.RESET_ALL}]<
    >                   bronze              >[{Fore.YELLOW}{self.ranks['bronze']}{Style.RESET_ALL}]<
    >                   silver              >[{Fore.WHITE}{self.ranks['silver']}{Style.RESET_ALL}]<
    >                   gold                >[{Fore.LIGHTYELLOW_EX}{self.ranks['gold']}{Style.RESET_ALL}]<
    >                   platinum            >[{Fore.CYAN}{self.ranks['platinum']}{Style.RESET_ALL}]<
    >                   diamond             >[{Fore.LIGHTMAGENTA_EX}{self.ranks['diamond']}{Style.RESET_ALL}]<
    >                   ascendant           >[{Fore.GREEN}{self.ranks['ascendant']}{Style.RESET_ALL}]<
    >                   immortal            >[{Fore.LIGHTRED_EX}{self.ranks['immortal']}{Style.RESET_ALL}]<
    >                   radiant             >[{Fore.YELLOW}{self.ranks['radiant']}{Style.RESET_ALL}]<
    >                   unknown             >[{Fore.YELLOW}{self.ranks['unknown']}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   EU                  >[{Fore.CYAN}{self.regions['eu']}{Style.RESET_ALL}]<
    >                   NA                  >[{Fore.CYAN}{self.regions['na']}{Style.RESET_ALL}]<
    >                   AP                  >[{Fore.CYAN}{self.regions['ap']}{Style.RESET_ALL}]<
    >                   BR                  >[{Fore.CYAN}{self.regions['br']}{Style.RESET_ALL}]<
    >                   KR                  >[{Fore.CYAN}{self.regions['kr']}{Style.RESET_ALL}]<
    >                   LATAM               >[{Fore.CYAN}{self.regions['latam']}{Style.RESET_ALL}]<
    >                   unknown             >[{Fore.LIGHTRED_EX}{self.regions['unknown']}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   errors              >[{Fore.LIGHTRED_EX}{self.err}{Style.RESET_ALL}]<
    >                   riot limits         >[{Fore.LIGHTRED_EX}{self.rlimits}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            ''')
                try:
                    token,entt,uuid,mailverif=authenticate.auth(account)
                    if token == 2:
                        self.err+=1
                    elif token==1:
                        if self.useproxy==True:
                            print('changing proxy')
                            continue
                        if self.riotlimitinarow<3:
                            print(sys.center('riot limit. waiting 30 seconds'))
                            time.sleep(30)
                            self.riotlimitinarow+=1
                            continue
                        else:
                            print(sys.center('3 riot limits in a row. skipping'))
                            self.riotlimitinarow=0
                            self.rlimits+=1
                            self.checked+=1
                            with open ('simplefolder\\riot_limits.txt', 'a', encoding='UTF-8') as file:
                                file.write(f'\n{account}')
                            break
                    elif token==3:
                        pass
                    elif token==0:
                        pass
                    elif token==4:
                        self.banned+=1
                    else:
                        if mailverif==True:
                            self.unverifiedmail+=1
                        while True:
                            reg,lvl=sys.get_region(token)
                            if reg!=False and reg!='':
                                self.regions[reg.lower()]+=1
                                if int(lvl)<20:
                                    self.locked+=1
                                else:
                                    rank=check.ranked(entt,token,uuid,reg).lower().split(' ')[0]
                                    try:
                                        self.ranks[rank]+=1
                                    except:
                                        self.ranks['unknown']+=1
                                skins=check.skins_en(entt,token,uuid,reg)
                                if skins != '':
                                    skinss=True
                                    self.skins+=1
                                break
                            elif reg==False and lvl=='riotlimit':
                                if self.useproxy==True:
                                    print('changing proxy')
                                    continue
                                if self.riotlimitinarow<3:
                                    print(sys.center('riot limit. waiting 30 seconds'))
                                    time.sleep(30)
                                    self.riotlimitinarow+=1
                                    continue
                                else:
                                    print(sys.center('3 riot limits in a row. skipping'))
                                    self.riotlimitinarow=0
                                    self.ranks['unknown']+=1
                                    self.regions['unknown']+=1
                                    rank=None
                                    lvl=None
                                    skinss=False
                                    reg=None
                                    unverifiedmail=True
                                    break
                            else:
                                self.ranks['unknown']+=1
                                self.regions['unknown']+=1
                                rank=None
                                lvl=None
                                skinss=False
                                reg=None
                                unverifiedmail=True
                                break
                        with open ('simplefolder\\valid.txt', 'a', encoding='UTF-8') as file:
                            file.write(f'\n{account} - [rank: {rank}][skins: {skinss}][lvl: {lvl}][server: {reg}][unverifiedmail: {unverifiedmail}]')
                        self.valid+=1
                except Exception as e:
                    #print(e)
                    #input()
                    self.err+=1
                self.checked+=1
                break

        # idk how to better check the last account
        os.system('cls')
        print(f'''
    {sys.center('https://github.com/LIL-JABA/valchecker')}
    {sys.center('F I N I S H E D')}
    {sys.center('you can now get full unfo using default checker')}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   checked              >[{Fore.YELLOW}{self.checked}/{count}{Style.RESET_ALL}]<
    >                   valid                >[{Fore.GREEN}{self.valid}{Style.RESET_ALL}]<
    >                   banned               >[{Fore.LIGHTRED_EX}{self.banned}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   skins                >[{Fore.GREEN}{self.skins}{Style.RESET_ALL}]<
    >                   unverified mail      >[{Fore.GREEN}{self.unverifiedmail}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   competitive locked  >[{Fore.LIGHTRED_EX}{self.locked}{Style.RESET_ALL}]<
    >                   unranked            >[{Fore.LIGHTGREEN_EX}{self.ranks['unranked']}{Style.RESET_ALL}]<
    >                   iron                >[{Fore.LIGHTBLACK_EX}{self.ranks['iron']}{Style.RESET_ALL}]<
    >                   bronze              >[{Fore.YELLOW}{self.ranks['bronze']}{Style.RESET_ALL}]<
    >                   silver              >[{Fore.WHITE}{self.ranks['silver']}{Style.RESET_ALL}]<
    >                   gold                >[{Fore.LIGHTYELLOW_EX}{self.ranks['gold']}{Style.RESET_ALL}]<
    >                   platinum            >[{Fore.CYAN}{self.ranks['platinum']}{Style.RESET_ALL}]<
    >                   diamond             >[{Fore.LIGHTMAGENTA_EX}{self.ranks['diamond']}{Style.RESET_ALL}]<
    >                   ascendant           >[{Fore.GREEN}{self.ranks['ascendant']}{Style.RESET_ALL}]<
    >                   immortal            >[{Fore.LIGHTRED_EX}{self.ranks['immortal']}{Style.RESET_ALL}]<
    >                   radiant             >[{Fore.YELLOW}{self.ranks['radiant']}{Style.RESET_ALL}]<
    >                   unknown             >[{Fore.YELLOW}{self.ranks['unknown']}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   EU                  >[{Fore.CYAN}{self.regions['eu']}{Style.RESET_ALL}]<
    >                   NA                  >[{Fore.CYAN}{self.regions['na']}{Style.RESET_ALL}]<
    >                   AP                  >[{Fore.CYAN}{self.regions['ap']}{Style.RESET_ALL}]<
    >                   BR                  >[{Fore.CYAN}{self.regions['br']}{Style.RESET_ALL}]<
    >                   KR                  >[{Fore.CYAN}{self.regions['kr']}{Style.RESET_ALL}]<
    >                   LATAM               >[{Fore.CYAN}{self.regions['latam']}{Style.RESET_ALL}]<
    >                   unknown             >[{Fore.LIGHTRED_EX}{self.regions['unknown']}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    >                   errors              >[{Fore.LIGHTRED_EX}{self.err}{Style.RESET_ALL}]<
    >                   riot limits         >[{Fore.LIGHTRED_EX}{self.rlimits}{Style.RESET_ALL}]<
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        ''')
