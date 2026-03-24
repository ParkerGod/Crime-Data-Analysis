"""
分析目标1: 犯罪趋势分析
- 年度趋势统计
- 年度趋势折线图
"""
import pandas as pd
import numpy as np
from typing import Dict
from src.crime_analysis.config import Config
from src.crime_analysis.plotting import PlotManager


def analyze_crime_trends(df: pd.DataFrame, config: Config = None) -> Dict:
    """
    分析犯罪趋势（年度趋势）

    Args:
        df: 包含特征的数据框
        config: 配置对象

    Returns:
        Dict: 包含统计结果和图表路径的字典
    """
    config = config or Config()
    plot_manager = PlotManager(config)

    results = {
        'title': '犯罪趋势分析',
        'tables': {},
        'figures': [],
        'statistics': {}
    }

    # 检查是否有年份列
    if 'year' not in df.columns:
        results['error'] = '缺少年份列'
        return results

    # 1. 年度趋势统计
    yearly_stats = df.groupby('year').size().reset_index(name='count')
    yearly_stats['growth_rate'] = yearly_stats['count'].pct_change() * 100
    results['tables']['yearly_trend'] = yearly_stats

    # 2. 统计信息
    results['statistics']['total_years'] = len(yearly_stats)
    results['statistics']['max_year'] = int(yearly_stats.loc[yearly_stats['count'].idxmax(), 'year'])
    results['statistics']['min_year'] = int(yearly_stats.loc[yearly_stats['count'].idxmin(), 'year'])
    results['statistics']['max_count'] = int(yearly_stats['count'].max())
    results['statistics']['min_count'] = int(yearly_stats['count'].min())

    if len(yearly_stats) > 1:
        results['statistics']['avg_annual_growth'] = round(yearly_stats['growth_rate'].mean(), 2)

    # 3. 绘制年度趋势图
    fig_path = plot_manager.plot_yearly_crime_trend(yearly_stats)
    results['figures'].append(fig_path)

    return results
