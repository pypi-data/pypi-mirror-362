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

print("🔧 修复GED似然函数")
print("=" * 60)
print(f"目标似然值: {arch_result.loglikelihood:.6f}")

# 尝试不同的GED实现，基于arch库的源码
def ged_likelihood_corrected(residuals, sigma, nu):
    """基于arch库源码的正确GED实现"""
    # arch库使用的GED参数化
    # 参考: https://github.com/bashtage/arch/blob/main/arch/univariate/distribution.py
    
    # 计算标准化因子
    g1 = gamma(1.0 / nu)
    g3 = gamma(3.0 / nu)
    lam = np.sqrt(g1 / g3)
    
    # 对数似然计算
    # log f(z) = log(nu) - log(2) - log(lam) - log(Γ(1/ν)) - log(σ) - 0.5 * |z/lam|^ν
    # 其中 z = ε/σ
    
    log_likelihood = 0.0
    
    for i in range(len(residuals)):
        eps = residuals[i]
        sig = sigma[i]
        
        # 标准化残差
        z = eps / sig
        
        # 计算 |z/λ|^ν
        abs_z_lam_pow_nu = np.power(np.abs(z / lam), nu)
        
        # 对数似然贡献
        ll_i = (np.log(nu) - np.log(2.0) - np.log(lam) - math.lgamma(1.0/nu) 
                - np.log(sig) - 0.5 * abs_z_lam_pow_nu)
        
        log_likelihood += ll_i
    
    return log_likelihood

def ged_likelihood_v2(residuals, sigma, nu):
    """另一种可能的实现"""
    # 不同的标准化方式
    lam = np.sqrt(gamma(1.0/nu) / gamma(3.0/nu))
    
    log_likelihood = 0.0
    
    for i in range(len(residuals)):
        eps = residuals[i]
        sig = sigma[i]
        
        # 标准化残差 (不同的方式)
        z = eps / (lam * sig)
        
        # 计算 |z|^ν
        abs_z_pow_nu = np.power(np.abs(z), nu)
        
        # 对数似然贡献
        ll_i = (np.log(nu) - np.log(2.0) - np.log(lam) - math.lgamma(1.0/nu) 
                - np.log(sig) - 0.5 * abs_z_pow_nu)
        
        log_likelihood += ll_i
    
    return log_likelihood

def ged_likelihood_v3(residuals, sigma, nu):
    """第三种实现 - 基于标准GED公式"""
    # 标准GED密度函数
    # f(x) = ν/(2^(1+1/ν) * Γ(1/ν) * σ) * exp(-0.5 * |x/σ|^ν / λ^ν)
    # 其中 λ = (Γ(1/ν)/Γ(3/ν))^(1/2)
    
    lam = np.sqrt(gamma(1.0/nu) / gamma(3.0/nu))
    
    log_likelihood = 0.0
    
    for i in range(len(residuals)):
        eps = residuals[i]
        sig = sigma[i]
        
        # 标准化残差
        z = eps / sig
        
        # 计算 |z|^ν / λ^ν
        abs_z_pow_nu_over_lam_nu = np.power(np.abs(z), nu) / np.power(lam, nu)
        
        # 对数似然贡献
        ll_i = (np.log(nu) - (1.0 + 1.0/nu) * np.log(2.0) - math.lgamma(1.0/nu) 
                - np.log(sig) - 0.5 * abs_z_pow_nu_over_lam_nu)
        
        log_likelihood += ll_i
    
    return log_likelihood

# 测试不同实现
print(f"\n🧪 测试修复的GED实现:")

# 使用arch库的条件波动率
ll_v1 = ged_likelihood_corrected(residuals, arch_cond_vol, nu)
ll_v2 = ged_likelihood_v2(residuals, arch_cond_vol, nu)
ll_v3 = ged_likelihood_v3(residuals, arch_cond_vol, nu)

print(f"实现v1: {ll_v1:.6f} (差异: {abs(ll_v1 - arch_result.loglikelihood):.6f})")
print(f"实现v2: {ll_v2:.6f} (差异: {abs(ll_v2 - arch_result.loglikelihood):.6f})")
print(f"实现v3: {ll_v3:.6f} (差异: {abs(ll_v3 - arch_result.loglikelihood):.6f})")

# 找到最佳实现
best_impl = min([(ll_v1, 'v1'), (ll_v2, 'v2'), (ll_v3, 'v3')], 
                key=lambda x: abs(x[0] - arch_result.loglikelihood))

print(f"\n✅ 最佳实现: {best_impl[1]} (似然值: {best_impl[0]:.6f})")

# 验证条件方差计算
def calculate_garch_variances_exact(residuals, omega, alpha, beta):
    """精确的GARCH条件方差计算"""
    n = len(residuals)
    sigma2 = np.zeros(n)
    
    # 初始方差 - 尝试不同的初始化方法
    sigma2[0] = omega / (1 - alpha - beta)  # 无条件方差
    
    for t in range(1, n):
        sigma2[t] = omega + alpha * residuals[t-1]**2 + beta * sigma2[t-1]
        # 确保方差为正
        sigma2[t] = max(sigma2[t], 1e-8)
    
    return sigma2

# 重新计算条件方差
manual_var_exact = calculate_garch_variances_exact(residuals, omega, alpha, beta)
manual_vol_exact = np.sqrt(manual_var_exact)

print(f"\n📊 精确条件方差对比:")
print(f"arch库方差均值: {(arch_cond_vol**2).mean():.8f}")
print(f"手动计算方差均值: {manual_var_exact.mean():.8f}")
print(f"方差差异: {np.abs((arch_cond_vol**2) - manual_var_exact).mean():.8f}")
print(f"最大方差差异: {np.abs((arch_cond_vol**2) - manual_var_exact).max():.8f}")

# 使用精确的条件方差重新测试
if best_impl[1] == 'v1':
    ll_exact = ged_likelihood_corrected(residuals, manual_vol_exact, nu)
elif best_impl[1] == 'v2':
    ll_exact = ged_likelihood_v2(residuals, manual_vol_exact, nu)
else:
    ll_exact = ged_likelihood_v3(residuals, manual_vol_exact, nu)

print(f"\n使用精确条件方差的似然值: {ll_exact:.6f} (差异: {abs(ll_exact - arch_result.loglikelihood):.6f})")

# 分析残差的统计特性
print(f"\n📈 残差统计分析:")
print(f"残差均值: {residuals.mean():.6f}")
print(f"残差标准差: {residuals.std():.6f}")
print(f"残差偏度: {pd.Series(residuals).skew():.4f}")
print(f"残差峰度: {pd.Series(residuals).kurtosis():.4f}")

# 检查极端值的影响
extreme_mask = np.abs(residuals) > 3 * np.std(residuals)
print(f"极端值数量: {np.sum(extreme_mask)}")
if np.sum(extreme_mask) > 0:
    print(f"极端值: {residuals[extreme_mask]}")
    
    # 计算去除极端值后的似然
    residuals_clean = residuals[~extreme_mask]
    sigma_clean = arch_cond_vol[~extreme_mask]
    
    if best_impl[1] == 'v1':
        ll_clean = ged_likelihood_corrected(residuals_clean, sigma_clean, nu)
    elif best_impl[1] == 'v2':
        ll_clean = ged_likelihood_v2(residuals_clean, sigma_clean, nu)
    else:
        ll_clean = ged_likelihood_v3(residuals_clean, sigma_clean, nu)
    
    print(f"去除极端值后的似然值: {ll_clean:.6f}")

print(f"\n💡 修复建议:")
print(f"1. 使用实现{best_impl[1]}作为GED似然函数")
print(f"2. 改进条件方差计算的数值精度")
print(f"3. 处理极端值以提高数值稳定性") 