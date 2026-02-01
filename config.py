# -*- coding: utf-8 -*-
"""
配置文件
=====================================
【模块说明】
系统配置文件。

【配置项】
1. 系统设置
2. 判断规则
3. 输出设置

【版本信息】
- 版本：v1.0
- 最后更新：2026-01-24
"""

import os

# 基础设置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# 八字生成设置
BAZI_SETTINGS = {
    'hour_interval': 2,           # 小时间隔
    'start_hour': 23,             # 起始小时（23:00）
    'use_continuous': True        # 使用连续时柱
}

# 吉局判断设置
JUDGMENT_SETTINGS = {
    'dragon': {
        'enable_yiqi_tiangan': True,
        'enable_yiqi_dizhi': True,
        'enable_sanhe': True,
        'enable_sanhui': True,
        'enable_jialu': True,
        'enable_gonggui': True,
        'enable_special': True
    },
    'mountain': {
        'enable_yiqi_tiangan': True,
        'enable_yiqi_dizhi': True,
        'enable_sanhe': True,
        'enable_sanhui': True
    },
    'fate': {
        'enable_basic': True,
        'enable_advanced': True
    }
}

# 凶神判断设置
EVIL_SETTINGS = {
    'major_evils': [
        '天克地冲',
        '岁冲月破',
        '年月三煞',
        '阴府太岁',
        '年月克山'
    ],
    'minor_evils': [
        '日时相冲',
        '刑冲破害',
        '孤辰寡宿',
        '劫煞灾煞'
    ],
    'threshold': {
        'major_count': 1,     # 大凶数量阈值
        'minor_count': 3      # 中小凶数量阈值
    }
}

# 输出设置
OUTPUT_SETTINGS = {
    'display': {
        'table_width': 120,
        'max_warnings': 3,        # 最多显示的警告数
        'show_details': True      # 是否显示详细判断
    },
    'excel': {
        'auto_open': False,       # 生成后自动打开
        'include_details': True   # 包含详细判断
    }
}

# 评分设置
SCORING_SETTINGS = {
    'weights': {
        'dragon': 40,      # 补龙权重
        'mountain': 30,    # 扶山权重
        'fate': 20,        # 向主命权重
        'evil': 10         # 凶神权重（负分）
    },
    'thresholds': {
        'excellent': 80,   # 优秀
        'good': 60,        # 良好
        'acceptable': 40   # 可接受
    }
}