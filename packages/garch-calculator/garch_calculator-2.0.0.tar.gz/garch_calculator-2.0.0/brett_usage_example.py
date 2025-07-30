#!/usr/bin/env python3
"""
Brett.csv数据的GARCH模型实际使用示例
展示如何使用优化后的参数进行预测
"""

import garch_lib as gc
import pandas as pd
import numpy as np
from brett_optimized_garch import BrettOptimizedGarch
import matplotlib.pyplot as plt

def simple_forecast_example():
    """简单的预测示例"""
    print("🎯 简单预测示例")
    print("=" * 50)
    
    # 读取数据
    df = pd.read_csv('brett.csv')
    returns = df['c_scaled'].values[:100]  # 使用前100个点作为历史数据
    
    # 方法1: 使用优化参数直接预测
    print("\n📊 方法1: 使用预设的优化参数")
    calc1 = BrettOptimizedGarch.create_calculator('default')
    calc1.add_returns(returns.tolist())
    
    forecast1 = calc1.forecast_volatility(horizon=1)
    print(f"   下期波动率预测: {forecast1.volatility:.6f}")
    print(f"   置信度分数: {forecast1.confidence_score:.6f}")
    
    # 方法2: 使用快速网格搜索优化
    print("\n🔍 方法2: 快速网格搜索 + 预测")
    grid_result = BrettOptimizedGarch.quick_grid_search(returns, grid_points=3)
    
    if grid_result['best_params']:
        best_params = grid_result['best_params']
        print(f"   网格搜索最优参数: ω={best_params['omega']:.4f}, "
              f"α={best_params['alpha']:.4f}, β={best_params['beta']:.4f}")
        
        # 使用最优参数预测
        calc2 = gc.GarchCalculator(history_size=len(returns) + 10)
        calc2.add_returns(returns.tolist())
        
        params = gc.GarchParameters()
        params.mu = best_params['mu']
        params.omega = best_params['omega']
        params.alpha = best_params['alpha']
        params.beta = best_params['beta']
        params.nu = best_params['nu']
        calc2.set_parameters(params)
        
        forecast2 = calc2.forecast_volatility(horizon=1)
        print(f"   优化后预测: {forecast2.volatility:.6f}")
        print(f"   似然值: {best_params['likelihood']:.6f}")

def rolling_prediction_example():
    """滚动预测示例"""
    print("\n🔄 滚动预测示例")
    print("=" * 50)
    
    # 执行滚动预测
    result = BrettOptimizedGarch.rolling_forecast_brett(
        param_set='default', 
        window_size=150, 
        data_points=250
    )
    
    if 'error' not in result:
        print(f"\n📈 滚动预测结果:")
        print(f"   成功率: {result['success_rate']:.2%} ({result['success_count']}/{result['total_attempts']})")
        print(f"   与arch库相关性: {result['correlation']:.4f}")
        print(f"   平均绝对误差: {result['mae']:.6f}")
        print(f"   MAPE: {result['mape']:.2f}%")
        print(f"   garch_lib平均预测: {result['garch_mean']:.6f}")
        print(f"   arch库平均预测: {result['arch_mean']:.6f}")
        
        # 显示最后几个预测
        print(f"\n📊 最后5个预测对比:")
        garch_preds = result['garch_predictions'][-5:]
        arch_preds = result['arch_predictions'][-5:]
        
        for i, (g, a) in enumerate(zip(garch_preds, arch_preds)):
            diff = abs(g - a)
            print(f"   {i+1}. garch_lib: {g:.4f}, arch: {a:.4f}, 差异: {diff:.4f}")

def parameter_comparison():
    """参数对比示例"""
    print("\n⚖️  参数集对比")
    print("=" * 50)
    
    df = pd.read_csv('brett.csv')
    test_data = df['c_scaled'].values[200:400]  # 使用200个点测试
    
    param_sets = ['default', 'high_volatility', 'stable_period', 'arch_like']
    
    results = {}
    for param_set in param_sets:
        try:
            comparison = BrettOptimizedGarch.compare_with_arch(test_data, param_set)
            if 'error' not in comparison:
                results[param_set] = comparison
        except Exception as e:
            print(f"   {param_set} 测试失败: {e}")
    
    # 显示对比结果
    print(f"\n📊 各参数集与arch库的对比:")
    print(f"{'参数集':<15} {'似然值差异':<12} {'参数距离':<12} {'是否更优':<8}")
    print("-" * 50)
    
    for name, result in results.items():
        param_distance = np.mean(list(result['param_differences'].values()))
        improvement = "✅" if result['improvement_over_arch'] else "❌"
        print(f"{name:<15} {result['likelihood_difference']:<12.4f} {param_distance:<12.4f} {improvement:<8}")

def quick_usage_template():
    """快速使用模板"""
    print("\n💡 快速使用模板")
    print("=" * 50)
    
    template_code = '''
# 1. 导入必要模块
import garch_lib as gc
from brett_optimized_garch import BrettOptimizedGarch

# 2. 准备你的收益率数据
returns = your_return_data  # numpy数组或列表

# 3. 方式A: 使用预设优化参数（推荐）
calc = BrettOptimizedGarch.create_calculator('default')
calc.add_returns(returns.tolist())
forecast = calc.forecast_volatility(1)
print(f"预测波动率: {forecast.volatility:.6f}")

# 4. 方式B: 自定义快速网格搜索
grid_result = BrettOptimizedGarch.quick_grid_search(returns)
if grid_result['best_params']:
    # 使用搜索到的最优参数
    params = gc.GarchParameters()
    best = grid_result['best_params']
    params.mu = best['mu']
    params.omega = best['omega']
    params.alpha = best['alpha']
    params.beta = best['beta']
    params.nu = best['nu']
    
    calc.set_parameters(params)
    forecast = calc.forecast_volatility(1)
    print(f"优化后预测: {forecast.volatility:.6f}")

# 5. 方式C: 直接获取参数对象
optimized_params = BrettOptimizedGarch.get_parameters('default')
calc.set_parameters(optimized_params)
'''
    
    print(template_code)

def main():
    """主函数演示"""
    print("🚀 Brett.csv GARCH模型使用示例")
    print("=" * 60)
    
    # 简单预测示例
    simple_forecast_example()
    
    # 滚动预测示例
    rolling_prediction_example()
    
    # 参数对比
    parameter_comparison()
    
    # 使用模板
    quick_usage_template()
    
    print(f"\n✅ 示例完成！")
    print(f"\n💎 关键优势:")
    print(f"   1. 参数已通过网格搜索优化，接近arch库水平")
    print(f"   2. 预设多种参数集，适应不同市场条件")
    print(f"   3. 支持快速网格搜索进一步优化")
    print(f"   4. 保持与arch库的高度一致性")
    
    print(f"\n📝 推荐使用流程:")
    print(f"   1. 大多数情况下使用 'default' 参数集")
    print(f"   2. 高波动期使用 'high_volatility' 参数集") 
    print(f"   3. 如需最优性能，运行快速网格搜索")
    print(f"   4. 定期与arch库对比验证")

if __name__ == "__main__":
    main() 