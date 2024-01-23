import os
import traceback
from collections import OrderedDict
from re import compile
import ssl
from typing import Any
from tkinter import *
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter

from codeparts import systems
from codeparts.data import Constants
from codeparts.systems import Account

syst = systems.system()


class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *a: Any, **k: Any) -> None:
        c = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        c.set_ciphers(':'.join(Constants.CIPHERS))
        k['ssl_context'] = c
        return super(SSLAdapter, self).init_poolmanager(*a, **k)


class Auth:
    def __init__(self) -> None:
        path = os.getcwd()
        self.useragent = Constants.RIOTCLIENT

    def auth(self, logpass: str = None, username=None, password=None, proxy=None) -> Account:
        account = Account()
        try:
            account.logpass = logpass
            headers = OrderedDict({
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "application/json, text/plain, */*",
                'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)'
            })
            session = requests.Session()
            session.headers = headers
            session.mount('https://', SSLAdapter())
            if username is None:
                username, password = logpass.split(':')[0].strip(), logpass.split(':')[1].strip()

            data = {"acr_values": "urn:riot:bronze",
                    "claims": "",
                    "client_id": "riot-client",
                    "nonce": "oYnVwCSrlS5IHKh7iI16oQ",
                    "redirect_uri": "http://localhost/redirect",
                    "response_type": "token id_token",
                    "scope": "openid link ban lol_region"
                    }
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)'
            }
            r = session.post(Constants.AUTH_URL, json=data, headers=headers, proxies=proxy, timeout=20)
            r2 = session.put(Constants.AUTH_URL, json={"type": "auth", "username": username, "password": password},
                             headers=headers, proxies=proxy, timeout=20)

            data = r2.json()
            if "access_token" in r2.text:
                pattern = compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
                token, token_id, _ = pattern.findall(data['response']['parameters']['uri'])[0]
            elif any(error in r2.text for error in ['invalid_session_id', 'auth_failure', 'rate_limited', 'multifactor', 'cloudflare']):
                account.code = 6
                return account
            else:
                account.code = 3
                return account

            headers = {'User-Agent': f'RiotClient/{self.useragent} %s (Windows;10;;Professional, x64)',
                       'Authorization': f'Bearer {token}'}
            with session.post(Constants.ENTITLEMENT_URL, headers=headers, json={}, proxies=proxy) as r:
                entitlement = r.json().get('entitlements_token', '')
            r = session.post(Constants.USERINFO_URL, headers=headers, json={}, proxies=proxy)
            data = r.json()
            gamename, tagline, register_date, puuid = data['acct']['game_name'], data['acct']['tag_line'], data['acct']['created_at'], data['sub']

            try:
                data2 = data['ban']
                data3 = data2['restrictions']
                typebanned = data3[0]['type']
                if typebanned in ['PERMANENT_BAN', 'PERMA_BAN'] or 'PERMANENT_BAN' in str(data3) or 'PERMA_BAN' in str(data3):
                    account.code = 4
                    return account
                elif typebanned in ['TIME_BAN', 'LEGACY_BAN']:
                    expire = data3[0]['dat']['expirationMillis']
                    expirepatched = datetime.utcfromtimestamp(int(expire) / 1000.0)
                    banuntil = expirepatched
                else:
                    banuntil = None
            except Exception:
                banuntil = None

            try:
                mailverif = not bool(data['email_verified'])
            except Exception:
                mailverif = True

            account.token, account.tokenid, account.entt, account.puuid = token, token_id, entitlement, puuid
            account.unverifiedmail, account.banuntil, account.gamename = mailverif, banuntil, gamename
            account.tagline, account.registerdate = tagline, datetime.utcfromtimestamp(int(register_date) / 1000.0)
            return account
        except Exception as e:
            account.errmsg, account.code = str(traceback.format_exc()), 2
            return account
