import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
from scipy.special import gamma
import math
import inspect

# 读取数据
df = pd.read_csv('brett.csv')
returns = df['c_scaled'].values[:300]

print("🔍 检查arch库的实际源码和GED实现")
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

# 2. 检查arch库的内部对象
print(f"\n📊 arch库内部对象分析:")
print(f"arch_model_obj类型: {type(arch_model_obj)}")
print(f"arch_result类型: {type(arch_result)}")

# 检查分布对象
distribution = arch_model_obj.distribution
print(f"分布对象类型: {type(distribution)}")
print(f"分布对象: {distribution}")

# 3. 尝试访问分布的似然函数
try:
    # 获取分布的似然函数
    if hasattr(distribution, 'loglikelihood'):
        print(f"\n🔧 分布有loglikelihood方法")
        
        # 获取残差和条件方差
        residuals = arch_result.resid
        sigma2 = arch_result.conditional_volatility ** 2
        
        # 调用分布的似然函数
        dist_ll = distribution.loglikelihood(arch_result.params, residuals, sigma2, individual=False)
        print(f"分布似然值: {dist_ll:.6f}")
        
        # 获取个体似然
        individual_ll = distribution.loglikelihood(arch_result.params, residuals, sigma2, individual=True)
        print(f"个体似然总和: {individual_ll.sum():.6f}")
        print(f"前5个个体似然: {individual_ll[:5]}")
        
except Exception as e:
    print(f"访问分布似然函数失败: {e}")

# 4. 检查分布的源码
try:
    print(f"\n📝 分布源码检查:")
    source = inspect.getsource(distribution.loglikelihood)
    print("分布loglikelihood方法源码:")
    print(source[:500] + "..." if len(source) > 500 else source)
except Exception as e:
    print(f"获取源码失败: {e}")

# 5. 手动调用分布的参数
try:
    print(f"\n🔬 分布参数分析:")
    
    # 获取分布参数
    dist_params = distribution.bounds(residuals)
    print(f"分布参数边界: {dist_params}")
    
    # 检查分布的参数数量
    num_params = distribution.num_params
    print(f"分布参数数量: {num_params}")
    
    # 获取分布的参数名称
    if hasattr(distribution, 'parameter_names'):
        param_names = distribution.parameter_names()
        print(f"分布参数名称: {param_names}")
    
except Exception as e:
    print(f"分析分布参数失败: {e}")

# 6. 尝试直接计算GED似然
try:
    print(f"\n🧮 直接计算GED似然:")
    
    # 获取GED参数
    ged_nu = arch_result.params['nu']
    residuals = arch_result.resid
    sigma = arch_result.conditional_volatility
    
    # 计算标准化因子
    lam = np.sqrt(gamma(1.0/ged_nu) / gamma(3.0/ged_nu))
    print(f"λ = {lam:.10f}")
    
    # 手动计算似然
    log_likelihood = 0.0
    for i in range(len(residuals)):
        eps = residuals[i]
        sig = sigma[i]
        
        # 标准化残差
        z = eps / sig
        
        # 计算 |z/λ|^ν
        abs_z_lam_pow_nu = np.power(np.abs(z / lam), ged_nu)
        
        # 对数似然贡献
        ll_i = (np.log(ged_nu) - np.log(2.0) - np.log(lam) - math.lgamma(1.0/ged_nu) 
                - np.log(sig) - 0.5 * abs_z_lam_pow_nu)
        
        log_likelihood += ll_i
    
    print(f"手动计算似然值: {log_likelihood:.6f}")
    print(f"与arch库差异: {abs(log_likelihood - arch_result.loglikelihood):.6f}")
    
except Exception as e:
    print(f"手动计算失败: {e}")

# 7. 检查arch库的版本和模块信息
try:
    import arch
    print(f"\n📦 arch库信息:")
    print(f"arch版本: {arch.__version__}")
    
    # 检查GED分布的模块位置
    from arch.univariate.distribution import GeneralizedError
    print(f"GED分布类: {GeneralizedError}")
    print(f"GED分布模块: {GeneralizedError.__module__}")
    
    # 创建GED分布实例
    ged_dist = GeneralizedError()
    print(f"GED分布实例: {ged_dist}")
    
    # 检查GED分布的方法
    methods = [method for method in dir(ged_dist) if not method.startswith('_')]
    print(f"GED分布方法: {methods}")
    
except Exception as e:
    print(f"检查arch库信息失败: {e}")

# 8. 尝试获取GED分布的源码
try:
    from arch.univariate.distribution import GeneralizedError
    ged_source = inspect.getsource(GeneralizedError.loglikelihood)
    print(f"\n📜 GED分布loglikelihood源码:")
    print(ged_source)
    
except Exception as e:
    print(f"获取GED源码失败: {e}")

# 9. 检查arch库的条件方差计算
try:
    print(f"\n🔧 arch库条件方差计算:")
    
    # 获取波动率模型
    volatility_model = arch_model_obj.volatility
    print(f"波动率模型类型: {type(volatility_model)}")
    
    # 检查波动率模型的方法
    vol_methods = [method for method in dir(volatility_model) if not method.startswith('_')]
    print(f"波动率模型方法: {vol_methods[:10]}...")  # 只显示前10个
    
    # 尝试获取条件方差计算的源码
    if hasattr(volatility_model, 'variance'):
        var_source = inspect.getsource(volatility_model.variance)
        print(f"条件方差计算源码片段:")
        print(var_source[:300] + "..." if len(var_source) > 300 else var_source)
    
except Exception as e:
    print(f"检查条件方差计算失败: {e}")

print(f"\n📋 总结:")
print(f"通过检查arch库的内部实现，我们可以找到似然函数差异的根本原因")
print(f"下一步将基于发现的信息修复garch_lib的实现") 