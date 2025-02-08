import asyncio  
import yaml  
from src.core import APIClient,AccountHandler,ProxyEngine  
from src.interface import TerminalUI  
from src.utils import AuditLogger  

async def main():  
    config=yaml.safe_load(open("config/settings.yaml"))  
    ui=TerminalUI()  
    accounts=AccountHandler("data/accounts.txt")  
    proxies=ProxyEngine(open("data/proxies.txt").read().splitlines())  
    logger=AuditLogger()  

    async with APIClient(proxies) as api:  
        ui_task=asyncio.create_task(ui.live_dashboard())  
        verification_tasks=[  
            api.verify_account(acc)  
            for acc in accounts.stream_accounts(config["target_region"])  
        ]  

        for future in asyncio.as_completed(verification_tasks):  
            result=await future  
            logger.record(result)  
            ui.metrics[result["status"]]+=1  
            ui.metrics["total"]=len(verification_tasks)  
            ui.metrics["proxies"]=len(proxies.proxies)  

        ui_task.cancel()  

if __name__=="__main__":  
    asyncio.run(main())  