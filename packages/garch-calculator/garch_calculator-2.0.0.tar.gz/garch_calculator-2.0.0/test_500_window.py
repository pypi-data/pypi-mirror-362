import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model

# 读取数据
print("📊 读取 brett.csv 文件...")
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values

# 专门测试500窗口大小
window_size = 500
print(f"\n🔍 专门测试窗口大小: {window_size}")

converged_count = 0
total_count = 0
failed_cases = []

# 测试前100个500窗口
for i in range(window_size, min(window_size + 100, len(returns))):
    window_data = returns[i-window_size:i]
    
    try:
        calc = gc.GarchCalculator(history_size=window_size + 10)
        calc.add_returns(window_data.tolist())
        result = calc.estimate_parameters()
        
        total_count += 1
        if result.converged:
            converged_count += 1
            print(f"✅ 索引 {i}: 收敛, 迭代={result.iterations}, 似然={result.log_likelihood:.2f}")
        else:
            failed_cases.append(i)
            print(f"❌ 索引 {i}: 未收敛, 迭代={result.iterations}, 似然={result.log_likelihood:.2f}")
            
    except Exception as e:
        print(f"💥 错误 at index {i}: {str(e)}")
        total_count += 1
        failed_cases.append(i)

convergence_rate = converged_count / total_count if total_count > 0 else 0
print(f"\n📊 500窗口收敛率: {convergence_rate:.2%} ({converged_count}/{total_count})")

# 详细分析第一个失败案例
if failed_cases:
    failed_index = failed_cases[0]
    print(f"\n🔍 详细分析失败案例: 索引 {failed_index}")
    window_data = returns[failed_index-window_size:failed_index]
    
    # 数据统计
    print(f"数据统计:")
    print(f"  均值: {np.mean(window_data):.6f}")
    print(f"  标准差: {np.std(window_data):.6f}")
    print(f"  最小值: {np.min(window_data):.6f}")
    print(f"  最大值: {np.max(window_data):.6f}")
    print(f"  数据点数: {len(window_data)}")
    
    # garch_lib详细结果
    calc = gc.GarchCalculator(history_size=window_size + 10)
    calc.add_returns(window_data.tolist())
    garch_result = calc.estimate_parameters()
    
    print(f"\ngarch_lib 详细结果:")
    print(f"  收敛: {garch_result.converged}")
    print(f"  迭代次数: {garch_result.iterations}")
    print(f"  似然值: {garch_result.log_likelihood:.6f}")
    print(f"  AIC: {garch_result.aic:.6f}")
    print(f"  BIC: {garch_result.bic:.6f}")
    print(f"  参数: μ={garch_result.parameters.mu:.6f}, ω={garch_result.parameters.omega:.6f}")
    print(f"        α={garch_result.parameters.alpha:.6f}, β={garch_result.parameters.beta:.6f}, ν={garch_result.parameters.nu:.6f}")
    
    # arch库对比
    try:
        arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
        arch_result = arch_model_obj.fit(disp='off', show_warning=False)
        
        print(f"\narch库 对比结果:")
        print(f"  似然值: {arch_result.loglikelihood:.6f}")
        print(f"  AIC: {arch_result.aic:.6f}")
        print(f"  BIC: {arch_result.bic:.6f}")
        print(f"  参数: ω={arch_result.params['omega']:.6f}, α={arch_result.params['alpha[1]']:.6f}")
        print(f"        β={arch_result.params['beta[1]']:.6f}, ν={arch_result.params['nu']:.6f}")
        
        # 似然值差异
        ll_diff = abs(garch_result.log_likelihood - arch_result.loglikelihood)
        print(f"\n📈 似然值差异: {ll_diff:.6f}")
        if ll_diff < 1.0:
            print("✅ 似然值非常接近，garch_lib结果实际上是合理的！")
        
    except Exception as e:
        print(f"arch库失败: {str(e)}")

# 测试手动设置更好的初始参数是否能提高收敛率
print(f"\n🔧 测试优化的初始参数...")

improved_converged = 0
for i in failed_cases[:10]:  # 测试前10个失败案例
    window_data = returns[i-window_size:i]
    
    calc = gc.GarchCalculator(history_size=window_size + 10)
    calc.add_returns(window_data.tolist())
    
    # 设置基于数据的智能初始参数
    sample_mean = np.mean(window_data)
    sample_var = np.var(window_data)
    
    # 更保守的初始参数
    initial_params = gc.GarchParameters()
    initial_params.mu = sample_mean
    initial_params.omega = max(0.1, sample_var * 0.005)  # 更小的omega
    initial_params.alpha = 0.03  # 很小的alpha
    initial_params.beta = 0.95   # 很大的beta，接近IGARCH
    initial_params.nu = 1.8      # 合理的nu
    
    calc.set_parameters(initial_params)
    result = calc.estimate_parameters()
    
    if result.converged:
        improved_converged += 1
        print(f"✅ 索引 {i}: 优化后收敛! 迭代={result.iterations}, 似然={result.log_likelihood:.2f}")
    else:
        print(f"❌ 索引 {i}: 仍未收敛, 迭代={result.iterations}, 似然={result.log_likelihood:.2f}")

if failed_cases:
    improvement_rate = improved_converged / min(len(failed_cases), 10)
    print(f"\n📊 优化初始参数后的改进率: {improvement_rate:.2%}") 