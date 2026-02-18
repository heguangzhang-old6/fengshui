#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
优化后的三合局检测测试
验证完整局优先，不重复计算次级局的逻辑
"""

import datetime
from sanhe_sanhui_detector import SanHeSanHuiDetector

def test_optimization():
    """测试优化后的检测逻辑"""
    
    print("=== 三合局优化检测测试 ===\n")
    
    detector = SanHeSanHuiDetector()
    
    # 测试用例：包含完整三合局的情况
    test_cases = [
        {
            'name': '寅午戌完整火局',
            'dizhi_list': ['寅', '午', '戌', '子'],  # 包含完整火局
            'expected_sanhe': [('火局', '完整')]
        },
        {
            'name': '巳酉丑完整金局',
            'dizhi_list': ['巳', '酉', '丑', '寅'],  # 包含完整金局
            'expected_sanhe': [('金局', '完整')]
        },
        {
            'name': '只有次级火局',
            'dizhi_list': ['寅', '午', '申', '子'],  # 只有寅午，无完整火局
            'expected_sanhe': [('火局', '次级')]
        },
        {
            'name': '多个完整局',
            'dizhi_list': ['寅', '午', '戌', '申'],  # 寅午戌完整火局 + 申子辰水局
            'expected_sanhe': [('火局', '完整'), ('水局', '次级')]  # 水局只显示次级因为完整局不存在
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {case['name']}")
        print(f"地支组合: {'-'.join(case['dizhi_list'])}")
        
        # 构造模拟八字字典
        mock_bazi = {
            'datetime': '2026-01-01 12:00',
            'bazi': '甲子 乙丑 丙寅 丁卯',
            'year_gz': '甲' + case['dizhi_list'][0],
            'month_gz': '乙' + case['dizhi_list'][1], 
            'day_gz': '丙' + case['dizhi_list'][2],
            'hour_gz': '丁' + case['dizhi_list'][3]
        }
        
        result = detector.detect_all_patterns(mock_bazi)
        
        print("检测结果:")
        if result['sanhe_patterns']:
            for pattern in result['sanhe_patterns']:
                print(f"  {pattern['name']} {pattern['level']}局")
        else:
            print("  无三合局")
            
        print(f"预期结果: {case['expected_sanhe']}")
        print("-" * 50)

def performance_comparison():
    """性能对比测试"""
    
    print("\n=== 性能优化效果 ===\n")
    
    detector = SanHeSanHuiDetector()
    
    # 测试大量数据
    import time
    
    # 模拟包含多个完整局的复杂情况
    complex_dizhi = ['寅', '午', '戌', '申', '子', '辰']  # 同时包含火局完整和水局次级
    
    start_time = time.time()
    
    # 模拟1000次检测
    for i in range(1000):
        mock_bazi = {
            'datetime': '2026-01-01 12:00',
            'bazi': '甲子 乙丑 丙寅 丁卯',
            'year_gz': '甲' + complex_dizhi[i % 6],
            'month_gz': '乙' + complex_dizhi[(i + 1) % 6],
            'day_gz': '丙' + complex_dizhi[(i + 2) % 6],
            'hour_gz': '丁' + complex_dizhi[(i + 3) % 6]
        }
        detector.detect_all_patterns(mock_bazi)
    
    end_time = time.time()
    
    print(f"1000次检测耗时: {end_time - start_time:.4f}秒")
    print(f"平均每次检测: {(end_time - start_time) * 1000:.2f}毫秒")

if __name__ == "__main__":
    test_optimization()
    performance_comparison()