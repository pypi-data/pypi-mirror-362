#!/usr/bin/env python3
"""
GARCH模型调试脚本
验证为什么波动率总是固定在0.014142
"""

import numpy as np
import yfinance as yf
import garch_lib as gc

def debug_garch_issue():
    print("🔍 调试GARCH模型问题...")
    
    # 测试1: 使用默认参数计算无条件方差
    print("\n=== 测试1: 默认参数 ===")
    calc = gc.GarchCalculator()
    params = calc.get_parameters()
    print(f"默认参数:")
    print(f"  omega: {params.omega}")
    print(f"  alpha: {params.alpha}")
    print(f"  beta: {params.beta}")
    print(f"  nu: {params.nu}")
    
    # 手动计算无条件方差
    persistence = params.alpha + params.beta
    unconditional_var = params.omega / (1.0 - persistence)
    print(f"  持续性 (α+β): {persistence}")
    print(f"  无条件方差: {unconditional_var}")
    print(f"  无条件波动率: {np.sqrt(unconditional_var)}")
    print(f"  当前波动率: {calc.get_current_volatility()}")
    
    # 测试2: 使用不同的股票数据
    print("\n=== 测试2: 不同股票数据 ===")
    
    stocks = ["AAPL", "MSFT", "GOOGL"]
    for symbol in stocks:
        print(f"\n--- 测试 {symbol} ---")
        
        # 下载数据
        stock = yf.Ticker(symbol)
        data = stock.history(period="1y")
        
        if data.empty:
            print(f"无法获取 {symbol} 数据")
            continue
            
        # 计算收益率
        prices = data['Close'].values
        returns = np.log(prices[1:] / prices[:-1])
        returns = returns - returns.mean()  # 中心化
        
        # 创建新的计算器
        calc = gc.GarchCalculator()
        calc.add_returns(returns.tolist())
        
        print(f"  数据点数: {len(returns)}")
        print(f"  收益率均值: {returns.mean():.6f}")
        print(f"  收益率标准差: {returns.std():.6f}")
        
        # 估计参数
        result = calc.estimate_parameters()
        print(f"  收敛状态: {'✅' if result.converged else '❌'}")
        
        if result.converged:
            print(f"  估计参数:")
            print(f"    omega: {result.parameters.omega:.6f}")
            print(f"    alpha: {result.parameters.alpha:.6f}")
            print(f"    beta: {result.parameters.beta:.6f}")
            print(f"    nu: {result.parameters.nu:.6f}")
        else:
            print(f"  未收敛 - 使用默认参数")
        
        print(f"  当前波动率: {calc.get_current_volatility():.6f}")
    
    # 测试3: 模拟不同的收益率数据
    print("\n=== 测试3: 模拟数据 ===")
    
    # 生成不同特征的模拟数据
    test_cases = [
        ("高波动率", np.random.normal(0, 0.03, 1000)),
        ("低波动率", np.random.normal(0, 0.01, 1000)),
        ("极高波动率", np.random.normal(0, 0.05, 1000)),
        ("零波动率", np.zeros(1000)),
    ]
    
    for name, returns in test_cases:
        print(f"\n--- {name} ---")
        calc = gc.GarchCalculator()
        calc.add_returns(returns.tolist())
        
        print(f"  数据标准差: {returns.std():.6f}")
        
        result = calc.estimate_parameters()
        print(f"  收敛状态: {'✅' if result.converged else '❌'}")
        print(f"  当前波动率: {calc.get_current_volatility():.6f}")
    
    # 测试4: 检查计算器的内部状态
    print("\n=== 测试4: 内部状态检查 ===")
    calc = gc.GarchCalculator()
    
    # 添加一些数据
    test_returns = np.random.normal(0, 0.02, 100)
    calc.add_returns(test_returns.tolist())
    
    print(f"配置信息:")
    print(calc.get_config_info())
    
    print(f"\n数据统计:")
    print(f"  数据点数: {calc.get_data_size()}")
    print(f"  有足够数据: {calc.has_enough_data()}")
    
    # 尝试手动设置参数
    print(f"\n--- 手动设置参数测试 ---")
    
    # 创建一个新的参数集
    new_params = gc.GarchParameters()
    new_params.omega = 0.001
    new_params.alpha = 0.05
    new_params.beta = 0.9
    new_params.nu = 2.0
    
    calc.set_parameters(new_params)
    print(f"设置新参数后的波动率: {calc.get_current_volatility():.6f}")
    
    # 计算新的无条件方差
    new_unconditional_var = new_params.omega / (1.0 - new_params.alpha - new_params.beta)
    print(f"新的无条件方差: {new_unconditional_var:.6f}")
    print(f"新的无条件波动率: {np.sqrt(new_unconditional_var):.6f}")

if __name__ == "__main__":
    debug_garch_issue() 