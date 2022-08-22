import random
import requests
import json
import os
from tkinter import filedialog
import tkinter
import valo_api as vapi
from codeparts import checkers

check=checkers.checkers()

class system():
    def __init__(self) -> None:
        self.proxylist=[]
        self.proxy = set()

    def get_region(self,token):
        session=requests.Session()
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko","Pragma": "no-cache","Accept": "*/*","Content-Type": "application/json","Authorization":f"Bearer {token}"}
        userinfo = session.post('https://auth.riotgames.com/userinfo',headers=headers,proxies=self.getproxy(self.proxylist))
        #print(userinfo.text)
        try:
            name=userinfo.text.split('game_name":"')[1].split('","')[0]
            tag=userinfo.text.split('tag_line":"')[1].split('","')[0]
        except Exception as e:
            return False,e
        #print(f'{name}\{tag}')
        try:
            regionn=vapi.get_account_details_v1(name,tag)
        #region=session.get(f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}",headers=user_agent,proxies=self.proxxy)
            reg=regionn.region
            lvl=regionn.account_level
            #print(reg,lvl)
            #input()
            return reg,lvl
        except Exception as e:
            #regions=['eu','na','ap','kr','latam','br']
            #for region in regions:
            #    ranked=check.skins_en(ent,token,uuid,region)
            #    print(ranked)
            #input()
            return False,'N/A'
                

    def load_settings(self):
        try:
            f = open('system\\settings.json')
            data = json.load(f)
            f.close()
            return data
        except:
            print("can't find settings.json\nplease download it from my github\n")
            return False

    def edit_settings(self):
        while True:
            os.system('cls')
            f = open('system\\settings.json','r+')
            data = json.load(f)
            deffile=data['default_file']
            max_rlimits=data['max_rlimits']
            rlimit_wait=data['rlimit_wait']
            default_region=data['default_region']
            print(f'  [1] default file: {deffile}')
            print(f'  [2] riot limits to skip the acc: {max_rlimits}')
            print(f'  [3] wait if there is a riot limit (seconds): {rlimit_wait}')
            #print(f'  [4] default region (enter 4 to see more): {default_region}')
            print(f'\n  [~] enter any other number to exit')
            edit=str(input('\nenter the number u want to edit >>>')).replace(' ','')
            if edit=='1':
                root = tkinter.Tk()
                file = filedialog.askopenfile(parent=root, mode='rb', title='select file with accounts (login:password)',
                    filetype=(("txt", "*.txt"), ("All files", "*.txt")))
                root.destroy()
                if file==None:
                    filename='None'
                else:
                    filename=str(file).split("name='")[1].split("'>")[0]
                data['default_file']=filename
            elif edit=='2':
                new_rlimits=input('enter the number of riot limits to skip this account (min 1) >>>')
                if new_rlimits<1 or new_rlimits>999:
                    return
                try:
                    data['max_rlimits']=int(new_rlimits)
                except:
                    print('u have to type a num from 1 to 999 (3 recommended)')
                    return
            elif edit=='3':
                new_maxrlimits=input('enter the number of seconds to wait if there is a riot limit (min 1) >>>')
                if int(new_maxrlimits)<1 or int(new_maxrlimits)>99999:
                    return
                try:
                    data['rlimit_wait']=int(new_maxrlimits)
                except:
                    print('u have to type a num from 1 to 99999 (30 recommended)')
                    return
            elif edit=='4':
                new_region=input('if region is unknown, the checker will try to check account in default region (eu,na,latam,ap,br,kr) >>>').lower().replace(' ','')
                data['default_region']=str(new_region)
            else:
                return
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()

    def load_proxy(self):
        with open("system\\proxy.txt", "r") as f:
            file_lines1 = f.readlines()
            if len(file_lines1) == 0:
                return
            for line1 in file_lines1:
                self.proxy.add(line1.strip())

        for i in list(self.proxy):
            self.proxylist.append({
                'http': 'http://EURB56DEGX:2ppZXsga@'+i
            })
        return self.proxylist
    
    def getproxy(self,proxlist):
        if len(proxlist) == 0:
            return None
        nextproxy=random.choice(proxlist)
        return nextproxy

    def center(self,var:str, space:int=None): # From Pycenter
        if not space:
            space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
        return "\n".join((' ' * int(space)) + var for var in var.splitlines())

syss=system()