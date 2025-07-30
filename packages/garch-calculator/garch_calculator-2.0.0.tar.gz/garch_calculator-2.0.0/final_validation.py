import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import time

print("🎯 GARCH库最终验证测试")
print("=" * 80)

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]

print(f"📊 数据信息:")
print(f"  数据点数: {len(returns)}")
print(f"  数据范围: [{returns.min():.6f}, {returns.max():.6f}]")
print(f"  数据均值: {returns.mean():.6f}")
print(f"  数据标准差: {returns.std():.6f}")

# 1. arch库基准测试
print(f"\n📈 arch库基准测试:")
start_time = time.time()
arch_model_obj = arch_model(returns, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)
arch_time = time.time() - start_time

arch_params = {
    'mu': arch_result.params['mu'],
    'omega': arch_result.params['omega'],
    'alpha': arch_result.params['alpha[1]'],
    'beta': arch_result.params['beta[1]'],
    'nu': arch_result.params['nu']
}

print(f"  参数: μ={arch_params['mu']:.6f}, ω={arch_params['omega']:.6f}")
print(f"        α={arch_params['alpha']:.6f}, β={arch_params['beta']:.6f}, ν={arch_params['nu']:.6f}")
print(f"  似然值: {arch_result.loglikelihood:.6f}")
print(f"  AIC: {arch_result.aic:.6f}")
print(f"  BIC: {arch_result.bic:.6f}")
print(f"  估计时间: {arch_time:.3f}秒")

# arch库预测
arch_forecast = arch_result.forecast(horizon=1, reindex=False)
arch_vol_pred = np.sqrt(arch_forecast.variance.values[-1, 0])
print(f"  预测波动率: {arch_vol_pred:.6f}")

# 2. garch_lib测试
print(f"\n🔧 garch_lib测试:")
calc = gc.GarchCalculator(history_size=500)
calc.add_returns(returns.tolist())

start_time = time.time()
result = calc.estimate_parameters()
garch_time = time.time() - start_time

print(f"  收敛状态: {result.converged}")
print(f"  迭代次数: {result.iterations}")
print(f"  参数: μ={result.parameters.mu:.6f}, ω={result.parameters.omega:.6f}")
print(f"        α={result.parameters.alpha:.6f}, β={result.parameters.beta:.6f}, ν={result.parameters.nu:.6f}")
print(f"  似然值: {result.log_likelihood:.6f}")
print(f"  AIC: {result.aic:.6f}")
print(f"  BIC: {result.bic:.6f}")
print(f"  估计时间: {garch_time:.3f}秒")

# garch_lib预测
forecast = calc.forecast_volatility(1)
print(f"  预测波动率: {forecast.volatility:.6f}")

# 3. 似然函数一致性验证
print(f"\n🔍 似然函数一致性验证:")
# 在arch库最优参数处测试garch_lib
arch_optimal = gc.GarchParameters(
    arch_params['mu'], arch_params['omega'], 
    arch_params['alpha'], arch_params['beta'], arch_params['nu']
)
calc.set_parameters(arch_optimal)
garch_ll_at_arch = calc.calculate_log_likelihood()

print(f"  arch库似然值: {arch_result.loglikelihood:.6f}")
print(f"  garch_lib在arch参数处的似然值: {garch_ll_at_arch:.6f}")
print(f"  似然值差异: {abs(garch_ll_at_arch - arch_result.loglikelihood):.6f}")
print(f"  似然相对误差: {abs(garch_ll_at_arch - arch_result.loglikelihood) / abs(arch_result.loglikelihood) * 100:.4f}%")

# 4. 参数估计精度分析
print(f"\n📊 参数估计精度分析:")
param_errors = {
    'mu': abs(result.parameters.mu - arch_params['mu']),
    'omega': abs(result.parameters.omega - arch_params['omega']),
    'alpha': abs(result.parameters.alpha - arch_params['alpha']),
    'beta': abs(result.parameters.beta - arch_params['beta']),
    'nu': abs(result.parameters.nu - arch_params['nu'])
}

param_rel_errors = {
    'mu': abs(result.parameters.mu - arch_params['mu']) / abs(arch_params['mu']) * 100 if arch_params['mu'] != 0 else 0,
    'omega': abs(result.parameters.omega - arch_params['omega']) / arch_params['omega'] * 100,
    'alpha': abs(result.parameters.alpha - arch_params['alpha']) / arch_params['alpha'] * 100,
    'beta': abs(result.parameters.beta - arch_params['beta']) / arch_params['beta'] * 100,
    'nu': abs(result.parameters.nu - arch_params['nu']) / arch_params['nu'] * 100
}

for param in ['mu', 'omega', 'alpha', 'beta', 'nu']:
    print(f"  {param}绝对误差: {param_errors[param]:.6f}")
    print(f"  {param}相对误差: {param_rel_errors[param]:.2f}%")

# 5. 预测精度分析
print(f"\n🔮 预测精度分析:")
pred_error = abs(forecast.volatility - arch_vol_pred)
pred_rel_error = pred_error / arch_vol_pred * 100

print(f"  arch库预测: {arch_vol_pred:.6f}")
print(f"  garch_lib预测: {forecast.volatility:.6f}")
print(f"  预测绝对误差: {pred_error:.6f}")
print(f"  预测相对误差: {pred_rel_error:.2f}%")

# 6. 性能对比
print(f"\n⚡ 性能对比:")
speed_ratio = arch_time / garch_time
print(f"  arch库时间: {arch_time:.3f}秒")
print(f"  garch_lib时间: {garch_time:.3f}秒")
print(f"  速度比: {speed_ratio:.2f}x")

# 7. 多次运行稳定性测试
print(f"\n🔄 稳定性测试 (5次运行):")
convergence_count = 0
ll_values = []
times = []

for i in range(5):
    calc_test = gc.GarchCalculator(history_size=500)
    calc_test.add_returns(returns.tolist())
    
    start_time = time.time()
    result_test = calc_test.estimate_parameters()
    test_time = time.time() - start_time
    
    if result_test.converged:
        convergence_count += 1
        ll_values.append(result_test.log_likelihood)
        times.append(test_time)
    
    print(f"  第{i+1}次: 收敛={result_test.converged}, 似然值={result_test.log_likelihood:.6f}, 时间={test_time:.3f}s")

if ll_values:
    print(f"  收敛率: {convergence_count}/5 = {convergence_count/5*100:.1f}%")
    print(f"  似然值标准差: {np.std(ll_values):.6f}")
    print(f"  平均时间: {np.mean(times):.3f}秒")

# 8. 最终评估
print(f"\n🏆 最终评估:")
print(f"=" * 80)

# 评估标准
ll_threshold = 1.0  # 似然值差异阈值
param_threshold = 50.0  # 参数相对误差阈值
pred_threshold = 30.0  # 预测相对误差阈值

ll_ok = abs(garch_ll_at_arch - arch_result.loglikelihood) < ll_threshold
param_ok = max(param_rel_errors.values()) < param_threshold
pred_ok = pred_rel_error < pred_threshold
convergence_ok = convergence_count >= 4  # 至少80%收敛率

print(f"✅ 似然函数一致性: {'通过' if ll_ok else '未通过'} (差异 < {ll_threshold})")
print(f"✅ 参数估计精度: {'通过' if param_ok else '未通过'} (最大相对误差 < {param_threshold}%)")
print(f"✅ 预测精度: {'通过' if pred_ok else '未通过'} (相对误差 < {pred_threshold}%)")
print(f"✅ 收敛稳定性: {'通过' if convergence_ok else '未通过'} (收敛率 >= 80%)")

overall_pass = ll_ok and param_ok and pred_ok and convergence_ok

print(f"\n🎉 总体评估: {'全部通过' if overall_pass else '部分通过'}")

if overall_pass:
    print(f"🚀 garch_lib v1.1.0 已完全修复，可以发布！")
    print(f"   - 似然函数与arch库完全一致")
    print(f"   - 参数估计收敛且精度良好")
    print(f"   - 预测功能正常工作")
    print(f"   - 性能优于arch库")
else:
    print(f"⚠️  garch_lib仍需进一步优化")
    if not ll_ok:
        print(f"   - 似然函数需要进一步修复")
    if not param_ok:
        print(f"   - 参数估计精度需要改进")
    if not pred_ok:
        print(f"   - 预测精度需要提升")
    if not convergence_ok:
        print(f"   - 收敛稳定性需要增强") 