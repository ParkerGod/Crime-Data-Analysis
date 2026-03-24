"""
配置文件 - 管理各种参数
"""
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """配置类"""

    # 文件路径
    data_dir: str = "data"
    output_dir: str = "outputs"
    input_file: Optional[str] = None

    # 年份范围
    year_start: int = 2010
    year_end: int = 2024

    # 地理网格设置
    lat_bins: int = 50
    lon_bins: int = 50

    # 显示设置
    show_plots: bool = False
    save_plots: bool = True

    # 图表设置
    figure_dpi: int = 300
    figure_format: str = "png"

    # 数据列名映射 (基于 Crime_Data.csv 实际列名)
    required_columns = [
        "DATE OCC",
        "Crm Cd Desc",
        "Vict Age",
        "LAT",
        "LON",
    ]

    date_column: str = "DATE OCC"
    crime_type_column: str = "Crm Cd Desc"
    location_column: str = "Premis Desc"
    arrest_column: str = "Status Desc"
    domestic_column: str = "Status"
    lat_column: str = "LAT"
    lon_column: str = "LON"

    def __post_init__(self):
        """初始化后处理"""
        # 确保输出目录存在
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)

    def get_output_path(self, filename: str) -> str:
        """获取输出文件路径"""
        return os.path.join(self.output_dir, filename)

    def get_data_path(self, filename: str) -> str:
        """获取数据文件路径"""
        return os.path.join(self.data_dir, filename)


# 默认配置实例
DEFAULT_CONFIG = Config()
