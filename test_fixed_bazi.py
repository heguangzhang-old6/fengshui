#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from core.ganzhi_calculator import get_traditional_bazi, get_year_ganzhi, get_month_ganzhi

def test_fixed_bazi():
    """测试修复后的八字计算"""
    
    print("=" * 60)
    print("修复后的八字计算测试")
    print("=" * 60)
    
    # 测试用例
    test_cases = [
        (2026, 7, 11, 12),  # 主要测试案例
        (2026, 6, 15, 12),  # 6月案例
        (2026, 8, 15, 12),  # 8月案例
        (2026, 12, 15, 12), # 12月案例
        (2027, 1, 15, 12),  # 次年1月案例
    ]
    
    print("测试结果:")
    print("-" * 60)
    print(f"{'日期':<12} {'年柱':<8} {'月柱':<8} {'日柱':<8} {'时柱':<8}")
    print("-" * 60)
    
    for year, month, day, hour in test_cases:
        try:
            bazi = get_traditional_bazi(year, month, day, hour)
            date_str = f"{year}-{month:02d}-{day:02d}"
            print(f"{date_str:<12} {bazi[0]:<8} {bazi[1]:<8} {bazi[2]:<8} {bazi[3]:<8}")
        except Exception as e:
            print(f"{date_str:<12} 错误: {e}")
    
    print("-" * 60)
    
    # 重点验证2026年7月11日
    print("\n详细验证 2026年7月11日:")
    test_date = datetime.date(2026, 7, 11)
    
    year_gz = get_year_ganzhi(test_date)
    print(f"年柱: {year_gz} {'✓' if year_gz == '丙午' else '✗'}")
    
    month_gz = get_month_ganzhi(test_date, year_gz[0])
    print(f"月柱: {month_gz} {'✓' if month_gz == '乙未' else '✗'}")
    
    # 完整验证
    bazi = get_traditional_bazi(2026, 7, 11, 12)
    print(f"完整八字: {bazi}")
    expected = ('丙午', '乙未', '癸巳', '戊午')
    is_correct = bazi == expected
    print(f"是否正确: {'✓' if is_correct else '✗'}")
    if not is_correct:
        print(f"期望结果: {expected}")

if __name__ == "__main__":
    test_fixed_bazi()