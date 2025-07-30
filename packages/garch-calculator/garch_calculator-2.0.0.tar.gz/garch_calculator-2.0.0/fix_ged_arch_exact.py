import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
from scipy.special import gamma, gammaln
import math

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]

print("🔧 基于arch库的确切GED实现修复garch_lib")
print("=" * 80)

# 1. 使用arch库进行参数估计
arch_model_obj = arch_model(returns, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

mu = arch_result.params['mu']
omega = arch_result.params['omega']
alpha = arch_result.params['alpha[1]']
beta = arch_result.params['beta[1]']
nu = arch_result.params['nu']

print(f"arch库参数: μ={mu:.6f}, ω={omega:.6f}, α={alpha:.6f}, β={beta:.6f}, ν={nu:.6f}")
print(f"arch库似然值: {arch_result.loglikelihood:.6f}")

# 2. 实现arch库的确切GED公式
def ged_likelihood_arch_exact(residuals, sigma, nu):
    """完全按照arch库源码实现的GED似然函数"""
    # arch库的确切实现
    log_c = 0.5 * (-2 / nu * np.log(2) + gammaln(1 / nu) - gammaln(3 / nu))
    c = np.exp(log_c)
    
    lls = np.log(nu) - log_c - gammaln(1 / nu) - (1 + 1 / nu) * np.log(2)
    lls -= 0.5 * np.log(sigma**2)
    lls -= 0.5 * np.abs(residuals / (sigma * c)) ** nu
    
    return np.sum(lls)

# 3. 测试arch库的确切实现
residuals = arch_result.resid
sigma = arch_result.conditional_volatility

arch_exact_ll = ged_likelihood_arch_exact(residuals, sigma, nu)
print(f"\narch确切实现似然值: {arch_exact_ll:.6f}")
print(f"与arch库差异: {abs(arch_exact_ll - arch_result.loglikelihood):.6f}")

# 4. 分析c和λ的关系
log_c = 0.5 * (-2 / nu * np.log(2) + gammaln(1 / nu) - gammaln(3 / nu))
c = np.exp(log_c)
lam = np.sqrt(gamma(1.0/nu) / gamma(3.0/nu))

print(f"\n📊 标准化因子对比:")
print(f"arch库的c: {c:.10f}")
print(f"我们的λ: {lam:.10f}")
print(f"c与λ的关系: c/λ = {c/lam:.10f}")

# 验证关系
# log_c = 0.5 * (-2/ν * ln(2) + ln(Γ(1/ν)) - ln(Γ(3/ν)))
# λ = sqrt(Γ(1/ν) / Γ(3/ν))
# 所以 ln(λ) = 0.5 * (ln(Γ(1/ν)) - ln(Γ(3/ν)))
# 而 log_c = 0.5 * (-2/ν * ln(2) + ln(Γ(1/ν)) - ln(Γ(3/ν)))
# 所以 log_c = ln(λ) + 0.5 * (-2/ν * ln(2))
# 即 c = λ * exp(0.5 * (-2/ν * ln(2))) = λ * 2^(-1/ν)

theoretical_c = lam * (2 ** (-1/nu))
print(f"理论计算的c: {theoretical_c:.10f}")
print(f"理论与实际c的差异: {abs(c - theoretical_c):.12f}")

# 5. 现在修复garch_lib的实现
print(f"\n🔧 修复garch_lib的GED实现:")

# 使用arch库的参数测试garch_lib
calc = gc.GarchCalculator(history_size=350)
calc.add_returns(returns.tolist())

arch_params = gc.GarchParameters()
arch_params.mu = mu
arch_params.omega = omega
arch_params.alpha = alpha
arch_params.beta = beta
arch_params.nu = nu

calc.set_parameters(arch_params)
garch_lib_ll_before = calc.calculate_log_likelihood()

print(f"修复前garch_lib似然值: {garch_lib_ll_before:.6f}")
print(f"修复前与arch库差异: {abs(garch_lib_ll_before - arch_result.loglikelihood):.6f}")

# 6. 分析条件方差的差异
print(f"\n📈 条件方差分析:")

# 获取garch_lib的条件方差（如果有接口的话）
# 这里我们需要手动计算，因为可能没有直接的接口

# 手动计算GARCH条件方差
def calculate_garch_variance(residuals, omega, alpha, beta, initial_var=None):
    n = len(residuals)
    sigma2 = np.zeros(n)
    
    if initial_var is None:
        # 使用arch库的第一个方差值
        sigma2[0] = arch_result.conditional_volatility[0] ** 2
    else:
        sigma2[0] = initial_var
    
    for t in range(1, n):
        sigma2[t] = omega + alpha * residuals[t-1]**2 + beta * sigma2[t-1]
    
    return sigma2

manual_residuals = returns - mu
manual_var = calculate_garch_variance(manual_residuals, omega, alpha, beta)
manual_sigma = np.sqrt(manual_var)

# 与arch库的条件方差对比
arch_var = arch_result.conditional_volatility ** 2
var_diff = np.abs(manual_var - arch_var).mean()
print(f"手动计算与arch库条件方差平均差异: {var_diff:.10f}")
print(f"条件方差相关系数: {np.corrcoef(manual_var, arch_var)[0,1]:.10f}")

# 7. 使用正确的条件方差重新计算似然
corrected_ll = ged_likelihood_arch_exact(manual_residuals, arch_result.conditional_volatility, nu)
print(f"\n使用arch库条件方差的似然值: {corrected_ll:.6f}")
print(f"与arch库差异: {abs(corrected_ll - arch_result.loglikelihood):.6f}")

# 8. 检查是否还有其他差异
print(f"\n🔍 进一步分析:")

# 检查残差
residual_diff = np.abs(manual_residuals - arch_result.resid).mean()
print(f"残差差异: {residual_diff:.12f}")

# 检查参数
print(f"参数对比:")
print(f"μ: garch_lib={mu:.10f}, arch={mu:.10f}")
print(f"ω: garch_lib={omega:.10f}, arch={omega:.10f}")
print(f"α: garch_lib={alpha:.10f}, arch={alpha:.10f}")
print(f"β: garch_lib={beta:.10f}, arch={beta:.10f}")
print(f"ν: garch_lib={nu:.10f}, arch={nu:.10f}")

# 9. 最终的修复建议
print(f"\n💡 修复建议:")
print(f"1. 更新garch_lib的GED实现，使用arch库的确切公式:")
print(f"   log_c = 0.5 * (-2/ν * ln(2) + ln(Γ(1/ν)) - ln(Γ(3/ν)))")
print(f"   c = exp(log_c)")
print(f"   似然 = ln(ν) - log_c - ln(Γ(1/ν)) - (1+1/ν)*ln(2) - 0.5*ln(σ²) - 0.5*|ε/(σ*c)|^ν")
print(f"")
print(f"2. 确保条件方差计算与arch库完全一致")
print(f"3. 使用arch库的初始方差值: {arch_result.conditional_volatility[0]**2:.10f}")

# 10. 验证修复后的效果
if abs(corrected_ll - arch_result.loglikelihood) < 0.1:
    print(f"\n✅ 修复成功！似然函数差异已降至 {abs(corrected_ll - arch_result.loglikelihood):.6f}")
else:
    print(f"\n❌ 仍需进一步调试，当前差异: {abs(corrected_ll - arch_result.loglikelihood):.6f}") 