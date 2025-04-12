import asyncio
import yaml
import sys
from pathlib import Path
from typing import Dict, Any, List
from contextlib import AsyncExitStack

from src.core import APIClient, AccountHandler, ProxyEngine
from src.interface import TerminalUI
from src.utils import AuditLogger

async def main() -> None:
    try:
        config_path = Path("config/settings.yaml")
        if not config_path.exists():
            print(f"Error: Configuration file not found at {config_path}")
            sys.exit(1)
            
        with open(config_path) as f:
            config = yaml.safe_load(f)
            
        accounts_path = Path("data/accounts.txt")
        proxies_path = Path("data/proxies.txt")
        
        if not accounts_path.exists() or not proxies_path.exists():
            print("Error: Required data files not found")
            sys.exit(1)
            
        ui = TerminalUI()
        accounts = AccountHandler(str(accounts_path))
        
        with open(proxies_path) as f:
            proxy_list = [line.strip() for line in f if line.strip()]
            
        if not proxy_list:
            print("Error: No valid proxies found")
            sys.exit(1)
            
        proxies = ProxyEngine(proxy_list)
        logger = AuditLogger()
        
        async with AsyncExitStack() as stack:
            api = await stack.enter_async_context(APIClient(proxies))
            ui_task = asyncio.create_task(ui.live_dashboard())
            
            target_region = config.get("target_region", "na")
            account_stream = accounts.stream_accounts(target_region)
            verification_tasks: List[asyncio.Task] = [
                asyncio.create_task(api.verify_account(acc)) 
                for acc in account_stream
            ]
            
            if not verification_tasks:
                print("Error: No accounts to verify")
                ui_task.cancel()
                sys.exit(0)
                
            ui.metrics["total"] = len(verification_tasks)
            ui.metrics["proxies"] = len(proxies.proxies)
            
            results: List[Dict[str, Any]] = []
            for future in asyncio.as_completed(verification_tasks):
                try:
                    result = await future
                    results.append(result)
                    logger.record(result)
                    
                    ui.metrics[result["status"]] = ui.metrics.get(result["status"], 0) + 1
                    ui.metrics["completed"] = len(results)
                    
                    if len(results) % 50 == 0:
                        proxies.health_check()
                        ui.metrics["proxies"] = len(proxies.proxies)
                        
                except Exception as e:
                    ui.metrics["errors"] = ui.metrics.get("errors", 0) + 1
                    logger.record_error(str(e))
            
            await asyncio.sleep(0.5)
            ui_task.cancel()
            
            try:
                await ui_task
            except asyncio.CancelledError:
                pass
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
