import garch_lib as gc
import pandas as pd
import numpy as np

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]  # 使用前300个数据点测试

# 测试garch_lib自身的参数估计
calc = gc.GarchCalculator(history_size=350)
calc.add_returns(returns.tolist())

print('测试garch_lib自身的参数估计...')
result = calc.estimate_parameters()

print(f'收敛状态: {result.converged}')
print(f'参数: omega={result.parameters.omega:.6f}, alpha={result.parameters.alpha:.6f}, beta={result.parameters.beta:.6f}, nu={result.parameters.nu:.6f}')
print(f'对数似然: {result.log_likelihood:.4f}')

if result.converged:
    forecast = calc.forecast_volatility(1)
    print(f'预测波动率: {forecast.volatility:.6f}')
else:
    print('参数估计未收敛') 