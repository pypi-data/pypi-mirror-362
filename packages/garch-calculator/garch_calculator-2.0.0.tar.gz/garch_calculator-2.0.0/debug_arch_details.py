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

print(f"arch库详细信息:")
print(f"  收敛标志: {arch_result.convergence_flag}")
print(f"  似然值: {arch_result.loglikelihood:.6f}")
print(f"  参数:")
for param, value in arch_result.params.items():
    print(f"    {param}: {value:.6f}")

# 获取arch库的条件方差
arch_variance = arch_result.conditional_volatility**2
print(f"\narch库条件方差 (前10个):")
for i in range(min(10, len(arch_variance))):
    print(f"  t={i}: {arch_variance[i]:.6f}")

# 获取arch库的残差
arch_residuals = arch_result.resid
print(f"\narch库残差 (前10个):")
for i in range(min(10, len(arch_residuals))):
    print(f"  t={i}: {arch_residuals[i]:.6f}")

# 检查arch库的初始化
print(f"\narch库初始化检查:")
print(f"  数据均值: {np.mean(window_data):.6f}")
print(f"  数据方差: {np.var(window_data):.6f}")
print(f"  数据方差(ddof=1): {np.var(window_data, ddof=1):.6f}")
print(f"  arch库第一个条件方差: {arch_variance[0]:.6f}")

# 尝试不同的初始化方法重新计算似然
omega = arch_result.params['omega']
alpha = arch_result.params['alpha[1]']
beta = arch_result.params['beta[1]']
nu = arch_result.params['nu']

def calculate_likelihood_with_init(returns, omega, alpha, beta, nu, init_method='sample_var'):
    """使用不同初始化方法计算似然"""
    n = len(returns)
    sigma2 = np.zeros(n)
    
    # 不同的初始化方法
    if init_method == 'sample_var':
        sigma2[0] = np.var(returns)
    elif init_method == 'sample_var_ddof1':
        sigma2[0] = np.var(returns, ddof=1)
    elif init_method == 'unconditional':
        sigma2[0] = omega / (1.0 - alpha - beta) if (alpha + beta) < 1 else np.var(returns)
    elif init_method == 'arch_first':
        sigma2[0] = arch_variance[0]  # 直接使用arch库的第一个值
    elif init_method == 'backcast':
        # 使用回溯方法 (arch库的默认方法)
        sigma2[0] = np.var(returns)
        # 进行几次迭代来稳定初始值
        for _ in range(10):
            sigma2_new = omega + alpha * returns[0]**2 + beta * sigma2[0]
            if abs(sigma2_new - sigma2[0]) < 1e-8:
                break
            sigma2[0] = sigma2_new
    
    # 计算条件方差序列
    for t in range(1, n):
        sigma2[t] = omega + alpha * returns[t-1]**2 + beta * sigma2[t-1]
    
    # 计算GED似然
    log_gamma_1_nu = sp.loggamma(1.0/nu)
    log_gamma_3_nu = sp.loggamma(3.0/nu)
    lambda_ged = np.sqrt(np.exp(log_gamma_1_nu - log_gamma_3_nu))
    log_constant = np.log(nu) - (1.0 + 1.0/nu) * np.log(2.0) - np.log(lambda_ged) - log_gamma_1_nu
    
    log_likelihood = 0.0
    for t in range(n):
        if sigma2[t] <= 0:
            return -np.inf, sigma2
        
        z = returns[t] / (lambda_ged * np.sqrt(sigma2[t]))
        abs_z_pow_nu = np.abs(z)**nu
        ll_t = log_constant - 0.5 * np.log(sigma2[t]) - 0.5 * abs_z_pow_nu
        log_likelihood += ll_t
    
    return log_likelihood, sigma2

# 测试不同初始化方法
init_methods = ['sample_var', 'sample_var_ddof1', 'unconditional', 'arch_first', 'backcast']
print(f"\n不同初始化方法的似然值:")
for method in init_methods:
    try:
        ll, sigma2 = calculate_likelihood_with_init(window_data, omega, alpha, beta, nu, method)
        print(f"  {method:15}: {ll:.6f} (初始方差: {sigma2[0]:.6f})")
    except Exception as e:
        print(f"  {method:15}: 错误 - {e}")

print(f"\narch库似然值: {arch_result.loglikelihood:.6f}")

# 检查arch库是否使用了不同的GED参数化
print(f"\nGED参数化检查:")
print(f"标准参数化 lambda: {np.sqrt(np.exp(sp.loggamma(1.0/nu) - sp.loggamma(3.0/nu))):.6f}")

# 尝试arch库可能使用的其他参数化
# 有些实现使用 c = 2^(1/nu) * sqrt(Gamma(3/nu)/Gamma(1/nu))
c_alt = 2**(1/nu) * np.sqrt(np.exp(sp.loggamma(3.0/nu) - sp.loggamma(1.0/nu)))
print(f"替代参数化 c: {c_alt:.6f}")

# 检查是否arch库使用了不同的似然公式
def calculate_arch_exact_likelihood(returns, omega, alpha, beta, nu):
    """尝试完全匹配arch库的似然计算"""
    n = len(returns)
    
    # 使用arch库的条件方差
    sigma2 = arch_variance.copy()
    
    # 使用arch库的GED实现
    # arch库可能使用不同的归一化
    log_likelihood = 0.0
    
    for t in range(n):
        if sigma2[t] <= 0:
            return -np.inf
        
        # 尝试不同的标准化方式
        # 方式1: 标准GED
        log_gamma_1_nu = sp.loggamma(1.0/nu)
        log_gamma_3_nu = sp.loggamma(3.0/nu)
        lambda_ged = np.sqrt(np.exp(log_gamma_1_nu - log_gamma_3_nu))
        
        z = returns[t] / (lambda_ged * np.sqrt(sigma2[t]))
        abs_z_pow_nu = np.abs(z)**nu
        
        log_constant = np.log(nu) - (1.0 + 1.0/nu) * np.log(2.0) - np.log(lambda_ged) - log_gamma_1_nu
        ll_t = log_constant - 0.5 * np.log(sigma2[t]) - 0.5 * abs_z_pow_nu
        
        log_likelihood += ll_t
    
    return log_likelihood

exact_ll = calculate_arch_exact_likelihood(window_data, omega, alpha, beta, nu)
print(f"\n使用arch条件方差的似然值: {exact_ll:.6f}")
print(f"与arch库差异: {abs(exact_ll - arch_result.loglikelihood):.6f}")

# 检查是否有常数项差异
print(f"\n常数项检查:")
print(f"数据点数: {len(window_data)}")
print(f"可能的常数差异: {(exact_ll - arch_result.loglikelihood) / len(window_data):.6f} per observation") 