import requests
import riot_auth
import asyncio
import sys
import json
import os

class system():
    def auth(self,login=None,password=None,logpass=None,response=4):
        try:
            if login == None and password==None:
                logpasss=logpass.split(':')
                login=logpasss[0]
                password=logpasss[1]
            # region asyncio.run() bug workaround for Windows, remove below 3.8 or above 3.11 beta 1
            if sys.platform == "win32":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            # endregion
            CREDS = login, password

            auth = riot_auth.RiotAuth()
            asyncio.run(auth.authorize(*CREDS))

            #print(f"Access Token Type: {auth.token_type}\n")
            #print(f"Access Token: {auth.access_token}\n")
            #print(f"Entitlements Token: {auth.entitlements_token}\n")
            #print(f"User ID: {auth.user_id}")

            # Reauth using cookies. Returns a bool indicating whether the reauth attempt was successful.
            asyncio.run(auth.reauthorize())
            if response==1:
                return auth.access_token
            elif response==2:
                return auth.entitlements_token
            elif response==3:
                return auth.user_id
            elif response==4:
                return auth.access_token, auth.entitlements_token, auth.user_id
        except Exception as e:
            return e,'err','err'

    def get_region(self,token):
        session=requests.Session()
        user_agent = {'User-agent': 'Mozilla/5.0'}
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko","Pragma": "no-cache","Accept": "*/*","Content-Type": "application/json","Authorization":f"Bearer {token}"}
        userinfo = session.post('https://auth.riotgames.com/userinfo',headers=headers)
        name=userinfo.text.split('game_name":"')[1].split('","')[0]
        tag=userinfo.text.split('tag_line":"')[1].split('","')[0]
        #print(f'{name}\{tag}')
        region=session.get(f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}",headers=user_agent)
        regionn=region.text
        #print(regionn)
        if '{"status":200,' in regionn:
            reg=regionn.split('"region":"')[1].split('","')[0]
            lvl=regionn.split('account_level":')[1].split(',"')[0]
            #print(reg,lvl)
            return reg,lvl           
        else:
            return False,f'{name}#{tag}'

    def load_settings(self):
        try:
            f = open('system\\settings.json')
            data = json.load(f)
            checkru=data['ru_check']
            f.close()
        except:
            print("can't find settings.json\nusung default settings\n")
            checkru='True'
        return checkru

    def edit_settings(self):
        while True:
            os.system('cls')
            f = open('system\\settings.json','r+')
            data = json.load(f)
            checkru=data['ru_check']
            print(f'  [1] check skins in russian: {checkru}')
            print(f'  [~] enter any other number to exit')
            edit=str(input('\nenter the number u want to turn on/off >>>')).replace(' ','')
            if edit=='1':
                if checkru=='True':
                    data['ru_check']='False'
                else:
                    data['ru_check']='True'
            else:
                return
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            f.close()


    def center(self,var:str, space:int=None): # From Pycenter
        if not space:
            space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
        return "\n".join((' ' * int(space)) + var for var in var.splitlines())

syss=system()