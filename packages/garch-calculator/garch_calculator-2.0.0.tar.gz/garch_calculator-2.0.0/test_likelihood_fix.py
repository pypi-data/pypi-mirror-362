import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]

print("🔧 测试似然函数修复")
print("=" * 60)

# 1. 使用arch库进行参数估计
arch_model_obj = arch_model(returns, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

print(f"arch库参数:")
print(f"  mu: {arch_result.params['mu']:.6f}")
print(f"  omega: {arch_result.params['omega']:.6f}")
print(f"  alpha: {arch_result.params['alpha[1]']:.6f}")
print(f"  beta: {arch_result.params['beta[1]']:.6f}")
print(f"  nu: {arch_result.params['nu']:.6f}")
print(f"  对数似然: {arch_result.loglikelihood:.4f}")

# 2. 手动设置arch库的参数到garch_lib并计算似然值
calc = gc.GarchCalculator(history_size=350)
calc.add_returns(returns.tolist())

# 创建参数对象
arch_params = gc.GarchParameters()
arch_params.mu = arch_result.params['mu']
arch_params.omega = arch_result.params['omega']
arch_params.alpha = arch_result.params['alpha[1]']
arch_params.beta = arch_result.params['beta[1]']
arch_params.nu = arch_result.params['nu']

# 设置参数并计算似然值
calc.set_parameters(arch_params)
garch_lib_ll = calc.calculate_log_likelihood()

print(f"\n🎯 似然函数对比:")
print(f"arch库似然值: {arch_result.loglikelihood:.6f}")
print(f"garch_lib似然值: {garch_lib_ll:.6f}")
print(f"差异: {abs(garch_lib_ll - arch_result.loglikelihood):.6f}")
print(f"相对误差: {abs(garch_lib_ll - arch_result.loglikelihood) / abs(arch_result.loglikelihood) * 100:.4f}%")

# 3. 预测对比
garch_lib_forecast = calc.forecast_volatility(1)
arch_forecast = arch_result.forecast(horizon=1, reindex=False)
arch_vol_pred = np.sqrt(arch_forecast.variance.values[-1, 0])

print(f"\n📈 预测对比:")
print(f"garch_lib预测: {garch_lib_forecast.volatility:.6f}")
print(f"arch库预测: {arch_vol_pred:.6f}")
print(f"预测差异: {abs(garch_lib_forecast.volatility - arch_vol_pred):.6f}")
print(f"预测相对误差: {abs(garch_lib_forecast.volatility - arch_vol_pred) / arch_vol_pred * 100:.2f}%")

# 4. 评估修复效果
ll_rel_err = abs(garch_lib_ll - arch_result.loglikelihood) / abs(arch_result.loglikelihood) * 100
pred_rel_err = abs(garch_lib_forecast.volatility - arch_vol_pred) / arch_vol_pred * 100

print(f"\n💡 修复效果评估:")
if ll_rel_err < 1.0 and pred_rel_err < 1.0:
    print(f"✅ 似然函数和预测修复成功！")
    print(f"   - 似然值相对误差: {ll_rel_err:.4f}% (目标: <1%)")
    print(f"   - 预测相对误差: {pred_rel_err:.2f}% (目标: <1%)")
elif ll_rel_err < 5.0 and pred_rel_err < 5.0:
    print(f"⚠️  部分修复成功，仍有改进空间")
    print(f"   - 似然值相对误差: {ll_rel_err:.4f}%")
    print(f"   - 预测相对误差: {pred_rel_err:.2f}%")
else:
    print(f"❌ 修复效果有限")
    print(f"   - 似然值相对误差: {ll_rel_err:.4f}%")
    print(f"   - 预测相对误差: {pred_rel_err:.2f}%")

print(f"\n📊 结论:")
if ll_rel_err < 1.0:
    print(f"✅ 似然函数修复成功！现在可以进行参数估计优化了。")
else:
    print(f"❌ 似然函数仍需进一步修复。") 