import ctypes
import os

class validsort():

    def __init__(self) -> None:
        path=os.getcwd()
        self.parentpath=os.path.abspath(os.path.join(path, os.pardir))

    def customsort(self):
        print('leave the string empty if this setting doesnt matter\n')
        region=str(input('enter region to search (eu; na; ap; br; kr; latam) >>>'))
        level=str(input('enter minimum level to search ("50" will search all accounts with level 50 or higher) >>>'))
        rank=str(input('enter rank to search (iron; bronze; silver; gold; platinum; diamond; ascendant; immortal; radiant) >>>'))
        skins=str(input('enter how many skins should this account has ("10" will search all accounts with skins amount 10 or higher) >>>'))
        mail=str(input('enter if this account should have unverified mail (true; false) >>>'))

        with open(f'{self.parentpath}/output/valid.txt','r',encoding='UTF-8') as f:
            text=f.read()
        accounts=text.split('###account###')
        count=len(accounts)
        sorted=0
        matches=0
        for account in accounts:
            ctypes.windll.kernel32.SetConsoleTitleW(f'sorted {sorted}/{count}  {matches} matches')
            print(f'sorted {sorted}/{count}')
            account=account.lower()

            # sort regions
            try:
                if f'region: {region}' in account:
                    #print(True)
                    if f'rank: {rank}' in account:
                        #print(True)
                        if level!='':
                            try:
                                level=int(level)
                                levelacc=int(account.split('level: ')[1].split('|')[0].replace('\n',''))
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
                                if f'|unverifiedmail: {mail}' in account:
                                    #print(True)
                                    with open(f'{self.parentpath}/output/sorted.txt','a',encoding='UTF-8') as f:
                                        f.write(account+'###account###')
                                        matches+=1
            except Exception as e:
                pass
            sorted+=1
        print(f'sorted {sorted}/{count}')
        return