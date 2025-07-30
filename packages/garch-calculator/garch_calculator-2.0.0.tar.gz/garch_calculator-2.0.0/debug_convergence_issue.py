import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import matplotlib.pyplot as plt

print("🔍 调试 garch_lib 收敛问题")
print("=" * 50)

# 1. 读取少量数据进行测试
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values
test_data = returns[0:200]  # 只使用前200个数据点

print(f"测试数据量: {len(test_data)} 个点")
print(f"数据范围: {test_data.min():.6f} 到 {test_data.max():.6f}")
print(f"数据统计: 均值={test_data.mean():.6f}, 标准差={test_data.std():.6f}")

# 2. 测试不同的数据缩放
print("\n🧪 测试不同数据缩放的影响:")
print("-" * 50)

scaling_factors = [1, 10, 100, 1000]
for scale in scaling_factors:
    print(f"\n📊 缩放因子: {scale}")
    
    try:
        # garch_lib 测试
        calc = gc.GarchCalculator(history_size=250)
        scaled_data = test_data * scale
        calc.add_returns(scaled_data.tolist())
        result = calc.estimate_parameters()
        
        print(f"  garch_lib - 收敛: {result.converged}")
        print(f"  参数: omega={result.parameters.omega:.6f}, alpha={result.parameters.alpha:.6f}")
        print(f"        beta={result.parameters.beta:.6f}, nu={result.parameters.nu:.6f}")
        print(f"  似然值: {result.log_likelihood:.6f}")
        
        if result.converged:
            forecast = calc.forecast_volatility(1)
            vol_pred = forecast.volatility / scale
            print(f"  预测波动率: {vol_pred:.6f}")
        
        # arch 库对比
        arch_model_obj = arch_model(scaled_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
        arch_result = arch_model_obj.fit(disp='off', show_warning=False)
        arch_forecast = arch_result.forecast(horizon=1, reindex=False)
        arch_vol = np.sqrt(arch_forecast.variance.values[-1, 0]) / scale
        
        print(f"  arch库预测: {arch_vol:.6f}")
        
    except Exception as e:
        print(f"  错误: {str(e)}")

# 3. 测试更简单的模拟数据
print(f"\n🎲 测试模拟 GARCH 数据:")
print("-" * 50)

# 生成简单的 GARCH(1,1) 模拟数据
np.random.seed(42)
n = 200
true_omega = 0.01
true_alpha = 0.1
true_beta = 0.8
true_nu = 1.5

# 模拟 GARCH(1,1) 过程
returns_sim = np.zeros(n)
sigma2 = np.zeros(n)
sigma2[0] = true_omega / (1 - true_alpha - true_beta)  # 无条件方差

for t in range(1, n):
    sigma2[t] = true_omega + true_alpha * returns_sim[t-1]**2 + true_beta * sigma2[t-1]
    returns_sim[t] = np.sqrt(sigma2[t]) * np.random.standard_t(true_nu * 2)  # 近似 GED

print(f"模拟数据统计: 均值={returns_sim.mean():.6f}, 标准差={returns_sim.std():.6f}")

try:
    # garch_lib 估计
    calc_sim = gc.GarchCalculator(history_size=250)
    calc_sim.add_returns(returns_sim.tolist())
    result_sim = calc_sim.estimate_parameters()
    
    print(f"\n📈 模拟数据结果:")
    print(f"  真实参数: omega={true_omega}, alpha={true_alpha}, beta={true_beta}, nu={true_nu}")
    print(f"  garch_lib - 收敛: {result_sim.converged}")
    print(f"  估计参数: omega={result_sim.parameters.omega:.6f}, alpha={result_sim.parameters.alpha:.6f}")
    print(f"            beta={result_sim.parameters.beta:.6f}, nu={result_sim.parameters.nu:.6f}")
    print(f"  似然值: {result_sim.log_likelihood:.6f}")
    
    # arch 库对比
    arch_model_sim = arch_model(returns_sim, vol='Garch', p=1, q=1, dist='ged', rescale=False)
    arch_result_sim = arch_model_sim.fit(disp='off', show_warning=False)
    
    print(f"\n  arch库估计:")
    print(f"  omega={arch_result_sim.params['omega']:.6f}, alpha={arch_result_sim.params['alpha[1]']:.6f}")
    print(f"  beta={arch_result_sim.params['beta[1]']:.6f}, nu={arch_result_sim.params['nu']:.6f}")
    
except Exception as e:
    print(f"  模拟数据测试错误: {str(e)}")

print(f"\n✅ 调试完成!") 