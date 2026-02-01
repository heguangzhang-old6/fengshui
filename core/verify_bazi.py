# -*- coding: utf-8 -*-
"""
八字系统验证脚本 (verify_bazi)
=====================================
【模块说明】
用于验证八字计算系统的正确性。

【验证项目】
1. 立春前后年柱切换正确性
2. 节气月份切换正确性
3. 子时日柱切换正确性
4. 时柱连续性验证
"""

import datetime
from core.ganzhi_calculator import get_traditional_bazi, get_continuous_bazi


def test_spring_transition():
    """验证立春前后年柱切换"""
    print("1. 立春前后年柱切换验证:")
    print("   a) 2026-02-03 15:00 (立春前):")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 2, 3, 15)
    print(f"      八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"      年柱应为：乙巳")
    print(f"      结果：{'✓' if year_gz == '乙巳' else '✗'}")

    print("   b) 2026-02-05 15:00 (立春后):")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 2, 5, 15)
    print(f"      八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"      年柱应为：丙午")
    print(f"      结果：{'✓' if year_gz == '丙午' else '✗'}")


def test_jieqi_month_transition():
    """验证节气月份切换"""
    print("\n2. 节气月份切换验证:")
    print("   a) 2026-03-05 15:00 (惊蛰前):")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 3, 5, 15)
    print(f"      八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"      月柱应为：庚寅 (丙年寅月)")
    print(f"      结果：{'✓' if month_gz == '庚寅' else '✗'}")

    print("   b) 2026-03-06 15:00 (惊蛰后):")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 3, 6, 15)
    print(f"      八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"      月柱应为：辛卯 (丙年卯月)")
    print(f"      结果：{'✓' if month_gz == '辛卯' else '✗'}")


def test_zi_hour_transition():
    """验证子时日柱切换"""
    print("\n3. 子时日柱切换验证:")
    print("   a) 2026-02-01 23:00:")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 2, 1, 23)
    print(f"      八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"      说明：23:00属于第二天子时")
    print(f"      日柱应为：丙午 (2月1日日柱)")
    print(f"      时柱应为：庚子 (丁日子时，第二天日干为丁)")
    day_correct = day_gz == '丙午'
    hour_correct = hour_gz == '庚子'
    print(f"      结果：日柱{'✓' if day_correct else '✗'}，时柱{'✓' if hour_correct else '✗'}")

    print("   b) 2026-02-02 01:00:")
    year_gz, month_gz, day_gz, hour_gz = get_traditional_bazi(2026, 2, 2, 1)
    print(f"      八字：{year_gz} {month_gz} {day_gz} {hour_gz}")
    print(f"      日柱应为：丁未 (2月2日日柱)")
    print(f"      时柱应为：辛丑 (丁日丑时)")
    day_correct = day_gz == '丁未'
    hour_correct = hour_gz == '辛丑'
    print(f"      结果：日柱{'✓' if day_correct else '✗'}，时柱{'✓' if hour_correct else '✗'}")


def test_hour_continuity():
    """验证时柱连续性"""
    print("\n4. 时柱连续性验证:")
    start_dt = datetime.datetime(2026, 1, 31, 23, 0)
    test_times = [
        datetime.datetime(2026, 1, 31, 23, 0),
        datetime.datetime(2026, 2, 1, 1, 0),
        datetime.datetime(2026, 2, 1, 3, 0),
    ]

    print(f"   起始时间：{start_dt.strftime('%Y-%m-%d %H:%M')}")

    prev_hour_gz = None
    from core.ganzhi_calculator import TIANGAN, DIZHI

    for dt in test_times:
        year_gz, month_gz, day_gz, hour_gz = get_continuous_bazi(start_dt, dt)

        if prev_hour_gz:
            prev_gan_idx = TIANGAN.index(prev_hour_gz[0])
            prev_zhi_idx = DIZHI.index(prev_hour_gz[1])
            curr_gan_idx = TIANGAN.index(hour_gz[0])
            curr_zhi_idx = DIZHI.index(hour_gz[1])

            gan_diff = (curr_gan_idx - prev_gan_idx) % 10
            zhi_diff = (curr_zhi_idx - prev_zhi_idx) % 12

            is_continuous = (gan_diff == 1 and zhi_diff == 1)
            status = "✓ 连续" if is_continuous else f"✗ 不连续(天干+{gan_diff},地支+{zhi_diff})"
            print(f"   {dt.strftime('%Y-%m-%d %H:%M')}: {hour_gz} {status}")
        else:
            print(f"   {dt.strftime('%Y-%m-%d %H:%M')}: {hour_gz} (起始)")

        prev_hour_gz = hour_gz


def test_sequence_generation():
    """测试序列生成"""
    print("\n5. 序列生成测试:")

    from core.bazi_generator import generate_odd_hour_sequence, check_hour_continuity

    start_date = datetime.date(2026, 1, 31)
    print(f"   从 {start_date} 开始，生成2天的奇数小时八字序列:")

    bazi_list = generate_odd_hour_sequence(
        start_date=start_date,
        days=2,
        hour_interval=2,
        use_continuous=True
    )

    # 检查连续性
    checked_list = check_hour_continuity(bazi_list)

    # 显示前5个结果
    print("   前5个结果:")
    for i, item in enumerate(checked_list[:5]):
        continuity = "连续" if item['is_continuous'] else f"不连续"
        print(f"     {item['datetime']} -> {item['bazi']} ({continuity})")

    print(f"\n   总共生成 {len(bazi_list)} 个八字")


if __name__ == "__main__":
    print("=" * 60)
    print("八字系统验证测试")
    print("=" * 60)

    # 运行所有验证
    test_spring_transition()
    test_jieqi_month_transition()
    test_zi_hour_transition()
    test_hour_continuity()
    test_sequence_generation()

    print("\n" + "=" * 60)
    print("验证完成！")
    print("=" * 60)