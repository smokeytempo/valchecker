import requests
import urllib3

BASE = "https://localhost:7680"
TESTURI = "/token/test"
CHECKURI = "/entry"

class AntiPublic:
    def __init__(self, token:str, session:str) -> None:
        urllib3.disable_warnings()
        self.token = token
        self.session = session

    def test(self) -> bool:
        try:
            with requests.get(BASE+TESTURI, headers={"Authorization": "Bearer "+ self.token}, verify=False) as r:
                return r.status_code == 200
        except:
            return False
    
    def check(self, logpass:str) -> bool:
        with requests.post(BASE+CHECKURI, headers={"Authorization": "Bearer "+ self.token, "Session": self.session}, data=logpass, verify=False) as r:
            return r.json()['result']