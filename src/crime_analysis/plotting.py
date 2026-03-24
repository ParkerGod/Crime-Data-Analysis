"""
统一绘图模块 - 所有图表保存到文件并关闭
"""
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, Tuple, List
import os

from .config import Config


class PlotManager:
    """图表管理器"""

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self._setup_style()

    def _setup_style(self):
        """设置图表样式"""
        plt.style.use('seaborn-v0_8-whitegrid')
        sns.set_palette("husl")
        plt.rcParams['figure.dpi'] = self.config.figure_dpi
        plt.rcParams['savefig.dpi'] = self.config.figure_dpi
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10

    def _save_and_close(self, fig: plt.Figure, filename: str) -> str:
        """
        保存图表并关闭

        Args:
            fig: matplotlib图表对象
            filename: 文件名

        Returns:
            str: 保存的文件路径
        """
        filepath = self.config.get_output_path(filename)
        fig.savefig(filepath, format=self.config.figure_format, bbox_inches='tight')
        plt.close(fig)
        return filepath

    def plot_crime_trend(self, df: pd.DataFrame, title: str = "Crime Trend") -> str:
        """
        绘制犯罪趋势图

        Args:
            df: 包含year和count的数据框
            title: 图表标题

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(14, 6))

        if 'year' in df.columns and 'count' in df.columns:
            ax.plot(df['year'], df['count'], marker='o', linewidth=2, markersize=6)
            ax.set_xlabel('Year')
            ax.set_ylabel('Number of Crimes')
            ax.set_title(title)
            ax.grid(True, alpha=0.3)

        return self._save_and_close(fig, 'crime_trend.png')

    def plot_yearly_crime_trend(self, yearly_stats: pd.DataFrame) -> str:
        """
        绘制年度犯罪趋势图

        Args:
            yearly_stats: 包含year和count的数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(14, 6))

        if 'year' in yearly_stats.columns and 'count' in yearly_stats.columns:
            ax.plot(yearly_stats['year'], yearly_stats['count'], marker='o', linewidth=2, markersize=6)
            ax.set_xlabel('Year', fontsize=14)
            ax.set_ylabel('Number of Crimes', fontsize=14)
            ax.set_title('Annual Crime Trend', fontsize=16, weight='bold')
            ax.grid(True, alpha=0.3)

        return self._save_and_close(fig, 'yearly_crime_trend.png')

    def plot_crime_by_type(self, df: pd.DataFrame, top_n: int = 10) -> str:
        """
        绘制犯罪类型分布图

        Args:
            df: 数据框
            top_n: 显示前N种犯罪类型

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(12, 8))

        crime_col = self.config.crime_type_column
        if crime_col in df.columns:
            crime_counts = df[crime_col].value_counts().head(top_n)

            crime_counts.plot(kind='barh', ax=ax)
            ax.set_xlabel('Number of Cases')
            ax.set_ylabel('Crime Type')
            ax.set_title(f'Top {top_n} Crime Types')
            ax.invert_yaxis()

        return self._save_and_close(fig, 'crime_by_type.png')

    def plot_top10_crime_categories(self, top10_df: pd.DataFrame) -> str:
        """
        绘制Top 10犯罪类别条形图
        对应原代码中的目标1

        Args:
            top10_df: 包含crime_type, count, short_label的数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        if 'count' in top10_df.columns and 'short_label' in top10_df.columns:
            sns.barplot(x=top10_df['count'], y=top10_df['short_label'],
                        palette="cubehelix", width=0.5, ax=ax)
            ax.set_title("Top 10 Crime Categories", fontsize=20, weight='bold')
            ax.set_xlabel("Number of Crimes", fontsize=16)
            ax.set_ylabel("Crime Type", fontsize=16)
            ax.tick_params(axis='x', labelsize=14)
            ax.tick_params(axis='y', labelsize=14, labelweight='bold')
            ax.grid(True, axis='x', linestyle='--', alpha=0.7)

        return self._save_and_close(fig, 'top10_crime_categories.png')

    def plot_crime_by_hour(self, df: pd.DataFrame) -> str:
        """
        绘制按小时分布的犯罪图

        Args:
            df: 数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(14, 6))

        if 'hour' in df.columns:
            hourly_counts = df['hour'].value_counts().sort_index()

            ax.bar(hourly_counts.index, hourly_counts.values, color='steelblue', alpha=0.7)
            ax.set_xlabel('Hour of Day')
            ax.set_ylabel('Number of Crimes')
            ax.set_title('Crime Distribution by Hour')
            ax.set_xticks(range(0, 24))

        return self._save_and_close(fig, 'crime_by_hour.png')

    def plot_crime_by_dayofweek(self, df: pd.DataFrame) -> str:
        """
        绘制按星期分布的犯罪图

        Args:
            df: 数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        if 'dayofweek' in df.columns:
            day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            daily_counts = df['dayofweek'].value_counts().sort_index()

            colors = ['steelblue' if i < 5 else 'coral' for i in range(7)]
            ax.bar(range(7), [daily_counts.get(i, 0) for i in range(7)], color=colors, alpha=0.7)
            ax.set_xlabel('Day of Week')
            ax.set_ylabel('Number of Crimes')
            ax.set_title('Crime Distribution by Day of Week')
            ax.set_xticks(range(7))
            ax.set_xticklabels(day_names)

        return self._save_and_close(fig, 'crime_by_dayofweek.png')

    def plot_crime_heatmap(self, df: pd.DataFrame) -> str:
        """
        绘制犯罪热力图（按小时和星期）

        Args:
            df: 数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(14, 8))

        if 'hour' in df.columns and 'dayofweek' in df.columns:
            pivot = df.pivot_table(
                index='hour',
                columns='dayofweek',
                aggfunc='size',
                fill_value=0
            )

            day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            pivot.columns = day_names

            sns.heatmap(pivot, annot=True, fmt='d', cmap='YlOrRd', ax=ax)
            ax.set_xlabel('Day of Week')
            ax.set_ylabel('Hour of Day')
            ax.set_title('Crime Heatmap (Hour vs Day)')

        return self._save_and_close(fig, 'crime_heatmap.png')

    def plot_geographic_distribution(self, df: pd.DataFrame, sample_size: int = 5000) -> str:
        """
        绘制地理分布散点图

        Args:
            df: 数据框
            sample_size: 采样数量（大数据集）

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(12, 12))

        lat_col = self.config.lat_column
        lon_col = self.config.lon_column

        if lat_col in df.columns and lon_col in df.columns:
            # 采样以避免图表过于密集
            plot_df = df.sample(min(sample_size, len(df))) if len(df) > sample_size else df

            ax.scatter(
                plot_df[lon_col],
                plot_df[lat_col],
                alpha=0.3,
                s=1,
                c='red'
            )
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.set_title(f'Geographic Distribution of Crimes (n={len(plot_df):,})')
            ax.set_aspect('equal')

        return self._save_and_close(fig, 'geographic_distribution.png')

    def plot_crime_hotspot_heatmap(self, df: pd.DataFrame, lat_bins, lon_bins, crime_density) -> str:
        """
        绘制犯罪热点热力图
        对应原代码中的目标3

        Args:
            df: 数据框
            lat_bins: 纬度分箱边界
            lon_bins: 经度分箱边界
            crime_density: 犯罪密度矩阵

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        lat_col = self.config.lat_column
        lon_col = self.config.lon_column

        if lat_col in df.columns and lon_col in df.columns:
            # 绘制热力图
            im = ax.imshow(
                crime_density.T,
                cmap='Blues',
                origin='lower',
                aspect='auto',
                extent=[df[lon_col].min(), df[lon_col].max(), df[lat_col].min(), df[lat_col].max()]
            )
            plt.colorbar(im, ax=ax, label='Crime Density')
            ax.set_title("Crime Hotspots (Enhanced Heatmap)", fontsize=20, weight='bold')
            ax.set_xlabel("Longitude", fontsize=16)
            ax.set_ylabel("Latitude", fontsize=16)
            ax.grid(True, linestyle='-', color='black', alpha=0.3)

        return self._save_and_close(fig, 'crime_hotspot_heatmap.png')

    def plot_arrest_rate(self, df: pd.DataFrame) -> str:
        """
        绘制逮捕率图表

        Args:
            df: 数据框

        Returns:
            str: 保存的文件路径
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        arrest_col = self.config.arrest_column
        crime_col = self.config.crime_type_column

        if arrest_col in df.columns:
            # 整体逮捕率
            arrest_counts = df[arrest_col].value_counts()
            colors = ['lightcoral', 'lightgreen']
            ax1.pie(
                arrest_counts.values,
                labels=['No Arrest', 'Arrest'] if False in arrest_counts.index else ['Arrest', 'No Arrest'],
                autopct='%1.1f%%',
                colors=colors,
                startangle=90
            )
            ax1.set_title('Overall Arrest Rate')

            # 按犯罪类型的逮捕率
            if crime_col in df.columns:
                arrest_by_type = df.groupby(crime_col)[arrest_col].mean().sort_values(ascending=False).head(10)
                arrest_by_type.plot(kind='barh', ax=ax2, color='steelblue')
                ax2.set_xlabel('Arrest Rate')
                ax2.set_ylabel('Crime Type')
                ax2.set_title('Arrest Rate by Crime Type (Top 10)')

        return self._save_and_close(fig, 'arrest_rate.png')

    def plot_monthly_trend(self, df: pd.DataFrame) -> str:
        """
        绘制月度趋势图

        Args:
            df: 数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(14, 6))

        if 'year' in df.columns and 'month' in df.columns:
            df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
            monthly_counts = df.groupby('year_month').size()

            ax.plot(range(len(monthly_counts)), monthly_counts.values, marker='o', linewidth=1.5)
            ax.set_xlabel('Month')
            ax.set_ylabel('Number of Crimes')
            ax.set_title('Monthly Crime Trend')

            # 设置x轴标签（每6个月显示一次）
            tick_positions = range(0, len(monthly_counts), 6)
            tick_labels = [monthly_counts.index[i] for i in tick_positions]
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(tick_labels, rotation=45, ha='right')

        return self._save_and_close(fig, 'monthly_trend.png')

    def plot_monthly_crime_trends(self, monthly_counts: pd.DataFrame) -> str:
        """
        绘制月度犯罪趋势条形图
        对应原代码中的目标2

        Args:
            monthly_counts: 包含month, count, month_name的数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        if 'month' in monthly_counts.columns and 'count' in monthly_counts.columns:
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            sns.barplot(x=monthly_counts['month'], y=monthly_counts['count'],
                        palette="crest", width=0.7, ax=ax)
            ax.set_title("Average Crime Trends by Month", fontsize=20, weight='bold')
            ax.set_xlabel("Month", fontsize=16)
            ax.set_ylabel("Number of Crimes", fontsize=16)
            ax.set_xticks(range(12))
            ax.set_xticklabels(month_names, fontsize=14)
            ax.tick_params(axis='y', labelsize=14)
            ax.grid(True, axis='y', linestyle='--', alpha=0.7)

        return self._save_and_close(fig, 'monthly_crime_trends.png')

    def plot_victim_age_by_crime_gender(self, df: pd.DataFrame) -> str:
        """
        绘制受害者年龄分布（按犯罪类型和性别）散点图
        对应原代码中的目标4

        Args:
            df: 包含Vict Age, Crm Cd Desc, Vict Sex的数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(12, 6))

        crime_col = self.config.crime_type_column

        if 'Vict Age' in df.columns and crime_col in df.columns and 'Vict Sex' in df.columns:
            # 使用stripplot绘制散点图
            sns.stripplot(data=df, x=crime_col, y='Vict Age', hue='Vict Sex',
                          jitter=True, dodge=True, alpha=0.7, palette='coolwarm', ax=ax)
            ax.set_title("Victim Age Distribution by Crime Type and Gender", fontsize=20, weight='bold')
            ax.set_xlabel("Crime Type", fontsize=16)
            ax.set_ylabel("Victim Age", fontsize=16)
            ax.tick_params(axis='x', rotation=25)
            ax.legend(title='Victim Sex', fontsize=12)

        return self._save_and_close(fig, 'victim_age_by_crime_gender.png')

    def plot_victim_age_histogram(self, df: pd.DataFrame) -> str:
        """
        绘制受害者年龄分布直方图

        Args:
            df: 包含Vict Age的数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        if 'Vict Age' in df.columns:
            sns.histplot(df['Vict Age'], bins=20, kde=True, color="green", ax=ax)
            ax.set_title("Victim Age Distribution", fontsize=20, weight='bold')
            ax.set_xlabel("Age", fontsize=16)
            ax.set_ylabel("Frequency", fontsize=16)

        return self._save_and_close(fig, 'victim_age_distribution.png')

    def plot_crime_status_distribution(self, df: pd.DataFrame) -> str:
        """
        绘制犯罪状态分布图

        Args:
            df: 数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(10, 6))

        status_col = 'Status Desc'
        if status_col in df.columns:
            status_counts = df[status_col].value_counts()
            status_counts.plot(kind='bar', stacked=True, color=sns.color_palette("Set2"), ax=ax)
            ax.set_title("Distribution of Crimes by Status Description", fontsize=20, weight='bold')
            ax.set_xlabel("Status", fontsize=16)
            ax.set_ylabel("Number of Crimes", fontsize=16)
            ax.tick_params(axis='x', rotation=0)

        return self._save_and_close(fig, 'crime_status_distribution.png')

    def plot_monthly_trends_by_area(self, df: pd.DataFrame) -> str:
        """
        绘制2020年各区域月度犯罪趋势图

        Args:
            df: 数据框

        Returns:
            str: 保存的文件路径
        """
        fig, ax = plt.subplots(figsize=(10, 8))

        if 'Month_Name' in df.columns and 'AREA NAME' in df.columns:
            month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                           'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

            monthly_crimes = df.groupby(['Month_Name', 'AREA NAME']).size().unstack(fill_value=0)

            for area in monthly_crimes.columns:
                ax.plot(monthly_crimes.index, monthly_crimes[area], label=area, marker='o')

            ax.set_title("Monthly Crime Trends by Area (2020)", fontsize=20, weight='bold')
            ax.set_xlabel("Month", fontsize=16)
            ax.set_ylabel("Number of Crimes", fontsize=16)
            ax.legend(title="Area", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

        return self._save_and_close(fig, 'monthly_trends_by_area.png')

    def create_summary_figure(self, df: pd.DataFrame) -> List[str]:
        """
        创建所有标准图表

        Args:
            df: 数据框

        Returns:
            List[str]: 所有保存的文件路径列表
        """
        files = []

        files.append(self.plot_crime_by_type(df))
        files.append(self.plot_crime_by_hour(df))
        files.append(self.plot_crime_by_dayofweek(df))
        files.append(self.plot_crime_heatmap(df))
        files.append(self.plot_geographic_distribution(df))
        files.append(self.plot_arrest_rate(df))

        if 'year' in df.columns:
            yearly_counts = df.groupby('year').size().reset_index(name='count')
            files.append(self.plot_crime_trend(yearly_counts))

        if 'year' in df.columns and 'month' in df.columns:
            files.append(self.plot_monthly_trend(df))

        return files
