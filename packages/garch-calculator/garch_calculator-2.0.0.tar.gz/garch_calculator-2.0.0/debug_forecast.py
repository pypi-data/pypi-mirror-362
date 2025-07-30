import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values
window_data = returns[200:300]  # 100个数据点

print("🔍 调试预测函数问题")
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

# 使用去均值数据
residuals = window_data - mu

# 创建garch_lib计算器
calc = gc.GarchCalculator(history_size=len(residuals) + 10)
calc.add_returns(residuals.tolist())

# 设置arch库的参数
arch_params = gc.GarchParameters()
arch_params.omega = omega
arch_params.alpha = alpha
arch_params.beta = beta
arch_params.nu = nu
calc.set_parameters(arch_params)

print(f"\n📊 garch_lib内部状态:")
print(f"  当前方差: {calc.get_current_variance():.6f}")
print(f"  当前波动率: {calc.get_current_volatility():.6f}")
print(f"  数据点数: {calc.get_data_size()}")

# 获取参数
params = calc.get_parameters()
print(f"  参数: ω={params.omega:.6f}, α={params.alpha:.6f}")
print(f"        β={params.beta:.6f}, ν={params.nu:.6f}")

# 计算无条件方差
unconditional_var = omega / (1 - alpha - beta)
print(f"  无条件方差: {unconditional_var:.6f}")
print(f"  无条件波动率: {np.sqrt(unconditional_var):.6f}")

# 计算持续性
persistence = alpha + beta
print(f"  持续性 (α+β): {persistence:.6f}")

# 手动计算最后一个条件方差（arch库方式）
arch_variances = arch_result.conditional_volatility**2
last_arch_var = arch_variances[-1]
print(f"  arch库最后条件方差: {last_arch_var:.6f}")
print(f"  arch库最后条件波动率: {np.sqrt(last_arch_var):.6f}")

# 手动计算GARCH预测
# σ²_{T+1} = ω + α * ε²_T + β * σ²_T
last_residual = residuals[-1]
manual_forecast_var = omega + alpha * (last_residual**2) + beta * last_arch_var
manual_forecast_vol = np.sqrt(manual_forecast_var)

print(f"\n📈 手动预测计算:")
print(f"  最后残差: {last_residual:.6f}")
print(f"  最后残差平方: {last_residual**2:.6f}")
print(f"  手动预测方差: {manual_forecast_var:.6f}")
print(f"  手动预测波动率: {manual_forecast_vol:.6f}")

# garch_lib预测
garch_forecast = calc.forecast_volatility(1)
print(f"\n🔧 garch_lib预测:")
print(f"  预测方差: {garch_forecast.variance:.6f}")
print(f"  预测波动率: {garch_forecast.volatility:.6f}")

# arch库预测
arch_forecast = arch_result.forecast(horizon=1, reindex=False)
arch_vol = np.sqrt(arch_forecast.variance.values[-1, 0])
print(f"\n📚 arch库预测:")
print(f"  预测波动率: {arch_vol:.6f}")

print(f"\n🔍 差异分析:")
print(f"  garch_lib vs 手动计算: {garch_forecast.volatility - manual_forecast_vol:.6f}")
print(f"  garch_lib vs arch库: {garch_forecast.volatility - arch_vol:.6f}")
print(f"  手动计算 vs arch库: {manual_forecast_vol - arch_vol:.6f}")

# 检查current_variance_是否正确更新
print(f"\n🔧 current_variance_问题诊断:")
print(f"  garch_lib当前方差: {calc.get_current_variance():.6f}")
print(f"  应该是的方差: {last_arch_var:.6f}")
print(f"  差异: {calc.get_current_variance() - last_arch_var:.6f}")

# 检查是否是无条件方差问题
if abs(calc.get_current_variance() - unconditional_var) < 1e-6:
    print("  ❌ 问题：current_variance_被设置为无条件方差，而不是最后的条件方差！")
else:
    print("  ✅ current_variance_不是无条件方差")

# 测试：如果我们手动设置current_variance会怎样？
print(f"\n🧪 测试：如果current_variance正确会怎样？")
# 由于没有直接设置current_variance的方法，我们用预测公式手动计算
correct_forecast_var = omega + alpha * (last_residual**2) + beta * last_arch_var
correct_forecast_vol = np.sqrt(correct_forecast_var)
print(f"  正确的预测波动率应该是: {correct_forecast_vol:.6f}")
print(f"  与arch库的差异: {correct_forecast_vol - arch_vol:.6f}") 