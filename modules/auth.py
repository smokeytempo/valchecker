# https://github.com/xharky/Valorant-auth-example

from requests import session as sesh
from requests.adapters import HTTPAdapter
from ssl import PROTOCOL_TLSv1_2
from urllib3 import PoolManager
from tkinter import *
from collections import OrderedDict
from re import compile




class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block,
                                       ssl_version=PROTOCOL_TLSv1_2)

class auth():
    def auth(self,logpass):
        username=logpass.split(':')[0]
        password=logpass.split(':')[1]
        headers = OrderedDict({
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "application/json, text/plain, */*",
            'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)'
        })
        session = sesh()
        session.headers = headers
        session.mount('https://', TLSAdapter())
        data = {
            "client_id": "play-valorant-web-prod",
            "nonce": "1",
            "redirect_uri": "https://playvalorant.com/opt_in",
            "response_type": "token id_token",
            'scope': 'account openid',
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
        }
        r = session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
        data = {
            'type': 'auth',
            'username': username,
            'password': password
        }
        r2 = session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers)
        data = r2.json()
        #print(r2.text)
        if "access_token" in r2.text:
            pattern = compile(
                'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            data = pattern.findall(data['response']['parameters']['uri'])[0]
            token = data[0]

        elif "auth_failure" in r2.text:
            return 0,0,0
        else:
            return 1,1,1
        headers = {
            'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
            'Authorization': f'Bearer {token}',
        }
        r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
        entitlement = r.json()['entitlements_token']
        r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
        data = r.json()
        puuid = data['sub']

        return token,entitlement,puuid
        #print(f"Accestoken: {token}")
        #print("-"*50)
        #print(f"Entitlements: {entitlement}")
        #print("-"*50)
        #print(f"Userid: {puuid}")