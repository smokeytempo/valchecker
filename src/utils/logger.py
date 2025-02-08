import logging  
from pathlib import Path  
import hashlib  

class AuditLogger:  
    def __init__(self):  
        Path("logs").mkdir(exist_ok=True)  
        self.success=logging.getLogger("success")  
        self.failure=logging.getLogger("failure")  
        self._configure_handlers()  

    def _configure_handlers(self):  
        success_handler=logging.FileHandler("logs/success.log",encoding="utf-8")  
        failure_handler=logging.FileHandler("logs/failed.log",encoding="utf-8")  
        success_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))  
        failure_handler.setFormatter(logging.Formatter("%(asctime)s|%(message)s"))  
        self.success.addHandler(success_handler)  
        self.failure.addHandler(failure_handler)  

    def record(self,result):  
        log_entry=f"{result['user']}|{result['status']}|{result['proxy']}"  
        digest=hashlib.sha3_256(log_entry.encode()).hexdigest()  
        if result["status"]=="valid":  
            self.success.info(f"{log_entry}|{digest}")  
        else:  
            self.failure.info(f"{log_entry}|{digest}")  