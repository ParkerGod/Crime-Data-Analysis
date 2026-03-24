"""
分析目标6-8单元测试
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
from analyses.objective_06 import analyze_victim_age_distribution
from analyses.objective_07 import analyze_crime_status_distribution
from analyses.objective_08 import analyze_monthly_trends_by_area


class TestAnalysisObjectives6To8(unittest.TestCase):
    """测试分析目标6-8"""

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
                '2020-09-10 18:30:00',
            ]),
            'Year': [2020, 2020, 2021, 2021, 2022, 2022, 2020, 2020],
            'Month': [1, 6, 3, 12, 7, 8, 3, 9],
            'Primary Type': ['THEFT', 'BATTERY', 'ASSAULT', 'THEFT', 'ROBBERY', 'BATTERY', 'THEFT', 'ASSAULT'],
            'Vict Age': [25, 34, 45, 67, 23, 89, 12, 56],
            'Vict Sex': ['M', 'F', 'M', 'F', 'M', 'F', 'X', 'M'],
            'Status Desc': ['Invest Cont', 'Adult Arrest', 'Invest Cont', 'Juvenile Arrest', 'Invest Cont', 'Adult Arrest', 'Invest Cont', 'Adult Arrest'],
            'AREA NAME': ['Central', 'North', 'South', 'Central', 'West', 'North', 'Central', 'South'],
            'Arrest': [False, True, False, False, True, False, True, False],
            'Latitude': [41.8781, 41.8782, 41.8783, 41.8784, 41.8785, 41.8786, 41.8787, 41.8788],
            'Longitude': [-87.6298, -87.6299, -87.6300, -87.6301, -87.6302, -87.6303, -87.6304, -87.6305],
        })

    def test_analyze_victim_age_distribution(self):
        """测试受害者年龄分布分析"""
        results = analyze_victim_age_distribution(self.test_data, self.config)

        # 检查结果结构
        self.assertIn('title', results)
        self.assertIn('tables', results)
        self.assertIn('statistics', results)

        # 检查统计信息
        self.assertIn('mean_age', results['statistics'])
        self.assertIn('median_age', results['statistics'])

        # 检查表格
        self.assertIn('age_group_distribution', results['tables'])
        age_groups = results['tables']['age_group_distribution']
        self.assertIn('age_group', age_groups.columns)
        self.assertIn('count', age_groups.columns)
        self.assertIn('percentage', age_groups.columns)

    def test_analyze_crime_status_distribution(self):
        """测试犯罪状态分布分析"""
        results = analyze_crime_status_distribution(self.test_data, self.config)

        # 检查结果结构
        self.assertIn('title', results)
        self.assertIn('tables', results)
        self.assertIn('statistics', results)

        # 检查统计信息
        self.assertIn('total_status_types', results['statistics'])
        self.assertIn('most_common_status', results['statistics'])

        # 检查表格
        self.assertIn('status_distribution', results['tables'])
        status_dist = results['tables']['status_distribution']
        self.assertIn('status', status_dist.columns)
        self.assertIn('count', status_dist.columns)
        self.assertIn('percentage', status_dist.columns)

        # 验证百分比总和接近100
        self.assertAlmostEqual(status_dist['percentage'].sum(), 100, delta=0.1)

    def test_analyze_monthly_trends_by_area(self):
        """测试2020年各区域月度犯罪趋势分析"""
        results = analyze_monthly_trends_by_area(self.test_data, self.config)

        # 检查结果结构
        self.assertIn('title', results)
        self.assertIn('tables', results)
        self.assertIn('statistics', results)

        # 检查统计信息
        self.assertIn('total_crimes_2020', results['statistics'])
        self.assertIn('total_areas', results['statistics'])

        # 检查表格
        self.assertIn('area_totals', results['tables'])
        area_totals = results['tables']['area_totals']
        self.assertIn('area_name', area_totals.columns)
        self.assertIn('total_crimes', area_totals.columns)


class TestAnalysisObjectives6To8EdgeCases(unittest.TestCase):
    """测试边界情况"""

    def setUp(self):
        self.config = Config()

    def test_victim_age_missing_column(self):
        """测试缺少受害者年龄列"""
        df = pd.DataFrame({'OtherColumn': [1, 2, 3]})
        results = analyze_victim_age_distribution(df, self.config)
        self.assertIn('error', results)

    def test_status_missing_column(self):
        """测试缺少状态列"""
        df = pd.DataFrame({'OtherColumn': [1, 2, 3]})
        results = analyze_crime_status_distribution(df, self.config)
        self.assertIn('error', results)

    def test_area_trends_missing_columns(self):
        """测试缺少区域列"""
        df = pd.DataFrame({'Year': [2020], 'Month': [1]})
        results = analyze_monthly_trends_by_area(df, self.config)
        self.assertIn('error', results)

    def test_victim_age_invalid_data(self):
        """测试无效年龄数据"""
        df = pd.DataFrame({
            'Vict Age': [-5, 0, 150, 200],  # 无效年龄
        })
        results = analyze_victim_age_distribution(df, self.config)
        self.assertIn('error', results)


if __name__ == '__main__':
    unittest.main()
