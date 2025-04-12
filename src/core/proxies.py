import random
from typing import List, Dict, Set, Optional

class ProxyEngine:
    def __init__(self, proxies: List[str]):
        self.proxies = proxies
        self.index = 0
        self.blacklist: Set[str] = set()
        self.current: Optional[str] = None
        
        if not proxies:
            raise ValueError("No proxies provided")

    def next(self) -> Dict[str, str]:
        attempts = 0
        max_attempts = len(self.proxies)
        
        while attempts < max_attempts:
            proxy = self.proxies[self.index]
            self.index = (self.index + 1) % len(self.proxies)
            
            if proxy not in self.blacklist:
                self.current = proxy
                return {"http://": proxy, "https://": proxy}
                
            attempts += 1
            
        self.blacklist.clear()
        self.current = self.proxies[0]
        return {"http://": self.proxies[0], "https://": self.proxies[0]}

    def cycle(self) -> None:
        if self.current:
            self.blacklist.add(self.current)
        
        available = [p for p in self.proxies if p not in self.blacklist]
        if available:
            self.index = self.proxies.index(random.choice(available))
        else:
            self.index = random.randint(0, len(self.proxies) - 1)

    def health_check(self) -> None:
        self.proxies = [p for p in self.proxies if p not in self.blacklist]
        self.blacklist.clear()
        
        if not self.proxies:
            raise RuntimeError("All proxies have been blacklisted and removed")
