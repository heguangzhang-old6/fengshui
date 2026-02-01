# -*- coding: utf-8 -*-
"""
八字序列生成模块 (bazi_generator)
=====================================
【模块说明】
本模块提供八字序列生成功能，基于八字计算核心模块。

【核心功能】
1. 传统八字序列生成
2. 连续时柱八字序列生成

【版本信息】
- 版本：v3.0（清理重构版）
- 适配Python版本：3.6+
- 最后更新：2026-01-24
"""

import datetime
from ganzhi_calculator import get_traditional_bazi, get_continuous_bazi


def generate_traditional_bazi_sequence(start_datetime: datetime.datetime,
                                       end_datetime: datetime.datetime,
                                       hour_interval: int = 2) -> list:
    """
    生成传统八字序列

    参数：
        start_datetime: datetime.datetime - 开始时间
        end_datetime: datetime.datetime - 结束时间
        hour_interval: int - 小时间隔（默认2小时）

    返回：
        list - 八字字典列表，每个字典包含：
            - datetime: 时间字符串
            - bazi: 八字字符串
            - year_gz: 年柱
            - month_gz: 月柱
            - day_gz: 日柱
            - hour_gz: 时柱
    """
    if hour_interval <= 0:
        raise ValueError("小时间隔必须大于0")

    results = []
    current_dt = start_datetime

    while current_dt <= end_datetime:
        try:
            year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(
                current_dt.year, current_dt.month, current_dt.day, current_dt.hour
            )

            time_str = current_dt.strftime("%Y-%m-%d %H:%M")
            bazi_str = f"{year_gz} {month_gz} {day_gz} {hour_gz}"

            results.append({
                'datetime': time_str,
                'bazi': bazi_str,
                'year_gz': year_gz,
                'month_gz': month_gz,
                'day_gz': day_gz,
                'hour_gz': hour_gz
            })

        except ValueError as e:
            print(f"警告：{current_dt} 计算失败 - {e}")

        current_dt += datetime.timedelta(hours=hour_interval)

    return results


def generate_continuous_bazi_sequence(start_datetime: datetime.datetime,
                                      end_datetime: datetime.datetime,
                                      hour_interval: int = 2) -> list:
    """
    生成连续时柱八字序列

    参数：
        start_datetime: datetime.datetime - 开始时间（也是连续时柱的参考起点）
        end_datetime: datetime.datetime - 结束时间
        hour_interval: int - 小时间隔（默认2小时，必须能被2整除）

    返回：
        list - 八字字典列表，包含连续性检查信息
    """
    if hour_interval <= 0 or hour_interval % 2 != 0:
        raise ValueError("小时间隔必须为正数且能被2整除")

    results = []
    current_dt = start_datetime
    prev_hour_gz = None

    while current_dt <= end_datetime:
        try:
            year_gz, month_gz, day_gz, hour_gz = get_continuous_bazi(start_datetime, current_dt)

            time_str = current_dt.strftime("%Y-%m-%d %H:%M")
            bazi_str = f"{year_gz} {month_gz} {day_gz} {hour_gz}"

            # 检查时柱连续性
            continuity_info = "起始"
            if prev_hour_gz:
                from ganzhi_calculator import TIANGAN, DIZHI
                prev_gan_idx = TIANGAN.index(prev_hour_gz[0])
                prev_zhi_idx = DIZHI.index(prev_hour_gz[1])
                curr_gan_idx = TIANGAN.index(hour_gz[0])
                curr_zhi_idx = DIZHI.index(hour_gz[1])

                gan_diff = (curr_gan_idx - prev_gan_idx) % 10
                zhi_diff = (curr_zhi_idx - prev_zhi_idx) % 12

                is_continuous = (gan_diff == 1 and zhi_diff == 1)
                continuity_info = "连续" if is_continuous else f"不连续(天干+{gan_diff},地支+{zhi_diff})"

            results.append({
                'datetime': time_str,
                'bazi': bazi_str,
                'year_gz': year_gz,
                'month_gz': month_gz,
                'day_gz': day_gz,
                'hour_gz': hour_gz,
                'continuity': continuity_info
            })

            prev_hour_gz = hour_gz

        except ValueError as e:
            print(f"警告：{current_dt} 计算失败 - {e}")

        current_dt += datetime.timedelta(hours=hour_interval)

    return results


def generate_odd_hour_sequence(start_date: datetime.date,
                               days: int = 10,
                               hour_interval: int = 2,
                               use_continuous: bool = True) -> list:
    """
    生成奇数小时八字序列（从23:00开始）

    参数：
        start_date: datetime.date - 开始日期
        days: int - 生成天数（默认10天）
        hour_interval: int - 小时间隔（默认2小时，必须能被2整除）
        use_continuous: bool - 是否使用连续时柱（默认True）

    返回：
        list - 八字字典列表
    """
    if hour_interval <= 0 or hour_interval % 2 != 0:
        raise ValueError("小时间隔必须为正数且能被2整除")

    # 从开始日期的23:00开始
    start_dt = datetime.datetime(start_date.year, start_date.month, start_date.day, 23, 0)
    end_dt = start_dt + datetime.timedelta(days=days)

    if use_continuous:
        return generate_continuous_bazi_sequence(start_dt, end_dt, hour_interval)
    else:
        return generate_traditional_bazi_sequence(start_dt, end_dt, hour_interval)


# -------------------------- 使用示例 --------------------------
if __name__ == "__main__":
    print("=== 八字序列生成模块示例 ===")

    # 示例1：生成连续时柱八字序列
    print("\n1. 连续时柱八字序列（从2026-01-31 23:00开始，2天）：")
    start_date = datetime.date(2026, 1, 31)
    results = generate_odd_hour_sequence(start_date, days=2, hour_interval=2, use_continuous=True)

    # 显示前10个结果
    for i, item in enumerate(results[:10]):
        continuity = f" [{item['continuity']}]" if 'continuity' in item else ""
        print(f"{item['datetime']} -> {item['bazi']}{continuity}")

    print(f"\n... 总共生成 {len(results)} 个八字")

    # 示例2：生成传统八字序列
    print("\n2. 传统八字序列（从2026-02-01 00:00开始，1天）：")
    start_dt = datetime.datetime(2026, 2, 1, 0, 0)
    end_dt = start_dt + datetime.timedelta(days=1)
    results = generate_traditional_bazi_sequence(start_dt, end_dt, hour_interval=2)

    for i, item in enumerate(results):
        print(f"{item['datetime']} -> {item['bazi']}")

    print(f"\n总共生成 {len(results)} 个八字")

    print("\n=== 示例完成 ===")