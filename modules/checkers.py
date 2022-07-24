import requests
from modules import systems

sys=systems.system()
sess=requests.Session()

class checkers():
    def skins_en(self,entitlement,token,puuid,region='EU'):
        try:

            if entitlement==False:
                return False

            headers ={
                "X-Riot-Entitlements-JWT": entitlement,
                "Authorization": f"Bearer {token}"
                }

            r = sess.get(f"https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/e7c63390-eda7-46e0-bb7a-a6abdacd2433",headers=headers)
            Skins = r.json()["Entitlements"]
            response_API = requests.get('https://lil-jaba.github.io/valskins/skinlist.html')
            response=response_API.text
            skinsList = response.splitlines()
            skinstr=''
            for skin in Skins:
                skinid = skin['ItemID']
                for item in skinsList:
                    details = item.split("|")
                    namepart=details[0]
                    idpart=details[1]
                    id = idpart.split(":")[0].lower()
                    name = namepart.split(":")[1].split(' Level')[0]
                    if id == skinid:
                        if name in skinstr:
                            pass
                        else:
                            skinstr += name + "\n"

            return skinstr
        except:
            return 'err'

    def skins_ru(self,entitlement,token,puuid,region='EU'):
        try:

            if entitlement==False:
                return False

            headers ={
                "X-Riot-Entitlements-JWT": entitlement,
                "Authorization": f"Bearer {token}"
                }

            r = sess.get(f"https://pd.{region}.a.pvp.net/store/v1/entitlements/{puuid}/e7c63390-eda7-46e0-bb7a-a6abdacd2433",headers=headers)
            Skins = r.json()["Entitlements"]
            response_API = requests.get('https://valorant-api.com/v1/weapons/skins/?language=ru-RU')
            skinstr=''
            for skin in Skins:
                skinid = skin['ItemID'].lower()
                response=response_API.text
                skin=response.split(skinid)[1].split(',')[1].replace('"displayName":"','').replace('\\"','').replace('"','').replace('u00A0','').replace("'",'').split(' уровень')[0]
                if skin in skinstr:
                    pass
                else:
                    skinstr += skin + "\n"

            return skinstr
        except:
            return 'err'

    def ranked(self,entitlement,token,puuid,region='EU'):
        try:

            if entitlement==False:
                return False
            RankIDtoRank = {"0":"Unranked","1":"", "2":"" ,"3":"Iron 1" ,"4":"Iron 2" ,"5":"Iron 3" ,\
"6":"Bronze 1" ,"7":"Bronze 2" ,"8":"Bronze 3" ,"9":"Silver 1" ,"10":"Silver 2", "11":"Silver 3" ,"12":"Gold 1" ,\
"13":"Gold 2" ,"14":"Gold 3" ,"15":"Platinum 1" ,"16":"Platinum 2" ,"17":"Plantinum 3" ,"18":"Diamond 1" ,"19":"Diamond 2"\
,"20":"Diamond 3" ,"21":"Ascendant 1" ,"22":"Ascendant 2" ,"23":"Ascendant 3" ,"24":"Immortal 1","25":"Immortal 2","26"\
:"Immortal 3","27":"Radiant"}
            headers = {"Content-Type": "application/json","Authorization": \
f"Bearer {token}","X-Riot-Entitlements-JWT": entitlement,"X-Riot-ClientVersion": \
"release-01.08-shipping-10-471230","X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cG\
UiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4\
wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9"}
            ranked = sess.get(f"https://pd.{region}.a.pvp.net/mmr/v1/players/{puuid}/competitiveupdates",headers=headers)
            if '","Matches":[]}' in ranked.text:
                rank = "UnRanked"
            else:
                rankid = ranked.text.split('"TierAfterUpdate":')[1].split(',"')[0]
                rank = RankIDtoRank[rankid]
            return rank
        except:
            return 'err'

            
    def lastplayed(self,puuid,region='eu'):
        try:

            if puuid==False:
                return False
            resp=requests.get(f'https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{region}/'+puuid.replace(' ',''))
            data=resp.json()
            lastmatch=data['data'][0]['metadata']['game_start_patched']
            return lastmatch
        except:
            return 'err'