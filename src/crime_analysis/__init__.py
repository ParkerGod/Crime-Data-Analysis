"""
犯罪数据分析包
"""
from .config import Config, DEFAULT_CONFIG
from .data import DataLoader
from .preprocess import DataPreprocessor
from .features import FeatureEngineer
from .plotting import PlotManager

__all__ = [
    'Config',
    'DEFAULT_CONFIG',
    'DataLoader',
    'DataPreprocessor',
    'FeatureEngineer',
    'PlotManager',
]

__version__ = '1.0.0'
