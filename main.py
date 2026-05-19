import sys
import os
import random
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, StarTools, register
from astrbot.api import logger

from jrrp import generate_fortune
from tarot import draw_spread, format_spread_result

CST = timezone(timedelta(hours=8), "Asia/Shanghai")

DISCLAIMER = "\n\n仅供娱乐，请勿当真\n请不要因此摔手机砸电脑等~"


class DailyTarotRecord:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_today(self) -> str:
        return datetime.now(CST).strftime("%Y%m%d")

    def _get_path(self, user_id: str, spread_type: str) -> Path:
        return self.data_dir / f"{self._get_today()}_{user_id}_{spread_type}.json"

    def save(self, user_id: str, spread_type: str, result: dict):
        path = self._get_path(user_id, spread_type)
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

    def load(self, user_id: str, spread_type: str) -> Optional[dict]:
        path = self._get_path(user_id, spread_type)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def has_drawn(self, user_id: str, spread_type: str) -> bool:
        return self._get_path(user_id, spread_type).exists()


@register(
    "jrrp_plus",
    "Ni-ShuWu",
    "今日人品 & 塔罗牌占卜插件。支持 /jrrp, /tarot, /tarot3, /tarot_celtic, /daily 等命令。每种塔罗牌阵每天独立限抽一次。",
    "2.2.1",
    "https://github.com/Ni-ShuWu/astrbot_plugin_jrrp_plus",
)
class JrrpPlusPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        data_dir = StarTools.get_data_dir("jrrp_plus")
        self.tarot_record = DailyTarotRecord(data_dir)
        logger.info(f"今日人品+ 插件已加载，数据目录: {data_dir}")

    @filter.command("jrrp")
    async def jrrp(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        user_id = event.get_sender_id()
        rp, description = generate_fortune(user_id)

        yield event.plain_result(
            f"✨ {user_name} 的今日人品 ✨\n"
            f"人品值：{rp}/100\n"
            f"{description}"
            f"{DISCLAIMER}"
        )

    @filter.command("tarot")
    async def tarot(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        cached = self.tarot_record.load(user_id, "single")
        if cached:
            text = (
                "你今天已经抽过单张塔罗牌了，这是今天的指引：\n"
                f"{format_spread_result(cached)}"
                f"{DISCLAIMER}"
            )
            yield event.plain_result(text)
            return

        rng = random.Random()
        result = draw_spread("single", rng)
        self.tarot_record.save(user_id, "single", result)
        yield event.plain_result(format_spread_result(result) + DISCLAIMER)

    @filter.command("tarot3")
    async def tarot3(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        cached = self.tarot_record.load(user_id, "three")
        if cached:
            text = (
                "你今天已经抽过三牌阵了，这是今天的牌面：\n"
                f"{format_spread_result(cached)}"
                f"{DISCLAIMER}"
            )
            yield event.plain_result(text)
            return

        rng = random.Random()
        result = draw_spread("three", rng)
        self.tarot_record.save(user_id, "three", result)
        yield event.plain_result(format_spread_result(result) + DISCLAIMER)

    @filter.command("tarot_celtic")
    async def tarot_celtic(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        cached = self.tarot_record.load(user_id, "celtic_cross")
        if cached:
            text = (
                "你今天已经抽过凯尔特十字阵了，这是今天的牌面：\n"
                f"{format_spread_result(cached)}"
                f"{DISCLAIMER}"
            )
            yield event.plain_result(text)
            return

        rng = random.Random()
        result = draw_spread("celtic_cross", rng)
        self.tarot_record.save(user_id, "celtic_cross", result)
        yield event.plain_result(format_spread_result(result) + DISCLAIMER)

    @filter.command("daily")
    async def daily(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        user_id = event.get_sender_id()

        rp, description = generate_fortune(user_id)
        fortune_text = (
            f"✨ {user_name} 的今日人品 ✨\n"
            f"人品值：{rp}/100\n"
            f"{description}"
        )

        cached = self.tarot_record.load(user_id, "single")
        if cached:
            tarot_text = (
                f"\n\n━━━ 今日塔罗指引（已抽取）━━━\n"
                f"{format_spread_result(cached)}"
            )
        else:
            rng = random.Random()
            result = draw_spread("single", rng)
            self.tarot_record.save(user_id, "single", result)
            tarot_text = (
                f"\n\n━━━ 今日塔罗指引 ━━━\n"
                f"{format_spread_result(result)}"
            )

        yield event.plain_result(fortune_text + tarot_text + DISCLAIMER)

    async def terminate(self):
        pass
