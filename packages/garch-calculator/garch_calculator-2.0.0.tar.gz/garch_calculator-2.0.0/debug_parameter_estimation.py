import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]  # 使用前300个数据点

print("🔍 参数估计调试分析")
print("=" * 60)

# 1. 使用arch库进行参数估计
print("\n📊 arch库参数估计:")
arch_model_obj = arch_model(returns, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

print(f"arch库参数:")
print(f"  mu: {arch_result.params['mu']:.6f}")
print(f"  omega: {arch_result.params['omega']:.6f}")
print(f"  alpha: {arch_result.params['alpha[1]']:.6f}")
print(f"  beta: {arch_result.params['beta[1]']:.6f}")
print(f"  nu: {arch_result.params['nu']:.6f}")
print(f"  对数似然: {arch_result.loglikelihood:.4f}")

# 2. 分析arch库的残差处理
mu = arch_result.params['mu']
residuals_arch = returns - mu
print(f"\n📈 arch库数据处理:")
print(f"  原始收益率均值: {returns.mean():.6f}")
print(f"  估计的mu: {mu:.6f}")
print(f"  去均值后残差均值: {residuals_arch.mean():.6f}")
print(f"  残差方差: {residuals_arch.var():.6f}")

# 3. 使用garch_lib进行参数估计（原始数据）
print(f"\n🔧 garch_lib参数估计（原始数据）:")
calc1 = gc.GarchCalculator(history_size=350)
calc1.add_returns(returns.tolist())
result1 = calc1.estimate_parameters()

print(f"garch_lib结果（原始数据）:")
print(f"  收敛: {result1.converged}")
print(f"  omega: {result1.parameters.omega:.6f}")
print(f"  alpha: {result1.parameters.alpha:.6f}")
print(f"  beta: {result1.parameters.beta:.6f}")
print(f"  nu: {result1.parameters.nu:.6f}")
print(f"  对数似然: {result1.log_likelihood:.4f}")

# 4. 使用garch_lib进行参数估计（去均值残差）
print(f"\n🔧 garch_lib参数估计（去均值残差）:")
calc2 = gc.GarchCalculator(history_size=350)
calc2.add_returns(residuals_arch.tolist())
result2 = calc2.estimate_parameters()

print(f"garch_lib结果（去均值残差）:")
print(f"  收敛: {result2.converged}")
print(f"  omega: {result2.parameters.omega:.6f}")
print(f"  alpha: {result2.parameters.alpha:.6f}")
print(f"  beta: {result2.parameters.beta:.6f}")
print(f"  nu: {result2.parameters.nu:.6f}")
print(f"  对数似然: {result2.log_likelihood:.4f}")

# 5. 手动设置arch库的参数到garch_lib
print(f"\n🎯 手动设置arch库参数到garch_lib:")
calc3 = gc.GarchCalculator(history_size=350)
calc3.add_returns(residuals_arch.tolist())

# 设置arch库的参数
arch_params = gc.GarchParameters()
arch_params.omega = arch_result.params['omega']
arch_params.alpha = arch_result.params['alpha[1]']
arch_params.beta = arch_result.params['beta[1]']
arch_params.nu = arch_result.params['nu']

calc3.set_parameters(arch_params)

# 计算似然值
manual_ll = calc3.calculate_log_likelihood()
print(f"手动设置arch参数后的似然值: {manual_ll:.4f}")
print(f"与arch库似然值差异: {abs(manual_ll - arch_result.loglikelihood):.6f}")

# 6. 分析似然函数计算
print(f"\n📊 似然函数分析:")

# 计算arch库的条件方差
arch_cond_vol = arch_result.conditional_volatility
arch_cond_var = arch_cond_vol ** 2

print(f"arch库条件方差统计:")
print(f"  均值: {arch_cond_var.mean():.6f}")
print(f"  最小值: {arch_cond_var.min():.6f}")
print(f"  最大值: {arch_cond_var.max():.6f}")
print(f"  最后值: {arch_cond_var[-1]:.6f}")

# 计算garch_lib的条件方差
def calculate_garch_variances(residuals, omega, alpha, beta):
    """手动计算GARCH条件方差"""
    n = len(residuals)
    sigma2 = np.zeros(n)
    
    # 初始方差（无条件方差）
    sigma2[0] = omega / (1 - alpha - beta)
    
    # GARCH递推
    for t in range(1, n):
        sigma2[t] = omega + alpha * residuals[t-1]**2 + beta * sigma2[t-1]
    
    return sigma2

garch_lib_var = calculate_garch_variances(residuals_arch, 
                                         arch_params.omega, 
                                         arch_params.alpha, 
                                         arch_params.beta)

print(f"\ngarch_lib条件方差统计:")
print(f"  均值: {garch_lib_var.mean():.6f}")
print(f"  最小值: {garch_lib_var.min():.6f}")
print(f"  最大值: {garch_lib_var.max():.6f}")
print(f"  最后值: {garch_lib_var[-1]:.6f}")

# 7. 比较条件方差序列
var_diff = np.abs(garch_lib_var - arch_cond_var)
print(f"\n条件方差差异:")
print(f"  平均绝对差异: {var_diff.mean():.8f}")
print(f"  最大差异: {var_diff.max():.8f}")
print(f"  相关系数: {np.corrcoef(garch_lib_var, arch_cond_var)[0,1]:.8f}")

# 8. 分析GED密度函数
print(f"\n📈 GED密度函数分析:")

def ged_log_likelihood_manual(residuals, sigma, nu):
    """手动计算GED对数似然"""
    from scipy.special import gamma
    import math
    
    # GED参数化
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

manual_ll_calc = ged_log_likelihood_manual(residuals_arch, 
                                          np.sqrt(garch_lib_var), 
                                          arch_params.nu)

print(f"手动计算的GED似然值: {manual_ll_calc:.4f}")
print(f"arch库似然值: {arch_result.loglikelihood:.4f}")
print(f"garch_lib似然值: {manual_ll:.4f}")
print(f"手动计算与arch库差异: {abs(manual_ll_calc - arch_result.loglikelihood):.6f}")
print(f"garch_lib与arch库差异: {abs(manual_ll - arch_result.loglikelihood):.6f}")

# 9. 检查初始参数的似然值
print(f"\n🎯 初始参数似然值检查:")
initial_params = [
    (5.0, 0.1, 0.8, 2.0),
    (15.0, 0.2, 0.6, 3.0),
    (1.0, 0.15, 0.75, 1.5),
    (arch_params.omega, arch_params.alpha, arch_params.beta, arch_params.nu)
]

for i, (omega, alpha, beta, nu) in enumerate(initial_params):
    test_calc = gc.GarchCalculator(history_size=350)
    test_calc.add_returns(residuals_arch.tolist())
    
    test_params = gc.GarchParameters()
    test_params.omega = omega
    test_params.alpha = alpha
    test_params.beta = beta
    test_params.nu = nu
    
    test_calc.set_parameters(test_params)
    test_ll = test_calc.calculate_log_likelihood()
    
    print(f"  参数组{i+1}: ω={omega:.1f}, α={alpha:.2f}, β={beta:.2f}, ν={nu:.1f} -> LL={test_ll:.4f}")

print(f"\n💡 分析结论:")
print(f"1. arch库和garch_lib的条件方差计算是否一致？")
print(f"2. GED似然函数计算是否有差异？")
print(f"3. 优化算法是否能找到正确的参数？") 