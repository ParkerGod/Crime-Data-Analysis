"""
分析目标6: 受害者年龄分布分析
- 受害者年龄直方图
- 年龄统计信息
"""
import pandas as pd
import numpy as np
from typing import Dict
from src.crime_analysis.config import Config
from src.crime_analysis.plotting import PlotManager


def analyze_victim_age_distribution(df: pd.DataFrame, config: Config = None) -> Dict:
    """
    分析受害者年龄分布

    Args:
        df: 包含特征的数据框
        config: 配置对象

    Returns:
        Dict: 包含统计结果和图表路径的字典
    """
    config = config or Config()
    plot_manager = PlotManager(config)

    results = {
        'title': '受害者年龄分布分析',
        'tables': {},
        'figures': [],
        'statistics': {}
    }

    # 检查是否有受害者年龄列
    if 'Vict Age' not in df.columns:
        results['error'] = '缺少受害者年龄列: Vict Age'
        return results

    # 过滤有效年龄数据 (0 < age <= 100)
    df_valid = df[(df['Vict Age'] > 0) & (df['Vict Age'] <= 100)].copy()

    if len(df_valid) == 0:
        results['error'] = '没有有效的受害者年龄数据'
        return results

    # 1. 年龄统计信息
    results['statistics']['total_valid_records'] = len(df_valid)
    results['statistics']['mean_age'] = round(df_valid['Vict Age'].mean(), 2)
    results['statistics']['median_age'] = round(df_valid['Vict Age'].median(), 2)
    results['statistics']['std_age'] = round(df_valid['Vict Age'].std(), 2)
    results['statistics']['min_age'] = int(df_valid['Vict Age'].min())
    results['statistics']['max_age'] = int(df_valid['Vict Age'].max())

    # 2. 年龄分组统计
    age_bins = [0, 18, 25, 35, 45, 55, 65, 100]
    age_labels = ['0-18', '19-25', '26-35', '36-45', '46-55', '56-65', '65+']
    df_valid['age_group'] = pd.cut(df_valid['Vict Age'], bins=age_bins, labels=age_labels, right=True)

    age_group_stats = df_valid['age_group'].value_counts().sort_index().reset_index()
    age_group_stats.columns = ['age_group', 'count']
    age_group_stats['percentage'] = (age_group_stats['count'] / len(df_valid) * 100).round(2)
    results['tables']['age_group_distribution'] = age_group_stats

    # 3. 绘制年龄分布直方图
    fig_path = plot_manager.plot_victim_age_histogram(df_valid)
    results['figures'].append(fig_path)

    return results
