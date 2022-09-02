import json
import os
import random
import tkinter
from tkinter import filedialog

import requests
import valo_api as vapi
from InquirerPy import inquirer
from InquirerPy.separator import Separator

from codeparts import checkers
from codeparts.data import Constants

check=checkers.checkers()

class system():
    def __init__(self) -> None:
        self.proxylist=[]
        self.proxy = set()

        path = os.getcwd()
        self.parentpath=os.path.abspath(os.path.join(path, os.pardir))

    def get_region(self,token):
        session=requests.Session()
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko","Pragma": "no-cache","Accept": "*/*","Content-Type": "application/json","Authorization":f"Bearer {token}"}
        userinfo = session.post('https://auth.riotgames.com/userinfo',headers=headers,proxies=self.getproxy(self.proxylist))
        #print(userinfo.text)
        try:
            name=userinfo.text.split('game_name":"')[1].split('","')[0]
            tag=userinfo.text.split('tag_line":"')[1].split('","')[0]
        except Exception as e:
            return False,'N/A'
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

    def get_region2(self,token):
        session=requests.Session()
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Authorization":f"Bearer {token}"}
        userinfo = session.post(Constants.USERINFO,headers=headers,proxies=self.getproxy(self.proxylist)).json()
        try:
            region = userinfo['region']['id']
            fixedregion = Constants.LOL2REG[region]
        except:
            fixedregion=False

        #headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'}
        #body = {"id_token": 1}
        #r=session.put('https://riot-geo.pas.si.riotgames.com/pas/v1/product/valorant',headers=headers,json=body).text
        #input(r)

        return fixedregion

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
            cooldown=data['cooldown']
            auto_sort=data['auto_sort']
            webhook=data['webhook']
            menu_choices=[
                Separator(),
                f'Default File: {deffile}',
                f'RLimits to skip an acc: {max_rlimits}',
                f'Wait if there is a RLimit (seconds): {rlimit_wait}',
                f'Default Region: {default_region}',
                f'Wait between checking accounts (seconds): {cooldown}',
                f'Auto sort accounts after checking: {auto_sort}',
                f'Discord Webhook: {webhook}',
                Separator(),
                'Exit'
            ]
            edit = inquirer.select(
                message="Please select an option you want to edit:",
                choices=menu_choices,
                default=menu_choices[0],
                pointer='>'
            ).execute()
            if edit==menu_choices[1]:
                root = tkinter.Tk()
                file = filedialog.askopenfile(parent=root, mode='rb', title='select file with accounts (login:password)',
                    filetype=(("txt", "*.txt"), ("All files", "*.txt")))
                root.destroy()
                if file==None:
                    filename='None'
                else:
                    filename=str(file).split("name='")[1].split("'>")[0]
                data['default_file']=filename
            elif edit==menu_choices[2]:
                new_rlimits=input('enter the number of riot limits to skip this account (min 1) >>>')
                if int(new_rlimits)<1 or int(new_rlimits)>999:
                    return
                try:
                    data['max_rlimits']=int(new_rlimits)
                except:
                    print('u have to type a num from 1 to 999 (3 recommended)')
                    return
            elif edit==menu_choices[3]:
                new_maxrlimits=input('enter the number of seconds to wait if there is a riot limit (min 1) >>>')
                if int(new_maxrlimits)<1 or int(new_maxrlimits)>99999:
                    return
                try:
                    data['rlimit_wait']=int(new_maxrlimits)
                except:
                    print('u have to type a num from 1 to 99999 (30 recommended)')
                    return
            elif edit==menu_choices[4]:
                new_region=input('if region is unknown, the checker will try to check account in default region (eu,na,latam,ap,br,kr) >>>').lower().replace(' ','')
                data['default_region']=str(new_region)
            elif edit==menu_choices[5]:
                new_cd=input('enter the number of seconds to wait between checking accounts (min 0) >>>')
                if int(new_cd)<0 or int(new_cd)>99999:
                    return
                data['cooldown']=int(new_cd)
            elif edit==menu_choices[6]:
                autosortlist=[
                    Separator(),
                    'Yes',
                    'No'
                ]
                newautosort= inquirer.select(
                    message='should checker automatically sort valid accounts?',
                    choices=autosortlist,
                    default=autosortlist[0],
                    pointer='>'
            ).execute().replace('Yes','True').replace('No','False')
                data['auto_sort']=newautosort
            elif edit==menu_choices[7]:
                newwebhook=input('ented the discotd webhook to use (leave it empty if u dont wanna use it): ')
                data['webhook']=newwebhook
            elif edit==menu_choices[9]:
                return
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()

    def load_proxy(self):
        with open(f"{self.parentpath}\\proxy.txt", "r") as f:
            file_lines1 = f.readlines()
            if len(file_lines1) == 0:
                return
            for line1 in file_lines1:
                self.proxy.add(line1.strip())

        for i in list(self.proxy):
            if '.' in i:
                if 'http' in i:
                    self.proxylist.append({
                        'http': i
                    })
                else:
                    self.proxylist.append({
                        'http': 'http://EURB56DEGX:2ppZXsga@'+i
                    })
        return self.proxylist
    
    def getproxy(self,proxlist):
        if proxlist == None:
            return None
        if len(proxlist) <= 1:
            return None
        nextproxy=random.choice(proxlist)
        return nextproxy

    def center(self,var:str, space:int=None): # From Pycenter
        if not space:
            space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
        return "\n".join((' ' * int(space)) + var for var in var.splitlines())

syss=system()
