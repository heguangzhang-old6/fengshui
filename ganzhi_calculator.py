# -*- coding: utf-8 -*-
"""
八字计算核心模块 (ganzhi_calculator)
=====================================
【模块说明】
本模块提供八字四柱（年柱/月柱/日柱/时柱）的核心计算功能，支持传统八字和连续时柱两种模式。

【核心功能】
1. 传统八字计算：按传统规则，时柱每天根据日干重新开始
2. 连续时柱八字：时柱随时间连续变化，天干地支各自循环

【版本信息】
- 版本：v3.1（修复版）
- 适配Python版本：3.6+
- 最后更新：2026-02-01
"""

import datetime

# -------------------------- 基础配置 --------------------------
TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

WUHU_DUN = {
    '甲': '丙', '乙': '戊', '丙': '庚', '丁': '壬', '戊': '甲',
    '己': '丙', '庚': '戊', '辛': '庚', '壬': '壬', '癸': '甲'
}

WUSHU_DUN = {
    '甲': '甲', '乙': '丙', '丙': '戊', '丁': '庚', '戊': '壬',
    '己': '甲', '庚': '丙', '辛': '戊', '壬': '庚', '癸': '壬'
}

MONTH_JIEQI_MAP = {
    '子': ('大雪', '小寒'), '丑': ('小寒', '立春'), '寅': ('立春', '惊蛰'),
    '卯': ('惊蛰', '清明'), '辰': ('清明', '立夏'), '巳': ('立夏', '芒种'),
    '午': ('芒种', '小暑'), '未': ('小暑', '立秋'), '申': ('立秋', '白露'),
    '酉': ('白露', '寒露'), '戌': ('寒露', '立冬'), '亥': ('立冬', '大雪')
}

JIEQI_RULE = {
    '大雪': {'month': 12, 'day': 7}, '小寒': {'month': 1, 'day': 5},  # 修正：小寒通常为1月5-6日
    '立春': {'month': 2, 'day': 4},  # 统一用2月4日，闰年处理在函数内
    '惊蛰': {'month': 3, 'day': 5},  # 修正：惊蛰通常为3月5-6日
    '清明': {'month': 4, 'day': 4},  # 修正：清明通常为4月4-5日
    '立夏': {'month': 5, 'day': 5}, '芒种': {'month': 6, 'day': 5},
    '小暑': {'month': 7, 'day': 7}, '立秋': {'month': 8, 'day': 7},
    '白露': {'month': 9, 'day': 7}, '寒露': {'month': 10, 'day': 8},
    '立冬': {'month': 11, 'day': 7}
}

BASE_DATE_DAY = datetime.date(1901, 1, 1)
BASE_DAY_GAN = 5
BASE_DAY_ZHI = 3

HOUR_DIZHI_MAP = {
    23: '子', 0: '子', 1: '丑', 2: '丑', 3: '寅', 4: '寅',
    5: '卯', 6: '卯', 7: '辰', 8: '辰', 9: '巳', 10: '巳',
    11: '午', 12: '午', 13: '未', 14: '未', 15: '申', 16: '申',
    17: '酉', 18: '酉', 19: '戌', 20: '戌', 21: '亥', 22: '亥'
}


# -------------------------- 工具函数 --------------------------
def _get_jieqi_date(target_year: int, jieqi_name: str) -> datetime.date:
    """获取节气日期（内部函数，简化版本）"""
    rule = JIEQI_RULE[jieqi_name]
    month = rule['month']
    base_day = rule['day']

    # 简化的节气计算：1900-2100年节气日期变化不大
    # 在实际应用中，可以替换为更精确的节气计算
    if jieqi_name == '立春':
        # 立春：2月4日左右
        return datetime.date(target_year, 2, 4)
    elif jieqi_name == '惊蛰':
        # 惊蛰：3月5日左右
        return datetime.date(target_year, 3, 5)
    elif jieqi_name == '清明':
        # 清明：4月4日左右
        return datetime.date(target_year, 4, 4)
    elif jieqi_name == '小寒':
        # 小寒：1月5日左右
        return datetime.date(target_year, 1, 5)
    else:
        return datetime.date(target_year, month, base_day)


# -------------------------- 核心计算函数 --------------------------
def get_year_ganzhi(input_date: datetime.date) -> str:
    """计算年柱干支（立春为界）"""
    target_year = input_date.year
    # 简化：立春固定为2月4日
    lichun_date = datetime.date(target_year, 2, 4)

    # 确定年柱归属年份
    calc_year = target_year - 1 if input_date < lichun_date else target_year
    # 计算年干支索引
    year_gan_idx = (calc_year - 4) % 10
    year_dz_idx = (calc_year - 4) % 12

    return TIANGAN[year_gan_idx] + DIZHI[year_dz_idx]


def get_month_ganzhi(input_date: datetime.date, year_gan: str) -> str:
    """计算月柱干支（简化版本）"""
    # 简化的月份地支映射（基于节气日期固定）
    month = input_date.month
    day = input_date.day

    # 月份地支映射（简化为固定日期）
    if month == 12 and day >= 7:  # 大雪后
        month_dz = '子'
    elif month == 1 and day < 6:  # 小寒前
        month_dz = '子'
    elif month == 1 and day >= 6:  # 小寒后
        month_dz = '丑'
    elif month == 2 and day < 4:  # 立春前
        month_dz = '丑'
    elif month == 2 and day >= 4:  # 立春后
        month_dz = '寅'
    elif month == 3 and day < 5:  # 惊蛰前
        month_dz = '寅'
    elif month == 3 and day >= 5:  # 惊蛰后
        month_dz = '卯'
    elif month == 4 and day < 4:  # 清明前
        month_dz = '卯'
    elif month == 4 and day >= 4:  # 清明后
        month_dz = '辰'
    elif month == 5 and day < 5:  # 立夏前
        month_dz = '辰'
    elif month == 5 and day >= 5:  # 立夏后
        month_dz = '巳'
    elif month == 6 and day < 6:  # 芒种前
        month_dz = '巳'
    elif month == 6 and day >= 6:  # 芒种后
        month_dz = '午'
    elif month == 7 and day < 7:  # 小暑前
        month_dz = '午'
    elif month == 7 and day >= 7:  # 小暑后
        month_dz = '未'
    elif month == 8 and day < 7:  # 立秋前
        month_dz = '未'
    elif month == 8 and day >= 7:  # 立秋后
        month_dz = '申'
    elif month == 9 and day < 7:  # 白露前
        month_dz = '申'
    elif month == 9 and day >= 7:  # 白露后
        month_dz = '酉'
    elif month == 10 and day < 8:  # 寒露前
        month_dz = '酉'
    elif month == 10 and day >= 8:  # 寒露后
        month_dz = '戌'
    elif month == 11 and day < 7:  # 立冬前
        month_dz = '戌'
    elif month == 11 and day >= 7:  # 立冬后
        month_dz = '亥'
    else:
        month_dz = '子'  # 默认

    # 五虎遁定月干
    yin_month_gan = WUHU_DUN[year_gan]
    yin_idx = DIZHI.index('寅')
    curr_idx = DIZHI.index(month_dz)
    offset = (curr_idx - yin_idx) % 12

    yin_gan_idx = TIANGAN.index(yin_month_gan)
    month_gan_idx = (yin_gan_idx + offset) % 10
    month_gan = TIANGAN[month_gan_idx]

    return month_gan + month_dz


def get_day_ganzhi(input_date: datetime.date) -> str:
    """计算日柱干支"""
    delta_days = (input_date - BASE_DATE_DAY).days
    day_gan_idx = (BASE_DAY_GAN + delta_days) % 10
    day_dz_idx = (BASE_DAY_ZHI + delta_days) % 12
    return TIANGAN[day_gan_idx] + DIZHI[day_dz_idx]


def get_hour_ganzhi_traditional(input_hour: int, day_gan: str) -> str:
    """传统时柱计算（五鼠遁）"""
    if input_hour not in HOUR_DIZHI_MAP:
        raise ValueError(f"小时数{input_hour}超出0-23范围")
    hour_dz = HOUR_DIZHI_MAP[input_hour]

    zi_hour_gan = WUSHU_DUN[day_gan]
    zi_idx = DIZHI.index('子')
    curr_idx = DIZHI.index(hour_dz)
    offset = (curr_idx - zi_idx) % 12

    zi_gan_idx = TIANGAN.index(zi_hour_gan)
    hour_gan_idx = (zi_gan_idx + offset) % 10
    hour_gan = TIANGAN[hour_gan_idx]

    return hour_gan + hour_dz


def get_hour_ganzhi_continuous(start_datetime: datetime.datetime, target_datetime: datetime.datetime) -> str:
    """连续时柱计算（天干地支各自连续）"""
    # 获取起始时间的传统时柱
    start_date = start_datetime.date()
    start_hour = start_datetime.hour

    # 获取起始时间的日柱
    start_day_gz = get_day_ganzhi(start_date)
    start_day_gan = start_day_gz[0]

    # 计算起始时间的时柱（正确处理23:00）
    if start_hour == 23:
        # 23:00属于第二天的子时
        next_day = start_date + datetime.timedelta(days=1)
        next_day_gz = get_day_ganzhi(next_day)
        start_hour_gz = get_hour_ganzhi_traditional(23, next_day_gz[0])
    else:
        start_hour_gz = get_hour_ganzhi_traditional(start_hour, start_day_gan)

    # 计算时间差（小时）
    time_diff_hours = (target_datetime - start_datetime).total_seconds() / 3600

    # 计算时辰差（每2小时一个时辰）
    hour_diff = int(time_diff_hours / 2)

    # 起始时柱的天干地支索引
    start_hour_gan = start_hour_gz[0]
    start_hour_zhi = start_hour_gz[1]
    start_gan_idx = TIANGAN.index(start_hour_gan)
    start_zhi_idx = DIZHI.index(start_hour_zhi)

    # 计算目标时柱索引
    target_gan_idx = (start_gan_idx + hour_diff) % 10
    target_zhi_idx = (start_zhi_idx + hour_diff) % 12

    return TIANGAN[target_gan_idx] + DIZHI[target_zhi_idx]


# -------------------------- 主要接口函数 --------------------------
def get_traditional_bazi(input_year: int, input_month: int, input_day: int, input_hour: int = 0) -> tuple:
    """
    计算传统八字

    参数：
        input_year: int - 公历年（1900-2100）
        input_month: int - 公历月（1-12）
        input_day: int - 公历日（1-31）
        input_hour: int - 24小时制小时数（0-23，默认0）

    返回：
        tuple - (年干支, 月干支, 日干支, 时干支)
    """
    # 基础校验
    if not (1900 <= input_year <= 2100):
        raise ValueError("仅支持1900-2100年的日期计算")

    input_date = datetime.date(input_year, input_month, input_day)

    # 计算年柱、月柱、日柱
    year_gz = get_year_ganzhi(input_date)
    month_gz = get_month_ganzhi(input_date, year_gz[0])
    day_gz = get_day_ganzhi(input_date)

    # 处理23:00的特殊情况
    if input_hour == 23:
        # 23:00属于第二天的子时
        next_day = input_date + datetime.timedelta(days=1)
        next_day_gz = get_day_ganzhi(next_day)
        hour_gz = get_hour_ganzhi_traditional(input_hour, next_day_gz[0])
    else:
        hour_gz = get_hour_ganzhi_traditional(input_hour, day_gz[0])

    return year_gz, month_gz, day_gz, hour_gz


def get_continuous_bazi(start_datetime: datetime.datetime, target_datetime: datetime.datetime) -> tuple:
    """
    计算连续时柱八字

    参数：
        start_datetime: datetime.datetime - 参考起始时间点
        target_datetime: datetime.datetime - 目标时间点

    返回：
        tuple - (年干支, 月干支, 日干支, 时干支)
    """
    target_date = target_datetime.date()

    # 计算年柱、月柱、日柱
    year_gz = get_year_ganzhi(target_date)
    month_gz = get_month_ganzhi(target_date, year_gz[0])
    day_gz = get_day_ganzhi(target_date)

    # 计算连续时柱
    hour_gz = get_hour_ganzhi_continuous(start_datetime, target_datetime)

    return year_gz, month_gz, day_gz, hour_gz


# -------------------------- 模块自测 --------------------------
if __name__ == "__main__":
    print("=== 八字计算模块自测 ===")

    # 测试关键点
    print("\n关键点测试:")

    # 1. 2026-01-24 15:00
    print("1. 2026-01-24 15:00:")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 1, 24, 15)
    print(f"  八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"  预期：乙巳 己丑 戊戌 庚申")

    # 2. 节气切换测试
    print("\n2. 节气切换测试:")
    print("  a) 2026-03-05 15:00 (惊蛰前):")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 3, 5, 15)
    print(f"    八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"    预期：丙午 己丑 戊申 庚申")

    print("  b) 2026-03-06 15:00 (惊蛰后):")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 3, 6, 15)
    print(f"    八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"    预期：丙午 庚寅 己酉 壬申")

    # 3. 子时切换测试
    print("\n3. 子时切换测试:")
    print("  a) 2026-02-01 23:00:")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 2, 1, 23)
    print(f"    八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"    预期：丙午 己丑 丙午 戊子")

    print("  b) 2026-02-02 01:00:")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 2, 2, 1)
    print(f"    八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"    预期：丙午 己丑 丁未 辛丑")

    print("\n=== 自测完成 ===")