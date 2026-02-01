# -*- coding: utf-8 -*-
"""
八字系统使用示例 (example_usage)
=====================================
【模块说明】
展示如何使用八字计算系统。

【使用示例】
1. 计算单个八字
2. 生成八字序列
3. 检查时柱连续性
"""

import datetime
from core.ganzhi_calculator import get_traditional_bazi, get_continuous_bazi
from core.bazi_generator import generate_odd_hour_sequence, check_hour_continuity


def example_single_bazi():
    """示例：计算单个八字"""
    print("1. 计算单个八字示例:")
    print("-" * 40)

    # 示例1：传统八字
    print("a) 传统八字计算:")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 1, 24, 15)
    print(f"   2026-01-24 15:00: {year_gz} {month_gz} {day_gz} {hour_gz}")

    # 示例2：连续八字
    print("\nb) 连续时柱八字计算:")
    start_dt = datetime.datetime(2026, 1, 31, 23, 0)
    target_dt = datetime.datetime(2026, 2, 1, 1, 0)
    year_gz, month_gz, day_gz, hour_gz = get_continuous_bazi(start_dt, target_dt)
    print(f"   起始时间: {start_dt}")
    print(f"   目标时间: {target_dt}")
    print(f"   八字: {year_gz} {month_gz} {day_gz} {hour_gz}")


def example_sequence():
    """示例：生成八字序列"""
    print("\n2. 生成八字序列示例:")
    print("-" * 40)

    start_date = datetime.date(2026, 1, 31)

    # 生成连续时柱八字序列
    print("a) 连续时柱八字序列 (从23:00开始，2天):")
    bazi_list = generate_odd_hour_sequence(
        start_date=start_date,
        days=2,
        hour_interval=2,
        use_continuous=True
    )

    # 检查连续性
    checked_list = check_hour_continuity(bazi_list)

    # 显示结果
    print("   日期时间        八字                 连续性")
    print("   " + "-" * 40)
    for item in checked_list[:8]:  # 显示前8个
        continuity = "✓" if item['is_continuous'] else f"✗(+{item['gan_diff']},{item['zhi_diff']})"
        print(f"   {item['datetime']}  {item['bazi']}  {continuity}")

    print(f"\n   总共生成 {len(bazi_list)} 个八字")


def example_key_points():
    """示例：关键时间点验证"""
    print("\n3. 关键时间点验证:")
    print("-" * 40)

    key_points = [
        ("2026-01-24 15:00", 2026, 1, 24, 15),
        ("2026-02-01 23:00", 2026, 2, 1, 23),
        ("2026-02-02 01:00", 2026, 2, 2, 1),
        ("2026-03-05 15:00", 2026, 3, 5, 15),
        ("2026-03-06 15:00", 2026, 3, 6, 15),
    ]

    for desc, y, m, d, h in key_points:
        try:
            year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(y, m, d, h)
            print(f"   {desc}: {year_gz} {month_gz} {day_gz} {hour_gz}")
        except Exception as e:
            print(f"   {desc}: 错误 - {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("八字系统使用示例")
    print("=" * 60)

    example_single_bazi()
    example_sequence()
    example_key_points()

    print("\n" + "=" * 60)
    print("示例完成！")
    print("=" * 60)