# -*- coding: utf-8 -*-
"""
显示管理模块
=====================================
【模块说明】
负责在控制台或界面显示择日结果。

【功能】
1. 显示择日结果表格
2. 显示详细判断信息
3. 显示警告和建议

【版本信息】
- 版本：v1.0
- 最后更新：2026-01-24
"""

from typing import List, Dict, Any
import textwrap


class DisplayManager:
    """显示管理器"""

    def __init__(self):
        self.table_width = 120

    def show_results(self, good_results: List[Dict],
                     conditions: Dict, bad_results: List[Dict] = None):
        """显示择日结果"""

        # 显示条件
        self._show_conditions(conditions)

        # 显示大凶结果（如果存在）
        if bad_results:
            self._show_bad_results(bad_results)

        # 显示可用结果
        if good_results:
            self._show_good_results(good_results)
        else:
            print("\n未找到合适的择日时辰")

    def _show_conditions(self, conditions: Dict):
        """显示输入条件"""
        print("\n择日条件:")
        print("-" * 40)
        print(f"龙: {conditions.get('dragon', '未指定')}")
        print(f"山: {conditions.get('mountain', '未指定')}")
        print(f"主命: {conditions.get('fate', '未指定')}")
        print(f"择日天数: {conditions.get('days', 10)}天")
        print("-" * 40)

    def _show_bad_results(self, bad_results: List[Dict]):
        """显示大凶结果"""
        print(f"\n⚠️  发现 {len(bad_results)} 个大凶时辰，已排除:")
        for i, result in enumerate(bad_results[:5], 1):
            print(f"  {i}. {result['datetime']} - {result['bazi']}")
            if result.get('warnings'):
                for warning in result['warnings'][:2]:
                    print(f"     {warning}")

        if len(bad_results) > 5:
            print(f"  ... 还有 {len(bad_results) - 5} 个大凶时辰")

    def _show_good_results(self, good_results: List[Dict]):
        """显示可用结果"""
        print(f"\n✅ 找到 {len(good_results)} 个可用时辰:")
        print("=" * self.table_width)

        # 表头
        header = f"{'序号':<4} {'日期时间':<16} {'八字':<20} {'补龙':<10} {'扶山':<10} {'向主命':<10} {'安全':<8} {'建议':<20}"
        print(header)
        print("-" * self.table_width)

        # 数据行
        for i, result in enumerate(good_results, 1):
            row = self._format_result_row(i, result)
            print(row)

            # 显示警告（如果有）
            if result.get('warnings'):
                for warning in result['warnings']:
                    wrapped = textwrap.fill(
                        f"    ⚠️ {warning}",
                        width=self.table_width
                    )
                    print(wrapped)

        print("=" * self.table_width)

    def _format_result_row(self, index: int, result: Dict) -> str:
        """格式化结果行"""
        judgments = result.get('judgments', {})

        dragon_judge = judgments.get('dragon', {})
        mountain_judge = judgments.get('mountain', {})
        fate_judge = judgments.get('fate', {})
        evil_judge = judgments.get('evil', {})

        # 简化的显示
        dragon_status = "✓" if dragon_judge.get('suitable') else "○"
        mountain_status = "✓" if mountain_judge.get('suitable') else "○"
        fate_status = "✓" if fate_judge.get('suitable') else "○"
        safety = evil_judge.get('safety_level', '未知')
        recommendation = result.get('recommendation', '')

        row = (
            f"{index:<4} "
            f"{result['datetime']:<16} "
            f"{result['bazi']:<20} "
            f"{dragon_status:<10} "
            f"{mountain_status:<10} "
            f"{fate_status:<10} "
            f"{safety:<8} "
            f"{recommendation:<20}"
        )

        return row

    def show_detailed_judgment(self, result: Dict):
        """显示详细判断信息"""
        print(f"\n详细判断 - {result['datetime']} {result['bazi']}")
        print("=" * 60)

        judgments = result.get('judgments', {})

        # 补龙判断
        if 'dragon' in judgments:
            self._show_judgment_detail("补龙判断", judgments['dragon'])

        # 扶山判断
        if 'mountain' in judgments:
            self._show_judgment_detail("扶山判断", judgments['mountain'])

        # 向主命判断
        if 'fate' in judgments:
            self._show_judgment_detail("向主命判断", judgments['fate'])

        # 凶神判断
        if 'evil' in judgments:
            self._show_evil_detail("凶神判断", judgments['evil'])

    def _show_judgment_detail(self, title: str, judgment: Dict):
        """显示判断详情"""
        print(f"\n{title}:")
        print(f"  合适: {'是' if judgment.get('suitable') else '否'}")
        print(f"  得分: {judgment.get('score', 0)}")

        patterns = judgment.get('patterns', [])
        if patterns:
            print(f"  格局: {', '.join(patterns)}")

    def _show_evil_detail(self, title: str, evil_judgment: Dict):
        """显示凶神详情"""
        print(f"\n{title}:")
        print(f"  安全等级: {evil_judgment.get('safety_level', '未知')}")

        major = evil_judgment.get('major_evils', [])
        if major:
            print(f"  大凶: {', '.join(major)}")

        minor = evil_judgment.get('minor_evils', [])
        if minor:
            print(f"  中小凶: {', '.join(minor)}")