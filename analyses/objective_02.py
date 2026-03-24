"""
分析目标2: Top 10犯罪类别分析
- 犯罪类型分布统计
- Top 10犯罪类别条形图
"""
import pandas as pd
import numpy as np
from typing import Dict
from src.crime_analysis.config import Config
from src.crime_analysis.plotting import PlotManager


def analyze_crime_types(df: pd.DataFrame, config: Config = None) -> Dict:
    """
    分析Top 10犯罪类别
    对应原代码中的目标1: Analyze and Visualize Top 10 Crime Categories

    Args:
        df: 包含特征的数据框
        config: 配置对象

    Returns:
        Dict: 包含统计结果和图表路径的字典
    """
    config = config or Config()
    plot_manager = PlotManager(config)
    crime_col = config.crime_type_column

    results = {
        'title': 'Top 10犯罪类别分析',
        'tables': {},
        'figures': [],
        'statistics': {}
    }

    if crime_col not in df.columns:
        results['error'] = f'缺少犯罪类型列: {crime_col}'
        return results

    # 1. 犯罪类型统计
    crime_counts = df[crime_col].value_counts()
    top10 = crime_counts.head(10).reset_index()
    top10.columns = ['crime_type', 'count']
    top10['percentage'] = (top10['count'] / len(df) * 100).round(2)

    # 简化的标签映射（与原代码一致）
    short_labels = {
        'VEHICLE - STOLEN': 'Stolen Vehicle',
        'BATTERY - SIMPLE ASSAULT': 'Battery Assault',
        'BURGLARY FROM VEHICLE': 'Burglary (Vehicle)',
        'VANDALISM - FELONY ($400 & OVER, ALL CHURCH VANDALISMS)': 'Felony Vandalism',
        'ASSAULT WITH DEADLY WEAPON, AGGRAVATED ASSAULT': 'Aggr. Assault w/ Weapon',
        'INTIMATE PARTNER - SIMPLE ASSAULT': 'IP Assault',
        'BURGLARY': 'Burglary',
        'THEFT PLAIN - PETTY ($950 & UNDER)': 'Petty Theft',
        'THEFT FROM MOTOR VEHICLE - PETTY ($950 & UNDER)': 'Theft from Vehicle',
        'VANDALISM - MISDEMEANOR ($399 OR UNDER)': 'Misdemeanor Vandalism'
    }
    top10['short_label'] = top10['crime_type'].map(short_labels).fillna(top10['crime_type'])

    results['tables']['top10_crimes'] = top10

    # 2. 统计信息
    results['statistics']['total_crime_types'] = len(crime_counts)
    results['statistics']['top_crime'] = top10.iloc[0]['crime_type']
    results['statistics']['top_crime_count'] = int(top10.iloc[0]['count'])
    results['statistics']['top_crime_percentage'] = top10.iloc[0]['percentage']
    results['statistics']['top10_total_percentage'] = round(top10['percentage'].sum(), 2)

    # 3. 绘制Top 10犯罪类别图
    fig_path = plot_manager.plot_top10_crime_categories(top10)
    results['figures'].append(fig_path)

    return results
