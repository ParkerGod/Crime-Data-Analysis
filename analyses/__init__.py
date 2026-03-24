"""
分析目标模块
"""
from .objective_01 import analyze_crime_trends
from .objective_02 import analyze_crime_types
from .objective_03 import analyze_temporal_patterns
from .objective_04 import analyze_geographic_distribution
from .objective_05 import analyze_arrest_patterns
from .objective_06 import analyze_victim_age_distribution
from .objective_07 import analyze_crime_status_distribution
from .objective_08 import analyze_monthly_trends_by_area

__all__ = [
    'analyze_crime_trends',
    'analyze_crime_types',
    'analyze_temporal_patterns',
    'analyze_geographic_distribution',
    'analyze_arrest_patterns',
    'analyze_victim_age_distribution',
    'analyze_crime_status_distribution',
    'analyze_monthly_trends_by_area',
]
