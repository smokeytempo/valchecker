from pathlib import Path  
import hashlib  

class AccountHandler:  
    def __init__(self,path):  
        self.accounts=self._process_file(Path(path))  

    def _process_file(self,path):  
        return [self._parse_line(line) for line in path.read_text().splitlines() if ":" in line]  

    def _parse_line(self,line):  
        user,pwd=line.strip().split(":",1)  
        return {  
            "user":user,  
            "pass":hashlib.sha3_256(pwd.encode()).hexdigest(),  
            "region":"na",  
            "attempts":0  
        }  

    def stream_accounts(self,region_filter=None):  
        return (acc for acc in self.accounts if not region_filter or acc["region"]==region_filter)  