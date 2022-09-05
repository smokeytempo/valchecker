import ctypes
import os
from InquirerPy import inquirer
from InquirerPy.separator import Separator

class validsort():

    def __init__(self) -> None:
        path=os.getcwd()
        self.parentpath=os.path.abspath(os.path.join(path, os.pardir))

    def customsort(self):
        clearno=[
            Separator(),
            'Yes',
            'No'
        ]

        regions=[
            Separator(),
            'EU',
            'NA',
            'AP',
            'BR',
            'KR',
            'LATAM',
            'Any'
        ]
        ranks=[
            Separator(),
            'locked',
            'unranked',
            'iron',
            'bronze',
            'silver',
            'gold',
            'platinum',
            'diamond',
            'ascendant',
            'immortal',
            'radiant',
            'Any'
        ]

        mails=[
            Separator(),
            'True',
            'False',
            'Any'
        ]

        clear = inquirer.select(
            message="You want to clear the sorted.txt file?",
            choices=clearno,
            default=clearno[0],
            pointer='>'
        ).execute()

        region = inquirer.select(
            message="region to search:",
            choices=regions,
            default=regions[0],
            pointer='>'
        ).execute()

        rank = inquirer.select(
            message="rank to search:",
            choices=ranks,
            default=ranks[0],
            pointer='>'
        ).execute()

        level=str(input('enter minimum level to search ("50" will search all accounts with level 50 or higher) >>>'))

        skins=str(input('enter how many skins should this account have ("10" will search all accounts with skins amount 10 or higher) >>>'))

        vp=str(input('enter how many VP should this account have ("1000" will search all accounts with VP amount 1000 or higher) >>>'))

        rp=str(input('enter how many RP should this account have ("1000" will search all accounts with RP amount 1000 or higher) >>>'))

        skin=str(input('enter what skin should be in this accounts (for example, prime vandal) >>>'))

        mail = inquirer.select(
            message="unverified mail:",
            choices=mails,
            default=mails[0],
            pointer='>'
        ).execute()

        region=region.lower().replace('any','')
        mail=mail.lower().replace('any','')
        rank=rank.lower().replace('any','')

        print(region,rank,level,skins,mail)

        if clear=='Yes':
            with open(f'{self.parentpath}/output/sorted.txt', 'w',encoding='UTF-8'):
                pass

        with open(f'{self.parentpath}/output/valid.txt','r',encoding='UTF-8',errors='ignore') as f:
            text=f.read()
        accounts=text.split('###account###')
        count=len(accounts)
        sorted=0
        matches=0
        for account in accounts:
            ctypes.windll.kernel32.SetConsoleTitleW(f'sorted {sorted}/{count}  {matches} matches')
            account=account.lower()

            # sort regions
            try:
                if f'region---------> {region}' in account:
                    if f'rank-----------> {rank}' in account:
                        if level!='':
                            try:
                                level=int(level)
                                levelacc=account.split('level----------> ')[1].split('|')[0].replace('\n','')
                                if levelacc == 'n/a':
                                    sorted+=1
                                    continue
                                else:
                                    levelacc=int(levelacc)
                                #print(levelacc)
                            except:
                                pass
                        else:
                            levelacc=1
                            level=0
                        if levelacc>=level or level=='':
                            if skins !='':
                                try:
                                    skinsam=int(skins)
                                    if account.split('|[ ')[1].split(' skins ]')[0] == 'n/a':
                                        sorted+=1
                                        continue
                                    else:
                                        skinsacc=int(account.split('|[ ')[1].split(' skins ]')[0])
                                    #print(skinsacc)
                                except:
                                    skinsacc=1
                                    skinsam=0
                            else:
                                skinsacc=1
                                skinsam=0
                            if skinsacc>=skinsam or skins =='':
                                if vp != '':
                                    try:
                                        vpam=int(vp)
                                        if account.split('|vp-------------> ')[1].split('|')[0].replace('\n','') == 'n/a':
                                            sorted+=1
                                            continue
                                        else:
                                            vpacc=int(account.split('|vp-------------> ')[1].split('|')[0].replace('\n',''))
                                    except:
                                        vpam=0
                                        vpacc=1
                                else:
                                    vpam=0
                                    vpacc=1
                                if vpacc>=vpam or vp =='':
                                    if rp != '':
                                        try:
                                            rpam=int(rp)
                                            if account.split('|rp-------------> ')[1].split('|')[0].replace('\n','') == 'n/a':
                                                sorted+=1
                                                continue
                                            else:
                                                rpacc=int(account.split('|rp-------------> ')[1].split('|')[0].replace('\n',''))
                                        except Exception as e:
                                            input(e)
                                            rpam=0
                                            rpacc=1
                                    else:
                                        rpam=0
                                        rpacc=1
                                    if rpacc>=rpam or rp =='':
                                        if f'unverifiedmail-> {mail}' in account:
                                            if skin in account:
                                                with open(f'{self.parentpath}/output/sorted.txt','a',encoding='UTF-8') as f:
                                                    f.write(account+'###account###')
                                                    matches+=1
                                                    print(f'sorted {sorted}/{count} MATCH')
            except Exception as e:
                pass
            print(f'sorted {sorted}/{count}')
            sorted+=1
        print(f'sorted {sorted}/{count}')
        return