"""
特征工程模块 - 从日期字段提取特征
"""
import pandas as pd
import numpy as np
from typing import List
from .config import Config


class FeatureEngineer:
    """特征工程师"""

    def __init__(self, config: Config = None):
        self.config = config or Config()

    def extract_datetime_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        从日期列提取时间特征

        Args:
            df: 包含日期列的数据框

        Returns:
            pd.DataFrame: 添加了时间特征的数据框
        """
        df = df.copy()
        date_col = self.config.date_column

        if date_col not in df.columns:
            raise ValueError(f"数据中缺少日期列: {date_col}")

        # 确保日期格式正确
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        # 提取基本时间特征
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['day'] = df[date_col].dt.day
        df['hour'] = df[date_col].dt.hour
        df['dayofweek'] = df[date_col].dt.dayofweek  # 0=周一, 6=周日
        df['dayofyear'] = df[date_col].dt.dayofyear
        df['weekofyear'] = df[date_col].dt.isocalendar().week

        # 提取周期性特征
        df['month_name'] = df[date_col].dt.month_name()
        df['day_name'] = df[date_col].dt.day_name()

        # 是否是周末
        df['is_weekend'] = df['dayofweek'].isin([5, 6])

        # 季度
        df['quarter'] = df[date_col].dt.quarter

        # 时间段 (早/中/晚/夜)
        df['time_period'] = df['hour'].apply(self._categorize_time_period)

        return df

    def _categorize_time_period(self, hour: int) -> str:
        """
        将小时分类为时间段

        Args:
            hour: 小时 (0-23)

        Returns:
            str: 时间段类别
        """
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'

    def create_geographic_grid(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        创建地理网格特征

        Args:
            df: 包含经纬度的数据框

        Returns:
            pd.DataFrame: 添加了网格特征的数据框
        """
        df = df.copy()
        lat_col = self.config.lat_column
        lon_col = self.config.lon_column

        if lat_col not in df.columns or lon_col not in df.columns:
            raise ValueError("数据中缺少经纬度列")

        # 创建网格
        lat_min, lat_max = df[lat_col].min(), df[lat_col].max()
        lon_min, lon_max = df[lon_col].min(), df[lon_col].max()

        # 使用分位数创建网格边界
        df['lat_bin'] = pd.cut(
            df[lat_col],
            bins=self.config.lat_bins,
            labels=False,
            include_lowest=True
        )
        df['lon_bin'] = pd.cut(
            df[lon_col],
            bins=self.config.lon_bins,
            labels=False,
            include_lowest=True
        )

        # 创建网格ID
        df['grid_id'] = df['lat_bin'].astype(str) + '_' + df['lon_bin'].astype(str)

        return df

    def encode_categorical(self, df: pd.DataFrame, columns: List[str] = None) -> pd.DataFrame:
        """
        对分类变量进行编码

        Args:
            df: 数据框
            columns: 需要编码的列，默认为犯罪类型和地点

        Returns:
            pd.DataFrame: 添加了编码特征的数据框
        """
        df = df.copy()

        if columns is None:
            columns = [self.config.crime_type_column, self.config.location_column]

        for col in columns:
            if col in df.columns:
                # 创建类别编码
                df[f'{col}_encoded'] = pd.Categorical(df[col]).codes

        return df

    def create_crime_severity_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        创建犯罪严重程度评分

        Args:
            df: 数据框

        Returns:
            pd.DataFrame: 添加了严重程度评分的数据框
        """
        df = df.copy()

        # 定义犯罪类型严重程度 (示例)
        severity_map = {
            'HOMICIDE': 10,
            'ASSAULT': 8,
            'BATTERY': 7,
            'ROBBERY': 8,
            'BURGLARY': 6,
            'THEFT': 5,
            'MOTOR VEHICLE THEFT': 6,
            'CRIMINAL DAMAGE': 4,
            'NARCOTICS': 5,
            'CRIMINAL TRESPASS': 3,
            'OTHER OFFENSE': 2,
        }

        crime_col = self.config.crime_type_column
        if crime_col in df.columns:
            df['severity_score'] = df[crime_col].map(
                lambda x: severity_map.get(str(x).upper(), 1)
            ).fillna(1)

        return df

    def extract_all_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        提取所有特征

        Args:
            df: 原始数据框

        Returns:
            pd.DataFrame: 包含所有特征的数据框
        """
        df = self.extract_datetime_features(df)
        df = self.create_geographic_grid(df)
        df = self.encode_categorical(df)
        df = self.create_crime_severity_score(df)

        return df

    def get_feature_columns(self) -> List[str]:
        """获取所有生成的特征列名"""
        return [
            'year', 'month', 'day', 'hour', 'dayofweek', 'dayofyear',
            'weekofyear', 'month_name', 'day_name', 'is_weekend',
            'quarter', 'time_period', 'lat_bin', 'lon_bin', 'grid_id',
            'severity_score'
        ]
