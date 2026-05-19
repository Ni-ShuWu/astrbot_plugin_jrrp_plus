import random
import json
from pathlib import Path
from typing import Optional

ALL_MAJOR_ARCANA = [
    {"id": 0, "name": "愚者", "suit": "大阿尔卡纳", "meaning_up": "新的开始，冒险，天真", "meaning_reverse": "鲁莽，风险，犹豫不决"},
    {"id": 1, "name": "魔术师", "suit": "大阿尔卡纳", "meaning_up": "创造力，技能，意志力", "meaning_reverse": "未利用的才能，沟通不畅"},
    {"id": 2, "name": "女祭司", "suit": "大阿尔卡纳", "meaning_up": "直觉，第六感，天启", "meaning_reverse": "粗心大意，易紧张，神经质"},
    {"id": 3, "name": "女皇", "suit": "大阿尔卡纳", "meaning_up": "丰收，母爱，创造力", "meaning_reverse": "过度保护，自私，失去创造力"},
    {"id": 4, "name": "皇帝", "suit": "大阿尔卡纳", "meaning_up": "权威，结构，控制", "meaning_reverse": "僵化，顽固，失去控制"},
    {"id": 5, "name": "教皇", "suit": "大阿尔卡纳", "meaning_up": "传统，信仰，教育", "meaning_reverse": "反叛，打破常规"},
    {"id": 6, "name": "恋人", "suit": "大阿尔卡纳", "meaning_up": "爱情，选择，关系", "meaning_reverse": "冲突，分离，错误选择"},
    {"id": 7, "name": "战车", "suit": "大阿尔卡纳", "meaning_up": "胜利，控制，意志力", "meaning_reverse": "缺乏方向，冲突，失控"},
    {"id": 8, "name": "力量", "suit": "大阿尔卡纳", "meaning_up": "勇气，耐心，内在力量", "meaning_reverse": "软弱，怀疑，失去信心"},
    {"id": 9, "name": "隐士", "suit": "大阿尔卡纳", "meaning_up": "内省，寻求，智慧", "meaning_reverse": "孤立，逃避，拒绝建议"},
    {"id": 10, "name": "命运之轮", "suit": "大阿尔卡纳", "meaning_up": "转折点，命运，机会", "meaning_reverse": "坏运气，抵抗变化"},
    {"id": 11, "name": "正义", "suit": "大阿尔卡纳", "meaning_up": "公正，真理，因果", "meaning_reverse": "不公正，偏见，欺骗"},
    {"id": 12, "name": "倒吊人", "suit": "大阿尔卡纳", "meaning_up": "牺牲，等待，新视角", "meaning_reverse": "停滞，不必要的牺牲"},
    {"id": 13, "name": "死神", "suit": "大阿尔卡纳", "meaning_up": "结束，转变，新生", "meaning_reverse": "抗拒变化，停滞"},
    {"id": 14, "name": "节制", "suit": "大阿尔卡纳", "meaning_up": "平衡，调和，耐心", "meaning_reverse": "不平衡，极端"},
    {"id": 15, "name": "恶魔", "suit": "大阿尔卡纳", "meaning_up": "束缚，欲望，物质", "meaning_reverse": "解脱，释放"},
    {"id": 16, "name": "高塔", "suit": "大阿尔卡纳", "meaning_up": "突变，灾难，启示", "meaning_reverse": "避免灾难，害怕改变"},
    {"id": 17, "name": "星星", "suit": "大阿尔卡纳", "meaning_up": "希望，灵感，宁静", "meaning_reverse": "绝望，失望"},
    {"id": 18, "name": "月亮", "suit": "大阿尔卡纳", "meaning_up": "潜意识，梦境，直觉", "meaning_reverse": "恐惧消退，清晰"},
    {"id": 19, "name": "太阳", "suit": "大阿尔卡纳", "meaning_up": "快乐，成功，活力", "meaning_reverse": "暂时挫折，过度自信"},
    {"id": 20, "name": "审判", "suit": "大阿尔卡纳", "meaning_up": "觉醒，重生，反思", "meaning_reverse": "怀疑，害怕改变"},
    {"id": 21, "name": "世界", "suit": "大阿尔卡纳", "meaning_up": "完成，成就，整合", "meaning_reverse": "未完成，延迟"},
]

_MINOR_TEMPLATES = [
    # (suit, name_display, meaning_up, meaning_reverse)
    # 权杖 (Wands) — 火元素，行动/事业/热情
    ("权杖", "权杖Ace", "创造力的开端，灵感的火花", "计划延迟，缺乏动力"),
    ("权杖", "权杖二", "未来的规划，勇敢的决策", "犹豫不决，害怕改变"),
    ("权杖", "权杖三", "远见卓识，探索未知", "挫折阻碍，延误时机"),
    ("权杖", "权杖四", "庆祝和谐，稳定基础", "不安于室，缺乏满足感"),
    ("权杖", "权杖五", "竞争冲突，激烈角逐", "逃避冲突，息事宁人"),
    ("权杖", "权杖六", "胜利凯旋，公众认可", "骄傲自满，潜藏失败"),
    ("权杖", "权杖七", "坚守阵地，迎接挑战", "不堪重负，轻言放弃"),
    ("权杖", "权杖八", "飞速发展，行动力强", "急躁冒进，失序混乱"),
    ("权杖", "权杖九", "坚韧不拔，最后的坚持", "固执己见，筋疲力尽"),
    ("权杖", "权杖十", "承担重任，压力山大", "崩溃边缘，无法承受"),
    ("权杖", "权杖侍从", "探索热情，新的消息", "缺乏经验，不成熟"),
    ("权杖", "权杖骑士", "勇往直前，冒险精神", "冲动鲁莽，横冲直撞"),
    ("权杖", "权杖王后", "温暖坚定，充满魅力", "依赖心强，善妒易怒"),
    ("权杖", "权杖国王", "领导才能，创业精神", "傲慢专横，控制欲强"),
    # 圣杯 (Cups) — 水元素，情感/关系/直觉
    ("圣杯", "圣杯Ace", "爱的萌芽，情感的丰盈", "情感空虚，内心压抑"),
    ("圣杯", "圣杯二", "心意相通，和谐联结", "关系破裂，误解分歧"),
    ("圣杯", "圣杯三", "欢庆友谊，快乐聚会", "过度放纵，乐极生悲"),
    ("圣杯", "圣杯四", "沉思内省，不满现状", "新的机会，即将觉醒"),
    ("圣杯", "圣杯五", "失落悲伤，追悔莫及", "接受现实，重新开始"),
    ("圣杯", "圣杯六", "美好回忆，纯真怀旧", "停滞不前，活在过去"),
    ("圣杯", "圣杯七", "幻想选择，内心投射", "看清现实，回归理性"),
    ("圣杯", "圣杯八", "勇敢放下，追寻真谛", "逃避问题，恐惧未知"),
    ("圣杯", "圣杯九", "心愿满足，幸福安康", "贪得无厌，内心空虚"),
    ("圣杯", "圣杯十", "美满家庭，幸福圆满", "家庭矛盾，和谐破裂"),
    ("圣杯", "圣杯侍从", "直觉灵敏，灵感涌现", "幼稚天真，逃避现实"),
    ("圣杯", "圣杯骑士", "浪漫追求，温柔告白", "情感泛滥，嫉妒不安"),
    ("圣杯", "圣杯王后", "温柔慈爱，善解人意", "过度依赖，情感勒索"),
    ("圣杯", "圣杯国王", "成熟稳重，富有同理心", "情绪化，冷漠疏离"),
    # 宝剑 (Swords) — 风元素，思维/冲突/正义
    ("宝剑", "宝剑Ace", "思维清晰，真理显现", "思维混乱，误解重重"),
    ("宝剑", "宝剑二", "理性抉择，权衡利弊", "自欺欺人，拒绝面对"),
    ("宝剑", "宝剑三", "心碎痛苦，悲伤煎熬", "伤痛愈合，释怀放下"),
    ("宝剑", "宝剑四", "休养生息，静心沉思", "停滞不前，拒绝休息"),
    ("宝剑", "宝剑五", "冲突败北，名誉受损", "和解放下，既往不咎"),
    ("宝剑", "宝剑六", "渡过难关，平静过渡", "抗拒改变，陷入困境"),
    ("宝剑", "宝剑七", "谋略计划，灵活应变", "内疚不安，欺骗隐瞒"),
    ("宝剑", "宝剑八", "自我束缚，思维局限", "挣脱枷锁，重获自由"),
    ("宝剑", "宝剑九", "焦虑失眠，噩梦缠身", "放下执念，重见希望"),
    ("宝剑", "宝剑十", "痛苦终结，绝望低谷", "涅槃重生，新的开始"),
    ("宝剑", "宝剑侍从", "警觉敏锐，善于沟通", "轻率八卦，言语伤人"),
    ("宝剑", "宝剑骑士", "果断行动，雷厉风行", "冲动攻击，不留余地"),
    ("宝剑", "宝剑王后", "独立思考，理性冷静", "尖酸刻薄，悲伤孤独"),
    ("宝剑", "宝剑国王", "理智分析，公正决断", "冷酷无情，独断专行"),
    # 星币 (Pentacles) — 土元素，物质/工作/健康
    ("星币", "星币Ace", "财富机遇，物质繁荣", "错失良机，贪心不足"),
    ("星币", "星币二", "灵活平衡，适应变化", "顾此失彼，财务紧张"),
    ("星币", "星币三", "团队合作，技能精进", "质量低劣，缺乏规划"),
    ("星币", "星币四", "储蓄积累，财务稳定", "吝啬守财，过度控制"),
    ("星币", "星币五", "经济困难，精神匮乏", "走出困境，重燃希望"),
    ("星币", "星币六", "慷慨给予，乐于分享", "接受施舍，依赖他人"),
    ("星币", "星币七", "耐心等待，评估成果", "分散精力，徒劳无功"),
    ("星币", "星币八", "勤奋工作，精益求精", "完美主义，盲目投入"),
    ("星币", "星币九", "自给自足，自律成就", "过度工作，身心俱疲"),
    ("星币", "星币十", "财富传承，家族昌盛", "家庭纷争，财产损失"),
    ("星币", "星币侍从", "学习实践，踏实肯干", "懒惰懈怠，好高骛远"),
    ("星币", "星币骑士", "踏实可靠，务实负责", "固执僵化，缺乏远见"),
    ("星币", "星币王后", "丰饶富足，务实稳重", "物质主义，忽视情感"),
    ("星币", "星币国王", "事业有成，理财有道", "贪婪腐败，唯利是图"),
]

ALL_MINOR_ARCANA = []
_next_id = 22
for suit, name, up, rev in _MINOR_TEMPLATES:
    ALL_MINOR_ARCANA.append({
        "id": _next_id,
        "name": name,
        "suit": suit,
        "meaning_up": up,
        "meaning_reverse": rev,
    })
    _next_id += 1

ALL_TAROT_CARDS = ALL_MAJOR_ARCANA + ALL_MINOR_ARCANA

_ALL_CARDS_BY_ID = {c["id"]: c for c in ALL_TAROT_CARDS}


def pick_tarot(random_source: random.Random) -> tuple:
    card = random_source.choice(ALL_TAROT_CARDS)
    is_reverse = random_source.random() < 0.3
    orientation = "逆位" if is_reverse else "正位"
    meaning = card["meaning_reverse"] if is_reverse else card["meaning_up"]
    return card, orientation, meaning


def format_tarot_card(card: dict, orientation: str, meaning: str) -> str:
    suit_tag = f"[{card['suit']}]"
    return f"🃏 {card['name']} {suit_tag}（{orientation}）\n   寓意：{meaning}"


def draw_spread(spread_name: str, random_source: random.Random) -> dict:
    spread_name = spread_name.lower()

    spreads = {
        "single": _spread_single,
        "three": _spread_three,
        "celtic_cross": _spread_celtic_cross,
    }

    func = spreads.get(spread_name, _spread_single)
    return func(random_source)


def format_spread_result(spread_result: dict) -> str:
    spread_name = spread_result["spread_name"]
    cards_info = spread_result["cards"]
    positions_desc = spread_result.get("positions_desc", "")

    lines = [f"🔮 {spread_name} 🔮"]
    if positions_desc:
        lines.append(positions_desc)
        lines.append("")

    for item in cards_info:
        lines.append(f"【{item['position']}】")
        lines.append(f"  🃏 {item['card']['name']} [{item['card']['suit']}]（{item['orientation']}）")
        lines.append(f"    寓意：{item['meaning']}")

    return "\n".join(lines)


def _pick_one(rng: random.Random, pool: Optional[list] = None) -> dict:
    cards = pool if pool is not None else ALL_TAROT_CARDS
    card = rng.choice(cards)
    is_reverse = rng.random() < 0.3
    return {
        "card": card,
        "orientation": "逆位" if is_reverse else "正位",
        "meaning": card["meaning_reverse"] if is_reverse else card["meaning_up"],
    }


def _spread_single(rng: random.Random) -> dict:
    info = _pick_one(rng)
    info["position"] = "今日指引"
    return {
        "spread_name": "单张牌占卜",
        "cards": [info],
        "positions_desc": "一张牌揭示你今日的整体能量。",
    }


def _spread_three(rng: random.Random) -> dict:
    indices = rng.sample(range(len(ALL_TAROT_CARDS)), 3)
    positions = ["过去", "现在", "未来"]
    cards_info = []
    for idx, pos in zip(indices, positions):
        card = ALL_TAROT_CARDS[idx]
        is_reverse = rng.random() < 0.3
        cards_info.append({
            "position": pos,
            "card": card,
            "orientation": "逆位" if is_reverse else "正位",
            "meaning": card["meaning_reverse"] if is_reverse else card["meaning_up"],
        })
    return {
        "spread_name": "三牌阵（过去·现在·未来）",
        "cards": cards_info,
        "positions_desc": "三张牌分别对应你的过去、现在与未来。",
    }


def _spread_celtic_cross(rng: random.Random) -> dict:
    indices = rng.sample(range(len(ALL_TAROT_CARDS)), 10)
    positions = [
        "现状", "挑战", "目标", "基础", "过去",
        "未来", "自我", "环境", "希望与恐惧", "最终结果",
    ]
    cards_info = []
    for idx, pos in zip(indices, positions):
        card = ALL_TAROT_CARDS[idx]
        is_reverse = rng.random() < 0.3
        cards_info.append({
            "position": pos,
            "card": card,
            "orientation": "逆位" if is_reverse else "正位",
            "meaning": card["meaning_reverse"] if is_reverse else card["meaning_up"],
        })
    return {
        "spread_name": "凯尔特十字阵",
        "cards": cards_info,
        "positions_desc": "经典十张牌阵，全面剖析你当下的处境。",
    }
