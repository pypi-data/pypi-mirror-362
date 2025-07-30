#!/usr/bin/env python3
"""
测试新的预设参数功能
验证v1.2.0的预设参数系统
"""

import garch_lib as gc
import pandas as pd
import numpy as np

def test_preset_parameters():
    """测试所有预设参数功能"""
    print("🚀 测试 garch_lib v1.2.0 预设参数功能")
    print("=" * 60)
    
    # 1. 测试获取预设名称
    print("📋 可用的预设参数:")
    preset_names = gc.GarchParameters.get_preset_names()
    for i, name in enumerate(preset_names, 1):
        print(f"   {i}. {name}")
    
    # 2. 测试每个预设参数
    print(f"\n⚙️  预设参数详情:")
    presets = {}
    
    # Brett优化参数
    brett_params = gc.GarchParameters.create_brett_optimized()
    presets['brett_optimized'] = brett_params
    print(f"\n🎯 Brett优化参数:")
    print(f"   mu: {brett_params.mu:.6f}")
    print(f"   omega: {brett_params.omega:.6f}")
    print(f"   alpha: {brett_params.alpha:.6f}")
    print(f"   beta: {brett_params.beta:.6f}")
    print(f"   nu: {brett_params.nu:.6f}")
    print(f"   持续性: {brett_params.get_persistence():.6f}")
    print(f"   无条件方差: {brett_params.get_unconditional_variance():.6f}")
    print(f"   参数有效性: {brett_params.is_valid()}")
    
    # 高波动率参数
    high_vol_params = gc.GarchParameters.create_high_volatility()
    presets['high_volatility'] = high_vol_params
    print(f"\n📈 高波动率参数:")
    print(f"   mu: {high_vol_params.mu:.6f}")
    print(f"   omega: {high_vol_params.omega:.6f}")
    print(f"   alpha: {high_vol_params.alpha:.6f}")
    print(f"   beta: {high_vol_params.beta:.6f}")
    print(f"   nu: {high_vol_params.nu:.6f}")
    print(f"   持续性: {high_vol_params.get_persistence():.6f}")
    
    # 稳定期参数
    stable_params = gc.GarchParameters.create_stable_period()
    presets['stable_period'] = stable_params
    print(f"\n📉 稳定期参数:")
    print(f"   mu: {stable_params.mu:.6f}")
    print(f"   omega: {stable_params.omega:.6f}")
    print(f"   alpha: {stable_params.alpha:.6f}")
    print(f"   beta: {stable_params.beta:.6f}")
    print(f"   nu: {stable_params.nu:.6f}")
    print(f"   持续性: {stable_params.get_persistence():.6f}")
    
    # Arch-like参数
    arch_params = gc.GarchParameters.create_arch_like()
    presets['arch_like'] = arch_params
    print(f"\n🔧 Arch-like参数:")
    print(f"   mu: {arch_params.mu:.6f}")
    print(f"   omega: {arch_params.omega:.6f}")
    print(f"   alpha: {arch_params.alpha:.6f}")
    print(f"   beta: {arch_params.beta:.6f}")
    print(f"   nu: {arch_params.nu:.6f}")
    print(f"   持续性: {arch_params.get_persistence():.6f}")
    
    # 3. 测试自适应参数
    print(f"\n🧠 自适应参数测试:")
    data_variance = 150.0
    data_mean = 2.0
    adaptive_params = gc.GarchParameters.create_adaptive(data_variance, data_mean)
    print(f"   输入: 方差={data_variance}, 均值={data_mean}")
    print(f"   mu: {adaptive_params.mu:.6f}")
    print(f"   omega: {adaptive_params.omega:.6f}")
    print(f"   alpha: {adaptive_params.alpha:.6f}")
    print(f"   beta: {adaptive_params.beta:.6f}")
    print(f"   nu: {adaptive_params.nu:.6f}")
    
    # 4. 测试字符串预设创建
    print(f"\n📝 字符串预设创建测试:")
    for name in preset_names:
        preset_by_name = gc.GarchParameters.create_preset(name)
        original = presets[name]
        match = (abs(preset_by_name.omega - original.omega) < 1e-10 and
                abs(preset_by_name.alpha - original.alpha) < 1e-10)
        print(f"   {name}: {'✅' if match else '❌'}")
    
    return presets

def test_with_real_data():
    """使用真实数据测试预设参数"""
    print(f"\n📊 真实数据测试")
    print("=" * 60)
    
    # 读取Brett数据
    try:
        df = pd.read_csv('brett.csv')
        returns = df['c_scaled'].values[:200]
        print(f"✅ 成功读取 {len(returns)} 个Brett数据点")
    except:
        # 如果没有Brett数据，创建模拟数据
        np.random.seed(42)
        returns = np.random.normal(2.0, 15.0, 200)
        print(f"📝 使用模拟数据 {len(returns)} 个数据点")
    
    print(f"   数据均值: {returns.mean():.6f}")
    print(f"   数据标准差: {returns.std():.6f}")
    
    # 测试每个预设参数的预测
    preset_names = ['brett_optimized', 'high_volatility', 'stable_period', 'arch_like']
    
    for preset_name in preset_names:
        print(f"\n🔮 使用 {preset_name} 预测:")
        
        # 创建计算器
        calc = gc.GarchCalculator(history_size=len(returns) + 10)
        calc.add_returns(returns.tolist())
        
        # 设置预设参数
        params = gc.GarchParameters.create_preset(preset_name)
        calc.set_parameters(params)
        
        # 计算似然值
        likelihood = calc.calculate_log_likelihood()
        
        # 预测波动率
        forecast = calc.forecast_volatility(1)
        
        print(f"   似然值: {likelihood:.4f}")
        print(f"   预测波动率: {forecast.volatility:.6f}")
        print(f"   置信度: {forecast.confidence_score:.6f}")

def performance_comparison():
    """性能对比测试"""
    print(f"\n⚡ 性能对比测试")
    print("=" * 60)
    
    try:
        df = pd.read_csv('brett.csv')
        returns = df['c_scaled'].values[:100]
    except:
        np.random.seed(42)
        returns = np.random.normal(0, 10, 100)
    
    import time
    
    # 测试预设参数的速度
    start_time = time.time()
    for _ in range(10):
        calc = gc.GarchCalculator()
        calc.add_returns(returns.tolist())
        params = gc.GarchParameters.create_brett_optimized()
        calc.set_parameters(params)
        forecast = calc.forecast_volatility(1)
    preset_time = time.time() - start_time
    
    # 测试参数估计的速度
    start_time = time.time()
    for _ in range(10):
        calc = gc.GarchCalculator()
        calc.add_returns(returns.tolist())
        result = calc.estimate_parameters()
        if result.converged:
            forecast = calc.forecast_volatility(1)
    estimation_time = time.time() - start_time
    
    print(f"📊 性能结果 (10次运行):")
    print(f"   预设参数方法: {preset_time:.4f}秒")
    print(f"   参数估计方法: {estimation_time:.4f}秒")
    print(f"   速度提升: {estimation_time/preset_time:.2f}x")

def main():
    """主测试函数"""
    print("🎉 GARCH Calculator v1.2.0 预设参数测试")
    print("🎯 新功能: 预设参数系统")
    print("")
    
    # 测试预设参数
    presets = test_preset_parameters()
    
    # 真实数据测试
    test_with_real_data()
    
    # 性能对比
    performance_comparison()
    
    print(f"\n✅ 所有测试完成!")
    print(f"\n💡 使用建议:")
    print(f"   • 默认使用 'brett_optimized' 参数")
    print(f"   • 高波动期使用 'high_volatility' 参数")
    print(f"   • 稳定期使用 'stable_period' 参数")
    print(f"   • 需要与arch库一致时使用 'arch_like' 参数")
    
    print(f"\n📝 使用示例:")
    print(f"   params = gc.GarchParameters.create_brett_optimized()")
    print(f"   calc = gc.GarchCalculator()")
    print(f"   calc.add_returns(your_data)")
    print(f"   calc.set_parameters(params)")
    print(f"   forecast = calc.forecast_volatility(1)")

if __name__ == "__main__":
    main() 