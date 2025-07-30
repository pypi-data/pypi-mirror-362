import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]

print("🔧 测试修复后的参数估计")
print("=" * 60)

# 1. 使用arch库进行参数估计作为基准
print("\n📊 arch库参数估计 (基准):")
arch_model_obj = arch_model(returns, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

print(f"arch库参数:")
print(f"  mu: {arch_result.params['mu']:.6f}")
print(f"  omega: {arch_result.params['omega']:.6f}")
print(f"  alpha: {arch_result.params['alpha[1]']:.6f}")
print(f"  beta: {arch_result.params['beta[1]']:.6f}")
print(f"  nu: {arch_result.params['nu']:.6f}")
print(f"  对数似然: {arch_result.loglikelihood:.4f}")

# 2. 使用修复后的garch_lib进行参数估计
print(f"\n🔧 修复后的garch_lib参数估计:")
calc = gc.GarchCalculator(history_size=350)
calc.add_returns(returns.tolist())
result = calc.estimate_parameters()

print(f"garch_lib结果:")
print(f"  收敛: {result.converged}")
print(f"  迭代次数: {result.iterations}")
print(f"  mu: {result.parameters.mu:.6f}")
print(f"  omega: {result.parameters.omega:.6f}")
print(f"  alpha: {result.parameters.alpha:.6f}")
print(f"  beta: {result.parameters.beta:.6f}")
print(f"  nu: {result.parameters.nu:.6f}")
print(f"  对数似然: {result.log_likelihood:.4f}")

# 3. 参数对比
if result.converged:
    print(f"\n📈 参数对比:")
    print(f"{'参数':<8} {'arch库':<12} {'garch_lib':<12} {'差异':<12} {'相对误差%':<12}")
    print("-" * 60)
    
    mu_diff = abs(result.parameters.mu - arch_result.params['mu'])
    mu_rel_err = mu_diff / abs(arch_result.params['mu']) * 100 if arch_result.params['mu'] != 0 else 0
    print(f"{'mu':<8} {arch_result.params['mu']:<12.6f} {result.parameters.mu:<12.6f} {mu_diff:<12.6f} {mu_rel_err:<12.2f}")
    
    omega_diff = abs(result.parameters.omega - arch_result.params['omega'])
    omega_rel_err = omega_diff / arch_result.params['omega'] * 100
    print(f"{'omega':<8} {arch_result.params['omega']:<12.6f} {result.parameters.omega:<12.6f} {omega_diff:<12.6f} {omega_rel_err:<12.2f}")
    
    alpha_diff = abs(result.parameters.alpha - arch_result.params['alpha[1]'])
    alpha_rel_err = alpha_diff / arch_result.params['alpha[1]'] * 100
    print(f"{'alpha':<8} {arch_result.params['alpha[1]']:<12.6f} {result.parameters.alpha:<12.6f} {alpha_diff:<12.6f} {alpha_rel_err:<12.2f}")
    
    beta_diff = abs(result.parameters.beta - arch_result.params['beta[1]'])
    beta_rel_err = beta_diff / arch_result.params['beta[1]'] * 100
    print(f"{'beta':<8} {arch_result.params['beta[1]']:<12.6f} {result.parameters.beta:<12.6f} {beta_diff:<12.6f} {beta_rel_err:<12.2f}")
    
    nu_diff = abs(result.parameters.nu - arch_result.params['nu'])
    nu_rel_err = nu_diff / arch_result.params['nu'] * 100
    print(f"{'nu':<8} {arch_result.params['nu']:<12.6f} {result.parameters.nu:<12.6f} {nu_diff:<12.6f} {nu_rel_err:<12.2f}")
    
    ll_diff = abs(result.log_likelihood - arch_result.loglikelihood)
    print(f"\n似然值差异: {ll_diff:.6f}")
    
    # 4. 预测对比
    print(f"\n🎯 预测对比:")
    
    # garch_lib预测
    garch_lib_forecast = calc.forecast_volatility(1)
    
    # arch库预测
    arch_forecast = arch_result.forecast(horizon=1, reindex=False)
    arch_vol_pred = np.sqrt(arch_forecast.variance.values[-1, 0])
    
    print(f"garch_lib预测波动率: {garch_lib_forecast.volatility:.6f}")
    print(f"arch库预测波动率: {arch_vol_pred:.6f}")
    print(f"预测差异: {abs(garch_lib_forecast.volatility - arch_vol_pred):.6f}")
    print(f"预测相对误差: {abs(garch_lib_forecast.volatility - arch_vol_pred) / arch_vol_pred * 100:.2f}%")
    
    # 5. 评估修复效果
    print(f"\n💡 修复效果评估:")
    
    # 参数估计精度
    avg_param_error = (mu_rel_err + omega_rel_err + alpha_rel_err + beta_rel_err + nu_rel_err) / 5
    print(f"平均参数相对误差: {avg_param_error:.2f}%")
    
    # 似然值精度
    ll_rel_err = ll_diff / abs(arch_result.loglikelihood) * 100
    print(f"似然值相对误差: {ll_rel_err:.4f}%")
    
    # 预测精度
    pred_rel_err = abs(garch_lib_forecast.volatility - arch_vol_pred) / arch_vol_pred * 100
    print(f"预测相对误差: {pred_rel_err:.2f}%")
    
    # 总体评估
    if avg_param_error < 5.0 and ll_rel_err < 1.0 and pred_rel_err < 1.0:
        print(f"\n✅ 修复成功！garch_lib现在与arch库高度一致")
    elif avg_param_error < 10.0 and ll_rel_err < 5.0:
        print(f"\n⚠️  部分修复成功，仍有改进空间")
    else:
        print(f"\n❌ 修复效果有限，需要进一步调试")
        
else:
    print(f"\n❌ garch_lib参数估计未收敛，修复失败")

print(f"\n🔍 调试信息:")
print(f"数据点数: {len(returns)}")
print(f"收益率均值: {returns.mean():.6f}")
print(f"收益率标准差: {returns.std():.6f}")
print(f"收益率范围: [{returns.min():.2f}, {returns.max():.2f}]") 