#!/usr/bin/env python3
"""
测试updateModel方法
"""

import numpy as np
import garch_lib as gc

def test_update_model():
    print("🔍 测试updateModel方法...")
    
    # 创建测试数据
    np.random.seed(42)
    returns = np.random.normal(0, 0.02, 100)
    
    calc = gc.GarchCalculator()
    calc.add_returns(returns.tolist())
    
    print(f"初始状态:")
    print(f"  波动率: {calc.get_current_volatility():.6f}")
    print(f"  方差: {calc.get_current_variance():.6f}")
    
    # 设置新参数
    new_params = gc.GarchParameters(0.00001, 0.05, 0.85, 1.8)
    calc.set_parameters(new_params)
    
    print(f"\n设置新参数后:")
    print(f"  波动率: {calc.get_current_volatility():.6f}")
    print(f"  方差: {calc.get_current_variance():.6f}")
    
    # 检查是否有update_model方法
    print(f"\n检查可用方法:")
    methods = [m for m in dir(calc) if not m.startswith('_')]
    print(f"可用方法: {methods}")
    
    # 尝试调用update_model
    if hasattr(calc, 'update_model'):
        print(f"\n调用update_model()...")
        result = calc.update_model()
        print(f"update_model结果: {result}")
        print(f"更新后波动率: {calc.get_current_volatility():.6f}")
        print(f"更新后方差: {calc.get_current_variance():.6f}")
    else:
        print(f"\n❌ 没有找到update_model方法")
    
    # 重新估计参数看看是否会更新current_variance
    print(f"\n尝试重新估计参数...")
    result = calc.estimate_parameters()
    print(f"估计结果:")
    print(f"  收敛: {result.converged}")
    print(f"  似然值: {result.log_likelihood:.6f}")
    print(f"  估计后波动率: {calc.get_current_volatility():.6f}")
    print(f"  估计后方差: {calc.get_current_variance():.6f}")

if __name__ == "__main__":
    test_update_model() 