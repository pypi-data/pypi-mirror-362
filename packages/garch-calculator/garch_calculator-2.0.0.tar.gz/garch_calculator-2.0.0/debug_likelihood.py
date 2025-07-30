import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import scipy.special as sp

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values

# 取一个小窗口进行测试
window_data = returns[200:300]  # 100个数据点，更小的窗口便于调试
print(f"测试数据统计:")
print(f"  数据点数: {len(window_data)}")
print(f"  均值: {np.mean(window_data):.6f}")
print(f"  标准差: {np.std(window_data):.6f}")

# 使用arch库获取参考参数
arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

print(f"\narch库参数:")
omega = arch_result.params['omega']
alpha = arch_result.params['alpha[1]']
beta = arch_result.params['beta[1]']
nu = arch_result.params['nu']
print(f"  omega: {omega:.6f}")
print(f"  alpha: {alpha:.6f}")
print(f"  beta: {beta:.6f}")
print(f"  nu: {nu:.6f}")
print(f"arch库似然值: {arch_result.loglikelihood:.6f}")

# 手动计算arch库风格的似然函数
def calculate_arch_style_likelihood(returns, omega, alpha, beta, nu):
    """按照arch库的方式计算似然函数"""
    n = len(returns)
    
    # 计算条件方差序列
    sigma2 = np.zeros(n)
    sigma2[0] = np.var(returns)  # 初始方差
    
    for t in range(1, n):
        sigma2[t] = omega + alpha * returns[t-1]**2 + beta * sigma2[t-1]
    
    # 计算GED似然
    # arch库的GED参数化：
    # lambda = sqrt(Gamma(1/nu) / Gamma(3/nu))
    log_gamma_1_nu = sp.loggamma(1.0/nu)
    log_gamma_3_nu = sp.loggamma(3.0/nu)
    lambda_ged = np.sqrt(np.exp(log_gamma_1_nu - log_gamma_3_nu))
    
    # 归一化常数的对数
    log_constant = np.log(nu) - (1.0 + 1.0/nu) * np.log(2.0) - np.log(lambda_ged) - log_gamma_1_nu
    
    log_likelihood = 0.0
    for t in range(n):
        if sigma2[t] <= 0:
            return -np.inf
        
        # 标准化残差
        z = returns[t] / (lambda_ged * np.sqrt(sigma2[t]))
        
        # |z|^nu
        abs_z_pow_nu = np.abs(z)**nu
        
        # 对数似然贡献
        ll_t = log_constant - 0.5 * np.log(sigma2[t]) - 0.5 * abs_z_pow_nu
        log_likelihood += ll_t
    
    return log_likelihood

# 计算手动实现的似然值
manual_ll = calculate_arch_style_likelihood(window_data, omega, alpha, beta, nu)
print(f"手动计算似然值: {manual_ll:.6f}")
print(f"与arch库差异: {abs(manual_ll - arch_result.loglikelihood):.6f}")

# 测试garch_lib的似然计算
calc = gc.GarchCalculator(history_size=len(window_data) + 10)
calc.add_returns(window_data.tolist())

arch_params = gc.GarchParameters(omega, alpha, beta, nu)
calc.set_parameters(arch_params)
garch_lib_ll = calc.calculate_log_likelihood()

print(f"\ngarch_lib似然值: {garch_lib_ll:.6f}")
print(f"与arch库差异: {abs(garch_lib_ll - arch_result.loglikelihood):.6f}")
print(f"与手动计算差异: {abs(garch_lib_ll - manual_ll):.6f}")

# 检查条件方差计算
print(f"\n条件方差检查:")
print(f"初始方差 (样本方差): {np.var(window_data):.6f}")

# 手动计算前几个条件方差
sigma2_manual = np.zeros(len(window_data))
sigma2_manual[0] = np.var(window_data)
for t in range(1, min(5, len(window_data))):
    sigma2_manual[t] = omega + alpha * window_data[t-1]**2 + beta * sigma2_manual[t-1]
    print(f"t={t}: sigma2={sigma2_manual[t]:.6f}, return={window_data[t-1]:.6f}")

# 检查GED参数
print(f"\nGED参数检查:")
log_gamma_1_nu = sp.loggamma(1.0/nu)
log_gamma_3_nu = sp.loggamma(3.0/nu)
lambda_ged = np.sqrt(np.exp(log_gamma_1_nu - log_gamma_3_nu))
print(f"nu: {nu:.6f}")
print(f"lambda: {lambda_ged:.6f}")
print(f"log_gamma(1/nu): {log_gamma_1_nu:.6f}")
print(f"log_gamma(3/nu): {log_gamma_3_nu:.6f}")

# 检查单个时间点的似然贡献
t = 1
sigma_t = np.sqrt(sigma2_manual[t])
z = window_data[t] / (lambda_ged * sigma_t)
abs_z_pow_nu = np.abs(z)**nu
log_constant = np.log(nu) - (1.0 + 1.0/nu) * np.log(2.0) - np.log(lambda_ged) - log_gamma_1_nu
ll_contribution = log_constant - 0.5 * np.log(sigma2_manual[t]) - 0.5 * abs_z_pow_nu

print(f"\n单点似然检查 (t={t}):")
print(f"return: {window_data[t]:.6f}")
print(f"sigma2: {sigma2_manual[t]:.6f}")
print(f"sigma: {sigma_t:.6f}")
print(f"z: {z:.6f}")
print(f"|z|^nu: {abs_z_pow_nu:.6f}")
print(f"log_constant: {log_constant:.6f}")
print(f"似然贡献: {ll_contribution:.6f}") 