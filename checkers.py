import requests
import system

sys=system.system()
sess=requests.Session()

class checkers():
    def skins_en(self,logpass):
        entitlement=sys.auth(logpass=logpass, response=2)
        token=sys.auth(logpass=logpass, response=1)
        puuid=sys.auth(logpass=logpass, response=3)

        if entitlement==False:
            return False

        heders ={
            "X-Riot-Entitlements-JWT": entitlement,
            "Authorization": f"Bearer {token}"
            }

        r = sess.get(f"https://pd.EU.a.pvp.net/store/v1/entitlements/{puuid}/e7c63390-eda7-46e0-bb7a-a6abdacd2433",headers=heders)
        Skins = r.json()["Entitlements"]
        response_API = requests.get('https://raw.githubusercontent.com/CSTCryst/Skin-Api/main/SkinList')
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

    def skins_ru(self,logpass):
        entitlement=sys.auth(logpass=logpass, response=2)
        token=sys.auth(logpass=logpass, response=1)
        puuid=sys.auth(logpass=logpass, response=3)

        if entitlement==False:
            return False

        heders ={
            "X-Riot-Entitlements-JWT": entitlement,
            "Authorization": f"Bearer {token}"
            }

        r = sess.get(f"https://pd.EU.a.pvp.net/store/v1/entitlements/{puuid}/e7c63390-eda7-46e0-bb7a-a6abdacd2433",headers=heders)
        Skins = r.json()["Entitlements"]
        response_API = requests.get('https://valorant-api.com/v1/weapons/skins/?language=ru-RU')
        data = response_API.json()
        skinstr=''
        for skin in Skins:
            skinid = skin['ItemID'].lower()
            for i in range(0,99999):
                id=data['data'][i]['uuid'].lower()
                for ii in range(0,20):
                    try:
                        style=data['data'][i]['chromas'][ii]['uuid'].lower()
                        if style == skinid:
                            if name in skinstr:
                                pass
                            else:
                                skinstr += name + "\n"
                            break
                    except:
                        break
                for ii in range(0,20):
                    try:
                        levels=data['data'][i]['levels'][ii]['uuid'].lower()
                        if levels == skinid:
                            if name in skinstr:
                                pass
                            else:
                                skinstr += name + "\n"
                            break
                    except:
                        break
                name = data['data'][i]['displayName']
                if id == skinid or style == skinid:
                    if name in skinstr:
                        pass
                    else:
                        skinstr += name + "\n"

        return skinstr