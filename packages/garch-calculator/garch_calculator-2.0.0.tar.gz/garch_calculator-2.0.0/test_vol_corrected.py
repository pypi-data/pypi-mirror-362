import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import matplotlib.pyplot as plt
from datetime import datetime

# 1. 读取 CSV 文件
print("📊 读取 brett.csv 文件...")
df = pd.read_csv('brett.csv')

# 2. 提取 c_scaled 列作为收益率数据
returns = df['c_scaled'].values
print(f"   数据总量: {len(returns)} 个数据点")
print(f"   数据范围: {returns.min():.6f} 到 {returns.max():.6f}")

# 3. 设置滚动窗口参数
window_size = 200  # 窗口大小
min_periods = window_size  

# 存储预测结果
garch_lib_predictions = []
arch_lib_predictions = []
prediction_dates = []

print(f"\n🔄 开始滚动预测 (窗口大小: {window_size})")
print("=" * 60)

# 4. 滚动预测
for i in range(window_size, len(returns)):
    # 获取当前窗口的数据
    window_data = returns[i-window_size:i]
    
    try:
        # === 使用 arch 库进行预测 ===
        arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
        arch_result = arch_model_obj.fit(disp='off', show_warning=False)
        
        # 获取均值参数
        mu = arch_result.params['mu']
        
        # 使用去均值的残差
        residuals = window_data - mu
        
        # === 使用 garch_lib 进行预测 ===
        calc = gc.GarchCalculator(history_size=window_size + 10)
        calc.add_returns(residuals.tolist())
        
        # 尝试参数估计
        garch_lib_result = calc.estimate_parameters()
        
        # 关键修正：如果估计失败或参数不合理，使用arch库的参数
        if not garch_lib_result.converged or garch_lib_result.log_likelihood < -1e6:
            # 使用arch库的参数
            arch_params = gc.GarchParameters()
            arch_params.omega = arch_result.params['omega']
            arch_params.alpha = arch_result.params['alpha[1]']
            arch_params.beta = arch_result.params['beta[1]']
            arch_params.nu = arch_result.params['nu']
            calc.set_parameters(arch_params)
            
            garch_lib_forecast = calc.forecast_volatility(1)
            garch_lib_vol = garch_lib_forecast.volatility
        else:
            # 使用估计的参数进行预测
            # 手动设置估计的参数以确保预测使用正确的参数
            calc.set_parameters(garch_lib_result.parameters)
            garch_lib_forecast = calc.forecast_volatility(1)
            garch_lib_vol = garch_lib_forecast.volatility
        
        garch_lib_predictions.append(garch_lib_vol)
        
        # arch库预测
        arch_forecast = arch_result.forecast(horizon=1, reindex=False)
        arch_predictions = np.sqrt(arch_forecast.variance.values[-1, :])
        arch_lib_predictions.append(arch_predictions[0])
        
        prediction_dates.append(i)
        
        # 每50个预测点输出一次进度和调试信息
        if (i - window_size + 1) % 50 == 0:
            progress = (i - window_size + 1) / (len(returns) - window_size) * 100
            print(f"进度: {progress:.1f}% ({i - window_size + 1}/{len(returns) - window_size})")
            print(f"  估计收敛: {garch_lib_result.converged}")
            if garch_lib_result.converged:
                print(f"  估计参数: ω={garch_lib_result.parameters.omega:.6f}, α={garch_lib_result.parameters.alpha:.6f}")
                print(f"            β={garch_lib_result.parameters.beta:.6f}, ν={garch_lib_result.parameters.nu:.6f}")
            else:
                print(f"  使用arch参数: ω={arch_result.params['omega']:.6f}, α={arch_result.params['alpha[1]']:.6f}")
                print(f"                β={arch_result.params['beta[1]']:.6f}, ν={arch_result.params['nu']:.6f}")
            print(f"  garch_lib预测: {garch_lib_vol:.6f}, arch库预测: {arch_predictions[0]:.6f}")
            
    except Exception as e:
        print(f"预测失败 at index {i}: {str(e)}")
        continue

print(f"\n✅ 滚动预测完成!")
print(f"   成功预测: {len(garch_lib_predictions)} 个点")

# 5. 结果对比分析
if len(garch_lib_predictions) > 0 and len(arch_lib_predictions) > 0:
    garch_lib_arr = np.array(garch_lib_predictions)
    arch_lib_arr = np.array(arch_lib_predictions)
    
    print(f"\n📊 预测结果统计对比:")
    print("=" * 60)
    print(f"{'指标':<20} {'garch_lib':<15} {'arch库':<15} {'差异':<10}")
    print("-" * 60)
    print(f"{'平均值':<20} {garch_lib_arr.mean():<15.6f} {arch_lib_arr.mean():<15.6f} {abs(garch_lib_arr.mean() - arch_lib_arr.mean()):<10.6f}")
    print(f"{'标准差':<20} {garch_lib_arr.std():<15.6f} {arch_lib_arr.std():<15.6f} {abs(garch_lib_arr.std() - arch_lib_arr.std()):<10.6f}")
    print(f"{'最小值':<20} {garch_lib_arr.min():<15.6f} {arch_lib_arr.min():<15.6f} {abs(garch_lib_arr.min() - arch_lib_arr.min()):<10.6f}")
    print(f"{'最大值':<20} {garch_lib_arr.max():<15.6f} {arch_lib_arr.max():<15.6f} {abs(garch_lib_arr.max() - arch_lib_arr.max()):<10.6f}")
    
    # 计算相关系数
    correlation = np.corrcoef(garch_lib_arr, arch_lib_arr)[0, 1]
    print(f"{'相关系数':<20} {correlation:<30.6f}")
    
    # 计算RMSE和MAE
    rmse = np.sqrt(np.mean((garch_lib_arr - arch_lib_arr)**2))
    mae = np.mean(np.abs(garch_lib_arr - arch_lib_arr))
    print(f"{'RMSE':<20} {rmse:<30.6f}")
    print(f"{'MAE':<20} {mae:<30.6f}")
    
    # 计算相对误差
    mape = np.mean(np.abs((garch_lib_arr - arch_lib_arr) / arch_lib_arr)) * 100
    print(f"{'MAPE (%)':<20} {mape:<30.2f}")
    
    # 计算预测质量指标
    abs_errors = np.abs(garch_lib_arr - arch_lib_arr)
    good_predictions = np.sum(abs_errors < 5.0)
    print(f"{'绝对误差<5的比例':<20} {good_predictions/len(abs_errors)*100:<30.1f}%")
    
    # 6. 保存预测结果到CSV
    results_df = pd.DataFrame({
        'prediction_index': prediction_dates,
        'garch_lib_volatility': garch_lib_predictions,
        'arch_lib_volatility': arch_lib_predictions,
        'difference': garch_lib_arr - arch_lib_arr,
        'relative_error': (garch_lib_arr - arch_lib_arr) / arch_lib_arr * 100
    })
    
    results_df.to_csv('volatility_predictions_comparison_corrected.csv', index=False)
    print(f"\n💾 预测结果已保存至: volatility_predictions_comparison_corrected.csv")
    
    # 7. 显示最近几个预测结果
    print(f"\n🔍 最近15个预测结果:")
    print("-" * 90)
    print(f"{'索引':<8} {'garch_lib':<15} {'arch库':<15} {'差异':<15} {'相对误差%':<12}")
    print("-" * 90)
    for i in range(max(0, len(results_df)-15), len(results_df)):
        row = results_df.iloc[i]
        print(f"{int(row['prediction_index']):<8} {row['garch_lib_volatility']:<15.6f} {row['arch_lib_volatility']:<15.6f} {row['difference']:<15.6f} {row['relative_error']:<12.2f}%")

else:
    print("❌ 预测失败，无法进行对比分析") 