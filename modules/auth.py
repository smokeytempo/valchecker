# https://github.com/xharky/Valorant-auth-example

from collections import OrderedDict
from msilib import type_binary
from re import compile
from ssl import PROTOCOL_TLSv1_2
from tkinter import *

from requests import session as sesh
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager


class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block,
                                       ssl_version=PROTOCOL_TLSv1_2)

class auth():
    def auth(self,logpass):
        try:
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
                "acr_values": "urn:riot:bronze",
                "claims": "",
                "client_id": "riot-client",
                "nonce": "oYnVwCSrlS5IHKh7iI16oQ",
                "redirect_uri": "http://localhost/redirect",
                "response_type": "token id_token",
                "scope": "openid link ban lol_region",
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
            #print(r2.text)
            data = r2.json()
            #print(data)
            if "access_token" in r2.text:
                pattern = compile(
                    'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
                data = pattern.findall(data['response']['parameters']['uri'])[0]
                token = data[0]

            elif "auth_failure" in r2.text:
                return 0,0,0
            elif 'rate_limited' in r2.text:
                return 1,1,1
            elif 'multifactor' in r2.text:
                return 3,3,3
            headers = {
                'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
                'Authorization': f'Bearer {token}'
            }
            r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={})
            entitlement = r.json()['entitlements_token']
            r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={})
            #print(r.text)
            #input()
            data = r.json()
            #print(data)
            #input()
            puuid = data['sub']
            try:
                data2=data['ban']
                data3 = data2['restrictions']
                for x in data3:
                    typebanned = x['type']
                if typebanned == "PERMANENT_BAN" or typebanned=='PERMA_BAN' or typebanned=='TIME_BAN' or typebanned or typebanned=='LEGACY_BAN':
                    return 4,4,4
                else:
                    pass
            except Exception as e:
                #print(e)
                #input()
                pass
            return token,entitlement,puuid
            #print(f"Accestoken: {token}")
            #print("-"*50)
            #print(f"Entitlements: {entitlement}")
            #print("-"*50)
            #print(f"Userid: {puuid}")
        except:
            return 2,2,2
