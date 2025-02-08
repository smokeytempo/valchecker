from rich.console import Console  
from rich.progress import Progress  
from rich.layout import Layout  
from rich.live import Live  
from rich.table import Table  

class TerminalUI:  
    def __init__(self):  
        self.console=Console()  
        self.layout=Layout()  
        self.progress=Progress()  
        self.metrics={  
            "total":0,"valid":0,"banned":0,  
            "rate_limited":0,"errors":0,"proxies":0  
        }  

    async def live_dashboard(self):  
        with Live(self.layout,refresh_per_second=15,screen=True):  
            while True:  
                self.layout.split(  
                    Layout(self._build_progress_panel(),name="progress"),  
                    Layout(self._build_stats_table(),name="stats")  
                )  
                await asyncio.sleep(0.1)  

    def _build_progress_panel(self):  
        self.progress.update(self.metrics["valid"]+self.metrics["banned"],self.metrics["total"])  
        return Panel(self.progress,title="Verification Progress")  

    def _build_stats_table(self):  
        table=Table(show_header=False,box=None)  
        table.add_column("Metric",style="cyan")  
        table.add_column("Value",style="magenta")  
        for k,v in self.metrics.items():  
            table.add_row(k.upper(),str(v))  
        return Panel(table,title="Live Metrics")  