import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values
window_data = returns[200:400]  # 200个数据点

print("🔍 调试 garch_lib 预测值总是10的问题")
print("=" * 60)

# 使用arch库获取参考
arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

print(f"arch库参数:")
mu = arch_result.params['mu']
omega = arch_result.params['omega']
alpha = arch_result.params['alpha[1]']
beta = arch_result.params['beta[1]']
nu = arch_result.params['nu']

print(f"  mu: {mu:.6f}")
print(f"  omega: {omega:.6f}")
print(f"  alpha: {alpha:.6f}")
print(f"  beta: {beta:.6f}")
print(f"  nu: {nu:.6f}")

# 使用garch_lib
calc = gc.GarchCalculator(history_size=len(window_data) + 10)

# 测试1: 使用原始数据
print(f"\n📊 测试1: 使用原始数据")
calc.add_returns(window_data.tolist())
result1 = calc.estimate_parameters()
print(f"  收敛: {result1.converged}")
print(f"  参数: omega={result1.parameters.omega:.6f}, alpha={result1.parameters.alpha:.6f}")
print(f"        beta={result1.parameters.beta:.6f}, nu={result1.parameters.nu:.6f}")

forecast1 = calc.forecast_volatility(1)
print(f"  预测波动率: {forecast1.volatility:.6f}")

# 测试2: 使用去均值数据
print(f"\n📊 测试2: 使用去均值数据")
residuals = window_data - mu
calc2 = gc.GarchCalculator(history_size=len(residuals) + 10)
calc2.add_returns(residuals.tolist())
result2 = calc2.estimate_parameters()
print(f"  收敛: {result2.converged}")
print(f"  参数: omega={result2.parameters.omega:.6f}, alpha={result2.parameters.alpha:.6f}")
print(f"        beta={result2.parameters.beta:.6f}, nu={result2.parameters.nu:.6f}")

forecast2 = calc2.forecast_volatility(1)
print(f"  预测波动率: {forecast2.volatility:.6f}")

# 测试3: 手动设置arch库的参数
print(f"\n📊 测试3: 手动设置arch库参数")
calc3 = gc.GarchCalculator(history_size=len(residuals) + 10)
calc3.add_returns(residuals.tolist())
# 创建GarchParameters对象
arch_params = gc.GarchParameters()
arch_params.omega = omega
arch_params.alpha = alpha
arch_params.beta = beta
arch_params.nu = nu
calc3.set_parameters(arch_params)

forecast3 = calc3.forecast_volatility(1)
print(f"  预测波动率: {forecast3.volatility:.6f}")

# 测试4: 检查内部状态
print(f"\n📊 测试4: 检查内部状态")
print(f"  数据点数: {len(residuals)}")
print(f"  最后几个数据点: {residuals[-5:].tolist()}")

# 获取arch库的预测作为对比
arch_forecast = arch_result.forecast(horizon=1, reindex=False)
arch_vol = np.sqrt(arch_forecast.variance.values[-1, 0])
print(f"  arch库预测: {arch_vol:.6f}")

# 测试5: 检查条件方差
print(f"\n📊 测试5: 检查条件方差计算")
# 手动计算最后一个条件方差
last_return = residuals[-1]
second_last_return = residuals[-2] if len(residuals) > 1 else 0

# 简单的GARCH(1,1)条件方差计算
# sigma^2_t = omega + alpha * epsilon^2_{t-1} + beta * sigma^2_{t-1}
# 假设初始方差为样本方差
initial_var = np.var(residuals)
manual_var = omega + alpha * (second_last_return**2) + beta * initial_var
manual_vol = np.sqrt(manual_var)

print(f"  最后一个残差: {last_return:.6f}")
print(f"  倒数第二个残差: {second_last_return:.6f}")
print(f"  初始方差: {initial_var:.6f}")
print(f"  手动计算条件方差: {manual_var:.6f}")
print(f"  手动计算波动率: {manual_vol:.6f}")

# 测试6: 检查是否是默认值问题
print(f"\n📊 测试6: 检查默认值")
calc4 = gc.GarchCalculator(history_size=10)
calc4.add_returns([0.01, -0.02, 0.015, -0.01, 0.005])  # 简单测试数据
forecast4 = calc4.forecast_volatility(1)
print(f"  简单数据预测: {forecast4.volatility:.6f}")

# 不估计参数，直接预测
calc5 = gc.GarchCalculator(history_size=len(residuals) + 10)
calc5.add_returns(residuals.tolist())
forecast5 = calc5.forecast_volatility(1)  # 不调用estimate_parameters
print(f"  不估计参数直接预测: {forecast5.volatility:.6f}") 