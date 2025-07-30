import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values
window_data = returns[200:300]  # 100个数据点

print("🔍 详细调试预测公式")
print("=" * 60)

# 使用arch库获取参考
arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

mu = arch_result.params['mu']
omega = arch_result.params['omega']
alpha = arch_result.params['alpha[1]']
beta = arch_result.params['beta[1]']
nu = arch_result.params['nu']

print(f"arch库参数: ω={omega:.6f}, α={alpha:.6f}, β={beta:.6f}, ν={nu:.6f}")

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

# 获取关键数值
current_var = calc.get_current_variance()
last_residual = residuals[-1]

print(f"\n📊 关键数值:")
print(f"  当前方差 (σ²_T): {current_var:.6f}")
print(f"  最后残差 (ε_T): {last_residual:.6f}")
print(f"  最后残差平方 (ε²_T): {last_residual**2:.6f}")

# 计算持续性和无条件方差
persistence = alpha + beta
unconditional_var = omega / (1 - persistence)

print(f"\n📈 GARCH参数:")
print(f"  持续性 (α+β): {persistence:.6f}")
print(f"  无条件方差: {unconditional_var:.6f}")

# 手动计算一步预测（标准GARCH公式）
# σ²_{T+1} = ω + α * ε²_T + β * σ²_T
manual_forecast_var = omega + alpha * (last_residual**2) + beta * current_var
manual_forecast_vol = np.sqrt(manual_forecast_var)

print(f"\n🧮 手动计算 (标准GARCH公式):")
print(f"  σ²_{{T+1}} = ω + α*ε²_T + β*σ²_T")
print(f"  σ²_{{T+1}} = {omega:.6f} + {alpha:.6f}*{last_residual**2:.6f} + {beta:.6f}*{current_var:.6f}")
print(f"  σ²_{{T+1}} = {omega:.6f} + {alpha * last_residual**2:.6f} + {beta * current_var:.6f}")
print(f"  σ²_{{T+1}} = {manual_forecast_var:.6f}")
print(f"  σ_{{T+1}} = {manual_forecast_vol:.6f}")

# garch_lib的多步预测公式（从C++代码中）
# 对于horizon=1的情况：
# forecast_var = unconditional_var + persistence^1 * (current_variance - unconditional_var)
garch_lib_formula_var = unconditional_var + persistence * (current_var - unconditional_var)
garch_lib_formula_vol = np.sqrt(garch_lib_formula_var)

print(f"\n🔧 garch_lib多步预测公式 (horizon=1):")
print(f"  σ²_{{T+1}} = σ²_∞ + ρ^h * (σ²_T - σ²_∞)")
print(f"  σ²_{{T+1}} = {unconditional_var:.6f} + {persistence:.6f}^1 * ({current_var:.6f} - {unconditional_var:.6f})")
print(f"  σ²_{{T+1}} = {unconditional_var:.6f} + {persistence:.6f} * {current_var - unconditional_var:.6f}")
print(f"  σ²_{{T+1}} = {unconditional_var:.6f} + {persistence * (current_var - unconditional_var):.6f}")
print(f"  σ²_{{T+1}} = {garch_lib_formula_var:.6f}")
print(f"  σ_{{T+1}} = {garch_lib_formula_vol:.6f}")

# 实际的garch_lib预测
garch_forecast = calc.forecast_volatility(1)

print(f"\n🔧 实际garch_lib预测:")
print(f"  预测方差: {garch_forecast.variance:.6f}")
print(f"  预测波动率: {garch_forecast.volatility:.6f}")

# arch库预测
arch_forecast = arch_result.forecast(horizon=1, reindex=False)
arch_vol = np.sqrt(arch_forecast.variance.values[-1, 0])

print(f"\n📚 arch库预测:")
print(f"  预测波动率: {arch_vol:.6f}")

print(f"\n🔍 差异分析:")
print(f"  标准GARCH vs arch库: {manual_forecast_vol - arch_vol:.6f}")
print(f"  多步公式 vs arch库: {garch_lib_formula_vol - arch_vol:.6f}")
print(f"  garch_lib vs arch库: {garch_forecast.volatility - arch_vol:.6f}")
print(f"  garch_lib vs 多步公式: {garch_forecast.volatility - garch_lib_formula_vol:.6f}")

print(f"\n💡 结论:")
if abs(manual_forecast_vol - arch_vol) < 1e-6:
    print("  ✅ 标准GARCH公式与arch库完全一致")
else:
    print("  ❌ 标准GARCH公式与arch库不一致")

if abs(garch_lib_formula_var - garch_forecast.variance) < 1e-6:
    print("  ✅ garch_lib使用的是多步预测公式")
else:
    print("  ❌ garch_lib没有使用多步预测公式")

print(f"\n🚨 问题:")
print(f"  多步预测公式对于horizon=1应该等价于标准GARCH公式")
print(f"  但实际差异为: {garch_lib_formula_vol - manual_forecast_vol:.6f}")

# 验证多步公式是否正确
# 对于GARCH(1,1)，一步预测应该是：σ²_{T+1} = ω + α*ε²_T + β*σ²_T
# 多步公式：σ²_{T+h} = σ²_∞ + ρ^h * (σ²_T - σ²_∞)
# 当h=1时，应该等价

# 展开多步公式：
# σ²_{T+1} = σ²_∞ + ρ * (σ²_T - σ²_∞)
#          = σ²_∞ + ρ*σ²_T - ρ*σ²_∞
#          = σ²_∞*(1-ρ) + ρ*σ²_T
#          = ω/(1-ρ)*(1-ρ) + ρ*σ²_T
#          = ω + ρ*σ²_T

# 但标准公式是：σ²_{T+1} = ω + α*ε²_T + β*σ²_T
# 差异在于：多步公式缺少了 α*ε²_T 项！

print(f"\n🔬 公式分析:")
print(f"  多步公式展开: σ²_{{T+1}} = ω + ρ*σ²_T = ω + {persistence:.6f}*{current_var:.6f} = {omega + persistence * current_var:.6f}")
print(f"  标准公式: σ²_{{T+1}} = ω + α*ε²_T + β*σ²_T = {omega:.6f} + {alpha * last_residual**2:.6f} + {beta * current_var:.6f} = {manual_forecast_var:.6f}")
print(f"  差异来源: α*ε²_T = {alpha * last_residual**2:.6f}")
print(f"  ❌ 多步预测公式对于h=1不正确！应该使用标准GARCH递推公式") 