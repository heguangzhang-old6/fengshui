# -*- coding: utf-8 -*-
"""
输入验证模块
=====================================
【模块说明】
验证用户输入的合法性。

【功能】
1. 验证龙、山、主命格式
2. 验证日期范围
3. 验证其他输入参数

【版本信息】
- 版本：v1.0
- 最后更新：2026-01-24
"""

import re
from typing import Dict, Any


class InputValidator:
    """输入验证器"""

    def __init__(self):
        self.patterns = {
            'dragon': r'^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]龙$',
            'mountain': r'^[子丑寅卯辰巳午未申酉戌亥]山[子丑寅卯辰巳午未申酉戌亥]向$',
            'fate': r'^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]年$',
            'days': r'^\d+$'
        }

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """验证输入数据"""

        # 验证龙
        if 'dragon' in input_data:
            if not re.match(self.patterns['dragon'], input_data['dragon']):
                print(f"龙格式错误: {input_data['dragon']}")
                return False

        # 验证山
        if 'mountain' in input_data:
            if not re.match(self.patterns['mountain'], input_data['mountain']):
                print(f"山格式错误: {input_data['mountain']}")
                return False

        # 验证主命
        if 'fate' in input_data:
            if not re.match(self.patterns['fate'], input_data['fate']):
                print(f"主命格式错误: {input_data['fate']}")
                return False

        # 验证天数
        if 'days' in input_data:
            try:
                days = int(input_data['days'])
                if days <= 0 or days > 365:
                    print(f"天数应在1-365之间: {days}")
                    return False
            except ValueError:
                print(f"天数格式错误: {input_data['days']}")
                return False

        return True

    def sanitize_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """清理输入数据"""
        sanitized = {}

        for key, value in input_data.items():
            if isinstance(value, str):
                # 去除首尾空格
                sanitized[key] = value.strip()
            else:
                sanitized[key] = value

        return sanitized