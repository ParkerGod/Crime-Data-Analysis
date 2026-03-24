"""
犯罪数据分析主入口
使用命令行参数指定分析目标、输入文件和输出目录
"""
import argparse
import sys
import os

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.crime_analysis.config import Config
from src.crime_analysis.pipeline import AnalysisPipeline, run_pipeline


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='犯罪数据分析工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行所有分析
  python main.py -i data/crimes.csv

  # 只运行特定分析目标
  python main.py -i data/crimes.csv -o trends temporal

  # 指定输出目录
  python main.py -i data/crimes.csv -o results/ trends types

可用的分析目标:
  trends      - 犯罪趋势分析 (年度趋势折线图) - 对应原图扩展
  types       - Top 10犯罪类别分析 (水平条形图) - 对应原图1
  temporal    - 月度犯罪趋势分析 (月度条形图) - 对应原图2
  geographic  - 犯罪热点检测 (网格热力图) - 对应原图3
  arrests     - 受害者年龄分布 (按犯罪类型和性别散点图) - 对应原图4
  victim_age  - 受害者年龄分布 (直方图) - 对应原图6
  status      - 犯罪状态分布分析 (条形图) - 对应原图7
  area_trends - 2020年各区域月度趋势 (折线图) - 对应原图8
  all         - 运行所有分析 (默认)
        """
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        required=True,
        help='输入数据文件路径 (支持 CSV, Parquet, Excel)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='outputs',
        help='输出目录路径 (默认: outputs)'
    )

    parser.add_argument(
        '--year-start',
        type=int,
        default=2010,
        help='起始年份 (默认: 2010)'
    )

    parser.add_argument(
        '--year-end',
        type=int,
        default=2024,
        help='结束年份 (默认: 2024)'
    )

    parser.add_argument(
        '--lat-bins',
        type=int,
        default=50,
        help='纬度网格数 (默认: 50)'
    )

    parser.add_argument(
        '--lon-bins',
        type=int,
        default=50,
        help='经度网格数 (默认: 50)'
    )

    parser.add_argument(
        '--show-plots',
        action='store_true',
        help='显示图表 (默认保存到文件)'
    )

    parser.add_argument(
        'objectives',
        nargs='*',
        default=['all'],
        help='要运行的分析目标 (默认: all)'
    )

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_arguments()

    # 检查输入文件是否存在
    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}")
        sys.exit(1)

    # 创建配置
    config = Config(
        year_start=args.year_start,
        year_end=args.year_end,
        lat_bins=args.lat_bins,
        lon_bins=args.lon_bins,
        show_plots=args.show_plots,
        save_plots=True,
        output_dir=args.output
    )

    # 处理分析目标 (8个目标对应8张图)
    available_objectives = [
        'trends',      # 目标1: 犯罪趋势分析
        'types',       # 目标2: 犯罪类型分析
        'temporal',    # 目标3: 时间模式分析
        'geographic',  # 目标4: 地理分布分析
        'arrests',     # 目标5: 受害者分析
        'victim_age',  # 目标6: 受害者年龄分布
        'status',      # 目标7: 犯罪状态分布
        'area_trends', # 目标8: 2020年区域月度趋势
    ]

    if 'all' in args.objectives:
        objectives = available_objectives
    else:
        # 验证目标名称
        invalid = [obj for obj in args.objectives if obj not in available_objectives]
        if invalid:
            print(f"错误: 未知的分析目标: {invalid}")
            print(f"可用目标: {available_objectives}")
            sys.exit(1)
        objectives = args.objectives

    print("=" * 60)
    print("犯罪数据分析工具")
    print("=" * 60)
    print(f"输入文件: {args.input}")
    print(f"输出目录: {args.output}")
    print(f"分析目标: {', '.join(objectives)}")
    print(f"年份范围: {args.year_start} - {args.year_end}")
    print("=" * 60)

    try:
        # 运行管道
        results = run_pipeline(
            input_file=args.input,
            output_dir=args.output,
            objectives=objectives,
            config=config
        )

        print("\n" + "=" * 60)
        print("分析完成!")
        print("=" * 60)

        # 打印简要结果
        for obj_name, obj_results in results.get('results', {}).items():
            print(f"\n[{obj_name}]")
            if 'statistics' in obj_results:
                for key, value in obj_results['statistics'].items():
                    print(f"  {key}: {value}")
            if 'error' in obj_results:
                print(f"  错误: {obj_results['error']}")

        print(f"\n详细结果已保存到: {args.output}")

    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
