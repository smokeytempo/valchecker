import asyncio
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Dict, Any, Optional


class TerminalUI:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()
        
        self.progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            TextColumn("[bold green]{task.completed}/{task.total}"),
            TimeElapsedColumn()
        )
        
        self.verification_task = self.progress.add_task("Verification", total=0)
        
        self.metrics = {
            "total": 0,
            "valid": 0,
            "banned": 0,
            "rate_limited": 0,
            "errors": 0,
            "proxies": 0,
            "completed": 0
        }
        
        self.status_colors = {
            "valid": "green",
            "banned": "red",
            "rate_limited": "yellow",
            "errors": "red",
            "proxies": "cyan",
            "total": "blue",
            "completed": "magenta"
        }

    async def live_dashboard(self) -> None:
        with Live(self.layout, refresh_per_second=15, screen=True) as live:
            while True:
                self.layout.split(
                    Layout(self._build_progress_panel(), name="progress", size=10),
                    Layout(self._build_stats_table(), name="stats", size=15),
                    Layout(self._build_rate_panel(), name="rate", size=5),
                )
                await asyncio.sleep(0.1)

    def _build_progress_panel(self) -> Panel:
        completed = self.metrics.get("completed", 0)
        total = self.metrics.get("total", 0)
        
        self.progress.update(
            self.verification_task, 
            completed=completed,
            total=total
        )
        
        return Panel(
            self.progress,
            title="[bold cyan]Verification Progress",
            border_style="cyan"
        )

    def _build_stats_table(self) -> Panel:
        table = Table(show_header=True, box=True, expand=True)
        table.add_column("Metric", style="cyan", justify="right")
        table.add_column("Value", style="magenta", justify="center")
        table.add_column("Percentage", style="yellow", justify="left")
        
        total = max(1, self.metrics.get("total", 1))
        
        for key, value in self.metrics.items():
            if key in ("completed", "total", "proxies"):
                continue
                
            color = self.status_colors.get(key, "white")
            percentage = f"{(value / total) * 100:.1f}%" if value > 0 else "0.0%"
            
            table.add_row(
                Text(key.upper(), style=f"bold {color}"),
                Text(str(value), style=color),
                Text(percentage, style=color)
            )
            
        return Panel(
            table,
            title="[bold yellow]Verification Metrics",
            border_style="yellow"
        )
        
    def _build_rate_panel(self) -> Panel:
        completed = self.metrics.get("completed", 0)
        proxies = self.metrics.get("proxies", 0)
        
        table = Table(show_header=False, box=False, expand=True)
        table.add_column("Key", style="cyan", justify="right")
        table.add_column("Value", style="green", justify="left")
        
        table.add_row("Completed", f"{completed}")
        table.add_row("Active Proxies", f"{proxies}")
        
        if completed > 0:
            success_rate = (self.metrics.get("valid", 0) / completed) * 100
            table.add_row(
                "Success Rate", 
                Text(f"{success_rate:.1f}%", 
                style="green" if success_rate > 50 else "yellow" if success_rate > 25 else "red")
            )
        
        return Panel(
            table,
            title="[bold green]Summary",
            border_style="green"
        )

    def update_metrics(self, key: str, value: Optional[int] = None, increment: bool = False) -> None:
        if increment:
            self.metrics[key] = self.metrics.get(key, 0) + 1
        elif value is not None:
            self.metrics[key] = value
