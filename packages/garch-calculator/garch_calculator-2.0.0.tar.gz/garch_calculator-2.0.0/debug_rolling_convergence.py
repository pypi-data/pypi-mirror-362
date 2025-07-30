import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import matplotlib.pyplot as plt

# 读取数据
print("📊 读取 brett.csv 文件...")
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values

# 测试不同窗口大小的收敛情况
window_sizes = [100, 150, 200, 250, 300]
convergence_rates = []

for window_size in window_sizes:
    print(f"\n🔍 测试窗口大小: {window_size}")
    
    converged_count = 0
    total_count = 0
    
    # 测试前50个窗口
    for i in range(window_size, min(window_size + 50, len(returns))):
        window_data = returns[i-window_size:i]
        
        try:
            calc = gc.GarchCalculator(history_size=window_size + 10)
            calc.add_returns(window_data.tolist())
            result = calc.estimate_parameters()
            
            total_count += 1
            if result.converged:
                converged_count += 1
                
        except Exception as e:
            print(f"错误 at index {i}: {str(e)}")
            total_count += 1
    
    convergence_rate = converged_count / total_count if total_count > 0 else 0
    convergence_rates.append(convergence_rate)
    print(f"   收敛率: {convergence_rate:.2%} ({converged_count}/{total_count})")

print(f"\n📈 不同窗口大小的收敛率:")
for i, window_size in enumerate(window_sizes):
    print(f"   窗口大小 {window_size}: {convergence_rates[i]:.2%}")

# 详细分析一个失败的案例
print(f"\n🔍 详细分析一个失败案例...")
window_size = 200
failed_index = None

for i in range(window_size, window_size + 100):
    if i >= len(returns):
        break
        
    window_data = returns[i-window_size:i]
    
    try:
        calc = gc.GarchCalculator(history_size=window_size + 10)
        calc.add_returns(window_data.tolist())
        result = calc.estimate_parameters()
        
        if not result.converged:
            failed_index = i
            break
            
    except Exception as e:
        print(f"异常 at index {i}: {str(e)}")
        failed_index = i
        break

if failed_index is not None:
    print(f"分析失败案例: 索引 {failed_index}")
    window_data = returns[failed_index-window_size:failed_index]
    
    # 数据统计
    print(f"数据统计:")
    print(f"  均值: {np.mean(window_data):.6f}")
    print(f"  标准差: {np.std(window_data):.6f}")
    print(f"  最小值: {np.min(window_data):.6f}")
    print(f"  最大值: {np.max(window_data):.6f}")
    print(f"  数据点数: {len(window_data)}")
    
    # 尝试garch_lib估计
    calc = gc.GarchCalculator(history_size=window_size + 10)
    calc.add_returns(window_data.tolist())
    garch_result = calc.estimate_parameters()
    
    print(f"\ngarch_lib 结果:")
    print(f"  收敛: {garch_result.converged}")
    print(f"  迭代次数: {garch_result.iterations}")
    print(f"  似然值: {garch_result.log_likelihood:.6f}")
    print(f"  参数: μ={garch_result.parameters.mu:.6f}, ω={garch_result.parameters.omega:.6f}")
    print(f"        α={garch_result.parameters.alpha:.6f}, β={garch_result.parameters.beta:.6f}, ν={garch_result.parameters.nu:.6f}")
    
    # 尝试arch库估计作为对比
    try:
        arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
        arch_result = arch_model_obj.fit(disp='off', show_warning=False)
        
        print(f"\narch库 结果:")
        print(f"  似然值: {arch_result.loglikelihood:.6f}")
        print(f"  参数: ω={arch_result.params['omega']:.6f}, α={arch_result.params['alpha[1]']:.6f}")
        print(f"        β={arch_result.params['beta[1]']:.6f}, ν={arch_result.params['nu']:.6f}")
        
    except Exception as e:
        print(f"arch库也失败了: {str(e)}")

# 测试更宽松的收敛条件
print(f"\n🔧 测试更宽松的收敛条件...")

# 创建一个修改版本的计算器，看看是否能提高收敛率
window_size = 200
test_indices = range(window_size, window_size + 20)

for i in test_indices:
    if i >= len(returns):
        break
        
    window_data = returns[i-window_size:i]
    
    calc = gc.GarchCalculator(history_size=window_size + 10)
    calc.add_returns(window_data.tolist())
    
    # 尝试手动设置更好的初始参数
    sample_var = np.var(window_data)
    initial_params = gc.GarchParameters()
    initial_params.mu = np.mean(window_data)
    initial_params.omega = sample_var * 0.01  # 更保守的omega
    initial_params.alpha = 0.05  # 更小的alpha
    initial_params.beta = 0.9   # 更大的beta
    initial_params.nu = 2.0     # 标准的nu
    
    calc.set_parameters(initial_params)
    result = calc.estimate_parameters()
    
    print(f"索引 {i}: 收敛={result.converged}, 迭代={result.iterations}, 似然={result.log_likelihood:.2f}") 