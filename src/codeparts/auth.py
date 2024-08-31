import os
from re import compile
import ssl
import traceback
from typing import Any
from datetime import datetime, timedelta
import base64

import json
import sys
import asyncio
from requests.adapters import HTTPAdapter
import httpx

from . import systems
from .data import Constants
from .systems import Account

syst = systems.system()

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
elif sys.platform == 'linux':
    asyncio.set_event_loop_policy(asyncio.DefaultEventLoopPolicy())
elif sys.platform == 'darwin':
    asyncio.set_event_loop_policy(asyncio.SelectorEventLoopPolicy())


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *a: Any, **k: Any) -> None:
        c = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        c.set_ciphers(':'.join(Constants.CIPHERS))
        k['ssl_context'] = c
        return super(SSLAdapter, self).init_poolmanager(*a, **k)


class Auth():
    def __init__(self, isDebug: bool = False) -> None:
        self.isDebug = bool(isDebug)
        path = str(os.getcwd())
        self.useragent = Constants.RIOTCLIENT
        self.parentpath = str(os.path.abspath(os.path.join(path, os.pardir)))

    async def auth(self, logpass: str = None, username: str = None, password: str = None, proxy=None) -> Account:
        account = Account()
        try:
            account.logpass = logpass
            sslcontext = httpx.create_ssl_context()
            sslcontext.set_ciphers(Constants.CIPHERS)
            sslcontext.set_ecdh_curve(Constants.ECDH_CURVE)
            client = httpx.Client(verify=sslcontext, proxy=proxy["http"] if proxy is not None else None)
            if username is None:
                username = logpass.split(':')[0].strip()
                password = logpass.split(':')[1].strip()

            try:
                # R1
                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)"
                        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.1502.79 Mobile"
                        " Safari/537.36"
                    ),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate"
                }
                body = {
                    "acr_values": "",
                    "claims": "",
                    "client_id": "riot-client",
                    "code_challenge": "",
                    "code_challenge_method": "",
                    "nonce": "SYXugqaAL5z7U7iioaTW5Q",
                    "redirect_uri": "http://localhost/redirect",
                    "response_type": "token id_token",
                    "scope": "openid link ban lol_region account email_verified locale region",
                }

                r = client.post(Constants.AUTH_URL, json=body, headers=headers)
                debugvalue_raw = r.text
                if self.isDebug:
                    print(debugvalue_raw)


                # R2
                data = {
                    "type": "auth",
                    "username": username,
                    "password": password,
                    "remember": True,
                }
                # HUGE thanks to https://github.com/sandbox-pokhara/league-client
                headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X)"
                        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.1502.79 Mobile"
                        " Safari/537.36"
                    ),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate",
                    "referer":"https://riotgames.com/"
                }
                r = client.put(Constants.AUTH_URL, json=data, headers=headers)
                body = r.text
                #input(body)
                if self.isDebug:
                    print(body)
                data = r.json()
                r2text = r.text
            except Exception as e:
                client.close()
                if self.isDebug:
                    print(e)
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

            headers = dict({
                'User-Agent': str(f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)'),
                'Authorization': str(f'Bearer {token}'),
            })
            try:
                r = client.post(Constants.ENTITLEMENT_URL, headers=headers, json={})
                entitlement = r.json()['entitlements_token']
                r = client.post(Constants.USERINFO_URL,
                                 headers=headers, json={})
            except Exception as _e:
                #print(_e)
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
            registerdatepatched = datetime.fromtimestamp(
                int(register_date) / 1000.0)
            puuid = data['sub']
            try:
                # input(data)
                data2 = data['ban']
                # input(data2)
                data3 = data2['restrictions']
                # input(data3)
                if len(data3) == 0:
                    banuntil = None
                else:
                    typebanned = data3[0]['type']
                    if typebanned == "PERMANENT_BAN" or typebanned == 'PERMA_BAN':
                        account.code = int(4)
                        banuntil = None
                    elif 'PERMANENT_BAN' in str(data3) or 'PERMA_BAN' in str(data3):
                        account.code = int(4)
                        banuntil = None
                    elif typebanned == 'TIME_BAN' or typebanned == 'LEGACY_BAN':
                        expire = data3[0]['dat']['expirationMillis']
                        expirepatched = datetime.fromtimestamp(
                            int(expire) / 1000.0)
                        if expirepatched > datetime.now() + timedelta(days=365 * 20):
                            account.code = 4
                        banuntil = expirepatched
                    else:
                        banuntil = None
                        pass
            except Exception as _e:
                # print(Exception)
                # input(_e)
                banuntil = None
                pass
            try:
                # headers= dict({
                #    'Authorization': f'Bearer {token}',
                #    'Content-Type': 'application/json',
                #    'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)',
                # })

                # r=session.get('https://email-verification.riotgames.com/api/v1/account/status',headers=headers,json={},proxies=sys.getproxy(self.proxlist)).text

                # mailverif=r.split(',"emailVerified":')[1].split('}')[0]
                # print(data)
                mailverif = bool(data['email_verified'])

            except Exception:
                # input(Exception)
                mailverif = True
            account.tokenid = token_id
            account.token = token
            account.entt = entitlement
            account.puuid = puuid
            account.unverifiedmail = not mailverif
            account.banuntil = banuntil
            account.gamename = gamename
            account.tagline = tagline
            account.registerdate = registerdatepatched
            if self.isDebug:
                print(puuid)
                print(entitlement+"\n-------")
                print(token+"\n-------")
                print(token_id)
                input()
            client.close()
            return account
        except Exception as _e:
            #input(_e)
            account.errmsg = traceback.format_exc()
            account.code = int(2)
            return account

    async def decode(self, account:Account) -> bool:
        # thanks nummy :3
        parts = account.token.split(".")
        if len(parts) != 3:
            return False
        payload = parts[1]
        payload += "=" * ((4 - len(payload) % 4) % 4)
        decoded = base64.urlsafe_b64decode(payload)
        account.decodedtoken = json.loads(decoded)
        return True