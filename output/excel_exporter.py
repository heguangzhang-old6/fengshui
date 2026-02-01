# -*- coding: utf-8 -*-
"""
Excel导出模块
=====================================
【模块说明】
将择日结果导出到Excel文件。

【功能】
1. 生成Excel报告
2. 包含多工作表
3. 格式化输出

【版本信息】
- 版本：v1.0
- 最后更新：2026-01-24
"""

import os
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd


class ExcelExporter:
    """Excel导出器"""

    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def export(self, good_results: List[Dict],
               bad_results: List[Dict] = None,
               conditions: Dict = None) -> str:
        """导出到Excel"""

        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"择日报告_{timestamp}.xlsx"
        filepath = os.path.join(self.output_dir, filename)

        # 创建Excel写入器
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:

            # 1. 写入摘要信息
            self._write_summary(writer, conditions, good_results, bad_results)

            # 2. 写入可用时辰
            if good_results:
                self._write_good_results(writer, good_results)

            # 3. 写入大凶时辰
            if bad_results:
                self._write_bad_results(writer, bad_results)

            # 4. 写入详细判断
            if good_results:
                self._write_detailed_judgments(writer, good_results)

        return filepath

    def _write_summary(self, writer, conditions, good_results, bad_results):
        """写入摘要信息"""
        summary_data = []

        if conditions:
            summary_data.append(['龙', conditions.get('dragon', '')])
            summary_data.append(['山', conditions.get('mountain', '')])
            summary_data.append(['主命', conditions.get('fate', '')])
            summary_data.append(['择日天数', conditions.get('days', '')])

        summary_data.append(['生成时间', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        summary_data.append(['可用时辰数', len(good_results)])
        summary_data.append(['大凶时辰数', len(bad_results) if bad_results else 0])

        df = pd.DataFrame(summary_data, columns=['项目', '值'])
        df.to_excel(writer, sheet_name='摘要', index=False)

    def _write_good_results(self, writer, good_results):
        """写入可用时辰"""
        rows = []
        for result in good_results:
            judgments = result.get('judgments', {})
            evil_judge = judgments.get('evil', {})

            row = {
                '日期时间': result['datetime'],
                '八字': result['bazi'],
                '补龙': '是' if judgments.get('dragon', {}).get('suitable') else '否',
                '扶山': '是' if judgments.get('mountain', {}).get('suitable') else '否',
                '向主命': '是' if judgments.get('fate', {}).get('suitable') else '否',
                '安全等级': evil_judge.get('safety_level', '未知'),
                '建议': result.get('recommendation', ''),
                '补龙格局': ', '.join(judgments.get('dragon', {}).get('patterns', [])),
                '扶山格局': ', '.join(judgments.get('mountain', {}).get('patterns', [])),
                '向主命格局': ', '.join(judgments.get('fate', {}).get('patterns', [])),
                '大凶': ', '.join(evil_judge.get('major_evils', [])),
                '中小凶': ', '.join(evil_judge.get('minor_evils', []))
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        df.to_excel(writer, sheet_name='可用时辰', index=False)

    def _write_bad_results(self, writer, bad_results):
        """写入大凶时辰"""
        rows = []
        for result in bad_results:
            row = {
                '日期时间': result['datetime'],
                '八字': result['bazi'],
                '警告': '; '.join(result.get('warnings', []))[:200]  # 限制长度
            }
            rows.append(row)

        df = pd.DataFrame(rows)
        df.to_excel(writer, sheet_name='大凶时辰', index=False)

    def _write_detailed_judgments(self, writer, good_results):
        """写入详细判断"""
        # TODO: 实现详细判断的写入
        pass