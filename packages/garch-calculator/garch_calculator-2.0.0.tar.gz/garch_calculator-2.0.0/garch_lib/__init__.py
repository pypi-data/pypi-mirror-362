"""
GARCH计算器库 - 高性能金融时间序列波动率建模

这个库提供了GARCH(1,1)-GED模型的高性能C++实现，
专门为金融时间序列分析设计。

主要特点:
- 基于增量更新的高效计算
- 支持GED（广义误差分布）
- 线程安全设计
- 实时波动率预测
"""

__version__ = "2.0.0"
__author__ = "biteasquirrel"
__email__ = "biteasquirrel@gmail.com"
__license__ = "MIT"

# 导入C++扩展模块中的所有类和函数
try:
    from ._garch_calculator import (
        # 主要类
        GarchCalculator,
        
        # 数据结构
        GarchParameters,
        PricePoint,
        VolatilityForecast,
        EstimationResult,
        BasicStats,
        
        # 工具函数
        calculate_basic_stats,
        calculate_autocorrelation,
        calculate_ljung_box_statistic,
        calculate_var,
        calculate_expected_shortfall,
    )
    
    # 设置模块级别的文档
    __all__ = [
        'GarchCalculator',
        'GarchParameters', 
        'PricePoint',
        'VolatilityForecast',
        'EstimationResult',
        'BasicStats',
        'calculate_basic_stats',
        'calculate_autocorrelation',
        'calculate_ljung_box_statistic',
        'calculate_var',
        'calculate_expected_shortfall',
    ]

except ImportError as e:
    import warnings
    warnings.warn(f"无法导入C++扩展模块: {e}")
    raise

# Version info as tuple
VERSION_INFO = tuple(map(int, __version__.split('.')))

def get_version():
    """Return the version string."""
    return __version__

def get_build_info():
    """Return build information."""
    try:
        from .garch_calculator import GarchCalculator
        return {
            'version': __version__,
            'has_extension': True,
            'thread_safe_support': True,
            'boost_support': True
        }
    except ImportError:
        return {
            'version': __version__,
            'has_extension': False,
            'thread_safe_support': False,
            'boost_support': False
        } 