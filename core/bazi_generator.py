# -*- coding: utf-8 -*-
"""
八字序列生成模块 (bazi_generator)
=====================================
【模块说明】
本模块提供八字序列生成功能，基于八字计算核心模块。

【核心功能】
1. 传统八字序列生成
2. 连续时柱八字序列生成
3. 奇数小时八字序列生成

【版本信息】
- 版本：v1.0（基线版）
- 最后更新：2026-01-24
"""

import datetime
from core.ganzhi_calculator import  get_traditional_bazi, get_continuous_bazi


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
        list - 八字字典列表
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
        list - 八字字典列表
    """
    if hour_interval <= 0 or hour_interval % 2 != 0:
        raise ValueError("小时间隔必须为正数且能被2整除")

    results = []
    current_dt = start_datetime

    while current_dt <= end_datetime:
        try:
            year_gz, month_gz, day_gz, hour_gz = get_continuous_bazi(start_datetime, current_dt)

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


def check_hour_continuity(bazi_sequence: list) -> list:
    """
    检查八字序列的时柱连续性

    参数：
        bazi_sequence: list - 八字序列

    返回：
        list - 添加了连续性检查结果的序列
    """
    from ganzhi_calculator import TIANGAN, DIZHI

    if not bazi_sequence:
        return []

    result = []
    prev_hour_gz = None

    for item in bazi_sequence:
        current_item = item.copy()
        hour_gz = item['hour_gz']

        if prev_hour_gz:
            prev_gan_idx = TIANGAN.index(prev_hour_gz[0])
            prev_zhi_idx = DIZHI.index(prev_hour_gz[1])
            curr_gan_idx = TIANGAN.index(hour_gz[0])
            curr_zhi_idx = DIZHI.index(hour_gz[1])

            gan_diff = (curr_gan_idx - prev_gan_idx) % 10
            zhi_diff = (curr_zhi_idx - prev_zhi_idx) % 12

            is_continuous = (gan_diff == 1 and zhi_diff == 1)
            current_item['is_continuous'] = is_continuous
            current_item['gan_diff'] = gan_diff
            current_item['zhi_diff'] = zhi_diff
        else:
            current_item['is_continuous'] = True
            current_item['gan_diff'] = 0
            current_item['zhi_diff'] = 0

        result.append(current_item)
        prev_hour_gz = hour_gz

    return result

if __name__ == "__main__":
    print("=" * 60)
    print("八字序列生成")
    print("=" * 60)

    start_date = datetime.date(2026, 2, 16)

    # 生成连续时柱八字序列
    print("a) 连续时柱八字序列 (从23:00开始，2天):")
    bazi_list = generate_odd_hour_sequence(
        start_date=start_date,
        days=3,
        hour_interval=2,
        use_continuous=True
    )

    print(f'共生成八字{len(bazi_list)}个')
    for item in bazi_list:
        # print(item)
        print(f"日期：{item.get('datetime','没发现日期')}\t八字：{item.get('bazi','没发现八字')}\t年柱：{item.get('year_gz','没发现年柱')}\t月柱：{item.get('month_gz','没发现月柱')}\t日柱：{item.get('day_gz','没发现日柱')}\t时柱：{item.get('hour_gz','没发现时柱')} ")

    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)