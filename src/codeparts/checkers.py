import json
import os
import requests
import pandas

from codeparts.data import Constants

sess=requests.Session()

class checkers():
    def __init__(self) -> None:
        path = os.getcwd()
        self.parentpath=os.path.abspath(os.path.join(path, os.pardir))

    def skins_en(self,entitlement,token,puuid,region='EU') -> str:
        if region.lower()=='latam' or region.lower()=='br':
            region='na'
        try:

            if entitlement==False:
                return False

            headers ={
                "X-Riot-Entitlements-JWT": entitlement,
                "Authorization": f"Bearer {token}"
                }

            r = sess.get(f"https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/e7c63390-eda7-46e0-bb7a-a6abdacd2433",headers=headers)
            #input(r.text)
            Skins = r.json()["Entitlements"]
            with open(f'{self.parentpath}\\src\\assets\\skins.json','r',encoding='utf-8') as f:
                response=f.read()
            skinstr=''
            for skin in Skins:
                try:
                    skinid = skin['ItemID'].lower()
                    skin=response.split(skinid)[1].split('"displayName": "')[1].split('",')[0].replace('"displayName":"','').replace('\\"','').replace('"','').replace('u00A0','').replace("'",'').split(' Level')[0]
                    #input(skin)
                    if skin not in skinstr:
                        skinstr += skin + "\n"
                        
                except:
                    pass

            return skinstr
        except Exception as e:
            #input(e)
            return 'err'

    def balance(self,ent,token,puuid,region) -> int:
        if region.lower()=='latam' or region.lower()=='br':
            region='na'
        headers = {"Content-Type": "application/json",
                            "Authorization": f"Bearer {token}",
                            "X-Riot-Entitlements-JWT": ent,
                    }
        try:
            r = requests.get(f"https://pd.{region}.a.pvp.net/store/v1/wallet/{puuid}",headers=headers)

            vp = int(r.json()["Balances"]["85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741"])
            rp = int(r.json()["Balances"]["e59aa87c-4cbf-517a-5983-6e81511be9b7"])
        except:
            vp = 'N/A'
            rp = 'N/A'
        return vp,rp

    def ranked(self,entitlement,token,puuid,region='EU') -> str:
        if region.lower()=='latam' or region.lower()=='br':
            region='na'
        try:

            if entitlement==False:
                return False
            RankIDtoRank = {"0":"Unranked","1":"", "2":"" ,"3":"Iron 1" ,"4":"Iron 2" ,"5":"Iron 3" ,\
"6":"Bronze 1" ,"7":"Bronze 2" ,"8":"Bronze 3" ,"9":"Silver 1" ,"10":"Silver 2", "11":"Silver 3" ,"12":"Gold 1" ,\
"13":"Gold 2" ,"14":"Gold 3" ,"15":"Platinum 1" ,"16":"Platinum 2" ,"17":"Platinum 3" ,"18":"Diamond 1" ,"19":"Diamond 2"\
,"20":"Diamond 3" ,"21":"Ascendant 1" ,"22":"Ascendant 2" ,"23":"Ascendant 3" ,"24":"Immortal 1","25":"Immortal 2","26"\
:"Immortal 3","27":"Radiant"}
            headers = {"Content-Type": "application/json","Authorization": \
f"Bearer {token}","X-Riot-Entitlements-JWT": entitlement,"X-Riot-ClientVersion": \
"release-01.08-shipping-10-471230","X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cG\
UiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4\
wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"}
            ranked = sess.get(f"https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates",headers=headers)
            #input(ranked.text)
            if '","Matches":[]}' in ranked.text:
                rank = "UnRanked"
            else:
                rankid = ranked.text.split('"TierAfterUpdate":')[1].split(',"')[0]
                rank = RankIDtoRank[rankid]
            return rank
        except:
            return 'err'

            
    def lastplayed(self,uuid,region,token,ent):
        if region.lower()=='latam' or region.lower()=='br':
            region='na'
        try:
            headers={"Content-Type": "application/json",
                            "Authorization": f"Bearer {token}",
                            "X-Riot-Entitlements-JWT": ent,
                            "X-Riot-ClientVersion": "release-01.08-shipping-10-471230",
                            "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"
            }
            r = requests.get(f"https://pd.{region}.a.pvp.net/match-history/v1/history/{uuid}?startIndex=0&endIndex=10",headers=headers)
            data = r.json()
            data2 = data["History"]
            for x in data2:
                data3 = x['GameStartTime']
            unix_time1 = data3
            unix_time1 = int(unix_time1)
            result_s2 = pandas.to_datetime(unix_time1,unit='ms')
            time=str(result_s2)
        except:
            time = "N/A"
        return time

    def skinprice(self,skin:str):
        try:
            price=Constants.skinprice[skin]
        except:
            price=0
        return price