"""
分析目标4: 犯罪热点检测（网格热力图）
- 基于经纬度的网格热力图
- 犯罪密度分析
"""
import pandas as pd
import numpy as np
from typing import Dict
from src.crime_analysis.config import Config
from src.crime_analysis.plotting import PlotManager


def analyze_geographic_distribution(df: pd.DataFrame, config: Config = None) -> Dict:
    """
    分析犯罪热点（网格热力图）
    对应原代码中的目标3: Crime Hotspot Detection Using Grid-Based Heatmap

    Args:
        df: 包含特征的数据框
        config: 配置对象

    Returns:
        Dict: 包含统计结果和图表路径的字典
    """
    config = config or Config()
    plot_manager = PlotManager(config)
    lat_col = config.lat_column
    lon_col = config.lon_column

    results = {
        'title': '犯罪热点检测（网格热力图）',
        'tables': {},
        'figures': [],
        'statistics': {}
    }

    if lat_col not in df.columns or lon_col not in df.columns:
        results['error'] = '缺少经纬度列'
        return results

    # 过滤有效坐标
    df_valid = df[
        (df[lat_col].notna()) &
        (df[lon_col].notna()) &
        (df[lat_col] != 0) &
        (df[lon_col] != 0)
    ].copy()

    if len(df_valid) == 0:
        results['error'] = '没有有效的地理坐标数据'
        return results

    # 1. 基本地理统计
    results['statistics']['lat_range'] = (df_valid[lat_col].min(), df_valid[lat_col].max())
    results['statistics']['lon_range'] = (df_valid[lon_col].min(), df_valid[lon_col].max())
    results['statistics']['center_point'] = (
        df_valid[lat_col].mean(),
        df_valid[lon_col].mean()
    )
    results['statistics']['total_records'] = len(df_valid)

    # 2. 创建网格热力图数据 (4x4网格，与原代码一致)
    lat_bins = np.linspace(df_valid[lat_col].min(), df_valid[lat_col].max(), 5)
    lon_bins = np.linspace(df_valid[lon_col].min(), df_valid[lon_col].max(), 5)

    crime_density, _, _ = np.histogram2d(
        df_valid[lat_col],
        df_valid[lon_col],
        bins=[lat_bins, lon_bins]
    )

    # 保存热力图数据
    heatmap_data = pd.DataFrame(
        crime_density,
        index=[f'Lat_{i}' for i in range(len(lat_bins)-1)],
        columns=[f'Lon_{i}' for i in range(len(lon_bins)-1)]
    )
    results['tables']['heatmap_grid_data'] = heatmap_data

    # 3. 热点统计
    max_density = crime_density.max()
    hotspot_count = np.sum(crime_density > max_density * 0.5)
    results['statistics']['max_density'] = int(max_density)
    results['statistics']['hotspot_grids'] = int(hotspot_count)

    # 4. 绘制热力图
    fig_path = plot_manager.plot_crime_hotspot_heatmap(df_valid, lat_bins, lon_bins, crime_density)
    results['figures'].append(fig_path)

    return results
