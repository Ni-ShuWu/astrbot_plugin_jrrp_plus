from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, StarTools, register
from astrbot.api import logger

from jrrp import generate_fortune
from tarot import draw_spread, format_spread_result
from data import DailyTarotRecord

import random

DISCLAIMER = "\n\n仅供娱乐，请勿当真\n请不要因此摔手机砸电脑等~"


@register(
    "jrrp_plus",
    "Ni-ShuWu",
    "今日人品 & 塔罗牌占卜插件。支持 /jrrp, /tarot, /tarot3, /tarot_celtic, /daily 等命令。",
    "2.2.0",
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
        cached = self.tarot_record.load(user_id)
        if cached:
            text = (
                "你已经抽过今天的塔罗牌了，这是你今天的指引：\n"
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
        cached = self.tarot_record.load(user_id)
        if cached:
            text = (
                "你今天已经抽过塔罗牌了，这是你今天的牌面：\n"
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
        cached = self.tarot_record.load(user_id)
        if cached:
            text = (
                "你今天已经抽过塔罗牌了，这是你今天的牌面：\n"
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

        cached = self.tarot_record.load(user_id)
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
