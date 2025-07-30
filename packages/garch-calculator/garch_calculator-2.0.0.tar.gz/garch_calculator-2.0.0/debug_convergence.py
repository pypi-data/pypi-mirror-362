#!/usr/bin/env python3
"""
GARCH收敛问题诊断脚本
"""

import numpy as np
import yfinance as yf
import garch_lib as gc

def test_convergence():
    print("🔍 GARCH收敛问题诊断")
    print("=" * 50)
    
    # 下载测试数据
    stock = yf.Ticker('AAPL')
    data = stock.history(period='1y')
    prices = data['Close'].values
    returns = np.log(prices[1:] / prices[:-1])
    returns = returns - returns.mean()
    
    print(f"数据统计:")
    print(f"  样本数: {len(returns)}")
    print(f"  均值: {returns.mean():.8f}")
    print(f"  标准差: {returns.std():.6f}")
    print(f"  最小值: {returns.min():.6f}")
    print(f"  最大值: {returns.max():.6f}")
    
    # 测试基本估计
    print(f"\n🔧 测试参数估计...")
    calc = gc.GarchCalculator()
    calc.add_returns(returns.tolist())
    
    result = calc.estimate_parameters()
    
    print(f"收敛状态: {result.converged}")
    print(f"迭代次数: {result.iterations}")
    print(f"对数似然: {result.log_likelihood:.6f}")
    print(f"参数:")
    print(f"  ω: {result.parameters.omega:.8f}")
    print(f"  α: {result.parameters.alpha:.6f}")
    print(f"  β: {result.parameters.beta:.6f}")
    print(f"  ν: {result.parameters.nu:.6f}")
    
    # 测试更新模型
    print(f"\n🔄 测试模型更新...")
    update_success = calc.update_model()
    print(f"更新成功: {update_success}")
    
    current_vol = calc.get_current_volatility()
    print(f"当前波动率: {current_vol:.6f}")
    
    # 比较结果
    print(f"\n📊 与arch库期望结果对比:")
    print(f"arch典型参数范围:")
    print(f"  ω: 0.000001 - 0.00001")
    print(f"  α: 0.05 - 0.15")
    print(f"  β: 0.8 - 0.95")
    print(f"  ν: 1.2 - 2.5")
    
    return result

if __name__ == "__main__":
    test_convergence() 