import os
from collections import OrderedDict
from re import compile
import ssl
import traceback
from typing import Any
from tkinter import *
from datetime import datetime, timedelta

import sys
import asyncio
import requests
from requests.adapters import HTTPAdapter

from . import systems
from .data import Constants
from .systems import Account
from .authclient import AuthClient

syst = systems.system()

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *a: Any, **k: Any) -> None:
        c = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        c.set_ciphers(':'.join(Constants.CIPHERS))
        k['ssl_context'] = c
        return super(SSLAdapter, self).init_poolmanager(*a, **k)


class Auth():
    def __init__(self, isDebug = False) -> None:
        self.isDebug = isDebug
        path = os.getcwd()
        self.useragent = Constants.RIOTCLIENT
        self.parentpath = os.path.abspath(os.path.join(path, os.pardir))

    async def auth(self, logpass: str = None, username=None, password=None, proxy=None) -> Account:
        account = Account()
        try:
            account.logpass = logpass
            session = requests.Session()
            ac = AuthClient()
            authsession = await ac.createSession()
            if username is None:
                username = logpass.split(':')[0].strip()
                password = logpass.split(':')[1].strip()

            try:
                # R1
                headers = {
                    "Accept-Encoding": "deflate, gzip, zstd",
                    "user-agent": "dsadasdasdasds",
                    "Cache-Control": "no-cache",
                    "Accept": "application/json",
                }
                body = {
                    "acr_values": "",
                    "claims": "",
                    "client_id": "riot-client",
                    "code_challenge": "",
                    "code_challenge_method": "",
                    "nonce": "dsadasdasdasdasd",
                    "redirect_uri": "http://localhost/redirect",
                    "response_type": "token id_token",
                    "scope": "openid link ban lol_region account",
                }
                async with authsession.post(
                    Constants.AUTH_URL,
                    json=body,
                    headers=headers,
                    proxy = proxy["http"] if proxy != None else None
                ) as r:
                    raw = await r.text()
                    #input(raw)

                # R2
                data = {
                    'type': 'auth',
                    'username': username,
                    'password': password
                }
                async with authsession.put(
                    Constants.AUTH_URL,
                    json=data,
                    headers=headers,
                    proxy = proxy["http"] if proxy != None else None
                ) as r:
                    try:
                        data = await r.json()
                    except:
                        account.code = 6
                        await authsession.close()
                        return account
                    r2text = await r.text()                
                await authsession.close()
            except Exception as e:
                #input(e)
                #input(traceback.format_exc())
                await authsession.close()
                if self.isDebug:
                    input(traceback.format_exc())
                account.code = 6
                return account
            if "access_token" in r2text:
                pattern = compile(
                    'access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
                data = pattern.findall(
                    data['response']['parameters']['uri'])[0]
                token = data[0]
                token_id = data[1]

            elif 'invalid_session_id' in r2text:
                account.code = 6
                return account
            elif "auth_failure" in r2text:
                account.code = 3
                return account
            elif 'rate_limited' in r2text:
                account.code = 1
                return account
            elif 'multifactor' in r2text:
                account.code = 3
                return account
            elif 'cloudflare' in r2text:
                account.code = 5
                return account
            else:
                account.code = 3
                return account

            headers = {
                'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)',
                'Authorization': f'Bearer {token}',
            }
            try:
                with session.post(Constants.ENTITLEMENT_URL, headers=headers, json={}, proxies=proxy) as r:
                    entitlement = r.json()['entitlements_token']
                r = session.post(Constants.USERINFO_URL,
                                 headers=headers, json={}, proxies=proxy)
            except:
                account.code = 6
                return account
            # print(r.text)
            # input()
            # input(r.text)
            data = r.json()
            # print(data)
            # input()
            gamename = data['acct']['game_name']
            tagline = data['acct']['tag_line']
            register_date = data['acct']['created_at']
            registerdatepatched = datetime.utcfromtimestamp(
                int(register_date) / 1000.0)
            puuid = data['sub']
            try:
                # input(data)
                data2 = data['ban']
                # input(data2)
                data3 = data2['restrictions']
                # input(data3)
                typebanned = data3[0]['type']
                # input(typebanned)
                # input(typebanned)
                if typebanned == "PERMANENT_BAN" or typebanned == 'PERMA_BAN':
                    account.code = 4
                    return account
                elif 'PERMANENT_BAN' in str(data3) or 'PERMA_BAN' in str(data3):
                    # input(True)
                    account.code = 4
                    return account
                elif typebanned == 'TIME_BAN' or typebanned == 'LEGACY_BAN':
                    expire = data3[0]['dat']['expirationMillis']
                    expirepatched = datetime.utcfromtimestamp(
                        int(expire) / 1000.0)
                    if expirepatched > datetime.now() + timedelta(days=365 * 20):
                        account.code = 4
                        return account
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
                #    'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)',
                # }

                # r=session.get('https://email-verification.riotgames.com/api/v1/account/status',headers=headers,json={},proxies=sys.getproxy(self.proxlist)).text

                # mailverif=r.split(',"emailVerified":')[1].split('}')[0]

                mailverif = bool(data['email_verified'])

            except Exception as e:
                # input(e)
                mailverif = True
            mailverif = not mailverif
            account.tokenid = token_id
            account.token = token
            account.entt = entitlement
            account.puuid = puuid
            account.unverifiedmail = mailverif
            account.banuntil = banuntil
            account.gamename = gamename
            account.tagline = tagline
            account.registerdate = registerdatepatched
            if self.isDebug:
                print(puuid)
                print(entitlement+"\n-------")
                print(token)
                input()
            return account
        except Exception as e:
            input(e)
            account.errmsg = str(traceback.format_exc())
            account.code = 2
            return account
