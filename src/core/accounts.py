from pathlib import Path
import hashlib
from typing import Dict, List, Iterator, Any, Optional


class AccountHandler:
    def __init__(self, path: str):
        self.path = Path(path)
        self.accounts = self._process_file(self.path)

    def _process_file(self, path: Path) -> List[Dict[str, Any]]:
        if not path.exists():
            raise FileNotFoundError(f"Account file not found: {path}")
            
        content = path.read_text(encoding='utf-8')
        return [
            self._parse_line(line) 
            for line in content.splitlines() 
            if line.strip() and ":" in line
        ]

    def _parse_line(self, line: str) -> Dict[str, Any]:
        parts = line.strip().split(":", 1)
        
        if len(parts) != 2:
            raise ValueError(f"Invalid account format: {line}")
            
        user, pwd = parts
        
        return {
            "user": user.strip(),
            "pass": hashlib.sha3_256(pwd.encode()).hexdigest(),
            "region": "na",
            "attempts": 0,
            "created": self.path.stat().st_mtime
        }

    def stream_accounts(self, region_filter: Optional[str] = None) -> Iterator[Dict[str, Any]]:
        for acc in self.accounts:
            if not region_filter or acc["region"] == region_filter:
                yield acc
                
    def get_account_count(self, region_filter: Optional[str] = None) -> int:
        return sum(1 for _ in self.stream_accounts(region_filter))
        
    def add_account(self, username: str, password: str, region: str = "na") -> None:
        new_account = {
            "user": username,
            "pass": hashlib.sha3_256(password.encode()).hexdigest(),
            "region": region,
            "attempts": 0,
            "created": Path().stat().st_mtime
        }
        
        self.accounts.append(new_account)
        
    def save_accounts(self, output_path: Optional[str] = None) -> None:
        target_path = Path(output_path) if output_path else self.path
        
        with open(target_path, 'w', encoding='utf-8') as f:
            for acc in self.accounts:
                f.write(f"{acc['user']}:{acc['pass']}\n")
