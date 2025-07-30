import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import scipy.special as sp

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values
window_data = returns[200:300]  # 100个数据点

# 使用arch库
arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

print(f"arch库参数:")
mu = arch_result.params['mu']
omega = arch_result.params['omega']
alpha = arch_result.params['alpha[1]']
beta = arch_result.params['beta[1]']
nu = arch_result.params['nu']

print(f"  mu (均值): {mu:.6f}")
print(f"  omega: {omega:.6f}")
print(f"  alpha: {alpha:.6f}")
print(f"  beta: {beta:.6f}")
print(f"  nu: {nu:.6f}")
print(f"arch库似然值: {arch_result.loglikelihood:.6f}")

# 计算去均值后的残差
residuals = window_data - mu
print(f"\n残差统计:")
print(f"  原始数据均值: {np.mean(window_data):.6f}")
print(f"  残差均值: {np.mean(residuals):.6f}")
print(f"  残差方差: {np.var(residuals):.6f}")

# 使用残差重新计算似然函数
def calculate_likelihood_with_mean(returns, mu, omega, alpha, beta, nu):
    """使用均值参数计算似然函数"""
    residuals = returns - mu
    n = len(residuals)
    
    # 计算条件方差序列
    sigma2 = np.zeros(n)
    sigma2[0] = np.var(residuals)  # 使用残差的方差作为初始值
    
    for t in range(1, n):
        sigma2[t] = omega + alpha * residuals[t-1]**2 + beta * sigma2[t-1]
    
    # 计算GED似然
    log_gamma_1_nu = sp.loggamma(1.0/nu)
    log_gamma_3_nu = sp.loggamma(3.0/nu)
    lambda_ged = np.sqrt(np.exp(log_gamma_1_nu - log_gamma_3_nu))
    log_constant = np.log(nu) - (1.0 + 1.0/nu) * np.log(2.0) - np.log(lambda_ged) - log_gamma_1_nu
    
    log_likelihood = 0.0
    for t in range(n):
        if sigma2[t] <= 0:
            return -np.inf, sigma2
        
        z = residuals[t] / (lambda_ged * np.sqrt(sigma2[t]))
        abs_z_pow_nu = np.abs(z)**nu
        ll_t = log_constant - 0.5 * np.log(sigma2[t]) - 0.5 * abs_z_pow_nu
        log_likelihood += ll_t
    
    return log_likelihood, sigma2

# 计算包含均值的似然值
manual_ll_with_mean, sigma2_manual = calculate_likelihood_with_mean(window_data, mu, omega, alpha, beta, nu)
print(f"\n包含均值的手动计算似然值: {manual_ll_with_mean:.6f}")
print(f"与arch库差异: {abs(manual_ll_with_mean - arch_result.loglikelihood):.6f}")

# 比较条件方差
arch_variance = arch_result.conditional_volatility**2
print(f"\n条件方差比较 (前5个):")
for i in range(5):
    print(f"  t={i}: 手动={sigma2_manual[i]:.6f}, arch={arch_variance[i]:.6f}, 差异={abs(sigma2_manual[i] - arch_variance[i]):.6f}")

# 现在测试garch_lib是否支持均值参数
print(f"\n测试garch_lib (使用去均值的数据):")
calc = gc.GarchCalculator(history_size=len(residuals) + 10)
calc.add_returns(residuals.tolist())

# 使用arch库的GARCH参数 (不包括mu)
arch_params = gc.GarchParameters(omega, alpha, beta, nu)
calc.set_parameters(arch_params)
garch_lib_ll = calc.calculate_log_likelihood()

print(f"garch_lib似然值 (去均值数据): {garch_lib_ll:.6f}")
print(f"与arch库差异: {abs(garch_lib_ll - arch_result.loglikelihood):.6f}")
print(f"与手动计算差异: {abs(garch_lib_ll - manual_ll_with_mean):.6f}")

# 尝试估计参数
result = calc.estimate_parameters()
print(f"\ngarch_lib参数估计:")
print(f"  收敛: {result.converged}")
print(f"  迭代次数: {result.iterations}")
print(f"  似然值: {result.log_likelihood:.6f}")

if result.converged:
    print(f"  估计参数:")
    print(f"    omega: {result.parameters.omega:.6f}")
    print(f"    alpha: {result.parameters.alpha:.6f}")
    print(f"    beta: {result.parameters.beta:.6f}")
    print(f"    nu: {result.parameters.nu:.6f}")
    
    print(f"\n与arch库参数比较:")
    print(f"    omega差异: {abs(result.parameters.omega - omega):.6f}")
    print(f"    alpha差异: {abs(result.parameters.alpha - alpha):.6f}")
    print(f"    beta差异: {abs(result.parameters.beta - beta):.6f}")
    print(f"    nu差异: {abs(result.parameters.nu - nu):.6f}")

# 检查初始化方法的影响
print(f"\n初始化方法影响:")
print(f"  残差方差: {np.var(residuals):.6f}")
print(f"  无条件方差: {omega / (1.0 - alpha - beta):.6f}")
print(f"  arch库第一个方差: {arch_variance[0]:.6f}")

# 尝试使用arch库的初始方差
def calculate_likelihood_arch_init(returns, mu, omega, alpha, beta, nu):
    """使用arch库的初始化方法"""
    residuals = returns - mu
    n = len(residuals)
    
    # 使用arch库的条件方差
    sigma2 = arch_variance.copy()
    
    # 计算GED似然
    log_gamma_1_nu = sp.loggamma(1.0/nu)
    log_gamma_3_nu = sp.loggamma(3.0/nu)
    lambda_ged = np.sqrt(np.exp(log_gamma_1_nu - log_gamma_3_nu))
    log_constant = np.log(nu) - (1.0 + 1.0/nu) * np.log(2.0) - np.log(lambda_ged) - log_gamma_1_nu
    
    log_likelihood = 0.0
    for t in range(n):
        if sigma2[t] <= 0:
            return -np.inf
        
        z = residuals[t] / (lambda_ged * np.sqrt(sigma2[t]))
        abs_z_pow_nu = np.abs(z)**nu
        ll_t = log_constant - 0.5 * np.log(sigma2[t]) - 0.5 * abs_z_pow_nu
        log_likelihood += ll_t
    
    return log_likelihood

arch_init_ll = calculate_likelihood_arch_init(window_data, mu, omega, alpha, beta, nu)
print(f"\n使用arch初始化的似然值: {arch_init_ll:.6f}")
print(f"与arch库差异: {abs(arch_init_ll - arch_result.loglikelihood):.6f}") 