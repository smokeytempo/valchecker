import random
import requests
import json
import os
from tkinter import filedialog
import tkinter
import valo_api as vapi

class system():
    def __init__(self) -> None:
        self.proxylist=[]
        self.proxxy={
                        'http':None,
                        'https':None
                    }
        self.useproxy=self.load_proxy()

    def get_region(self,token):
        if self.useproxy==True:
            np=self.proxy(self.proxxy)
            self.proxxy={
                'http':np,
                'https':np
            }
        session=requests.Session()
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko","Pragma": "no-cache","Accept": "*/*","Content-Type": "application/json","Authorization":f"Bearer {token}"}
        userinfo = session.post('https://auth.riotgames.com/userinfo',headers=headers,proxies=self.proxxy)
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
            #print(regionn)
            reg=regionn.region
            lvl=regionn.account_level
            #print(reg,lvl)
            #input()
            return reg,lvl
        except Exception as e:
            if "Rate Limited" in str(e):
                return False,'riotlimit'
            return False,False

    def load_settings(self):
        try:
            f = open('system\\settings.json')
            data = json.load(f)
            out={'checkru':data['ru_check'],'default_file':data['default_file'],'saveout':data['saveout']}
            f.close()
            return out
        except:
            print("can't find settings.json\nplease download it from my github\n")
            return False

    def edit_settings(self):
        while True:
            os.system('cls')
            f = open('system\\settings.json','r+')
            data = json.load(f)
            checkru=data['ru_check']
            deffile=data['default_file']
            saveout=data['saveout']
            print(f'  [1] check skins in russian: {checkru}')
            print(f'  [2] default file: {deffile}')
            print(f'  [3] always save output to out.txt: {saveout}')
            print(f'\n  [~] enter any other number to exit')
            edit=str(input('\nenter the number u want to turn on/off >>>')).replace(' ','')
            if edit=='1':
                if checkru=='True':
                    data['ru_check']='False'
                else:
                    data['ru_check']='True'
            elif edit=='2':
                root = tkinter.Tk()
                file = filedialog.askopenfile(parent=root, mode='rb', title='select file with accounts (login:password)',
                    filetype=(("txt", "*.txt"), ("All files", "*.txt")))
                root.destroy()
                if file==None:
                    filename='None'
                else:
                    filename=str(file).split("name='")[1].split("'>")[0]
                data['default_file']=filename
            elif edit=='3':
                if saveout=='True':
                    data['saveout']='False'
                else:
                    data['saveout']='True'
            else:
                return
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()

    def load_proxy(self):
        with open ('system\\proxy.txt', 'r', encoding='UTF-8') as file:
            lines=file.readlines()
            for line in lines:
                if line !='' and line !=' ' and line != '\n':
                    if line not in self.proxylist:
                        self.proxylist.append(line)
        if len(self.proxylist)<=1:
            return False
        else:
            return True
    
    def proxy(self,nowproxy):
        nextproxy=random.choice(self.proxylist)
        while nextproxy==nowproxy:
            nextproxy=random.choice(self.proxylist)
            if 'default#pleasedonotdeletethis' in nextproxy:
                nextproxy=None
        return nextproxy

    def center(self,var:str, space:int=None): # From Pycenter
        if not space:
            space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
        return "\n".join((' ' * int(space)) + var for var in var.splitlines())

syss=system()