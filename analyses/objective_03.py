"""
分析目标3: 月度犯罪趋势分析
- 按月份统计犯罪数量
- 月度趋势条形图
"""
import pandas as pd
import numpy as np
from typing import Dict
from src.crime_analysis.config import Config
from src.crime_analysis.plotting import PlotManager


def analyze_temporal_patterns(df: pd.DataFrame, config: Config = None) -> Dict:
    """
    分析月度犯罪趋势
    对应原代码中的目标2: Time-Series Analysis of Crime Trends by Month

    Args:
        df: 包含特征的数据框
        config: 配置对象

    Returns:
        Dict: 包含统计结果和图表路径的字典
    """
    config = config or Config()
    plot_manager = PlotManager(config)

    results = {
        'title': '月度犯罪趋势分析',
        'tables': {},
        'figures': [],
        'statistics': {}
    }

    # 检查是否有月份列
    if 'month' not in df.columns:
        results['error'] = '缺少月份列'
        return results

    # 1. 按月份统计犯罪数量
    monthly_counts = df.groupby('month').size().reset_index(name='count')
    monthly_counts['percentage'] = (monthly_counts['count'] / len(df) * 100).round(2)

    # 添加月份名称
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_counts['month_name'] = [month_names[i-1] for i in monthly_counts['month']]

    results['tables']['monthly_trends'] = monthly_counts

    # 2. 统计信息
    peak_month = monthly_counts.loc[monthly_counts['count'].idxmax(), 'month_name']
    low_month = monthly_counts.loc[monthly_counts['count'].idxmin(), 'month_name']
    results['statistics']['peak_month'] = peak_month
    results['statistics']['lowest_month'] = low_month
    results['statistics']['peak_count'] = int(monthly_counts['count'].max())
    results['statistics']['lowest_count'] = int(monthly_counts['count'].min())

    # 3. 绘制月度趋势图
    fig_path = plot_manager.plot_monthly_crime_trends(monthly_counts)
    results['figures'].append(fig_path)

    return results
