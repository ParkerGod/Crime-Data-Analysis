"""
分析目标8: 2020年各区域月度犯罪趋势分析
- 按区域统计月度犯罪数量
- 时间序列趋势图
"""
import pandas as pd
import numpy as np
from typing import Dict
from src.crime_analysis.config import Config
from src.crime_analysis.plotting import PlotManager


def analyze_monthly_trends_by_area(df: pd.DataFrame, config: Config = None) -> Dict:
    """
    分析2020年各区域月度犯罪趋势

    Args:
        df: 包含特征的数据框
        config: 配置对象

    Returns:
        Dict: 包含统计结果和图表路径的字典
    """
    config = config or Config()
    plot_manager = PlotManager(config)

    results = {
        'title': '2020年各区域月度犯罪趋势分析',
        'tables': {},
        'figures': [],
        'statistics': {}
    }

    # 检查必要列
    if 'Year' not in df.columns or 'Month' not in df.columns:
        results['error'] = '缺少年份或月份列'
        return results

    if 'AREA NAME' not in df.columns:
        results['error'] = '缺少区域名称列: AREA NAME'
        return results

    # 筛选2020年数据
    df_2020 = df[df['Year'] == 2020].copy()

    if len(df_2020) == 0:
        results['error'] = '没有2020年的数据'
        return results

    # 1. 月度统计
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # 将月份转换为分类类型以保持顺序
    df_2020['Month_Name'] = pd.Categorical(
        df_2020['Month'].map({i: month_order[i-1] for i in range(1, 13)}),
        categories=month_order,
        ordered=True
    )

    # 2. 按区域和月份统计
    monthly_by_area = df_2020.groupby(['Month_Name', 'AREA NAME']).size().unstack(fill_value=0)
    results['tables']['monthly_by_area'] = monthly_by_area.reset_index()

    # 3. 各区域年度总计
    area_totals = df_2020['AREA NAME'].value_counts().reset_index()
    area_totals.columns = ['area_name', 'total_crimes']
    results['tables']['area_totals'] = area_totals

    # 4. 统计信息
    results['statistics']['total_crimes_2020'] = len(df_2020)
    results['statistics']['total_areas'] = len(area_totals)
    results['statistics']['highest_crime_area'] = area_totals.iloc[0]['area_name']
    results['statistics']['highest_crime_count'] = int(area_totals.iloc[0]['total_crimes'])

    # 5. 绘制趋势图
    fig_path = plot_manager.plot_monthly_trends_by_area(df_2020)
    results['figures'].append(fig_path)

    return results
