from collections import OrderedDict
from re import compile
import re
from ssl import PROTOCOL_TLSv1_2
from tkinter import *
import traceback
import pandas
import asyncio
import http,http.client
import sys

from requests import session as sesh,exceptions
import requests
from requests.adapters import HTTPAdapter
import urllib3.exceptions
from urllib3 import PoolManager

from codeparts import systems
from codeparts import riot_auth
from codeparts.riot_auth import auth_exceptions,auth

sys=systems.system()

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections, maxsize=maxsize, block=block,
                                       ssl_version=PROTOCOL_TLSv1_2)

class auth():
    def __init__(self) -> None:
        pass

    def auth(self,logpass=None,username=None,password=None,proxy=None):
        try:
            if username ==None:
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
            session.mount('http://', TLSAdapter())
            #data = {
            #    "acr_values": "urn:riot:bronze",
            #    "claims": "",
            #    "client_id": "riot-client",
            #    "nonce": "oYnVwCSrlS5IHKh7iI16oQ",
            #    "redirect_uri": "http://localhost/redirect",
            #    "response_type": "token id_token",
            #    "scope": "openid link ban lol_region",
            #}
            #headers = {
            #    'Content-Type': 'application/json',
            #    'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)'
            #}
            #try:
            #    r = session.post(f'https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers,proxies=proxy,timeout=20)
            #    data = {
            #        'type': 'auth',
            #        'username': username,
            #        'password': password
            #    }
            #    r2 = session.put('https://auth.riotgames.com/api/v1/authorization', json=data, headers=headers,proxies=proxy,timeout=20)
            #    input(r2.text)
            ##except requests.exceptions.ConnectTimeout:
            ##    return 6,6,6,True,None
            ##except requests.exceptions.ProxyError:
            ##    return 6,6,6,True,None
            ##except urllib3.exceptions.MaxRetryError:
            ##    return 6,6,6,True,None
            ##except http.client.RemoteDisconnected:
            ##    return 6,6,6,True,None
            ##except urllib3.exceptions.ConnectTimeoutError:
            ##    return 6,6,6,True,None
            ##except urllib3.exceptions.TimeoutError:
            ##    return 6,6,6,True,None
            #except Exception as e:
            #    input(e)
            #    return 6,6,6,True,None
            ##print(r2.text)
            #try:
            #    data = r2.json()
            #except:
            #    return 6,6,6,6,None
            #if "access_token" in r2.text:
            #    pattern = compile(
            #        'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
            #    data = pattern.findall(data['response']['parameters']['uri'])[0]
            #    token = data[0]
            #    token_id=data[1]
#
            #elif 'invalid_session_id' in r2.text:
            #    return 6,6,6,6,None
            #elif "auth_failure" in r2.text:
            #    return 3,3,3,3,None
            #elif 'rate_limited' in r2.text:
            #    return 1,1,1,1,None
            #elif 'multifactor' in r2.text:
            #    return 3,3,3,3,None
            #elif 'cloudflare' in r2.text:
            #    return 5,5,5,5,None
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            try:
                auth = riot_auth.RiotAuth(proxy)
                asyncio.run(auth.authorize(username,password))
            except riot_auth.RiotRatelimitError: return 1,1,1,1,None
            except riot_auth.RiotAuthenticationError: return 3,3,3,3,None
            except riot_auth.RiotMultifactorError: return 3,3,3,3,None
            except riot_auth.RiotAuthError: return 3,3,3,3,None
            token=auth.access_token
            #respauth=asyncio.run(auth.reauthorize())
            #input(respauth)

            #headers = {
            #    'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
            #    'Authorization': f'Bearer {token}'
            #}
            #try:
            #    r = session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={},proxies=proxy)
            #    input(r.text)
            #    entitlement = r.json()['entitlements_token']
            #    r = session.post('https://auth.riotgames.com/userinfo', headers=headers, json={},proxies=proxy)
            #except:
            #    return 6,6,6,True,None
            #print(r.text)
            #input()
            entitlement=auth.entitlements_token
            #print(data)
            #input()
            data=auth.data2
            #input(data)
            puuid = data['sub']
            try:
                data2=data['ban']
                #input(data2)
                data3 = data2['restrictions']
                #input(data3)
                typebanned = data3[0]['type']
                #input(typebanned)
                if typebanned == "PERMANENT_BAN" or typebanned=='PERMA_BAN':
                    #input(True)
                    return 4,4,4,4,None
                elif 'PERMANENT_BAN' in str(data3) or 'PERMA_BAN' in str(data3):
                    #input(True)
                    return 4,4,4,4,None
                elif typebanned=='TIME_BAN' or typebanned=='LEGACY_BAN':
                    expire=data3[0]['dat']['expirationMillis']
                    expirepatched = pandas.to_datetime(int(expire),unit='ms')
                    #input(expire)
                    banuntil=expirepatched
                else:
                    banuntil=None
                    pass
            except Exception as e:
                #print(e)
                #input(e)
                banuntil=None
                pass
            try:
                #headers={
                #    'Authorization': f'Bearer {token}',
                #    'Content-Type': 'application/json',
                #    'User-Agent': 'RiotClient/51.0.0.4429735.4381201 rso-auth (Windows;10;;Professional, x64)',
                #}

                #r=session.get('https://email-verification.riotgames.com/api/v1/account/status',headers=headers,json={},proxies=sys.getproxy(self.proxlist)).text

                #mailverif=r.split(',"emailVerified":')[1].split('}')[0]

                mailverif=bool(data['email_verified'])

            except Exception as e:
                #input(e)
                mailverif=True
            if mailverif==True:
                mailverif=False
            else:
                mailverif=True
            return token,entitlement,puuid,mailverif,banuntil
        except Exception as e:
            #input(e)
            #print(str(traceback.format_exc()))
            return 2,2,2,str(traceback.format_exc()),None
