import os
import traceback
from collections import OrderedDict
from re import compile
from ssl import PROTOCOL_TLSv1_2
from tkinter import *
import asyncio
import sys

import pandas
import requests
from requests.adapters import HTTPAdapter
from urllib3 import PoolManager

from codeparts import systems
from codeparts.riot_auth import *

syst = systems.system()


class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=PROTOCOL_TLSv1_2,
        )


class auth():
    def __init__(self) -> None:
        path = os.getcwd()
        self.parentpath = os.path.abspath(os.path.join(path, os.pardir))

    def auth(self, logpass: str = None, username=None, password=None, proxy=None):
        try:
            headers = OrderedDict({
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "application/json, text/plain, */*",
                'User-Agent': 'RiotClient/62.0.1.4852117.4789131 %s (Windows;10;;Professional, x64)'
            })
            session = requests.Session()
            session.trust_env = False
            session.headers = headers
            #session.mount('http://', TLSAdapter())
            session.mount('https://', TLSAdapter())
            # proxy=None
            # session.proxies = proxy
            if username is None:
                username = logpass.split(':')[0].strip()
                password = logpass.split(':')[1].strip()

            # data = {
            #     "client_id": "play-valorant-web-prod",
            #     "nonce": "1",
            #     "redirect_uri": "https://playvalorant.com/opt_in",
            #     "response_type": "token id_token",
            #     'scope': 'account openid link ban lol_region',
            # }
            # headers = {
            #     'Content-Type': 'application/json',
            #     'User-Agent': 'RiotClient/62.0.1.4852117.4789131 %s (Windows;10;;Professional, x64)'
            # }
            # try:
            #     r = session.post(f'https://auth.riotgames.com/api/v1/authorization',
            #                      json=data, headers=headers, proxies=proxy, timeout=20)
            #     #input(r.text)
            #     data = {
            #         'type': 'auth',
            #         'username': username,
            #         'password': password
            #     }
            #     r2 = session.put('https://auth.riotgames.com/api/v1/authorization',
            #                      json=data, headers=headers, proxies=proxy, timeout=20)
            #     input(r2.text) #!!!!!!!!!!!!!!!!!!!!!!!!! DELETE THIS SHIT
            # except Exception as e:
            #     input(e)
            #     return 6, 6, 6, True, None
            # # print(r2.text)
            # try:
            #     data = r2.json()
            # except:
            #     return 6, 6, 6, 6, None
            # if "access_token" in r2.text:
            #     pattern = compile(
            #         'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            #     data = pattern.findall(
            #         data['response']['parameters']['uri'])[0]
            #     token = data[0]
            #     token_id = data[1]

            # elif 'invalid_session_id' in r2.text:
            #     return 6, 6, 6, 6, None
            # elif "auth_failure" in r2.text:
            #     return 3, 3, 3, 3, None
            # elif 'rate_limited' in r2.text:
            #     return 1, 1, 1, 1, None
            # elif 'multifactor' in r2.text:
            #     return 3, 3, 3, 3, None
            # elif 'cloudflare' in r2.text:
            #     return 5, 5, 5, 5, None
            if sys.platform == "win32":
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

            auth = RiotAuth()
            try:
                asyncio.run(auth.authorize(username,password))
            except RiotMultifactorError:
                return 3, 3, 3, 3, None
            except RiotRatelimitError:
                return 1, 1, 1, 1, None
            except RiotAuthError:
                return 3, 3, 3, 3, None
            token = auth.access_token
            entitlement = auth.entitlements_token
            data = auth.data2

            asyncio.run(auth.reauthorize())


            # headers = {
            #     'User-Agent': 'RiotClient/62.0.1.4852117.4789131 %s (Windows;10;;Professional, x64)',
            #     'Authorization': f'Bearer {token}',
            # }
            # try:
            #     with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}, proxies=proxy) as r:
            #         entitlement = r.json()['entitlements_token']
            #     r = session.post('https://auth.riotgames.com/userinfo',
            #                      headers=headers, json={}, proxies=proxy)
            # except:
            #     return 6, 6, 6, True, None
            # # print(r.text)
            # # input()
            # input(r.text)
            # data = r.json()
            # # print(data)
            # # input()
            puuid = data['sub']
            try:
                data2 = data['ban']
                # input(data2)
                data3 = data2['restrictions']
                # input(data3)
                typebanned = data3[0]['type']
                # input(typebanned)
                if typebanned == "PERMANENT_BAN" or typebanned == 'PERMA_BAN':
                    # input(True)
                    return 4, 4, 4, 4, None
                elif 'PERMANENT_BAN' in str(data3) or 'PERMA_BAN' in str(data3):
                    # input(True)
                    return 4, 4, 4, 4, None
                elif typebanned == 'TIME_BAN' or typebanned == 'LEGACY_BAN':
                    expire = data3[0]['dat']['expirationMillis']
                    expirepatched = pandas.to_datetime(int(expire), unit='ms')
                    # input(expire)
                    banuntil = expirepatched
                else:
                    banuntil = None
                    pass
            except Exception as e:
                # print(e)
                # input(e)
                banuntil = None
                pass
            try:
                # headers={
                #    'Authorization': f'Bearer {token}',
                #    'Content-Type': 'application/json',
                #    'User-Agent': 'RiotClient/62.0.1.4852117.4789131 %s (Windows;10;;Professional, x64)',
                # }

                # r=session.get('https://email-verification.riotgames.com/api/v1/account/status',headers=headers,json={},proxies=sys.getproxy(self.proxlist)).text

                # mailverif=r.split(',"emailVerified":')[1].split('}')[0]

                mailverif = bool(data['email_verified'])

            except Exception as e:
                # input(e)
                mailverif = True
            if mailverif == True:
                mailverif = False
            else:
                mailverif = True
            return token, entitlement, puuid, mailverif, banuntil
        except Exception as e:
            # input(e)
            # print(str(traceback.format_exc()))
            return 2, 2, 2, str(traceback.format_exc()), None
