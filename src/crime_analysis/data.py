"""
数据读取模块 - 负责读取数据并检查必要列
"""
import pandas as pd
from typing import Tuple, List
from .config import Config


class DataLoader:
    """数据加载器"""

    def __init__(self, config: Config = None):
        self.config = config or Config()

    def load_data(self, file_path: str = None) -> pd.DataFrame:
        """
        加载犯罪数据

        Args:
            file_path: 数据文件路径，如果为None则使用config中的路径

        Returns:
            pd.DataFrame: 加载的数据

        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 缺少必要列
        """
        if file_path is None:
            file_path = self.config.input_file

        if file_path is None:
            raise ValueError("未指定输入文件路径")

        # 根据文件扩展名选择读取方式
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.parquet'):
            df = pd.read_parquet(file_path)
        elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"不支持的文件格式: {file_path}")

        # 检查必要列
        self._validate_columns(df)

        return df

    def _validate_columns(self, df: pd.DataFrame) -> None:
        """
        验证数据是否包含必要的列

        Args:
            df: 待验证的数据框

        Raises:
            ValueError: 缺少必要列
        """
        missing_cols = []
        for col in self.config.required_columns:
            if col not in df.columns:
                missing_cols.append(col)

        if missing_cols:
            raise ValueError(f"数据缺少必要列: {missing_cols}")

    def get_column_info(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        获取数据列信息

        Args:
            df: 数据框

        Returns:
            pd.DataFrame: 列信息统计
        """
        info = {
            'Column': df.columns,
            'Type': df.dtypes.values,
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values,
            'Null Percentage': (df.isnull().sum() / len(df) * 100).values
        }
        return pd.DataFrame(info)

    def get_basic_stats(self, df: pd.DataFrame) -> dict:
        """
        获取数据基本统计信息

        Args:
            df: 数据框

        Returns:
            dict: 基本统计信息
        """
        return {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024 / 1024,
            'date_range': self._get_date_range(df) if self.config.date_column in df.columns else None
        }

    def _get_date_range(self, df: pd.DataFrame) -> Tuple:
        """获取日期范围"""
        date_col = self.config.date_column
        if date_col in df.columns:
            try:
                dates = pd.to_datetime(df[date_col], errors='coerce')
                return (dates.min(), dates.max())
            except:
                return None
        return None
