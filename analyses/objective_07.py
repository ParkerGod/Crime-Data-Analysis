"""
分析目标7: 犯罪状态分布分析
- 按状态描述统计犯罪数量
- 状态分布可视化
"""
import pandas as pd
import numpy as np
from typing import Dict
from src.crime_analysis.config import Config
from src.crime_analysis.plotting import PlotManager


def analyze_crime_status_distribution(df: pd.DataFrame, config: Config = None) -> Dict:
    """
    分析犯罪状态分布

    Args:
        df: 包含特征的数据框
        config: 配置对象

    Returns:
        Dict: 包含统计结果和图表路径的字典
    """
    config = config or Config()
    plot_manager = PlotManager(config)

    results = {
        'title': '犯罪状态分布分析',
        'tables': {},
        'figures': [],
        'statistics': {}
    }

    # 检查是否有状态描述列
    status_col = 'Status Desc'
    if status_col not in df.columns:
        results['error'] = f'缺少状态描述列: {status_col}'
        return results

    # 1. 状态分布统计
    status_counts = df[status_col].value_counts().reset_index()
    status_counts.columns = ['status', 'count']
    status_counts['percentage'] = (status_counts['count'] / len(df) * 100).round(2)
    results['tables']['status_distribution'] = status_counts

    # 2. 统计信息
    results['statistics']['total_status_types'] = len(status_counts)
    results['statistics']['most_common_status'] = status_counts.iloc[0]['status']
    results['statistics']['most_common_count'] = int(status_counts.iloc[0]['count'])
    results['statistics']['most_common_percentage'] = status_counts.iloc[0]['percentage']

    # 3. 绘制状态分布图
    fig_path = plot_manager.plot_crime_status_distribution(df)
    results['figures'].append(fig_path)

    return results
