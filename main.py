# -*- coding: utf-8 -*-
"""
风水择日系统主程序
=====================================
【模块说明】
风水择日系统主程序，协调各个模块完成择日任务。

【核心流程】
1. 接收用户输入（龙、山、主命、时间段）
2. 生成八字序列
3. 进行吉凶判断
4. 输出结果

【版本信息】
- 版本：v1.0
- 最后更新：2026-01-24
"""

import datetime
import argparse
from typing import Dict, List, Tuple, Any

# 导入自定义模块
from core.bazi_generator import generate_odd_hour_sequence
from conditions.dragon_judge import DragonJudge
from conditions.mountain_judge import MountainJudge
from conditions.fate_judge import FateJudge
from conditions.evil_judge import EvilJudge
from output.display import DisplayManager
from output.excel_exporter import ExcelExporter
from utils.validator import InputValidator
from utils.logger import setup_logger


class FengShuiZeriSystem:
    """风水择日系统主类"""

    def __init__(self):
        """初始化系统"""
        self.logger = setup_logger("fengshui_zeri")
        self.validator = InputValidator()

        # 初始化判断器
        self.dragon_judge = DragonJudge()
        self.mountain_judge = MountainJudge()
        self.fate_judge = FateJudge()
        self.evil_judge = EvilJudge()

        # 初始化输出器
        self.display = DisplayManager()
        self.excel_exporter = ExcelExporter()

        # 存储结果
        self.results = []

    def get_user_input(self) -> Dict[str, Any]:
        """获取用户输入"""
        print("=" * 60)
        print("风水择日系统")
        print("=" * 60)

        # 这里可以替换为GUI输入或命令行参数
        user_input = {}

        # 基础条件输入
        user_input['dragon'] = input("请输入龙（如：甲辰龙）: ").strip()
        user_input['mountain'] = input("请输入山（如：壬山丙向）: ").strip()
        user_input['fate'] = input("请输入主命（如：戊午年）: ").strip()

        # 时间段输入
        days_input = input("请输入择日天数（默认10天）: ").strip()
        user_input['days'] = int(days_input) if days_input else 10

        # 验证输入
        if not self.validator.validate_input(user_input):
            raise ValueError("输入条件不合法，请重新输入")

        return user_input

    def generate_bazi_sequence(self, start_date: datetime.date, days: int) -> List[Dict]:
        """生成八字序列"""
        self.logger.info(f"开始生成八字序列，起始日期：{start_date}，天数：{days}")

        # 生成奇数小时八字序列
        bazi_list = generate_odd_hour_sequence(
            start_date=start_date,
            days=days,
            hour_interval=2,
            use_continuous=True
        )

        self.logger.info(f"成功生成 {len(bazi_list)} 个八字")
        return bazi_list

    def judge_bazi(self, bazi_item: Dict, conditions: Dict) -> Dict:
        """判断单个八字的吉凶"""
        result = {
            'datetime': bazi_item['datetime'],
            'bazi': bazi_item['bazi'],
            'judgments': {},
            'scores': {},
            'warnings': [],
            'recommendation': None
        }

        try:
            # 提取八字四柱
            year_gz, month_gz, day_gz, hour_gz = bazi_item['bazi'].split()

            # 1. 补龙吉局判断
            dragon_result = self.dragon_judge.judge(
                bazi=(year_gz, month_gz, day_gz, hour_gz),
                dragon=conditions['dragon']
            )
            result['judgments']['dragon'] = dragon_result

            # 2. 扶山吉局判断
            mountain_result = self.mountain_judge.judge(
                bazi=(year_gz, month_gz, day_gz, hour_gz),
                mountain=conditions['mountain']
            )
            result['judgments']['mountain'] = mountain_result

            # 3. 向主命吉局判断
            fate_result = self.fate_judge.judge(
                bazi=(year_gz, month_gz, day_gz, hour_gz),
                fate=conditions['fate']
            )
            result['judgments']['fate'] = fate_result

            # 4. 凶神恶煞判断
            evil_result = self.evil_judge.judge_all(
                bazi=(year_gz, month_gz, day_gz, hour_gz),
                conditions=conditions
            )
            result['judgments']['evil'] = evil_result
            result['warnings'] = evil_result.get('warnings', [])

            # 5. 综合评分
            result['scores'] = self._calculate_scores(
                dragon_result, mountain_result, fate_result, evil_result
            )

            # 6. 生成建议
            result['recommendation'] = self._generate_recommendation(result)

        except Exception as e:
            self.logger.error(f"判断八字 {bazi_item['datetime']} 时出错: {e}")
            result['error'] = str(e)

        return result

    def _calculate_scores(self, dragon_result, mountain_result,
                          fate_result, evil_result) -> Dict:
        """计算综合评分"""
        # TODO: 实现评分算法
        scores = {
            'dragon_score': 0,
            'mountain_score': 0,
            'fate_score': 0,
            'evil_score': 0,
            'total_score': 0
        }
        return scores

    def _generate_recommendation(self, result: Dict) -> str:
        """生成建议"""
        # TODO: 根据判断结果生成建议
        if result['warnings']:
            return "需谨慎考虑"
        return "可供选择"

    def filter_results(self, results: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """过滤结果，分离大凶和其他"""
        very_bad = []
        others = []

        for result in results:
            # 判断是否为大凶（例如有天克地冲等大凶之象）
            is_very_bad = False
            evil_judgment = result['judgments'].get('evil', {})

            if 'major_evils' in evil_judgment and evil_judgment['major_evils']:
                is_very_bad = True

            if is_very_bad:
                very_bad.append(result)
            else:
                others.append(result)

        return others, very_bad

    def run(self):
        """运行主程序"""
        try:
            # 1. 获取用户输入
            conditions = self.get_user_input()

            # 2. 从当前时间开始
            start_date = datetime.date.today()

            # 3. 生成八字序列
            bazi_list = self.generate_bazi_sequence(start_date, conditions['days'])

            # 4. 逐个判断八字
            self.logger.info("开始进行吉凶判断...")
            for bazi_item in bazi_list:
                result = self.judge_bazi(bazi_item, conditions)
                self.results.append(result)

            # 5. 过滤结果
            good_results, bad_results = self.filter_results(self.results)

            # 6. 输出结果
            print("\n" + "=" * 60)
            print("择日结果")
            print("=" * 60)

            # 显示界面输出
            self.display.show_results(good_results, conditions, bad_results)

            # 导出Excel
            excel_path = self.excel_exporter.export(
                good_results, bad_results, conditions
            )
            print(f"\n结果已导出到: {excel_path}")

            self.logger.info("择日完成")

        except Exception as e:
            self.logger.error(f"系统运行出错: {e}")
            print(f"错误: {e}")
            return False

        return True


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='风水择日系统')
    parser.add_argument('--debug', action='store_true', help='调试模式')
    parser.add_argument('--log', type=str, default='fengshui.log', help='日志文件')

    args = parser.parse_args()

    # 创建并运行系统
    system = FengShuiZeriSystem()
    success = system.run()

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())