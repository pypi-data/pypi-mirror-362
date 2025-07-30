import numpy as np
import pandas as pd
from scipy.special import gamma
import math
from arch import arch_model

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]

# 使用arch库估计参数
arch_model_obj = arch_model(returns, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

# 获取参数和数据
mu = arch_result.params['mu']
omega = arch_result.params['omega']
alpha = arch_result.params['alpha[1]']
beta = arch_result.params['beta[1]']
nu = arch_result.params['nu']

residuals = returns - mu
arch_cond_vol = arch_result.conditional_volatility

print("🔍 GED似然函数详细调试")
print("=" * 60)
print(f"参数: ω={omega:.6f}, α={alpha:.6f}, β={beta:.6f}, ν={nu:.6f}")
print(f"arch库似然值: {arch_result.loglikelihood:.6f}")

# 1. 手动计算GARCH条件方差
def calculate_garch_variances(residuals, omega, alpha, beta):
    n = len(residuals)
    sigma2 = np.zeros(n)
    sigma2[0] = omega / (1 - alpha - beta)  # 无条件方差
    
    for t in range(1, n):
        sigma2[t] = omega + alpha * residuals[t-1]**2 + beta * sigma2[t-1]
    
    return sigma2

manual_var = calculate_garch_variances(residuals, omega, alpha, beta)
manual_vol = np.sqrt(manual_var)

print(f"\n📊 条件方差对比:")
print(f"arch库方差均值: {(arch_cond_vol**2).mean():.6f}")
print(f"手动计算方差均值: {manual_var.mean():.6f}")
print(f"方差差异: {np.abs((arch_cond_vol**2) - manual_var).mean():.8f}")

# 2. 不同的GED似然函数实现

def ged_likelihood_arch_style(residuals, sigma, nu):
    """arch库风格的GED似然函数"""
    # arch库的GED参数化
    lambda_ged = np.sqrt(gamma(1/nu) / gamma(3/nu))
    
    # 对数归一化常数
    log_const = (np.log(nu) - (1 + 1/nu) * np.log(2) - 
                np.log(lambda_ged) - math.lgamma(1/nu))
    
    # 标准化残差
    z = residuals / (lambda_ged * sigma)
    
    # 计算|z|^nu
    abs_z_pow_nu = np.power(np.abs(z), nu)
    
    # 对数似然
    log_lik = np.sum(log_const - np.log(sigma) - 0.5 * abs_z_pow_nu)
    
    return log_lik

def ged_likelihood_alternative(residuals, sigma, nu):
    """替代的GED似然函数实现"""
    # 不同的参数化方式
    c = np.sqrt(gamma(3/nu) / gamma(1/nu))
    
    # 对数归一化常数
    log_const = (np.log(nu) - np.log(2) - np.log(c) - math.lgamma(1/nu))
    
    # 标准化残差
    z = residuals / (c * sigma)
    
    # 计算|z|^nu
    abs_z_pow_nu = np.power(np.abs(z), nu)
    
    # 对数似然
    log_lik = np.sum(log_const - np.log(sigma) - 0.5 * abs_z_pow_nu)
    
    return log_lik

def ged_likelihood_standard(residuals, sigma, nu):
    """标准的GED似然函数"""
    # 标准GED参数化
    # f(x) = (nu / (2 * sigma * gamma(1/nu))) * exp(-0.5 * |x/sigma|^nu)
    
    log_const = (np.log(nu) - np.log(2) - math.lgamma(1/nu))
    
    # 标准化残差
    z = residuals / sigma
    
    # 计算|z|^nu
    abs_z_pow_nu = np.power(np.abs(z), nu)
    
    # 对数似然
    log_lik = np.sum(log_const - np.log(sigma) - 0.5 * abs_z_pow_nu)
    
    return log_lik

# 3. 测试不同的实现
print(f"\n🧪 不同GED实现对比:")

# 使用arch库的条件波动率
ll_arch_style = ged_likelihood_arch_style(residuals, arch_cond_vol, nu)
ll_alternative = ged_likelihood_alternative(residuals, arch_cond_vol, nu)
ll_standard = ged_likelihood_standard(residuals, arch_cond_vol, nu)

print(f"arch风格实现: {ll_arch_style:.6f} (差异: {abs(ll_arch_style - arch_result.loglikelihood):.6f})")
print(f"替代实现: {ll_alternative:.6f} (差异: {abs(ll_alternative - arch_result.loglikelihood):.6f})")
print(f"标准实现: {ll_standard:.6f} (差异: {abs(ll_standard - arch_result.loglikelihood):.6f})")

# 使用手动计算的条件波动率
ll_arch_style_manual = ged_likelihood_arch_style(residuals, manual_vol, nu)
ll_alternative_manual = ged_likelihood_alternative(residuals, manual_vol, nu)
ll_standard_manual = ged_likelihood_standard(residuals, manual_vol, nu)

print(f"\n使用手动计算的条件波动率:")
print(f"arch风格实现: {ll_arch_style_manual:.6f} (差异: {abs(ll_arch_style_manual - arch_result.loglikelihood):.6f})")
print(f"替代实现: {ll_alternative_manual:.6f} (差异: {abs(ll_alternative_manual - arch_result.loglikelihood):.6f})")
print(f"标准实现: {ll_standard_manual:.6f} (差异: {abs(ll_standard_manual - arch_result.loglikelihood):.6f})")

# 4. 分析arch库的内部实现
print(f"\n🔬 arch库内部分析:")

# 检查arch库是否使用了均值调整
print(f"原始收益率均值: {returns.mean():.6f}")
print(f"arch估计的mu: {mu:.6f}")
print(f"残差均值: {residuals.mean():.6f}")

# 检查arch库的GED参数化
lambda_arch = np.sqrt(gamma(1/nu) / gamma(3/nu))
c_alt = np.sqrt(gamma(3/nu) / gamma(1/nu))

print(f"\nGED标准化因子:")
print(f"λ (arch风格): {lambda_arch:.6f}")
print(f"c (替代风格): {c_alt:.6f}")
print(f"λ * c = {lambda_arch * c_alt:.6f} (应该等于1)")

# 5. 逐点分析似然贡献
print(f"\n📈 逐点似然分析 (前10个点):")
print(f"{'t':<3} {'residual':<10} {'sigma':<10} {'z':<10} {'|z|^nu':<10} {'ll_contrib':<12}")
print("-" * 65)

for t in range(min(10, len(residuals))):
    res = residuals[t]
    sig = arch_cond_vol[t]
    z = res / (lambda_arch * sig)
    abs_z_pow_nu = np.power(np.abs(z), nu)
    
    log_const = (np.log(nu) - (1 + 1/nu) * np.log(2) - 
                np.log(lambda_arch) - math.lgamma(1/nu))
    ll_contrib = log_const - np.log(sig) - 0.5 * abs_z_pow_nu
    
    print(f"{t:<3} {res:<10.4f} {sig:<10.4f} {z:<10.4f} {abs_z_pow_nu:<10.4f} {ll_contrib:<12.6f}")

# 6. 检查数值稳定性
print(f"\n⚠️  数值稳定性检查:")
extreme_residuals = np.abs(residuals) > 3 * np.std(residuals)
print(f"极端残差数量: {np.sum(extreme_residuals)}")
if np.sum(extreme_residuals) > 0:
    print(f"极端残差值: {residuals[extreme_residuals]}")

# 检查条件方差的稳定性
print(f"条件方差范围: [{manual_var.min():.6f}, {manual_var.max():.6f}]")
print(f"条件方差变异系数: {manual_var.std() / manual_var.mean():.4f}")

# 7. 最终结论
print(f"\n💡 调试结论:")
print(f"1. 最接近arch库的实现是: {'arch风格' if abs(ll_arch_style - arch_result.loglikelihood) < 0.1 else '需要进一步调试'}")
print(f"2. 条件方差计算{'一致' if np.abs((arch_cond_vol**2) - manual_var).mean() < 1e-6 else '有差异'}")
print(f"3. 主要差异来源: {'GED参数化' if abs(ll_arch_style - arch_result.loglikelihood) > 1 else '数值精度'}") 