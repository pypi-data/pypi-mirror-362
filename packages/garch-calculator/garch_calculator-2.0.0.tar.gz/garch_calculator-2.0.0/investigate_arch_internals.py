import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
from scipy.special import gamma
import math

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]

print("🔍 深入调查arch库内部实现")
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

# 2. 深入分析arch库的内部数据
print(f"\n📊 arch库内部数据分析:")

# 获取arch库的残差
arch_residuals = arch_result.resid
print(f"arch库残差数量: {len(arch_residuals)}")
print(f"arch库残差均值: {arch_residuals.mean():.8f}")
print(f"arch库残差标准差: {arch_residuals.std():.6f}")

# 手动计算的残差
manual_residuals = returns - mu
print(f"手动计算残差均值: {manual_residuals.mean():.8f}")
print(f"残差差异: {np.abs(arch_residuals - manual_residuals).mean():.10f}")

# 3. 分析arch库的条件方差计算
arch_cond_vol = arch_result.conditional_volatility
arch_cond_var = arch_cond_vol ** 2

print(f"\n📈 arch库条件方差详细分析:")
print(f"条件方差数量: {len(arch_cond_var)}")
print(f"第一个条件方差: {arch_cond_var[0]:.10f}")
print(f"理论无条件方差: {omega / (1 - alpha - beta):.10f}")
print(f"差异: {abs(arch_cond_var[0] - omega / (1 - alpha - beta)):.10f}")

# 4. 尝试不同的初始化方法
def test_variance_initialization():
    """测试不同的方差初始化方法"""
    print(f"\n🧪 测试不同的方差初始化方法:")
    
    # 方法1: 无条件方差
    unconditional_var = omega / (1 - alpha - beta)
    print(f"方法1 - 无条件方差: {unconditional_var:.10f}")
    
    # 方法2: 样本方差
    sample_var = manual_residuals.var()
    print(f"方法2 - 样本方差: {sample_var:.10f}")
    
    # 方法3: arch库的第一个条件方差
    arch_first_var = arch_cond_var[0]
    print(f"方法3 - arch库第一个方差: {arch_first_var:.10f}")
    
    # 方法4: 使用前几个残差的平方均值
    if len(manual_residuals) >= 10:
        initial_var = np.mean(manual_residuals[:10]**2)
        print(f"方法4 - 前10个残差平方均值: {initial_var:.10f}")
    
    return unconditional_var, sample_var, arch_first_var

test_variance_initialization()

# 5. 尝试完全复制arch库的条件方差计算
def replicate_arch_variance_exactly():
    """尝试完全复制arch库的条件方差计算"""
    print(f"\n🎯 尝试完全复制arch库的条件方差:")
    
    n = len(manual_residuals)
    sigma2 = np.zeros(n)
    
    # 尝试不同的初始化
    methods = [
        ("无条件方差", omega / (1 - alpha - beta)),
        ("arch第一个方差", arch_cond_var[0]),
        ("样本方差", manual_residuals.var()),
    ]
    
    best_method = None
    best_diff = float('inf')
    
    for method_name, init_var in methods:
        sigma2[0] = init_var
        
        # GARCH递推
        for t in range(1, n):
            sigma2[t] = omega + alpha * manual_residuals[t-1]**2 + beta * sigma2[t-1]
        
        # 计算与arch库的差异
        diff = np.abs(sigma2 - arch_cond_var).mean()
        print(f"{method_name}: 平均差异 = {diff:.10f}")
        
        if diff < best_diff:
            best_diff = diff
            best_method = (method_name, init_var, sigma2.copy())
    
    return best_method

best_variance_method = replicate_arch_variance_exactly()

# 6. 使用最佳方差方法重新计算似然
if best_variance_method:
    method_name, init_var, best_sigma2 = best_variance_method
    best_sigma = np.sqrt(best_sigma2)
    
    print(f"\n🏆 使用最佳方差方法 ({method_name}) 重新计算似然:")
    
    # 精确arch风格的GED似然
    def ged_likelihood_precise(residuals, sigma, nu):
        lam = np.sqrt(gamma(1.0/nu) / gamma(3.0/nu))
        log_likelihood = 0.0
        
        for i in range(len(residuals)):
            eps = residuals[i]
            sig = sigma[i]
            z = eps / sig
            abs_z_lam_pow_nu = np.power(np.abs(z / lam), nu)
            ll_i = (np.log(nu) - np.log(2.0) - np.log(lam) - math.lgamma(1.0/nu) 
                    - np.log(sig) - 0.5 * abs_z_lam_pow_nu)
            log_likelihood += ll_i
        
        return log_likelihood
    
    precise_ll = ged_likelihood_precise(manual_residuals, best_sigma, nu)
    print(f"精确似然值: {precise_ll:.6f}")
    print(f"与arch库差异: {abs(precise_ll - arch_result.loglikelihood):.6f}")

# 7. 检查arch库是否使用了不同的GED参数化
print(f"\n🔬 检查GED参数化差异:")

# 尝试arch库可能使用的不同GED公式
def test_ged_formulations(residuals, sigma, nu):
    """测试不同的GED公式"""
    results = []
    
    # 公式1: 标准GED (我们当前使用的)
    lam = np.sqrt(gamma(1.0/nu) / gamma(3.0/nu))
    ll1 = 0.0
    for i in range(len(residuals)):
        eps, sig = residuals[i], sigma[i]
        z = eps / sig
        abs_z_lam_pow_nu = np.power(np.abs(z / lam), nu)
        ll1 += np.log(nu) - np.log(2.0) - np.log(lam) - math.lgamma(1.0/nu) - np.log(sig) - 0.5 * abs_z_lam_pow_nu
    results.append(("标准GED", ll1))
    
    # 公式2: 不同的标准化
    ll2 = 0.0
    for i in range(len(residuals)):
        eps, sig = residuals[i], sigma[i]
        z = eps / (sig * lam)
        abs_z_pow_nu = np.power(np.abs(z), nu)
        ll2 += np.log(nu) - np.log(2.0) - np.log(lam) - math.lgamma(1.0/nu) - np.log(sig) - 0.5 * abs_z_pow_nu
    results.append(("不同标准化", ll2))
    
    # 公式3: 另一种参数化
    c = np.sqrt(gamma(3.0/nu) / gamma(1.0/nu))
    ll3 = 0.0
    for i in range(len(residuals)):
        eps, sig = residuals[i], sigma[i]
        z = eps / (sig * c)
        abs_z_pow_nu = np.power(np.abs(z), nu)
        ll3 += np.log(nu) - np.log(2.0) - np.log(c) - math.lgamma(1.0/nu) - np.log(sig) - 0.5 * abs_z_pow_nu
    results.append(("c参数化", ll3))
    
    return results

ged_results = test_ged_formulations(manual_residuals, arch_cond_vol, nu)
print(f"不同GED公式的似然值:")
for name, ll in ged_results:
    diff = abs(ll - arch_result.loglikelihood)
    print(f"{name}: {ll:.6f} (差异: {diff:.6f})")

# 8. 最终分析
print(f"\n📋 深度分析结论:")
best_ged = min(ged_results, key=lambda x: abs(x[1] - arch_result.loglikelihood))
print(f"最接近arch库的GED实现: {best_ged[0]}")
print(f"似然值: {best_ged[1]:.6f}")
print(f"差异: {abs(best_ged[1] - arch_result.loglikelihood):.6f}")

if abs(best_ged[1] - arch_result.loglikelihood) < 1.0:
    print(f"✅ 找到了接近的实现！")
else:
    print(f"❌ 仍需进一步调试")
    print(f"可能的问题:")
    print(f"1. arch库使用了不同的数值计算方法")
    print(f"2. 存在我们未发现的实现细节")
    print(f"3. arch库可能有特殊的数值优化") 