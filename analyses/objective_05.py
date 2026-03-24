"""
分析目标5: 受害者年龄分布分析（按犯罪类型和性别）
- Top 5犯罪类型的受害者年龄分布
- 按性别分类的散点图
"""
import pandas as pd
import numpy as np
from typing import Dict
from src.crime_analysis.config import Config
from src.crime_analysis.plotting import PlotManager


def analyze_arrest_patterns(df: pd.DataFrame, config: Config = None) -> Dict:
    """
    分析受害者年龄分布（按犯罪类型和性别）
    对应原代码中的目标4: Victim Age Distribution by Crime Type and Gender

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
        'title': '受害者年龄分布分析（按犯罪类型和性别）',
        'tables': {},
        'figures': [],
        'statistics': {}
    }

    # 检查必要列
    if 'Vict Age' not in df.columns:
        results['error'] = '缺少受害者年龄列: Vict Age'
        return results

    if crime_col not in df.columns:
        results['error'] = f'缺少犯罪类型列: {crime_col}'
        return results

    # 过滤有效年龄数据 (0 < age <= 100)
    df_valid = df[(df['Vict Age'] > 0) & (df['Vict Age'] <= 100)].copy()

    if len(df_valid) == 0:
        results['error'] = '没有有效的受害者年龄数据'
        return results

    # 1. 获取Top 5犯罪类型
    top5_crimes = df_valid[crime_col].value_counts().head(5).index.tolist()
    df_top5 = df_valid[df_valid[crime_col].isin(top5_crimes)].copy()

    results['statistics']['top5_crimes'] = top5_crimes
    results['statistics']['total_records_analyzed'] = len(df_top5)

    # 2. 按犯罪类型和性别统计
    if 'Vict Sex' in df_top5.columns:
        stats_by_crime_gender = df_top5.groupby([crime_col, 'Vict Sex'])['Vict Age'].agg([
            'count', 'mean', 'median', 'std'
        ]).reset_index()
        stats_by_crime_gender.columns = ['crime_type', 'victim_sex', 'count', 'mean_age', 'median_age', 'std_age']
        results['tables']['stats_by_crime_gender'] = stats_by_crime_gender

        # 性别分布
        gender_dist = df_top5['Vict Sex'].value_counts().reset_index()
        gender_dist.columns = ['sex', 'count']
        gender_dist['percentage'] = (gender_dist['count'] / len(df_top5) * 100).round(2)
        results['tables']['gender_distribution'] = gender_dist

    # 3. 按犯罪类型统计年龄
    age_by_crime = df_top5.groupby(crime_col)['Vict Age'].agg([
        'count', 'mean', 'median', 'std', 'min', 'max'
    ]).reset_index()
    age_by_crime.columns = ['crime_type', 'count', 'mean_age', 'median_age', 'std_age', 'min_age', 'max_age']
    age_by_crime = age_by_crime.round(2)
    results['tables']['age_by_crime_type'] = age_by_crime

    # 4. 绘制散点图
    fig_path = plot_manager.plot_victim_age_by_crime_gender(df_top5)
    results['figures'].append(fig_path)

    return results
