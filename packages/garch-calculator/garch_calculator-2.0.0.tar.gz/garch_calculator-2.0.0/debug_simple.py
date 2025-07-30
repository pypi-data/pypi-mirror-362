import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values

# 取一个小窗口进行测试
window_data = returns[200:400]  # 200个数据点
print(f"测试数据统计:")
print(f"  数据点数: {len(window_data)}")
print(f"  均值: {np.mean(window_data):.6f}")
print(f"  标准差: {np.std(window_data):.6f}")
print(f"  最小值: {np.min(window_data):.6f}")
print(f"  最大值: {np.max(window_data):.6f}")

print("\n" + "="*60)
print("测试 arch 库:")

# 使用arch库
arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
arch_result = arch_model_obj.fit(disp='off', show_warning=False)
print(f"arch库收敛: {arch_result.convergence_flag}")
print(f"arch库参数:")
print(f"  omega: {arch_result.params['omega']:.6f}")
print(f"  alpha: {arch_result.params['alpha[1]']:.6f}")
print(f"  beta: {arch_result.params['beta[1]']:.6f}")
print(f"  nu: {arch_result.params['nu']:.6f}")
print(f"arch库似然值: {arch_result.loglikelihood:.6f}")

print("\n" + "="*60)
print("测试 garch_lib:")

# 使用garch_lib
calc = gc.GarchCalculator(history_size=len(window_data) + 10)
calc.add_returns(window_data.tolist())

# 尝试估计参数
result = calc.estimate_parameters()
print(f"garch_lib收敛: {result.converged}")
print(f"garch_lib迭代次数: {result.iterations}")
print(f"garch_lib似然值: {result.log_likelihood:.6f}")

if result.converged:
    print(f"garch_lib参数:")
    print(f"  omega: {result.parameters.omega:.6f}")
    print(f"  alpha: {result.parameters.alpha:.6f}")
    print(f"  beta: {result.parameters.beta:.6f}")
    print(f"  nu: {result.parameters.nu:.6f}")
else:
    print("garch_lib未收敛，无法获取有效参数")

print("\n" + "="*60)
print("手动测试似然函数:")

# 使用arch库的参数测试garch_lib的似然函数
arch_params = gc.GarchParameters(
    arch_result.params['omega'],
    arch_result.params['alpha[1]'],
    arch_result.params['beta[1]'],
    arch_result.params['nu']
)

calc.set_parameters(arch_params)
garch_lib_ll = calc.calculate_log_likelihood()
print(f"使用arch参数的garch_lib似然值: {garch_lib_ll:.6f}")
print(f"arch库似然值: {arch_result.loglikelihood:.6f}")
print(f"似然值差异: {abs(garch_lib_ll - arch_result.loglikelihood):.6f}")

if abs(garch_lib_ll - arch_result.loglikelihood) > 1e-3:
    print("⚠️  似然函数计算存在显著差异!")
else:
    print("✅ 似然函数计算基本一致") 