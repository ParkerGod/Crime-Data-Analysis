"""
流程编排模块 - 串联各个模块
"""
import pandas as pd
from typing import List, Dict, Optional, Callable
from datetime import datetime
import json
import os

from .config import Config
from .data import DataLoader
from .preprocess import DataPreprocessor
from .features import FeatureEngineer
from .plotting import PlotManager

# 导入分析目标
from analyses.objective_01 import analyze_crime_trends
from analyses.objective_02 import analyze_crime_types
from analyses.objective_03 import analyze_temporal_patterns
from analyses.objective_04 import analyze_geographic_distribution
from analyses.objective_05 import analyze_arrest_patterns
from analyses.objective_06 import analyze_victim_age_distribution
from analyses.objective_07 import analyze_crime_status_distribution
from analyses.objective_08 import analyze_monthly_trends_by_area


class AnalysisPipeline:
    """分析流程管道"""

    # 可用的分析目标 (对应8张图)
    AVAILABLE_OBJECTIVES = {
        'trends': analyze_crime_trends,           # 目标1: 犯罪趋势分析
        'types': analyze_crime_types,             # 目标2: 犯罪类型分析
        'temporal': analyze_temporal_patterns,    # 目标3: 时间模式分析
        'geographic': analyze_geographic_distribution,  # 目标4: 地理分布分析
        'arrests': analyze_arrest_patterns,       # 目标5: 逮捕模式分析
        'victim_age': analyze_victim_age_distribution,  # 目标6: 受害者年龄分布
        'status': analyze_crime_status_distribution,    # 目标7: 犯罪状态分布
        'area_trends': analyze_monthly_trends_by_area,  # 目标8: 区域月度趋势
    }

    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.data_loader = DataLoader(self.config)
        self.preprocessor = DataPreprocessor(self.config)
        self.feature_engineer = FeatureEngineer(self.config)
        self.plot_manager = PlotManager(self.config)
        self.raw_data = None
        self.cleaned_data = None
        self.featured_data = None

    def load_data(self, file_path: str = None) -> 'AnalysisPipeline':
        """
        加载数据

        Args:
            file_path: 数据文件路径

        Returns:
            self (链式调用)
        """
        print("[Pipeline] 正在加载数据...")
        self.raw_data = self.data_loader.load_data(file_path)
        print(f"[Pipeline] 数据加载完成: {len(self.raw_data):,} 行")

        # 显示基本信息
        stats = self.data_loader.get_basic_stats(self.raw_data)
        print(f"[Pipeline] 列数: {stats['total_columns']}")
        print(f"[Pipeline] 内存占用: {stats['memory_usage_mb']:.2f} MB")

        return self

    def preprocess(self) -> 'AnalysisPipeline':
        """
        数据预处理

        Returns:
            self (链式调用)
        """
        if self.raw_data is None:
            raise ValueError("请先加载数据")

        print("\n[Pipeline] 开始数据清洗...")
        self.cleaned_data, report = self.preprocessor.clean(self.raw_data)

        # 打印清洗报告
        summary = self.preprocessor.get_cleaning_summary(report)
        print(summary)

        return self

    def extract_features(self) -> 'AnalysisPipeline':
        """
        特征提取

        Returns:
            self (链式调用)
        """
        if self.cleaned_data is None:
            raise ValueError("请先进行数据预处理")

        print("\n[Pipeline] 正在提取特征...")
        self.featured_data = self.feature_engineer.extract_all_features(self.cleaned_data)

        feature_cols = self.feature_engineer.get_feature_columns()
        added_features = [col for col in feature_cols if col in self.featured_data.columns]
        print(f"[Pipeline] 已添加 {len(added_features)} 个特征")

        return self

    def run_analysis(self, objectives: List[str] = None) -> Dict:
        """
        运行分析

        Args:
            objectives: 要运行的分析目标列表，None表示运行所有

        Returns:
            Dict: 所有分析结果
        """
        if self.featured_data is None:
            raise ValueError("请先提取特征")

        if objectives is None:
            objectives = list(self.AVAILABLE_OBJECTIVES.keys())

        results = {
            'timestamp': datetime.now().isoformat(),
            'objectives_run': objectives,
            'results': {}
        }

        print(f"\n[Pipeline] 开始运行 {len(objectives)} 个分析目标...")

        for obj_name in objectives:
            if obj_name not in self.AVAILABLE_OBJECTIVES:
                print(f"[Pipeline] 警告: 未知的分析目标 '{obj_name}'，已跳过")
                continue

            print(f"\n[Pipeline] 运行分析目标: {obj_name}")
            analyzer = self.AVAILABLE_OBJECTIVES[obj_name]

            try:
                obj_results = analyzer(self.featured_data, self.config)
                results['results'][obj_name] = obj_results
                print(f"[Pipeline] ✓ {obj_name} 完成")
            except Exception as e:
                print(f"[Pipeline] ✗ {obj_name} 失败: {str(e)}")
                results['results'][obj_name] = {'error': str(e)}

        return results

    def save_results(self, results: Dict, output_dir: str = None) -> str:
        """
        保存分析结果

        Args:
            results: 分析结果字典
            output_dir: 输出目录

        Returns:
            str: 输出目录路径
        """
        if output_dir is None:
            output_dir = self.config.output_dir

        os.makedirs(output_dir, exist_ok=True)

        # 保存JSON结果
        results_file = os.path.join(output_dir, 'analysis_results.json')

        # 转换DataFrame为字典以便JSON序列化
        json_results = self._convert_to_json_serializable(results)

        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(json_results, f, ensure_ascii=False, indent=2)

        print(f"\n[Pipeline] 结果已保存到: {output_dir}")
        print(f"[Pipeline] 报告文件: {results_file}")

        # 保存表格为CSV
        self._save_tables_as_csv(results, output_dir)

        return output_dir

    def _convert_to_json_serializable(self, obj):
        """将对象转换为JSON可序列化的格式"""
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient='records')
        elif isinstance(obj, dict):
            return {k: self._convert_to_json_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._convert_to_json_serializable(item) for item in obj]
        elif isinstance(obj, (int, float, str, bool, type(None))):
            return obj
        else:
            return str(obj)

    def _save_tables_as_csv(self, results: Dict, output_dir: str):
        """将表格保存为CSV文件"""
        for obj_name, obj_results in results.get('results', {}).items():
            if 'tables' in obj_results:
                for table_name, table_data in obj_results['tables'].items():
                    if isinstance(table_data, pd.DataFrame):
                        filename = f"{obj_name}_{table_name}.csv"
                        filepath = os.path.join(output_dir, filename)
                        table_data.to_csv(filepath, index=False)
                        print(f"[Pipeline] 表格已保存: {filename}")

    def run_full_pipeline(self, file_path: str = None, objectives: List[str] = None) -> Dict:
        """
        运行完整流程

        Args:
            file_path: 数据文件路径
            objectives: 分析目标列表

        Returns:
            Dict: 分析结果
        """
        return (
            self
            .load_data(file_path)
            .preprocess()
            .extract_features()
            .run_analysis(objectives)
        )


def run_pipeline(
    input_file: str,
    output_dir: str = "outputs",
    objectives: List[str] = None,
    config: Config = None
) -> Dict:
    """
    便捷的管道运行函数

    Args:
        input_file: 输入文件路径
        output_dir: 输出目录
        objectives: 分析目标列表
        config: 配置对象

    Returns:
        Dict: 分析结果
    """
    config = config or Config()
    config.output_dir = output_dir
    config.input_file = input_file

    pipeline = AnalysisPipeline(config)
    results = pipeline.run_full_pipeline(input_file, objectives)
    pipeline.save_results(results, output_dir)

    return results
