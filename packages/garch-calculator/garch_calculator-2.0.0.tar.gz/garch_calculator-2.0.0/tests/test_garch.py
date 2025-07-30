#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GARCH Calculator Python 测试脚本

展示如何使用GARCH计算器进行增量波动率建模
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import os

# 添加路径以便导入模块 (如果模块尚未安装)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import garch_calculator as gc
    print("✓ GARCH Calculator 模块导入成功")
except ImportError as e:
    print(f"✗ GARCH Calculator 模块导入失败: {e}")
    print("请先编译安装模块: python setup.py build_ext --inplace")
    sys.exit(1)

def generate_sample_data(n_points=1000, initial_price=100.0, volatility=0.02):
    """
    生成模拟的金融时间序列数据
    
    Args:
        n_points: 数据点数量
        initial_price: 初始价格
        volatility: 基础波动率
    
    Returns:
        prices: 价格序列
        timestamps: 时间戳序列
    """
    print(f"📊 生成 {n_points} 个样本数据点...")
    
    np.random.seed(42)  # 确保可重复性
    
    # 生成时间戳 (微秒级)
    current_time = int(time.time() * 1000000)
    timestamps = np.arange(current_time, current_time + n_points * 1000000, 1000000)
    
    # 生成价格序列 (使用GARCH过程模拟)
    prices = np.zeros(n_points)
    prices[0] = initial_price
    
    # 模拟GARCH过程
    omega = 0.00001
    alpha = 0.1
    beta = 0.85
    variance = omega / (1 - alpha - beta)
    
    for i in range(1, n_points):
        # 更新方差
        if i > 1:
            log_return = np.log(prices[i-1] / prices[i-2])
            variance = omega + alpha * log_return**2 + beta * variance
        
        # 生成收益率
        volatility_t = np.sqrt(variance)
        log_return = np.random.normal(0, volatility_t)
        
        # 更新价格
        prices[i] = prices[i-1] * np.exp(log_return)
    
    return prices, timestamps

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    # 创建计算器
    calc = gc.GarchCalculator(history_size=500, min_samples=50)
    print(f"✓ 创建计算器: {calc}")
    
    # 生成数据
    prices, timestamps = generate_sample_data(200)
    
    # 逐个添加数据点
    print("📈 逐个添加价格数据点...")
    for i, (price, ts) in enumerate(zip(prices, timestamps)):
        success = calc.add_price_point(price, ts)
        if not success:
            print(f"✗ 添加第 {i} 个数据点失败")
            return False
        
        if i % 50 == 0:
            print(f"  已添加 {i+1} 个数据点")
    
    print(f"✓ 成功添加 {calc.get_data_size()} 个数据点")
    
    # 检查是否有足够数据
    if calc.has_enough_data():
        print("✓ 有足够数据进行参数估计")
    else:
        print("✗ 数据不足，无法进行参数估计")
        return False
    
    return True

def test_parameter_estimation():
    """测试参数估计"""
    print("\n🔬 测试参数估计...")
    
    calc = gc.GarchCalculator(history_size=1000, min_samples=50)
    
    # 批量添加数据
    prices, timestamps = generate_sample_data(300)
    success = calc.add_price_points(prices.tolist(), timestamps.tolist())
    
    if not success:
        print("✗ 批量添加数据失败")
        return False
    
    print("✓ 批量添加数据成功")
    
    # 估计参数
    print("🎯 开始参数估计...")
    start_time = time.time()
    result = calc.estimate_parameters()
    end_time = time.time()
    
    if result.converged:
        print(f"✓ 参数估计收敛 (耗时: {(end_time - start_time)*1000:.2f}ms)")
        print(f"  参数: {result.parameters}")
        print(f"  对数似然: {result.log_likelihood:.4f}")
        print(f"  AIC: {result.aic:.4f}")
        print(f"  BIC: {result.bic:.4f}")
        print(f"  迭代次数: {result.iterations}")
    else:
        print("✗ 参数估计未收敛")
        return False
    
    # 计算当前状态
    current_var = calc.get_current_variance()
    current_vol = calc.get_current_volatility()
    confidence = calc.calculate_confidence_score()
    
    print(f"📊 当前状态:")
    print(f"  当前方差: {current_var:.8f}")
    print(f"  当前波动率: {current_vol:.8f}")
    print(f"  置信度: {confidence:.4f}")
    
    return True

def test_incremental_updates():
    """测试增量更新"""
    print("\n⏱️ 测试增量更新性能...")
    
    calc = gc.GarchCalculator(history_size=1000, min_samples=50)
    
    # 初始数据
    initial_prices, initial_timestamps = generate_sample_data(200)
    calc.add_price_points(initial_prices.tolist(), initial_timestamps.tolist())
    
    # 估计初始参数
    result = calc.estimate_parameters()
    if not result.converged:
        print("✗ 初始参数估计失败")
        return False
    
    print("✓ 初始参数估计完成")
    
    # 测试增量更新性能
    new_prices, new_timestamps = generate_sample_data(100)
    
    update_times = []
    volatilities = []
    
    print("🔄 开始增量更新测试...")
    for i, (price, ts) in enumerate(zip(new_prices, new_timestamps)):
        start_time = time.time()
        
        # 添加新数据点
        calc.add_price_point(price, ts)
        
        # 更新模型
        calc.update_model()
        
        # 预测波动率
        forecast = calc.forecast_volatility(horizon=1)
        
        end_time = time.time()
        
        update_times.append((end_time - start_time) * 1000)  # 转换为毫秒
        volatilities.append(forecast.volatility)
        
        if i % 20 == 0:
            print(f"  更新 {i+1}/100, 耗时: {update_times[-1]:.3f}ms, 波动率: {forecast.volatility:.6f}")
    
    avg_time = np.mean(update_times)
    print(f"✓ 增量更新完成")
    print(f"  平均更新时间: {avg_time:.3f}ms")
    print(f"  最大更新时间: {max(update_times):.3f}ms")
    print(f"  最小更新时间: {min(update_times):.3f}ms")
    
    return True, volatilities

def test_forecasting():
    """测试波动率预测"""
    print("\n🔮 测试波动率预测...")
    
    calc = gc.GarchCalculator(history_size=1000, min_samples=50)
    
    # 添加数据并估计参数
    prices, timestamps = generate_sample_data(400)
    calc.add_price_points(prices.tolist(), timestamps.tolist())
    result = calc.estimate_parameters()
    
    if not result.converged:
        print("✗ 参数估计失败")
        return False
    
    # 多步预测
    horizons = [1, 5, 10, 20, 50]
    forecasts = []
    
    print("📈 多步波动率预测:")
    for h in horizons:
        forecast = calc.forecast_volatility(horizon=h)
        forecasts.append(forecast)
        print(f"  {h}步预测: 波动率={forecast.volatility:.6f}, 方差={forecast.variance:.8f}, 置信度={forecast.confidence_score:.4f}")
    
    return True, forecasts

def test_numpy_integration():
    """测试NumPy集成"""
    print("\n🔢 测试NumPy集成...")
    
    calc = gc.GarchCalculator(history_size=1000, min_samples=50)
    
    # 使用NumPy数组
    prices, _ = generate_sample_data(300)
    
    # 使用NumPy方法添加数据
    success = calc.add_prices_numpy(prices)
    if not success:
        print("✗ NumPy数组添加失败")
        return False
    
    print("✓ NumPy数组添加成功")
    
    # 获取NumPy格式的结果
    log_returns = calc.get_log_returns_numpy()
    variance_series = calc.get_variance_series_numpy()
    
    print(f"✓ 获取对数收益率序列: shape={log_returns.shape}, dtype={log_returns.dtype}")
    print(f"✓ 获取方差序列: shape={variance_series.shape}, dtype={variance_series.dtype}")
    
    # 计算统计量
    stats = gc.calculate_basic_stats(log_returns.tolist())
    print(f"📊 收益率统计:")
    print(f"  均值: {stats.mean:.8f}")
    print(f"  标准差: {stats.std_dev:.8f}")
    print(f"  偏度: {stats.skewness:.4f}")
    print(f"  峰度: {stats.kurtosis:.4f}")
    
    return True

def test_risk_metrics():
    """测试风险指标计算"""
    print("\n⚠️ 测试风险指标计算...")
    
    calc = gc.GarchCalculator()
    prices, _ = generate_sample_data(300)
    calc.add_prices_numpy(prices)
    calc.estimate_parameters()
    
    current_vol = calc.get_current_volatility()
    
    # 计算VaR和ES
    var_95 = gc.calculate_var(current_vol, 0.05)
    var_99 = gc.calculate_var(current_vol, 0.01)
    es_95 = gc.calculate_expected_shortfall(current_vol, 0.05)
    es_99 = gc.calculate_expected_shortfall(current_vol, 0.01)
    
    print(f"📊 风险指标 (当前波动率: {current_vol:.6f}):")
    print(f"  VaR (95%): {var_95:.6f}")
    print(f"  VaR (99%): {var_99:.6f}")
    print(f"  ES (95%): {es_95:.6f}")
    print(f"  ES (99%): {es_99:.6f}")
    
    return True

def test_thread_safety():
    """测试线程安全"""
    print("\n🔒 测试线程安全...")
    
    calc = gc.GarchCalculator()
    calc.set_thread_safe(True)
    
    prices, _ = generate_sample_data(100)
    success = calc.add_prices_numpy(prices)
    
    if success:
        print("✓ 线程安全模式下数据添加成功")
        return True
    else:
        print("✗ 线程安全模式下数据添加失败")
        return False

def create_visualization(volatilities=None, forecasts=None):
    """创建可视化图表"""
    try:
        print("\n📈 创建可视化图表...")
        
        if volatilities is not None:
            plt.figure(figsize=(12, 8))
            
            # 子图1: 波动率时间序列
            plt.subplot(2, 2, 1)
            plt.plot(volatilities)
            plt.title('增量更新波动率序列')
            plt.xlabel('时间步')
            plt.ylabel('波动率')
            plt.grid(True)
            
            # 子图2: 波动率分布
            plt.subplot(2, 2, 2)
            plt.hist(volatilities, bins=30, alpha=0.7, edgecolor='black')
            plt.title('波动率分布')
            plt.xlabel('波动率')
            plt.ylabel('频次')
            plt.grid(True)
        
        if forecasts is not None:
            # 子图3: 多步预测
            plt.subplot(2, 2, 3)
            horizons = [1, 5, 10, 20, 50]
            forecast_vols = [f.volatility for f in forecasts]
            plt.plot(horizons, forecast_vols, 'ro-')
            plt.title('多步波动率预测')
            plt.xlabel('预测步数')
            plt.ylabel('预测波动率')
            plt.grid(True)
        
        # 子图4: 置信度
        if forecasts is not None:
            plt.subplot(2, 2, 4)
            confidence_scores = [f.confidence_score for f in forecasts]
            plt.plot(horizons, confidence_scores, 'go-')
            plt.title('预测置信度')
            plt.xlabel('预测步数')
            plt.ylabel('置信度')
            plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('garch_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print("✓ 图表已保存为 garch_results.png")
        
    except ImportError:
        print("📊 Matplotlib 未安装，跳过可视化")
    except Exception as e:
        print(f"✗ 可视化创建失败: {e}")

def main():
    """主测试函数"""
    print("🚀 GARCH Calculator 测试开始")
    print("=" * 50)
    
    test_results = []
    
    # 基本功能测试
    try:
        result = test_basic_functionality()
        test_results.append(("基本功能", result))
    except Exception as e:
        print(f"✗ 基本功能测试异常: {e}")
        test_results.append(("基本功能", False))
    
    # 参数估计测试
    try:
        result = test_parameter_estimation()
        test_results.append(("参数估计", result))
    except Exception as e:
        print(f"✗ 参数估计测试异常: {e}")
        test_results.append(("参数估计", False))
    
    # 增量更新测试
    try:
        result, volatilities = test_incremental_updates()
        test_results.append(("增量更新", result))
    except Exception as e:
        print(f"✗ 增量更新测试异常: {e}")
        test_results.append(("增量更新", False))
        volatilities = None
    
    # 预测测试
    try:
        result, forecasts = test_forecasting()
        test_results.append(("波动率预测", result))
    except Exception as e:
        print(f"✗ 波动率预测测试异常: {e}")
        test_results.append(("波动率预测", False))
        forecasts = None
    
    # NumPy集成测试
    try:
        result = test_numpy_integration()
        test_results.append(("NumPy集成", result))
    except Exception as e:
        print(f"✗ NumPy集成测试异常: {e}")
        test_results.append(("NumPy集成", False))
    
    # 风险指标测试
    try:
        result = test_risk_metrics()
        test_results.append(("风险指标", result))
    except Exception as e:
        print(f"✗ 风险指标测试异常: {e}")
        test_results.append(("风险指标", False))
    
    # 线程安全测试
    try:
        result = test_thread_safety()
        test_results.append(("线程安全", result))
    except Exception as e:
        print(f"✗ 线程安全测试异常: {e}")
        test_results.append(("线程安全", False))
    
    # 测试结果汇总
    print("\n" + "=" * 50)
    print("🏁 测试结果汇总:")
    
    passed = 0
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✓ 通过" if result else "✗ 失败"
        print(f"  {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试都通过了！")
    else:
        print("⚠️ 部分测试失败，请检查上述错误信息")
    
    # 创建可视化 (如果有数据)
    if 'volatilities' in locals() and 'forecasts' in locals():
        create_visualization(volatilities, forecasts)

if __name__ == "__main__":
    main() 