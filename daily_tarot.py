import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

CST = timezone(timedelta(hours=8), "Asia/Shanghai")


class DailyTarotRecord:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_today(self) -> str:
        return datetime.now(CST).strftime("%Y%m%d")

    def _get_path(self, user_id: str) -> Path:
        return self.data_dir / f"{self._get_today()}_{user_id}.json"

    def save(self, user_id: str, spread_type: str, result: dict):
        path = self._get_path(user_id)
        data = {
            "date": self._get_today(),
            "spread_type": spread_type,
            "spread_name": result["spread_name"],
            "cards": result["cards"],
            "positions_desc": result.get("positions_desc", ""),
            "timestamp": datetime.now(CST).isoformat(),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, user_id: str) -> Optional[dict]:
        path = self._get_path(user_id)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def has_drawn(self, user_id: str) -> bool:
        return self._get_path(user_id).exists()
