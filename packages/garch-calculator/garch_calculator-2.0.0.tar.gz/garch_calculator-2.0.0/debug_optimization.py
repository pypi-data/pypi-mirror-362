import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import time
import numpy as np

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]

print("🔍 深度诊断优化算法问题")
print("=" * 80)

# 1. arch库参数估计
arch_model_obj = arch_model(returns, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)

mu = arch_result.params['mu']
omega = arch_result.params['omega']
alpha = arch_result.params['alpha[1]']
beta = arch_result.params['beta[1]']
nu = arch_result.params['nu']

print(f"arch库最优参数: μ={mu:.6f}, ω={omega:.6f}, α={alpha:.6f}, β={beta:.6f}, ν={nu:.6f}")
print(f"arch库似然值: {arch_result.loglikelihood:.6f}")

# 2. 测试garch_lib在arch库最优参数处的似然值
calc = gc.GarchCalculator(history_size=500)
calc.add_returns(returns.tolist())

# 设置arch库的最优参数
arch_optimal_params = gc.GarchParameters(mu, omega, alpha, beta, nu)
calc.set_parameters(arch_optimal_params)

garch_lib_ll_at_optimal = calc.calculate_log_likelihood()
print(f"\ngarch_lib在arch库最优参数处的似然值: {garch_lib_ll_at_optimal:.6f}")
print(f"与arch库的差异: {abs(garch_lib_ll_at_optimal - arch_result.loglikelihood):.6f}")

# 3. 测试梯度计算
print(f"\n🔧 梯度计算测试:")

# 创建一个简单的数值梯度函数
def numerical_gradient(params, epsilon=1e-6):
    grad = []
    
    # mu梯度
    params_plus = gc.GarchParameters(params.mu + epsilon, params.omega, params.alpha, params.beta, params.nu)
    params_minus = gc.GarchParameters(params.mu - epsilon, params.omega, params.alpha, params.beta, params.nu)
    ll_plus = calc.calculate_log_likelihood(params_plus)
    ll_minus = calc.calculate_log_likelihood(params_minus)
    if np.isfinite(ll_plus) and np.isfinite(ll_minus):
        grad_mu = (ll_plus - ll_minus) / (2 * epsilon)
    else:
        grad_mu = 0.0
    grad.append(grad_mu)
    
    # omega梯度
    params_plus = gc.GarchParameters(params.mu, params.omega + epsilon, params.alpha, params.beta, params.nu)
    params_minus = gc.GarchParameters(params.mu, params.omega - epsilon, params.alpha, params.beta, params.nu)
    ll_plus = calc.calculate_log_likelihood(params_plus)
    ll_minus = calc.calculate_log_likelihood(params_minus)
    if np.isfinite(ll_plus) and np.isfinite(ll_minus):
        grad_omega = (ll_plus - ll_minus) / (2 * epsilon)
    else:
        grad_omega = 0.0
    grad.append(grad_omega)
    
    # alpha梯度
    params_plus = gc.GarchParameters(params.mu, params.omega, params.alpha + epsilon, params.beta, params.nu)
    params_minus = gc.GarchParameters(params.mu, params.omega, params.alpha - epsilon, params.beta, params.nu)
    ll_plus = calc.calculate_log_likelihood(params_plus)
    ll_minus = calc.calculate_log_likelihood(params_minus)
    if np.isfinite(ll_plus) and np.isfinite(ll_minus):
        grad_alpha = (ll_plus - ll_minus) / (2 * epsilon)
    else:
        grad_alpha = 0.0
    grad.append(grad_alpha)
    
    # beta梯度
    params_plus = gc.GarchParameters(params.mu, params.omega, params.alpha, params.beta + epsilon, params.nu)
    params_minus = gc.GarchParameters(params.mu, params.omega, params.alpha, params.beta - epsilon, params.nu)
    ll_plus = calc.calculate_log_likelihood(params_plus)
    ll_minus = calc.calculate_log_likelihood(params_minus)
    if np.isfinite(ll_plus) and np.isfinite(ll_minus):
        grad_beta = (ll_plus - ll_minus) / (2 * epsilon)
    else:
        grad_beta = 0.0
    grad.append(grad_beta)
    
    # nu梯度
    params_plus = gc.GarchParameters(params.mu, params.omega, params.alpha, params.beta, params.nu + epsilon)
    params_minus = gc.GarchParameters(params.mu, params.omega, params.alpha, params.beta, params.nu - epsilon)
    ll_plus = calc.calculate_log_likelihood(params_plus)
    ll_minus = calc.calculate_log_likelihood(params_minus)
    if np.isfinite(ll_plus) and np.isfinite(ll_minus):
        grad_nu = (ll_plus - ll_minus) / (2 * epsilon)
    else:
        grad_nu = 0.0
    grad.append(grad_nu)
    
    return grad

# 在更合理的参数处测试梯度
reasonable_params = gc.GarchParameters(0.0, 10.0, 0.1, 0.8, 2.0)
numerical_grad = numerical_gradient(reasonable_params)

print(f"合理参数处的数值梯度:")
print(f"  ∂L/∂μ = {numerical_grad[0]:.6f}")
print(f"  ∂L/∂ω = {numerical_grad[1]:.6f}")
print(f"  ∂L/∂α = {numerical_grad[2]:.6f}")
print(f"  ∂L/∂β = {numerical_grad[3]:.6f}")
print(f"  ∂L/∂ν = {numerical_grad[4]:.6f}")

# 测试在arch库最优参数附近的梯度
near_optimal_params = gc.GarchParameters(mu, omega, alpha, beta, nu)
numerical_grad_optimal = numerical_gradient(near_optimal_params)

print(f"\narch库最优参数处的数值梯度:")
print(f"  ∂L/∂μ = {numerical_grad_optimal[0]:.6f}")
print(f"  ∂L/∂ω = {numerical_grad_optimal[1]:.6f}")
print(f"  ∂L/∂α = {numerical_grad_optimal[2]:.6f}")
print(f"  ∂L/∂β = {numerical_grad_optimal[3]:.6f}")
print(f"  ∂L/∂ν = {numerical_grad_optimal[4]:.6f}")

# 4. 测试参数空间的似然函数形状
print(f"\n📊 似然函数形状分析:")

# 测试omega参数的影响
omega_values = [0.1, 1.0, 5.0, 10.0, 15.0, 20.0, 25.0]
print(f"omega参数扫描 (固定其他参数为初始值):")
for omega_test in omega_values:
    test_params = gc.GarchParameters(0.0, omega_test, 0.1, 0.85, 1.5)
    if test_params.is_valid():
        ll = calc.calculate_log_likelihood(test_params)
        print(f"  ω={omega_test:5.1f}: LL={ll:10.6f}")

# 测试alpha参数的影响
alpha_values = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
print(f"\nalpha参数扫描 (固定其他参数为初始值):")
for alpha_test in alpha_values:
    test_params = gc.GarchParameters(0.0, 0.00001, alpha_test, 0.85, 1.5)
    if test_params.is_valid():
        ll = calc.calculate_log_likelihood(test_params)
        print(f"  α={alpha_test:5.2f}: LL={ll:10.6f}")

# 5. 测试优化算法的第一步
print(f"\n🚀 优化算法第一步测试:")
result = calc.estimate_parameters()
print(f"优化结果:")
print(f"  收敛: {result.converged}")
print(f"  迭代次数: {result.iterations}")
print(f"  最终参数: μ={result.parameters.mu:.6f}, ω={result.parameters.omega:.6f}")
print(f"              α={result.parameters.alpha:.6f}, β={result.parameters.beta:.6f}, ν={result.parameters.nu:.6f}")
print(f"  最终似然值: {result.log_likelihood:.6f}")

# 6. 手动测试一个简单的梯度上升步骤
print(f"\n🔧 手动梯度上升测试:")
current_params = gc.GarchParameters(0.0, 10.0, 0.2, 0.7, 2.0)  # 更合理的初始值
current_ll = calc.calculate_log_likelihood(current_params)
print(f"起始参数: μ={current_params.mu:.6f}, ω={current_params.omega:.6f}, α={current_params.alpha:.6f}, β={current_params.beta:.6f}, ν={current_params.nu:.6f}")
print(f"起始似然值: {current_ll:.6f}")

# 计算梯度
grad = numerical_gradient(current_params, epsilon=1e-4)
print(f"梯度: [{grad[0]:.6f}, {grad[1]:.6f}, {grad[2]:.6f}, {grad[3]:.6f}, {grad[4]:.6f}]")

# 尝试一个小的梯度上升步骤
step_size = 0.001
new_params = gc.GarchParameters(
    current_params.mu + step_size * grad[0],
    max(1e-6, current_params.omega + step_size * grad[1]),
    max(0.0, min(0.99, current_params.alpha + step_size * grad[2])),
    max(0.0, min(0.99, current_params.beta + step_size * grad[3])),
    max(1.01, current_params.nu + step_size * grad[4])
)

# 确保平稳性约束
if new_params.alpha + new_params.beta >= 0.999:
    scale = 0.998 / (new_params.alpha + new_params.beta)
    new_params.alpha *= scale
    new_params.beta *= scale

new_ll = calc.calculate_log_likelihood(new_params)
print(f"梯度步后参数: μ={new_params.mu:.6f}, ω={new_params.omega:.6f}, α={new_params.alpha:.6f}, β={new_params.beta:.6f}, ν={new_params.nu:.6f}")
print(f"梯度步后似然值: {new_ll:.6f}")
print(f"似然值改进: {new_ll - current_ll:.6f}")