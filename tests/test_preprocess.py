"""
数据清洗模块单元测试
"""
import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crime_analysis.preprocess import DataPreprocessor
from crime_analysis.config import Config


class TestDataPreprocessor(unittest.TestCase):
    """测试数据清洗功能"""

    def setUp(self):
        """设置测试数据"""
        self.config = Config()
        self.preprocessor = DataPreprocessor(self.config)

        # 创建测试数据
        self.test_data = pd.DataFrame({
            'Date': [
                '2020-01-15 10:30:00',
                '2020-06-20 15:45:00',
                '2021-03-10 08:00:00',
                '2022-12-25 23:59:00',
                None,  # 缺失日期
                '2023-05-01 12:00:00',
            ],
            'Primary Type': ['THEFT', 'BATTERY', None, 'THEFT', 'ASSAULT', 'THEFT'],
            'Description': ['OVER $500', 'SIMPLE', 'AGGRAVATED', 'OVER $500', 'SIMPLE', 'OVER $500'],
            'Location Description': ['STREET', 'SIDEWALK', 'APARTMENT', None, 'STREET', 'STREET'],
            'Arrest': [False, True, False, False, True, False],
            'Domestic': [False, False, True, False, False, False],
            'Latitude': [41.8781, 41.8782, 41.8783, 0, 41.8785, 41.8786],  # 包含0值
            'Longitude': [-87.6298, -87.6299, -87.6300, -87.6301, None, -87.6303],  # 包含None
        })

    def test_parse_dates(self):
        """测试日期解析"""
        df = self.preprocessor._parse_dates(self.test_data)

        # 检查日期列是否被正确解析
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(df['Date']))

        # 检查有效日期是否被正确解析
        self.assertEqual(df['Date'].iloc[0].year, 2020)
        self.assertEqual(df['Date'].iloc[0].month, 1)
        self.assertEqual(df['Date'].iloc[0].day, 15)

    def test_handle_missing_values(self):
        """测试缺失值处理"""
        df = self.preprocessor._parse_dates(self.test_data)
        df, report = self.preprocessor._handle_missing_values(df)

        # 检查关键列缺失的行是否被删除
        self.assertFalse(df['Date'].isnull().any())
        self.assertFalse(df['Primary Type'].isnull().any())

        # 检查非关键列缺失是否被填充
        self.assertFalse(df['Location Description'].isnull().any())

        # 检查报告是否生成
        self.assertIn('actions', report)

    def test_handle_duplicates(self):
        """测试重复数据处理"""
        # 添加重复行
        df_with_dup = pd.concat([self.test_data, self.test_data.iloc[[0]]], ignore_index=True)

        df, report = self.preprocessor._handle_duplicates(df_with_dup)

        # 检查重复行是否被删除
        self.assertEqual(len(df), len(df_with_dup) - 1)
        self.assertEqual(report['duplicates_removed'], 1)

    def test_filter_year_range(self):
        """测试年份范围过滤"""
        df = self.preprocessor._parse_dates(self.test_data)
        df, report = self.preprocessor._filter_year_range(df)

        # 检查是否在年份范围内
        if 'year' in df.columns:
            years = df['Date'].dt.year
            self.assertTrue(all(years >= self.config.year_start))
            self.assertTrue(all(years <= self.config.year_end))

    def test_clean_coordinates(self):
        """测试坐标清理"""
        df, report = self.preprocessor._clean_coordinates(self.test_data)

        # 检查无效坐标是否被删除
        self.assertFalse((df['Latitude'] == 0).any())
        self.assertFalse(df['Latitude'].isnull().any())
        self.assertFalse(df['Longitude'].isnull().any())

        # 检查坐标范围
        self.assertTrue(all(df['Latitude'].between(-90, 90)))
        self.assertTrue(all(df['Longitude'].between(-180, 180)))

    def test_full_clean_pipeline(self):
        """测试完整清洗流程"""
        df, report = self.preprocessor.clean(self.test_data)

        # 检查报告结构
        self.assertIn('original_rows', report)
        self.assertIn('final_rows', report)
        self.assertIn('removed_rows', report)

        # 检查数据质量
        self.assertFalse(df['Date'].isnull().any())
        self.assertFalse(df['Primary Type'].isnull().any())
        self.assertFalse(df['Latitude'].isnull().any())
        self.assertFalse(df['Longitude'].isnull().any())

        # 检查行数减少
        self.assertLess(len(df), len(self.test_data))


class TestDataPreprocessorEdgeCases(unittest.TestCase):
    """测试边界情况"""

    def setUp(self):
        self.config = Config()
        self.preprocessor = DataPreprocessor(self.config)

    def test_empty_dataframe(self):
        """测试空数据框"""
        empty_df = pd.DataFrame()
        df, report = self.preprocessor.clean(empty_df)
        self.assertEqual(len(df), 0)

    def test_all_missing_critical_columns(self):
        """测试关键列全部缺失"""
        df = pd.DataFrame({
            'Date': [None, None, None],
            'Primary Type': [None, None, None],
            'Latitude': [None, None, None],
            'Longitude': [None, None, None],
        })

        df, report = self.preprocessor.clean(df)
        # 所有行都应该被删除
        self.assertEqual(len(df), 0)

    def test_invalid_coordinates(self):
        """测试无效坐标"""
        df = pd.DataFrame({
            'Date': ['2020-01-01'] * 5,
            'Primary Type': ['THEFT'] * 5,
            'Latitude': [100, -100, 0, 41.8, None],  # 包含无效值
            'Longitude': [-87.6, -200, 200, None, -87.6],
        })

        df_cleaned, _ = self.preprocessor.clean(df)
        # 只有一行有效数据
        self.assertEqual(len(df_cleaned), 1)


if __name__ == '__main__':
    unittest.main()
