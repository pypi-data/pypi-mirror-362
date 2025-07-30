#!/usr/bin/env python3
"""
测试GARCH似然函数的脚本
验证似然函数计算是否正常
"""

import numpy as np
import garch_lib as gc

def test_likelihood_function():
    print("🔍 测试GARCH似然函数...")
    
    # 创建简单的测试数据
    np.random.seed(42)  # 确保可重现
    n = 100
    true_returns = np.random.normal(0, 0.02, n)
    
    calc = gc.GarchCalculator()
    calc.add_returns(true_returns.tolist())
    
    # 测试1: 默认参数的似然值
    print(f"\n=== 测试1: 默认参数的似然值 ===")
    default_params = calc.get_parameters()
    print(f"默认参数: ω={default_params.omega:.6f}, α={default_params.alpha:.6f}, β={default_params.beta:.6f}, ν={default_params.nu:.6f}")
    
    default_ll = calc.calculate_log_likelihood()
    print(f"默认参数似然值: {default_ll:.6f}")
    
    # 测试2: 不同参数的似然值
    print(f"\n=== 测试2: 不同参数的似然值 ===")
    
    test_params_list = [
        (0.00001, 0.05, 0.9, 2.0),   # 高持续性
        (0.0001, 0.1, 0.8, 1.5),     # 中等持续性
        (0.001, 0.2, 0.7, 1.2),      # 低持续性
        (0.0005, 0.15, 0.75, 1.8),   # 平衡参数
    ]
    
    best_ll = -np.inf
    best_params = None
    
    for omega, alpha, beta, nu in test_params_list:
        params = gc.GarchParameters(omega, alpha, beta, nu)
        
        # 检查参数有效性
        if not params.is_valid():
            print(f"参数 (ω={omega}, α={alpha}, β={beta}, ν={nu}) 无效，跳过")
            continue
        
        ll = calc.calculate_log_likelihood(params)
        print(f"参数 (ω={omega:.6f}, α={alpha:.3f}, β={beta:.3f}, ν={nu:.1f}): 似然值 = {ll:.6f}")
        
        if ll > best_ll:
            best_ll = ll
            best_params = (omega, alpha, beta, nu)
    
    print(f"\n最佳参数: ω={best_params[0]:.6f}, α={best_params[1]:.3f}, β={best_params[2]:.3f}, ν={best_params[3]:.1f}")
    print(f"最佳似然值: {best_ll:.6f}")
    
    # 测试3: 手动设置最佳参数并检查
    print(f"\n=== 测试3: 设置最佳参数 ===")
    best_garch_params = gc.GarchParameters(*best_params)
    calc.set_parameters(best_garch_params)
    
    print(f"设置最佳参数后:")
    print(f"  当前波动率: {calc.get_current_volatility():.6f}")
    print(f"  当前方差: {calc.get_current_variance():.6f}")
    
    # 测试4: 尝试手动优化
    print(f"\n=== 测试4: 简单网格搜索 ===")
    
    # 简单的网格搜索
    omega_range = [0.00001, 0.0001, 0.0005, 0.001]
    alpha_range = [0.05, 0.1, 0.15, 0.2]
    beta_range = [0.7, 0.75, 0.8, 0.85, 0.9]
    nu_range = [1.2, 1.5, 1.8, 2.0]
    
    best_grid_ll = -np.inf
    best_grid_params = None
    total_tests = 0
    valid_tests = 0
    
    for omega in omega_range:
        for alpha in alpha_range:
            for beta in beta_range:
                for nu in nu_range:
                    total_tests += 1
                    
                    # 检查平稳性约束
                    if alpha + beta >= 0.9999:
                        continue
                    
                    params = gc.GarchParameters(omega, alpha, beta, nu)
                    if not params.is_valid():
                        continue
                    
                    valid_tests += 1
                    ll = calc.calculate_log_likelihood(params)
                    
                    if ll > best_grid_ll:
                        best_grid_ll = ll
                        best_grid_params = (omega, alpha, beta, nu)
    
    print(f"网格搜索结果:")
    print(f"  总测试: {total_tests}")
    print(f"  有效测试: {valid_tests}")
    print(f"  最佳参数: ω={best_grid_params[0]:.6f}, α={best_grid_params[1]:.3f}, β={best_grid_params[2]:.3f}, ν={best_grid_params[3]:.1f}")
    print(f"  最佳似然值: {best_grid_ll:.6f}")
    print(f"  默认似然值: {default_ll:.6f}")
    print(f"  改进: {best_grid_ll - default_ll:.6f}")
    
    # 测试5: 验证梯度信息
    print(f"\n=== 测试5: 条件方差计算测试 ===")
    
    # 获取收益率数据
    returns = calc.get_log_returns()
    print(f"收益率数据:")
    print(f"  数量: {len(returns)}")
    print(f"  均值: {np.mean(returns):.6f}")
    print(f"  标准差: {np.std(returns):.6f}")
    print(f"  最小值: {np.min(returns):.6f}")
    print(f"  最大值: {np.max(returns):.6f}")
    
    # 计算不同参数下的条件方差
    test_param = gc.GarchParameters(*best_grid_params)
    conditional_vars = calc.calculate_conditional_variances(returns, test_param)
    
    print(f"\n条件方差序列:")
    print(f"  数量: {len(conditional_vars)}")
    print(f"  均值: {np.mean(conditional_vars):.6f}")
    print(f"  标准差: {np.std(conditional_vars):.6f}")
    print(f"  最小值: {np.min(conditional_vars):.6f}")
    print(f"  最大值: {np.max(conditional_vars):.6f}")
    
    # 测试6: GED似然函数测试
    print(f"\n=== 测试6: GED似然函数测试 ===")
    
    sigma_t = [np.sqrt(v) for v in conditional_vars]
    ged_ll = calc.calculate_ged_log_likelihood(returns, sigma_t, test_param.nu)
    
    print(f"GED似然值: {ged_ll:.6f}")
    print(f"平均每点似然: {ged_ll/len(returns):.6f}")
    
    # 和标准正态分布比较
    normal_ll = -0.5 * len(returns) * np.log(2 * np.pi) - 0.5 * sum(r**2 for r in returns)
    print(f"标准正态似然: {normal_ll:.6f}")
    print(f"GED vs 正态改进: {ged_ll - normal_ll:.6f}")

if __name__ == "__main__":
    test_likelihood_function() 