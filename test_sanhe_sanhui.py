#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
三合局、三会局快速检测测试
"""

import datetime
from sanhe_sanhui_detector import SanHeSanHuiDetector, find_sanhe_sanhui_patterns

def quick_test():
    """快速测试几个典型日期"""
    
    print("=== 三合三会局快速测试 ===\n")
    
    # 测试几个已知包含格局的日期
    test_dates = [
        datetime.date(2026, 2, 16),  # 可能包含寅卯辰
        datetime.date(2026, 5, 15),  # 可能包含巳午未
        datetime.date(2026, 8, 15),  # 可能包含申酉戌
        datetime.date(2026, 11, 15), # 可能包含亥子丑
    ]
    
    detector = SanHeSanHuiDetector()
    
    for test_date in test_dates:
        print(f"测试日期: {test_date}")
        
        # 生成一天的八字数据
        from core.bazi_generator import generate_odd_hour_sequence
        bazi_list = generate_odd_hour_sequence(
            start_date=test_date,
            days=1,
            hour_interval=2,
            use_continuous=True
        )
        
        print(f"生成八字数: {len(bazi_list)}")
        
        # 检测每个八字
        found_any = False
        for bazi_dict in bazi_list[:3]:  # 只测试前3个
            result = detector.detect_all_patterns(bazi_dict)
            
            if result['total_patterns'] > 0:
                found_any = True
                print(f"  {result['datetime']} - {result['bazi']}")
                print(f"    地支: {'-'.join(result['dizhi_list'])}")
                
                if result['sanhe_patterns']:
                    sanhe_desc = [f"{p['name']}({p['level']})" for p in result['sanhe_patterns']]
                    print(f"    三合局: {', '.join(sanhe_desc)}")
                
                if result['sanhui_patterns']:
                    sanhui_desc = [p['name'] for p in result['sanhui_patterns']]
                    print(f"    三会局: {', '.join(sanhui_desc)}")
                print()
        
        if not found_any:
            print("  未找到明显格局")
        print("-" * 50)

if __name__ == "__main__":
    quick_test()