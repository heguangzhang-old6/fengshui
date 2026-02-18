import pandas as pd
from core.bazi_generator import generate_odd_hour_sequence
import datetime


def process_bazi_data(start_date, days=10):
    """完整的八字数据处理管道"""

    # 1. 生成原始数据
    bazi_list = generate_odd_hour_sequence(
        start_date=start_date,
        days=days,
        hour_interval=2,
        use_continuous=True
    )

    # 2. 转换为 DataFrame
    df = pd.DataFrame(bazi_list)

    return df

if __name__ == "__main__":
    # 使用示例
    start_date = datetime.date(2026, 2, 16)
    df = process_bazi_data(start_date, days=365)
    # 提取天干地支成分
    df['year_gan'] = df['year_gz'].str[0]  # 年柱天干
    df['year_zhi'] = df['year_gz'].str[1]  # 年柱地支
    df['month_gan'] = df['month_gz'].str[0]
    df['month_zhi'] = df['month_gz'].str[1]
    df['day_gan'] = df['day_gz'].str[0]
    df['day_zhi'] = df['day_gz'].str[1]
    df['hour_gan'] = df['hour_gz'].str[0]
    df['hour_zhi'] = df['hour_gz'].str[1]
    print("处理结果概览:")
    print(df.head().columns)
    print(df.head())
    # 保存到 Excel
    output_file = "bazi_analysis.xlsx"
    df.to_excel(output_file, index=False, sheet_name="八字数据")

    print(f"数据已保存到: {output_file}")

    # 如果需要多个工作表的复杂分析
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 原始数据
        df.to_excel(writer, sheet_name='原始数据', index=False)
