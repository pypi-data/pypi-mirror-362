import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
from scipy.special import gamma
import math

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]

print("🔬 深度调试似然函数差异")
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

# 2. 计算残差
residuals = returns - mu
print(f"\n📊 残差统计:")
print(f"残差数量: {len(residuals)}")
print(f"残差均值: {residuals.mean():.8f}")
print(f"残差标准差: {residuals.std():.6f}")

# 3. 手动计算GARCH条件方差（完全按照arch库的方式）
def calculate_arch_style_variances(residuals, omega, alpha, beta):
    """完全按照arch库的方式计算条件方差"""
    n = len(residuals)
    sigma2 = np.zeros(n)
    
    # 初始方差：使用无条件方差
    sigma2[0] = omega / (1 - alpha - beta)
    
    # GARCH递推
    for t in range(1, n):
        sigma2[t] = omega + alpha * residuals[t-1]**2 + beta * sigma2[t-1]
    
    return sigma2

manual_var = calculate_arch_style_variances(residuals, omega, alpha, beta)
manual_vol = np.sqrt(manual_var)

# 4. 获取arch库的条件方差
arch_cond_vol = arch_result.conditional_volatility
arch_cond_var = arch_cond_vol ** 2

print(f"\n📈 条件方差对比:")
print(f"arch库方差均值: {arch_cond_var.mean():.8f}")
print(f"手动计算方差均值: {manual_var.mean():.8f}")
print(f"方差差异均值: {np.abs(arch_cond_var - manual_var).mean():.8f}")
print(f"方差差异最大值: {np.abs(arch_cond_var - manual_var).max():.8f}")
print(f"方差相关系数: {np.corrcoef(arch_cond_var, manual_var)[0,1]:.10f}")

# 5. 详细的GED似然函数实现对比
def ged_likelihood_exact_arch(residuals, sigma, nu):
    """严格按照arch库源码实现的GED似然函数"""
    # arch库的GED实现
    # 参考：https://github.com/bashtage/arch/blob/main/arch/univariate/distribution.py
    
    # 计算标准化因子
    lam = np.sqrt(gamma(1.0/nu) / gamma(3.0/nu))
    
    # 对数似然计算
    log_likelihood = 0.0
    
    for i in range(len(residuals)):
        eps = residuals[i]
        sig = sigma[i]
        
        # 标准化残差
        z = eps / sig
        
        # 计算 |z/λ|^ν
        abs_z_lam_pow_nu = np.power(np.abs(z / lam), nu)
        
        # 对数似然贡献
        # log f(z) = log(ν) - log(2) - log(λ) - log(Γ(1/ν)) - log(σ) - 0.5 * |z/λ|^ν
        ll_i = (np.log(nu) - np.log(2.0) - np.log(lam) - math.lgamma(1.0/nu) 
                - np.log(sig) - 0.5 * abs_z_lam_pow_nu)
        
        log_likelihood += ll_i
    
    return log_likelihood

def ged_likelihood_v3_corrected(residuals, sigma, nu):
    """修正的v3实现"""
    # 标准化因子
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

# 6. 测试不同的GED实现
print(f"\n🧪 GED似然函数实现对比:")

# 使用arch库的条件波动率
ll_exact_arch = ged_likelihood_exact_arch(residuals, arch_cond_vol, nu)
ll_v3_corrected = ged_likelihood_v3_corrected(residuals, arch_cond_vol, nu)

print(f"arch库似然值: {arch_result.loglikelihood:.6f}")
print(f"精确arch实现: {ll_exact_arch:.6f} (差异: {abs(ll_exact_arch - arch_result.loglikelihood):.6f})")
print(f"v3修正实现: {ll_v3_corrected:.6f} (差异: {abs(ll_v3_corrected - arch_result.loglikelihood):.6f})")

# 使用手动计算的条件波动率
ll_exact_arch_manual = ged_likelihood_exact_arch(residuals, manual_vol, nu)
ll_v3_corrected_manual = ged_likelihood_v3_corrected(residuals, manual_vol, nu)

print(f"\n使用手动计算的条件波动率:")
print(f"精确arch实现: {ll_exact_arch_manual:.6f} (差异: {abs(ll_exact_arch_manual - arch_result.loglikelihood):.6f})")
print(f"v3修正实现: {ll_v3_corrected_manual:.6f} (差异: {abs(ll_v3_corrected_manual - arch_result.loglikelihood):.6f})")

# 7. 测试garch_lib的当前实现
calc = gc.GarchCalculator(history_size=350)
calc.add_returns(returns.tolist())

arch_params = gc.GarchParameters()
arch_params.mu = mu
arch_params.omega = omega
arch_params.alpha = alpha
arch_params.beta = beta
arch_params.nu = nu

calc.set_parameters(arch_params)
garch_lib_ll = calc.calculate_log_likelihood()

print(f"\n🔧 garch_lib当前实现:")
print(f"garch_lib似然值: {garch_lib_ll:.6f} (差异: {abs(garch_lib_ll - arch_result.loglikelihood):.6f})")

# 8. 逐点分析似然贡献的差异
print(f"\n🔍 逐点似然分析 (前10个点):")
print(f"{'t':<3} {'residual':<10} {'arch_sigma':<12} {'manual_sigma':<12} {'arch_ll':<12} {'manual_ll':<12} {'diff':<10}")
print("-" * 85)

lam = np.sqrt(gamma(1.0/nu) / gamma(3.0/nu))

for t in range(min(10, len(residuals))):
    eps = residuals[t]
    arch_sig = arch_cond_vol[t]
    manual_sig = manual_vol[t]
    
    # arch库的似然贡献
    z_arch = eps / arch_sig
    abs_z_lam_pow_nu_arch = np.power(np.abs(z_arch / lam), nu)
    ll_arch = (np.log(nu) - np.log(2.0) - np.log(lam) - math.lgamma(1.0/nu) 
               - np.log(arch_sig) - 0.5 * abs_z_lam_pow_nu_arch)
    
    # 手动计算的似然贡献
    z_manual = eps / manual_sig
    abs_z_lam_pow_nu_manual = np.power(np.abs(z_manual / lam), nu)
    ll_manual = (np.log(nu) - np.log(2.0) - np.log(lam) - math.lgamma(1.0/nu) 
                 - np.log(manual_sig) - 0.5 * abs_z_lam_pow_nu_manual)
    
    diff = ll_arch - ll_manual
    
    print(f"{t:<3} {eps:<10.4f} {arch_sig:<12.6f} {manual_sig:<12.6f} {ll_arch:<12.6f} {ll_manual:<12.6f} {diff:<10.6f}")

# 9. 分析最佳的实现方式
best_impl = min([
    (ll_exact_arch, "精确arch实现(arch条件方差)"),
    (ll_v3_corrected, "v3修正实现(arch条件方差)"),
    (ll_exact_arch_manual, "精确arch实现(手动条件方差)"),
    (ll_v3_corrected_manual, "v3修正实现(手动条件方差)")
], key=lambda x: abs(x[0] - arch_result.loglikelihood))

print(f"\n💡 最佳实现:")
print(f"最接近arch库的实现: {best_impl[1]}")
print(f"似然值: {best_impl[0]:.6f}")
print(f"与arch库差异: {abs(best_impl[0] - arch_result.loglikelihood):.6f}")

# 10. 检查数值精度问题
print(f"\n🔬 数值精度分析:")
print(f"GED形状参数 ν: {nu:.6f}")
print(f"λ = sqrt(Γ(1/ν)/Γ(3/ν)): {lam:.10f}")
print(f"log(Γ(1/ν)): {math.lgamma(1.0/nu):.10f}")
print(f"log(Γ(3/ν)): {math.lgamma(3.0/nu):.10f}")

# 检查极端值
extreme_residuals = np.abs(residuals) > 3 * np.std(residuals)
print(f"极端残差数量: {np.sum(extreme_residuals)}")
if np.sum(extreme_residuals) > 0:
    print(f"极端残差值: {residuals[extreme_residuals]}")
    print(f"对应的条件方差: {manual_var[extreme_residuals]}")

print(f"\n📋 修复建议:")
if abs(best_impl[0] - arch_result.loglikelihood) < 0.1:
    print(f"✅ 找到了正确的实现方式！")
    print(f"建议使用: {best_impl[1]}")
else:
    print(f"❌ 仍需进一步调试")
    print(f"可能的问题:")
    print(f"1. 条件方差计算的初始化方式")
    print(f"2. GED参数化的细微差异")
    print(f"3. 数值精度问题") 