import random
from datetime import datetime, timezone, timedelta

CST = timezone(timedelta(hours=8), "Asia/Shanghai")

FORTUNE_LEVELS = [
    (1, 10, "额……是百分制哦💦"),
    (11, 30, "运气略显卡顿，建议重启一下自己~"),
    (31, 50, "平淡如白开水的一天，平平淡淡才是真~"),
    (51, 70, "运气不错哦！适合试试抽卡或者告白！✨"),
    (71, 90, "今日锦鲤附体！做什么都会顺风顺水！🐟"),
    (91, 100, "欧皇降世！你就是今天的天选之人！👑"),
]

FORTUNE_WEIGHTS = [1, 3, 4, 4, 3, 1]
FORTUNE_RANGES = [(1, 10), (11, 30), (31, 50), (51, 70), (71, 90), (91, 100)]


def generate_fortune(user_id: str) -> tuple:
    utc_8 = datetime.now(CST)
    date_str = utc_8.strftime("%Y%m%d")
    userseed = hash(date_str + user_id)
    rng = random.Random(userseed)

    selected_range = rng.choices(FORTUNE_RANGES, weights=FORTUNE_WEIGHTS, k=1)[0]
    rp = rng.randint(selected_range[0], selected_range[1])

    description = next(
        desc for low, high, desc in FORTUNE_LEVELS if low <= rp <= high
    )

    if rp == 100:
        description = "等一下，100？！？！天选之子啊！"

    return rp, description
