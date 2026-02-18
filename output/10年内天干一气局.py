import pandas as pd
from core.bazi_generator import generate_odd_hour_sequence
import datetime
import numpy as np


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

    # 3. 提取天干地支成分
    df['year_gan'] = df['year_gz'].str[0]  # 年柱天干
    df['year_zhi'] = df['year_gz'].str[1]  # 年柱地支
    df['month_gan'] = df['month_gz'].str[0]
    df['month_zhi'] = df['month_gz'].str[1]
    df['day_gan'] = df['day_gz'].str[0]
    df['day_zhi'] = df['day_gz'].str[1]
    df['hour_gan'] = df['hour_gz'].str[0]
    df['hour_zhi'] = df['hour_gz'].str[1]

    # 4. 判断天干一气局
    df['is_tiangan_yiqi'] = (
            (df['year_gan'] == df['month_gan']) &
            (df['month_gan'] == df['day_gan']) &
            (df['day_gan'] == df['hour_gan'])
    )

    # 5. 判断地支一气局
    df['is_dizhi_yiqi'] = (
            (df['year_zhi'] == df['month_zhi']) &
            (df['month_zhi'] == df['day_zhi']) &
            (df['day_zhi'] == df['hour_zhi'])
    )

    # 6. 综合判断（天干一气或地支一气）
    df['is_yiqi'] = df['is_tiangan_yiqi'] | df['is_dizhi_yiqi']

    # 7. 添加类型标签
    df['pattern_type'] = np.where(
        df['is_tiangan_yiqi'] & df['is_dizhi_yiqi'], '天干地支双一气',
        np.where(df['is_tiangan_yiqi'], '天干一气局',
                 np.where(df['is_dizhi_yiqi'], '地支一气局', '普通八字'))
    )

    return df


def find_future_yiqi_patterns(years_ahead=10):
    """查找从当前时间开始未来指定年数内的一气局"""

    print(f"开始查找未来{years_ahead}年内的天干一气局和地支一气局...")

    # 设置时间范围
    current_date = datetime.date.today()
    end_date = current_date + datetime.timedelta(days=years_ahead * 365)

    print(f"时间范围: {current_date} 到 {end_date}")

    try:
        # 生成未来指定年数的八字数据
        total_days = (end_date - current_date).days
        df = process_bazi_data(current_date, days=total_days)

        # 筛选一气局（天干一气或地支一气）
        yiqi_df = df[df['is_yiqi']].copy()

        if not yiqi_df.empty:
            # 按类型分类统计
            type_stats = yiqi_df['pattern_type'].value_counts()

            print(f"\n查找完成！总共找到 {len(yiqi_df)} 个一气局")
            print("\n各类型分布统计:")
            for pattern_type, count in type_stats.items():
                print(f"  {pattern_type}: {count} 个")

            # 天干一气局统计
            tiangan_count = yiqi_df['is_tiangan_yiqi'].sum()
            print(f"\n天干一气局: {tiangan_count} 个")

            # 地支一气局统计
            dizhi_count = yiqi_df['is_dizhi_yiqi'].sum()
            print(f"地支一气局: {dizhi_count} 个")

            return yiqi_df
        else:
            print("未找到任何一气局")
            return pd.DataFrame()

    except Exception as e:
        print(f"查找过程中出错: {e}")
        return pd.DataFrame()


def analyze_yiqi_patterns(df):
    """分析一气局的详细规律"""

    if df.empty:
        print("没有数据可分析")
        return

    print("\n=== 一气局详细分析 ===")

    # 1. 时间分布分析
    df['datetime_obj'] = pd.to_datetime(df['datetime'])
    df['year'] = df['datetime_obj'].dt.year
    df['month'] = df['datetime_obj'].dt.month
    df['day'] = df['datetime_obj'].dt.day
    df['hour'] = df['datetime_obj'].dt.hour

    # 按年份分布
    yearly_dist = df.groupby('year').size()
    print("\n按年份分布:")
    for year, count in yearly_dist.items():
        print(f"  {year}年: {count} 个")

    # 按月份分布
    monthly_dist = df.groupby('month').size().sort_index()
    print("\n按月份分布:")
    month_names = ['一月', '二月', '三月', '四月', '五月', '六月',
                   '七月', '八月', '九月', '十月', '十一月', '十二月']
    for month, count in monthly_dist.items():
        print(f"  {month_names[month - 1]}: {count} 个")

    # 按时辰分布
    hourly_dist = df.groupby('hour').size().sort_index()
    print("\n按时辰分布:")
    for hour, count in hourly_dist.items():
        print(f"  {hour:02d}:00: {count} 个")

    # 2. 类型详细分析
    print("\n=== 类型详细分析 ===")

    # 天干一气局分析
    tiangan_df = df[df['is_tiangan_yiqi']]
    if not tiangan_df.empty:
        print(f"\n天干一气局 ({len(tiangan_df)} 个):")
        gan_stats = tiangan_df.groupby('year_gan').size().sort_values(ascending=False)
        print("天干分布:")
        for gan, count in gan_stats.items():
            print(f"  {gan}天干: {count} 个")

    # 地支一气局分析
    dizhi_df = df[df['is_dizhi_yiqi']]
    if not dizhi_df.empty:
        print(f"\n地支一气局 ({len(dizhi_df)} 个):")
        zhi_stats = dizhi_df.groupby('year_zhi').size().sort_values(ascending=False)
        print("地支分布:")
        for zhi, count in zhi_stats.items():
            print(f"  {zhi}地支: {count} 个")


def save_yiqi_report(df, filename=None):
    """保存详细的分析报告"""

    if df.empty:
        print("没有数据可保存")
        return

    if filename is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"一气局分析报告_{timestamp}.xlsx"

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 1. 完整数据
        df.to_excel(writer, sheet_name='完整数据', index=False)

        # 2. 天干一气局
        tiangan_df = df[df['is_tiangan_yiqi']].copy()
        if not tiangan_df.empty:
            tiangan_df.to_excel(writer, sheet_name='天干一气局', index=False)

        # 3. 地支一气局
        dizhi_df = df[df['is_dizhi_yiqi']].copy()
        if not dizhi_df.empty:
            dizhi_df.to_excel(writer, sheet_name='地支一气局', index=False)

        # 4. 统计汇总
        summary_data = []

        # 总体统计
        total_count = len(df)
        tiangan_count = df['is_tiangan_yiqi'].sum()
        dizhi_count = df['is_dizhi_yiqi'].sum()

        summary_data.append({
            '类别': '总计',
            '数量': total_count,
            '占比(%)': 100.0
        })
        summary_data.append({
            '类别': '天干一气局',
            '数量': tiangan_count,
            '占比(%)': round(tiangan_count / total_count * 100, 2)
        })
        summary_data.append({
            '类别': '地支一气局',
            '数量': dizhi_count,
            '占比(%)': round(dizhi_count / total_count * 100, 2)
        })

        # 天干分布（如果是天干一气局）
        if tiangan_count > 0:
            gan_stats = df[df['is_tiangan_yiqi']].groupby('year_gan').size()
            for gan, count in gan_stats.items():
                summary_data.append({
                    '类别': f'{gan}天干一气',
                    '数量': count,
                    '占比(%)': round(count / total_count * 100, 2)
                })

        # 地支分布（如果是地支一气局）
        if dizhi_count > 0:
            zhi_stats = df[df['is_dizhi_yiqi']].groupby('year_zhi').size()
            for zhi, count in zhi_stats.items():
                summary_data.append({
                    '类别': f'{zhi}地支一气',
                    '数量': count,
                    '占比(%)': round(count / total_count * 100, 2)
                })

        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='统计汇总', index=False)

        # 5. 时间分布
        df['year_only'] = pd.to_datetime(df['datetime']).dt.year
        yearly_dist = df.groupby('year_only').size()
        yearly_df = pd.DataFrame({
            '年份': yearly_dist.index,
            '数量': yearly_dist.values
        })
        yearly_df.to_excel(writer, sheet_name='年份分布', index=False)

    print(f"分析报告已保存到: {filename}")


def display_sample_results(df, sample_size=20):
    """显示样本结果"""

    if df.empty:
        print("没有数据可显示")
        return

    print(f"\n=== 前{sample_size}个一气局示例 ===")
    print(f"{'序号':<4} {'日期时间':<20} {'八字':<25} {'类型':<15}")
    print("-" * 65)

    for idx, (i, row) in enumerate(df.head(sample_size).iterrows()):
        print(f"{idx + 1:<4} {row['datetime']:<20} {row['bazi']:<25} {row['pattern_type']:<15}")


if __name__ == "__main__":
    # 查找未来10年内的所有一气局
    yiqi_df = find_future_yiqi_patterns(years_ahead=10)

    # 分析规律
    analyze_yiqi_patterns(yiqi_df)

    # 保存详细报告
    save_yiqi_report(yiqi_df)

    # 显示样本结果
    display_sample_results(yiqi_df)

    # 显示详细信息
    if not yiqi_df.empty:
        print(f"\n=== 详细统计 ===")
        print(f"总数量: {len(yiqi_df)} 个")
        print(f"天干一气局: {yiqi_df['is_tiangan_yiqi'].sum()} 个")
        print(f"地支一气局: {yiqi_df['is_dizhi_yiqi'].sum()} 个")
        print(f"双重一气局: {((yiqi_df['is_tiangan_yiqi']) & (yiqi_df['is_dizhi_yiqi'])).sum()} 个")
