#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
三合局、三会局检测器（优化版）
=============================
用于检测指定时间段内八字中的三合局和三会局格局

优化特性：
- 完整局优先：如果存在完整三合局，则不显示对应的次级局
- 避免重复：同一类型的局只显示最高级别的结果
- 性能优化：减少不必要的重复计算

三合局定义：
- 金局：巳酉丑（完整）或 酉丑、巳酉（次级）
- 火局：寅午戌（完整）或 寅午、午戌（次级）  
- 木局：亥卯未（完整）或 亥卯、卯未（次级）
- 水局：申子辰（完整）或 申子、子辰（次级）

三会局定义：
- 北方三会局：亥子丑
- 东方三会局：寅卯辰  
- 南方三会局：巳午未
- 西方三会局：申酉戌
"""

import pandas as pd
from core.bazi_generator import generate_odd_hour_sequence
import datetime
from collections import Counter


class SanHeSanHuiDetector:
    """三合局、三会局检测器"""
    
    def __init__(self):
        # 三合局定义
        self.sanhe_patterns = {
            '金局_complete': ['巳', '酉', '丑'],
            '金局_secondary1': ['酉', '丑'],
            '金局_secondary2': ['巳', '酉'],
            
            '火局_complete': ['寅', '午', '戌'],
            '火局_secondary1': ['寅', '午'],
            '火局_secondary2': ['午', '戌'],
            
            '木局_complete': ['亥', '卯', '未'],
            '木局_secondary1': ['亥', '卯'],
            '木局_secondary2': ['卯', '未'],
            
            '水局_complete': ['申', '子', '辰'],
            '水局_secondary1': ['申', '子'],
            '水局_secondary2': ['子', '辰']
        }
        
        # 三会局定义
        self.sanhui_patterns = {
            '北方三会局': ['亥', '子', '丑'],
            '东方三会局': ['寅', '卯', '辰'],
            '南方三会局': ['巳', '午', '未'],
            '西方三会局': ['申', '酉', '戌']
        }
    
    def detect_sanhe(self, dizhi_list):
        """检测三合局（完整局优先，不重复计算次级局）"""
        found_patterns = []
        
        # 统计地支出现次数
        dizhi_counter = Counter(dizhi_list)
        
        # 记录已找到完整局的类型，避免重复计算次级局
        found_complete_types = set()
        
        # 优先检测完整三合局
        for pattern_name, pattern_dizhi in self.sanhe_patterns.items():
            if len(pattern_dizhi) == 3:  # 完整三合
                if all(dizhi_counter[dz] > 0 for dz in pattern_dizhi):
                    base_name = pattern_name.replace('_complete', '')
                    found_patterns.append({
                        'type': '三合局',
                        'name': base_name,
                        'level': '完整',
                        'components': pattern_dizhi
                    })
                    found_complete_types.add(base_name)
        
        # 只有在没有完整局的情况下才检测次级局
        for pattern_name, pattern_dizhi in self.sanhe_patterns.items():
            if len(pattern_dizhi) != 3:  # 次级三合
                base_name = pattern_name.split('_')[0]
                # 如果该类型的完整局已经找到，则跳过次级局
                if base_name in found_complete_types:
                    continue
                
                if all(dizhi_counter[dz] > 0 for dz in pattern_dizhi):
                    found_patterns.append({
                        'type': '三合局',
                        'name': base_name,
                        'level': '次级',
                        'components': pattern_dizhi
                    })
        
        return found_patterns
    
    def detect_sanhui(self, dizhi_list):
        """检测三会局"""
        found_patterns = []
        
        # 统计地支出现次数
        dizhi_counter = Counter(dizhi_list)
        
        # 检测三会局
        for pattern_name, pattern_dizhi in self.sanhui_patterns.items():
            if all(dizhi_counter[dz] > 0 for dz in pattern_dizhi):
                found_patterns.append({
                    'type': '三会局',
                    'name': pattern_name,
                    'level': '完整',
                    'components': pattern_dizhi
                })
        
        return found_patterns
    
    def detect_all_patterns(self, bazi_dict):
        """检测单个八字的所有格局"""
        # 提取四柱地支
        year_zhi = bazi_dict['year_gz'][1]
        month_zhi = bazi_dict['month_gz'][1]
        day_zhi = bazi_dict['day_gz'][1]
        hour_zhi = bazi_dict['hour_gz'][1]
        
        dizhi_list = [year_zhi, month_zhi, day_zhi, hour_zhi]
        
        # 检测三合局和三会局
        sanhe_patterns = self.detect_sanhe(dizhi_list)
        sanhui_patterns = self.detect_sanhui(dizhi_list)
        
        return {
            'datetime': bazi_dict['datetime'],
            'bazi': bazi_dict['bazi'],
            'dizhi_list': dizhi_list,
            'sanhe_patterns': sanhe_patterns,
            'sanhui_patterns': sanhui_patterns,
            'has_sanhe': len(sanhe_patterns) > 0,
            'has_sanhui': len(sanhui_patterns) > 0,
            'total_patterns': len(sanhe_patterns) + len(sanhui_patterns)
        }


def find_sanhe_sanhui_patterns(start_date, days=365):
    """查找指定时间段内的所有三合、三会局"""
    
    print(f"开始查找 {start_date} 起 {days} 天内的三合、三会局...")
    
    # 生成八字序列
    bazi_list = generate_odd_hour_sequence(
        start_date=start_date,
        days=days,
        hour_interval=2,
        use_continuous=True
    )
    
    print(f"共生成 {len(bazi_list)} 个八字")
    
    # 初始化检测器
    detector = SanHeSanHuiDetector()
    
    # 检测所有八字
    results = []
    pattern_stats = {
        'sanhe_complete': Counter(),
        'sanhe_secondary': Counter(),
        'sanhui': Counter()
    }
    
    for bazi_dict in bazi_list:
        result = detector.detect_all_patterns(bazi_dict)
        
        # 统计格局
        if result['has_sanhe'] or result['has_sanhui']:
            results.append(result)
            
            # 更新统计
            for pattern in result['sanhe_patterns']:
                if pattern['level'] == '完整':
                    pattern_stats['sanhe_complete'][pattern['name']] += 1
                else:
                    pattern_stats['sanhe_secondary'][pattern['name']] += 1
                    
            for pattern in result['sanhui_patterns']:
                pattern_stats['sanhui'][pattern['name']] += 1
    
    print(f"\n查找完成！共找到 {len(results)} 个含有三合/三会局的八字")
    
    # 显示统计结果
    print("\n=== 格局统计 ===")
    
    if pattern_stats['sanhe_complete']:
        print("完整三合局:")
        for name, count in pattern_stats['sanhe_complete'].most_common():
            print(f"  {name}: {count} 个")
    
    if pattern_stats['sanhe_secondary']:
        print("次级三合局:")
        for name, count in pattern_stats['sanhe_secondary'].most_common():
            print(f"  {name}: {count} 个")
    
    if pattern_stats['sanhui']:
        print("三会局:")
        for name, count in pattern_stats['sanhui'].most_common():
            print(f"  {name}: {count} 个")
    
    return results, pattern_stats


def save_patterns_report(results, stats, filename=None):
    """保存格局分析报告"""
    
    if not results:
        print("没有找到任何格局，无需保存报告")
        return
    
    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"三合三会局分析_{timestamp}.xlsx"
    
    # 转换为DataFrame
    report_data = []
    for result in results:
        row = {
            '日期时间': result['datetime'],
            '八字': result['bazi'],
            '地支组合': '-'.join(result['dizhi_list']),
            '三合局数量': len(result['sanhe_patterns']),
            '三会局数量': len(result['sanhui_patterns']),
            '总格局数': result['total_patterns']
        }
        
        # 添加具体格局信息
        sanhe_names = [f"{p['name']}({p['level']})" for p in result['sanhe_patterns']]
        sanhui_names = [p['name'] for p in result['sanhui_patterns']]
        
        row['三合局详情'] = '; '.join(sanhe_names) if sanhe_names else ''
        row['三会局详情'] = '; '.join(sanhui_names) if sanhui_names else ''
        
        report_data.append(row)
    
    df = pd.DataFrame(report_data)
    
    # 保存到Excel
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 详细数据
        df.to_excel(writer, sheet_name='详细数据', index=False)
        
        # 统计汇总
        summary_data = []
        
        # 三合局统计
        for name, count in stats['sanhe_complete'].items():
            summary_data.append({
                '格局类型': '完整三合局',
                '名称': name,
                '数量': count,
                '占比(%)': round(count/len(results)*100, 2)
            })
        
        for name, count in stats['sanhe_secondary'].items():
            summary_data.append({
                '格局类型': '次级三合局',
                '名称': name,
                '数量': count,
                '占比(%)': round(count/len(results)*100, 2)
            })
        
        # 三会局统计
        for name, count in stats['sanhui'].items():
            summary_data.append({
                '格局类型': '三会局',
                '名称': name,
                '数量': count,
                '占比(%)': round(count/len(results)*100, 2)
            })
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='统计汇总', index=False)
    
    print(f"分析报告已保存到: {filename}")
    return filename


def display_sample_results(results, sample_size=20):
    """显示样本结果"""
    
    if not results:
        print("未找到任何格局")
        return
    
    print(f"\n=== 前{sample_size}个格局示例 ===")
    print(f"{'序号':<4} {'日期时间':<20} {'八字':<20} {'格局类型':<30}")
    print("-" * 80)
    
    for i, result in enumerate(results[:sample_size]):
        patterns_desc = []
        
        # 三合局描述
        for pattern in result['sanhe_patterns']:
            level_desc = "完整" if pattern['level'] == '完整' else "次级"
            patterns_desc.append(f"{pattern['name']}{level_desc}")
        
        # 三会局描述
        for pattern in result['sanhui_patterns']:
            patterns_desc.append(pattern['name'])
        
        patterns_str = "; ".join(patterns_desc)
        print(f"{i+1:<4} {result['datetime']:<20} {result['bazi']:<20} {patterns_str:<30}")


if __name__ == "__main__":
    # 示例：查找未来一年的三合三会局
    start_date = datetime.date.today()
    
    # 查找格局
    results, stats = find_sanhe_sanhui_patterns(start_date, days=365)
    
    # 显示样本结果
    display_sample_results(results)
    
    # 保存报告
    if results:
        save_patterns_report(results, stats)
        
        print(f"\n=== 总结 ===")
        print(f"总八字数: {len(results)} 个")
        print(f"含三合局: {sum(1 for r in results if r['has_sanhe'])} 个")
        print(f"含三会局: {sum(1 for r in results if r['has_sanhui'])} 个")
        print(f"同时含有: {sum(1 for r in results if r['has_sanhe'] and r['has_sanhui'])} 个")