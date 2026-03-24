"""
分析目标单元测试
"""
import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from crime_analysis.config import Config
from crime_analysis.features import FeatureEngineer
from analyses.objective_01 import analyze_crime_trends
from analyses.objective_02 import analyze_crime_types
from analyses.objective_03 import analyze_temporal_patterns
from analyses.objective_04 import analyze_geographic_distribution
from analyses.objective_05 import analyze_arrest_patterns


class TestAnalysisObjectives(unittest.TestCase):
    """测试分析目标函数"""

    def setUp(self):
        """设置测试数据"""
        self.config = Config()

        # 创建测试数据
        self.test_data = pd.DataFrame({
            'Date': pd.to_datetime([
                '2020-01-15 10:30:00',
                '2020-06-20 15:45:00',
                '2021-03-10 08:00:00',
                '2021-12-25 23:59:00',
                '2022-07-04 14:20:00',
                '2022-08-15 20:00:00',
                '2020-03-01 12:00:00',
                '2021-09-10 18:30:00',
            ]),
            'Primary Type': ['THEFT', 'BATTERY', 'ASSAULT', 'THEFT', 'ROBBERY', 'BATTERY', 'THEFT', 'ASSAULT'],
            'Location Description': ['STREET', 'SIDEWALK', 'APARTMENT', 'STREET', 'STORE', 'SIDEWALK', 'STREET', 'APARTMENT'],
            'Arrest': [False, True, False, False, True, False, True, False],
            'Domestic': [False, False, True, False, False, False, False, True],
            'Latitude': [41.8781, 41.8782, 41.8783, 41.8784, 41.8785, 41.8786, 41.8787, 41.8788],
            'Longitude': [-87.6298, -87.6299, -87.6300, -87.6301, -87.6302, -87.6303, -87.6304, -87.6305],
        })

        # 提取特征
        engineer = FeatureEngineer(self.config)
        self.featured_data = engineer.extract_all_features(self.test_data)

    def test_analyze_crime_trends(self):
        """测试犯罪趋势分析"""
        results = analyze_crime_trends(self.featured_data, self.config)

        # 检查结果结构
        self.assertIn('title', results)
        self.assertIn('tables', results)
        self.assertIn('statistics', results)

        # 检查统计信息
        self.assertIn('max_year', results['statistics'])
        self.assertIn('min_year', results['statistics'])

        # 检查表格
        self.assertIn('yearly_trend', results['tables'])
        yearly = results['tables']['yearly_trend']
        self.assertIn('year', yearly.columns)
        self.assertIn('count', yearly.columns)

        # 验证数据
        self.assertEqual(len(yearly), 3)  # 2020, 2021, 2022
        self.assertEqual(yearly['count'].sum(), len(self.test_data))

    def test_analyze_crime_types(self):
        """测试犯罪类型分析"""
        results = analyze_crime_types(self.featured_data, self.config)

        # 检查结果结构
        self.assertIn('title', results)
        self.assertIn('tables', results)
        self.assertIn('statistics', results)

        # 检查统计信息
        self.assertIn('total_types', results['statistics'])
        self.assertIn('top_crime', results['statistics'])

        # 检查表格
        self.assertIn('crime_type_distribution', results['tables'])
        dist = results['tables']['crime_type_distribution']
        self.assertIn('crime_type', dist.columns)
        self.assertIn('count', dist.columns)
        self.assertIn('percentage', dist.columns)

        # 验证百分比总和接近100
        self.assertAlmostEqual(dist['percentage'].sum(), 100, delta=0.1)

        # 检查Top 10
        self.assertIn('top10_crimes', results['tables'])

    def test_analyze_temporal_patterns(self):
        """测试时间模式分析"""
        results = analyze_temporal_patterns(self.featured_data, self.config)

        # 检查结果结构
        self.assertIn('title', results)
        self.assertIn('tables', results)
        self.assertIn('statistics', results)

        # 检查统计信息
        self.assertIn('peak_hour', results['statistics'])

        # 检查表格
        self.assertIn('hourly_distribution', results['tables'])
        hourly = results['tables']['hourly_distribution']
        self.assertIn('hour', hourly.columns)
        self.assertIn('count', hourly.columns)

        # 检查星期分布
        self.assertIn('daily_distribution', results['tables'])

        # 检查热力图数据
        self.assertIn('heatmap_data', results['tables'])

    def test_analyze_geographic_distribution(self):
        """测试地理分布分析"""
        results = analyze_geographic_distribution(self.featured_data, self.config)

        # 检查结果结构
        self.assertIn('title', results)
        self.assertIn('tables', results)
        self.assertIn('statistics', results)

        # 检查统计信息
        self.assertIn('lat_range', results['statistics'])
        self.assertIn('lon_range', results['statistics'])
        self.assertIn('center_point', results['statistics'])

        # 检查网格统计
        self.assertIn('grid_statistics', results['tables'])

    def test_analyze_arrest_patterns(self):
        """测试逮捕模式分析"""
        results = analyze_arrest_patterns(self.featured_data, self.config)

        # 检查结果结构
        self.assertIn('title', results)
        self.assertIn('tables', results)
        self.assertIn('statistics', results)

        # 检查统计信息
        self.assertIn('total_records', results['statistics'])
        self.assertIn('arrest_count', results['statistics'])
        self.assertIn('arrest_rate', results['statistics'])

        # 验证逮捕率计算
        total = results['statistics']['total_records']
        arrests = results['statistics']['arrest_count']
        rate = results['statistics']['arrest_rate']
        expected_rate = round(arrests / total * 100, 2)
        self.assertEqual(rate, expected_rate)

        # 检查表格
        self.assertIn('arrest_by_type', results['tables'])
        arrest_by_type = results['tables']['arrest_by_type']
        self.assertIn('arrest_rate', arrest_by_type.columns)


class TestAnalysisObjectivesEdgeCases(unittest.TestCase):
    """测试边界情况"""

    def setUp(self):
        self.config = Config()

    def test_empty_dataframe(self):
        """测试空数据框"""
        empty_df = pd.DataFrame({
            'Date': pd.to_datetime([]),
            'Primary Type': [],
            'Arrest': [],
            'Latitude': [],
            'Longitude': [],
        })

        # 大多数分析应该能处理空数据框
        results = analyze_crime_trends(empty_df, self.config)
        self.assertIn('tables', results)

    def test_missing_columns(self):
        """测试缺少列的情况"""
        df = pd.DataFrame({'OtherColumn': [1, 2, 3]})

        # 应该返回包含错误信息的结果
        results = analyze_arrest_patterns(df, self.config)
        self.assertIn('error', results)

    def test_single_record(self):
        """测试单条记录"""
        df = pd.DataFrame({
            'Date': pd.to_datetime(['2020-01-01 12:00:00']),
            'Primary Type': ['THEFT'],
            'Arrest': [True],
            'Latitude': [41.8],
            'Longitude': [-87.6],
        })

        engineer = FeatureEngineer(self.config)
        featured_df = engineer.extract_all_features(df)

        results = analyze_crime_types(featured_df, self.config)
        self.assertEqual(results['statistics']['total_types'], 1)
        self.assertEqual(results['statistics']['top_crime'], 'THEFT')


if __name__ == '__main__':
    unittest.main()
