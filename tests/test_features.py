"""
特征工程模块单元测试
"""
import unittest
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crime_analysis.features import FeatureEngineer
from crime_analysis.config import Config


class TestFeatureEngineer(unittest.TestCase):
    """测试特征工程功能"""

    def setUp(self):
        """设置测试数据"""
        self.config = Config()
        self.engineer = FeatureEngineer(self.config)

        # 创建测试数据
        self.test_data = pd.DataFrame({
            'Date': pd.to_datetime([
                '2020-01-15 10:30:00',
                '2020-06-20 15:45:00',
                '2021-03-10 08:00:00',
                '2021-12-25 23:59:00',
                '2022-07-04 14:20:00',
            ]),
            'Primary Type': ['THEFT', 'BATTERY', 'ASSAULT', 'THEFT', 'ROBBERY'],
            'Location Description': ['STREET', 'SIDEWALK', 'APARTMENT', 'STREET', 'STORE'],
            'Latitude': [41.8781, 41.8782, 41.8783, 41.8784, 41.8785],
            'Longitude': [-87.6298, -87.6299, -87.6300, -87.6301, -87.6302],
            'Arrest': [False, True, False, False, True],
        })

    def test_extract_datetime_features(self):
        """测试日期特征提取"""
        df = self.engineer.extract_datetime_features(self.test_data)

        # 检查基本时间特征
        self.assertIn('year', df.columns)
        self.assertIn('month', df.columns)
        self.assertIn('day', df.columns)
        self.assertIn('hour', df.columns)
        self.assertIn('dayofweek', df.columns)
        self.assertIn('quarter', df.columns)

        # 检查特征值是否正确
        self.assertEqual(df['year'].iloc[0], 2020)
        self.assertEqual(df['month'].iloc[0], 1)
        self.assertEqual(df['day'].iloc[0], 15)
        self.assertEqual(df['hour'].iloc[0], 10)

        # 检查星期几 (2020-01-15 是星期三)
        self.assertEqual(df['dayofweek'].iloc[0], 2)

        # 检查季度
        self.assertEqual(df['quarter'].iloc[0], 1)
        self.assertEqual(df['quarter'].iloc[1], 2)

    def test_is_weekend_feature(self):
        """测试周末特征"""
        df = self.engineer.extract_datetime_features(self.test_data)

        self.assertIn('is_weekend', df.columns)

        # 2020-01-15 是星期三，不是周末
        self.assertFalse(df['is_weekend'].iloc[0])

    def test_time_period_feature(self):
        """测试时间段特征"""
        df = self.engineer.extract_datetime_features(self.test_data)

        self.assertIn('time_period', df.columns)

        # 10:30 是 Morning
        self.assertEqual(df['time_period'].iloc[0], 'Morning')

        # 15:45 是 Afternoon
        self.assertEqual(df['time_period'].iloc[1], 'Afternoon')

        # 23:59 是 Night
        self.assertEqual(df['time_period'].iloc[3], 'Night')

    def test_create_geographic_grid(self):
        """测试地理网格特征"""
        df = self.engineer.create_geographic_grid(self.test_data)

        self.assertIn('lat_bin', df.columns)
        self.assertIn('lon_bin', df.columns)
        self.assertIn('grid_id', df.columns)

        # 检查网格ID格式
        self.assertTrue(all(isinstance(x, str) for x in df['grid_id']))
        self.assertTrue(all('_' in x for x in df['grid_id']))

    def test_encode_categorical(self):
        """测试分类变量编码"""
        df = self.engineer.encode_categorical(self.test_data)

        self.assertIn('Primary Type_encoded', df.columns)
        self.assertIn('Location Description_encoded', df.columns)

        # 检查编码是否为整数
        self.assertTrue(pd.api.types.is_integer_dtype(df['Primary Type_encoded']))

    def test_create_crime_severity_score(self):
        """测试严重程度评分"""
        df = self.engineer.create_crime_severity_score(self.test_data)

        self.assertIn('severity_score', df.columns)

        # 检查评分范围
        self.assertTrue(all(df['severity_score'] >= 1))
        self.assertTrue(all(df['severity_score'] <= 10))

        # HOMICIDE 应该是最高分
        df_homicide = pd.DataFrame({
            'Primary Type': ['HOMICIDE', 'ASSAULT', 'THEFT']
        })
        df_homicide = self.engineer.create_crime_severity_score(df_homicide)
        self.assertEqual(df_homicide['severity_score'].iloc[0], 10)

    def test_extract_all_features(self):
        """测试提取所有特征"""
        df = self.engineer.extract_all_features(self.test_data)

        expected_features = self.engineer.get_feature_columns()
        for feature in expected_features:
            self.assertIn(feature, df.columns)

    def test_categorize_time_period(self):
        """测试时间段分类函数"""
        # Morning: 5-12
        self.assertEqual(self.engineer._categorize_time_period(5), 'Morning')
        self.assertEqual(self.engineer._categorize_time_period(11), 'Morning')

        # Afternoon: 12-17
        self.assertEqual(self.engineer._categorize_time_period(12), 'Afternoon')
        self.assertEqual(self.engineer._categorize_time_period(16), 'Afternoon')

        # Evening: 17-21
        self.assertEqual(self.engineer._categorize_time_period(17), 'Evening')
        self.assertEqual(self.engineer._categorize_time_period(20), 'Evening')

        # Night: 21-5
        self.assertEqual(self.engineer._categorize_time_period(21), 'Night')
        self.assertEqual(self.engineer._categorize_time_period(4), 'Night')
        self.assertEqual(self.engineer._categorize_time_period(0), 'Night')


class TestFeatureEngineerEdgeCases(unittest.TestCase):
    """测试边界情况"""

    def setUp(self):
        self.config = Config()
        self.engineer = FeatureEngineer(self.config)

    def test_empty_dataframe(self):
        """测试空数据框"""
        empty_df = pd.DataFrame({'Date': pd.to_datetime([])})

        with self.assertRaises((ValueError, IndexError)):
            self.engineer.extract_datetime_features(empty_df)

    def test_invalid_date_column(self):
        """测试无效日期列"""
        df = pd.DataFrame({'OtherColumn': [1, 2, 3]})

        with self.assertRaises(ValueError):
            self.engineer.extract_datetime_features(df)

    def test_unknown_crime_type(self):
        """测试未知犯罪类型"""
        df = pd.DataFrame({'Primary Type': ['UNKNOWN_TYPE', 'OTHER']})
        df = self.engineer.create_crime_severity_score(df)

        # 未知类型应该得到默认分数1
        self.assertEqual(df['severity_score'].iloc[0], 1)


if __name__ == '__main__':
    unittest.main()
