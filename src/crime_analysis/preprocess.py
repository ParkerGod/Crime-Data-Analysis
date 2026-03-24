"""
数据清洗模块 - 处理缺失值和重复数据
"""
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
from .config import Config


class DataPreprocessor:
    """数据预处理器"""

    def __init__(self, config: Config = None):
        self.config = config or Config()

    def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        执行完整的数据清洗流程

        Args:
            df: 原始数据框

        Returns:
            Tuple[pd.DataFrame, Dict]: (清洗后的数据, 清洗报告)
        """
        report = {
            'original_rows': len(df),
            'original_columns': len(df.columns),
        }

        # 1. 处理日期列
        df = self._parse_dates(df)

        # 2. 处理缺失值
        df, missing_report = self._handle_missing_values(df)
        report['missing_values'] = missing_report

        # 3. 处理重复数据
        df, duplicate_report = self._handle_duplicates(df)
        report['duplicates'] = duplicate_report

        # 4. 过滤年份范围
        df, year_report = self._filter_year_range(df)
        report['year_filter'] = year_report

        # 5. 清理坐标数据
        df, coord_report = self._clean_coordinates(df)
        report['coordinates'] = coord_report

        report['final_rows'] = len(df)
        report['removed_rows'] = report['original_rows'] - report['final_rows']
        report['removal_percentage'] = round(report['removed_rows'] / report['original_rows'] * 100, 2)

        return df, report

    def _parse_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """解析日期列"""
        df = df.copy()
        date_col = self.config.date_column

        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """
        处理缺失值

        策略：
        - 日期缺失：删除该行
        - 坐标缺失：删除该行
        - 犯罪类型缺失：删除该行
        - 其他列缺失：填充为"Unknown"
        """
        df = df.copy()
        report = {
            'before': df.isnull().sum().to_dict(),
            'actions': []
        }

        # 关键列缺失则删除行
        critical_cols = [
            self.config.date_column,
            self.config.crime_type_column,
            self.config.lat_column,
            self.config.lon_column
        ]

        for col in critical_cols:
            if col in df.columns:
                before_count = len(df)
                df = df.dropna(subset=[col])
                removed = before_count - len(df)
                if removed > 0:
                    report['actions'].append(f"删除 {col} 缺失的行: {removed} 条")

        # 其他列填充为 Unknown
        fillable_cols = [
            self.config.location_column,
            'Description'
        ]

        for col in fillable_cols:
            if col in df.columns:
                missing_count = df[col].isnull().sum()
                if missing_count > 0:
                    df[col] = df[col].fillna('Unknown')
                    report['actions'].append(f"填充 {col} 缺失值: {missing_count} 条")

        report['after'] = df.isnull().sum().to_dict()

        return df, report

    def _handle_duplicates(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """处理重复数据"""
        df = df.copy()

        before_count = len(df)
        df = df.drop_duplicates()
        removed = before_count - len(df)

        report = {
            'duplicates_removed': removed,
            'duplicates_percentage': round(removed / before_count * 100, 2) if before_count > 0 else 0
        }

        return df, report

    def _filter_year_range(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """过滤年份范围"""
        df = df.copy()
        date_col = self.config.date_column

        if date_col not in df.columns:
            return df, {'filtered': False, 'reason': '无日期列'}

        before_count = len(df)

        # 提取年份
        df['_year'] = df[date_col].dt.year

        # 过滤
        df = df[
            (df['_year'] >= self.config.year_start) &
            (df['_year'] <= self.config.year_end)
        ]

        # 删除临时列
        df = df.drop(columns=['_year'])

        removed = before_count - len(df)

        report = {
            'filtered': True,
            'year_start': self.config.year_start,
            'year_end': self.config.year_end,
            'rows_removed': removed,
            'rows_remaining': len(df)
        }

        return df, report

    def _clean_coordinates(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
        """清理坐标数据"""
        df = df.copy()
        lat_col = self.config.lat_column
        lon_col = self.config.lon_column

        before_count = len(df)

        # 过滤无效坐标
        if lat_col in df.columns and lon_col in df.columns:
            df = df[
                (df[lat_col].notna()) &
                (df[lon_col].notna()) &
                (df[lat_col] != 0) &
                (df[lon_col] != 0) &
                (df[lat_col].between(-90, 90)) &
                (df[lon_col].between(-180, 180))
            ]

        removed = before_count - len(df)

        report = {
            'invalid_coordinates_removed': removed,
            'valid_coordinates': len(df)
        }

        return df, report

    def get_cleaning_summary(self, report: Dict[str, Any]) -> str:
        """生成清洗报告摘要"""
        lines = [
            "=" * 50,
            "数据清洗报告",
            "=" * 50,
            f"原始数据: {report['original_rows']:,} 行",
            f"清洗后: {report['final_rows']:,} 行",
            f"删除: {report['removed_rows']:,} 行 ({report['removal_percentage']}%)",
            "",
            "详细处理:",
        ]

        # 缺失值处理
        if 'missing_values' in report and 'actions' in report['missing_values']:
            lines.append("  [缺失值处理]")
            for action in report['missing_values']['actions']:
                lines.append(f"    - {action}")

        # 重复数据处理
        if 'duplicates' in report:
            dup = report['duplicates']
            lines.append(f"  [重复数据] 删除 {dup['duplicates_removed']} 条 ({dup['duplicates_percentage']}%)")

        # 年份过滤
        if 'year_filter' in report and report['year_filter'].get('filtered'):
            yf = report['year_filter']
            lines.append(f"  [年份过滤] {yf['year_start']}-{yf['year_end']}, 删除 {yf['rows_removed']} 条")

        # 坐标清理
        if 'coordinates' in report:
            coord = report['coordinates']
            lines.append(f"  [坐标清理] 删除无效坐标 {coord['invalid_coordinates_removed']} 条")

        lines.append("=" * 50)

        return "\n".join(lines)
