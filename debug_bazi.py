#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from core.ganzhi_calculator import get_traditional_bazi, get_year_ganzhi, get_month_ganzhi

def debug_bazi_calculation():
    """调试八字计算逻辑"""
    
    print("=" * 50)
    print("八字计算调试")
    print("=" * 50)
    
    # 测试日期：2026年7月11日
    test_date = datetime.date(2026, 7, 11)
    print(f"测试日期: {test_date}")
    print(f"预期结果: 丙午年、乙未月")
    print()
    
    # 1. 计算年柱
    print("1. 年柱计算:")
    year_gz = get_year_ganzhi(test_date)
    print(f"   输入日期: {test_date}")
    print(f"   计算结果: {year_gz}")
    print(f"   是否正确: {'✓' if year_gz == '丙午' else '✗'}")
    print()
    
    # 2. 计算月柱
    print("2. 月柱计算:")
    month_gz = get_month_ganzhi(test_date, year_gz[0])
    print(f"   输入年干: {year_gz[0]}")
    print(f"   输入日期: {test_date.month}月{test_date.day}日")
    print(f"   计算结果: {month_gz}")
    print(f"   预期结果: 乙未")
    print(f"   是否正确: {'✓' if month_gz == '乙未' else '✗'}")
    print()
    
    # 3. 完整八字计算
    print("3. 完整八字计算:")
    bazi = get_traditional_bazi(2026, 7, 11, 12)
    print(f"   输入: 2026-07-11 12:00")
    print(f"   结果: {bazi}")
    print()
    
    # 4. 分析月柱计算过程
    print("4. 月柱计算详细过程:")
    analyze_month_calculation(test_date, year_gz[0])

def analyze_month_calculation(date, year_gan):
    """分析月柱计算过程"""
    
    month = date.month
    day = date.day
    
    print(f"   输入: {year_gan}年 {month}月{day}日")
    
    # 检查地支判断
    print("   地支判断过程:")
    
    if month == 1 or (month == 2 and day < 4):
        month_dz = '丑'
        print(f"   1-2月或2月4日前 → 丑月")
    elif (month == 2 and day >= 4) or (month == 3 and day < 6):
        month_dz = '寅'
        print(f"   2月4日后-3月6日前 → 寅月")
    elif (month == 3 and day >= 6) or (month == 4 and day < 4):
        month_dz = '卯'
        print(f"   3月6日后-4月4日前 → 卯月")
    elif (month == 4 and day >= 4) or (month == 5 and day < 5):
        month_dz = '辰'
        print(f"   4月4日后-5月5日前 → 辰月")
    elif (month == 5 and day >= 5) or (month == 6 and day < 6):
        month_dz = '巳'
        print(f"   5月5日后-6月6日前 → 巳月")
    else:
        # 问题就在这里！
        month_dz = ['未', '申', '酉', '戌', '亥', '子'][(month - 6) % 6]
        print(f"   其他月份 → {month_dz}月 (通过公式计算)")
    
    print(f"   确定地支: {month_dz}")
    
    # 检查天干计算
    print("   天干计算过程:")
    from core.ganzhi_calculator import WUHU_DUN, TIANGAN, DIZHI
    
    yin_month_gan = WUHU_DUN[year_gan]
    print(f"   年干{year_gan}对应的寅月天干: {yin_month_gan}")
    
    yin_idx = DIZHI.index('寅')
    curr_idx = DIZHI.index(month_dz)
    offset = (curr_idx - yin_idx) % 12
    print(f"   寅月索引: {yin_idx}, 当前月索引: {curr_idx}")
    print(f"   偏移量: {offset}")
    
    yin_gan_idx = TIANGAN.index(yin_month_gan)
    month_gan_idx = (yin_gan_idx + offset) % 10
    month_gan = TIANGAN[month_gan_idx]
    print(f"   寅月天干索引: {yin_gan_idx}")
    print(f"   当前月天干索引: {month_gan_idx}")
    print(f"   当前月天干: {month_gan}")
    
    print(f"   最终月柱: {month_gan}{month_dz}")

if __name__ == "__main__":
    debug_bazi_calculation()