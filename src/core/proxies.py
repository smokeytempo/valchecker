import random  
import asyncio  

class ProxyEngine:  
    def __init__(self,proxies):  
        self.proxies=proxies  
        self.index=0  
        self.blacklist=set()  

    def next(self):  
        while True:  
            proxy=self.proxies[self.index]  
            self.index=(self.index+1)%len(self.proxies)  
            if proxy not in self.blacklist:  
                return {"http://":proxy,"https://":proxy}  

    def cycle(self):  
        self.blacklist.add(self.proxies[self.index])  
        self.index=random.randint(0,len(self.proxies)-1)  

    def health_check(self):  
        self.proxies=[p for p in self.proxies if p not in self.blacklist]  
        self.blacklist.clear()  