import logging
import json
import time
from pathlib import Path
import hashlib
from typing import Dict, Any, Optional, Union
import os


class AuditLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True, parents=True)
        self.success_logger = self._create_logger("success")
        self.failure_logger = self._create_logger("failure")
        self.error_logger = self._create_logger("error")
        self.summary_logger = self._create_logger("summary", formatter="json")
        self.stats = {
            "started": int(time.time()),
            "valid": 0,
            "banned": 0,
            "rate_limited": 0,
            "errors": 0,
            "total": 0
        }

    def _create_logger(self, name: str, formatter: str = "line") -> logging.Logger:
        logger = logging.getLogger(f"audit.{name}")
        logger.setLevel(logging.INFO)
        logger.propagate = False
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        file_handler = logging.FileHandler(
            self.log_dir / f"{name}.log", 
            encoding="utf-8",
            mode="a"
        )
        
        if formatter == "json":
            file_handler.setFormatter(
                logging.Formatter("%(message)s")
            )
        else:
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s|%(message)s", 
                datefmt="%Y-%m-%d %H:%M:%S")
            )
            
        logger.addHandler(file_handler)
        return logger

    def record(self, result: Dict[str, Any]) -> None:
        self.stats["total"] += 1
        status = result.get("status", "error")
        self.stats[status] = self.stats.get(status, 0) + 1
        username = result.get("user", "unknown")
        proxy = result.get("proxy", "none")
        region = result.get("region", "unknown")
        latency = result.get("latency", 0)
        
        log_entry = f"{username}|{status}|{region}|{proxy}|{latency:.3f}"
        
        digest = hashlib.sha3_256(log_entry.encode()).hexdigest()
        full_entry = f"{log_entry}|{digest}"
        
        if status == "valid":
            self.success_logger.info(full_entry)
        else:
            self.failure_logger.info(full_entry)
            
        if self.stats["total"] % 10 == 0:
            self._update_summary()

    def record_error(self, error_message: str) -> None:
        self.stats["errors"] += 1
        self.error_logger.error(error_message)
        
    def _update_summary(self) -> None:
        elapsed = int(time.time()) - self.stats["started"]
        rate = self.stats["total"] / max(1, elapsed)
        
        summary = {
            "timestamp": int(time.time()),
            "elapsed_seconds": elapsed,
            "verification_rate": rate,
            "stats": {k: v for k, v in self.stats.items()}
        }
        
        self.summary_logger.info(json.dumps(summary))
        
    def finalize(self) -> Dict[str, Any]:
        self._update_summary()
        return dict(self.stats)
        
    def export_to_csv(self, output_file: Optional[str] = None) -> str:
        if not output_file:
            timestamp = int(time.time())
            output_file = self.log_dir / f"export_{timestamp}.csv"
        else:
            output_file = Path(output_file)
            
        success_log = self.log_dir / "success.log"
        
        with open(output_file, "w", encoding="utf-8") as f_out:
            f_out.write("timestamp,username,status,region,proxy,latency,hash\n")
            
            if success_log.exists():
                with open(success_log, "r", encoding="utf-8") as f_in:
                    for line in f_in:
                        if "|" in line:
                            timestamp, *parts = line.strip().split("|")
                            f_out.write(f"{timestamp},{','.join(parts)}\n")
                            
        return str(output_file)
