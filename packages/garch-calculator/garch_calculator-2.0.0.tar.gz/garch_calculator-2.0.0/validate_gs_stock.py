#!/usr/bin/env python3
"""
高盛(GS)股票数据GARCH模型验证脚本
使用yfinance获取真实股票数据，比较garch_lib和Python arch库的表现
"""

import numpy as np
import pandas as pd
import time
import warnings
import sys
import os
import yfinance as yf
from datetime import datetime, timedelta
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

warnings.filterwarnings('ignore')
sys.path.append('.')

try:
    from arch import arch_model
    HAS_ARCH = True
    print("✓ Successfully imported arch library")
except ImportError:
    HAS_ARCH = False
    print("❌ Failed to import arch library")

try:
    import garch_calculator as gc
    HAS_GARCH_LIB = True
    print("✓ Successfully imported garch_calculator")
except ImportError:
    HAS_GARCH_LIB = False
    print("❌ Failed to import garch_calculator")

def download_gs_data(period="5y", interval="1d"):
    """下载高盛股票数据"""
    print(f"📊 下载高盛(GS)股票数据...")
    print(f"   期间: {period}, 间隔: {interval}")
    
    try:
        # 创建股票对象
        gs = yf.Ticker("GS")
        
        # 下载历史数据
        data = gs.history(period=period, interval=interval)
        
        if data.empty:
            print("❌ 未能获取到数据")
            return None
        
        print(f"✓ 成功获取数据，时间范围: {data.index[0]} 到 {data.index[-1]}")
        print(f"✓ 数据点数: {len(data)}")
        print(f"✓ 价格范围: ${data['Close'].min():.2f} - ${data['Close'].max():.2f}")
        
        return data
    
    except Exception as e:
        print(f"❌ 下载数据失败: {e}")
        return None

def prepare_returns_data(stock_data, return_type="log"):
    """准备收益率数据"""
    print(f"\n📈 准备收益率数据 (类型: {return_type})")
    
    # 使用收盘价
    prices = stock_data['Close'].dropna()
    
    if return_type == "log":
        # 对数收益率
        returns = np.log(prices / prices.shift(1)).dropna()
    else:
        # 简单收益率
        returns = (prices / prices.shift(1) - 1).dropna()
    
    # 去除极端异常值（超过5个标准差）
    mean_return = returns.mean()
    std_return = returns.std()
    returns = returns[np.abs(returns - mean_return) <= 5 * std_return]
    
    # 中心化处理（去除均值）
    returns = returns - returns.mean()
    
    print(f"✓ 收益率统计:")
    print(f"   数据点数: {len(returns)}")
    print(f"   均值: {returns.mean():.8f}")
    print(f"   标准差: {returns.std():.6f}")
    print(f"   偏度: {returns.skew():.4f}")
    print(f"   峰度: {returns.kurtosis():.4f}")
    print(f"   最小值: {returns.min():.6f}")
    print(f"   最大值: {returns.max():.6f}")
    
    return returns.values

def test_arch_lib(returns, test_ratio=0.2):
    """测试Python arch库"""
    if not HAS_ARCH:
        print("\n❌ 跳过arch库测试 - 库未安装")
        return None
        
    print("\n" + "="*60)
    print("🐍 Python arch库测试")
    print("="*60)
    
    start_time = time.time()
    
    try:
        # 分割数据
        split_point = int(len(returns) * (1 - test_ratio))
        train_returns = returns[:split_point]
        test_returns = returns[split_point:]
        
        print(f"训练数据: {len(train_returns)} 点")
        print(f"测试数据: {len(test_returns)} 点")
        
        # 创建并拟合GARCH(1,1)-GED模型
        print("\n🔧 拟合GARCH(1,1)-GED模型...")
        model = arch_model(train_returns, vol='GARCH', p=1, q=1, dist='ged', rescale=False)
        fitted_model = model.fit(disp='off', show_warning=False)
        fit_time = time.time() - start_time
        
        # 获取参数
        params = fitted_model.params
        
        print(f"✓ 模型拟合完成 (耗时: {fit_time:.4f}秒)")
        print(f"✓ 收敛状态: {fitted_model.convergence_flag == 0}")
        
        # 样本内波动率预测
        start_vol_time = time.time()
        insample_volatility = fitted_model.conditional_volatility
        
        # 样本外预测
        forecast_horizon = len(test_returns)
        try:
            forecast = fitted_model.forecast(horizon=forecast_horizon, start=split_point)
            if forecast.variance.values.shape[0] > 0:
                forecast_volatility = np.sqrt(forecast.variance.values[-1, :])
            else:
                # 备用方案
                last_vol = insample_volatility[-1] if len(insample_volatility) > 0 else np.std(train_returns)
                forecast_volatility = np.full(forecast_horizon, last_vol)
        except Exception as e:
            print(f"⚠️  预测失败，使用备用方法: {e}")
            last_vol = insample_volatility[-1] if len(insample_volatility) > 0 else np.std(train_returns)
            forecast_volatility = np.full(forecast_horizon, last_vol)
        
        vol_prediction_time = time.time() - start_vol_time
        
        # 计算实际波动率（rolling std）
        window_size = 10
        actual_volatility = []
        for i in range(len(test_returns)):
            if i < window_size:
                actual_vol = np.std(test_returns[:i+1]) if i > 0 else np.std(train_returns[-window_size:])
            else:
                actual_vol = np.std(test_returns[i-window_size:i])
            actual_volatility.append(actual_vol)
        actual_volatility = np.array(actual_volatility)
        
        result = {
            'library': 'arch',
            'omega': params['omega'],
            'alpha': params['alpha[1]'],
            'beta': params['beta[1]'],
            'nu': params['nu'],
            'log_likelihood': fitted_model.loglikelihood,
            'aic': fitted_model.aic,
            'bic': fitted_model.bic,
            'fit_time': fit_time,
            'vol_prediction_time': vol_prediction_time,
            'converged': fitted_model.convergence_flag == 0,
            'insample_volatility': insample_volatility,
            'forecast_volatility': forecast_volatility,
            'actual_volatility': actual_volatility,
            'train_size': len(train_returns),
            'test_size': len(test_returns)
        }
        
        # 计算预测精度
        if len(forecast_volatility) == len(actual_volatility):
            result['forecast_mse'] = mean_squared_error(actual_volatility, forecast_volatility)
            result['forecast_mae'] = mean_absolute_error(actual_volatility, forecast_volatility)
            result['forecast_rmse'] = np.sqrt(result['forecast_mse'])
        
        print(f"✓ 参数估计:")
        print(f"   ω (omega): {result['omega']:.8f}")
        print(f"   α (alpha): {result['alpha']:.6f}")
        print(f"   β (beta):  {result['beta']:.6f}")
        print(f"   ν (nu):    {result['nu']:.6f}")
        print(f"✓ 对数似然: {result['log_likelihood']:.6f}")
        print(f"✓ AIC: {result['aic']:.6f}")
        print(f"✓ BIC: {result['bic']:.6f}")
        if 'forecast_rmse' in result:
            print(f"✓ 波动率预测RMSE: {result['forecast_rmse']:.6f}")
        
        return result
        
    except Exception as e:
        print(f"❌ arch库测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_garch_lib(returns, test_ratio=0.2):
    """测试garch_lib实现"""
    if not HAS_GARCH_LIB:
        print("\n❌ 跳过garch_lib测试 - 库未安装")
        return None
        
    print("\n" + "="*60)
    print("⚡ garch_lib测试")
    print("="*60)
    
    start_time = time.time()
    
    try:
        # 分割数据
        split_point = int(len(returns) * (1 - test_ratio))
        train_returns = returns[:split_point]
        test_returns = returns[split_point:]
        
        print(f"训练数据: {len(train_returns)} 点")
        print(f"测试数据: {len(test_returns)} 点")
        
        # 创建计算器
        min_samples = min(50, len(train_returns) // 3)
        calc = gc.GarchCalculator(history_size=len(train_returns)+100, min_samples=min_samples)
        print(f"GarchCalculator初始化: history_size={len(train_returns)+100}, min_samples={min_samples}")
        
        # 将收益率转换为价格序列
        base_price = 100.0
        train_prices = np.zeros(len(train_returns) + 1)
        train_prices[0] = base_price
        
        # 数值稳定性处理
        returns_std = np.std(train_returns)
        if returns_std > 1.0:
            scale_factor = 0.5 / returns_std
        elif returns_std < 0.001:
            scale_factor = 0.01 / returns_std
        else:
            scale_factor = 1.0
        
        scaled_returns = train_returns * scale_factor
        
        # 生成价格序列
        for i in range(len(train_returns)):
            clamped_return = np.clip(scaled_returns[i], -0.49, 2.0)
            new_price = train_prices[i] * (1 + clamped_return)
            
            if new_price <= 0 or not np.isfinite(new_price):
                new_price = train_prices[i] * (1 + np.sign(clamped_return) * 0.001)
            
            train_prices[i+1] = new_price
        
        print(f"缩放因子: {scale_factor:.6f}")
        print(f"价格序列范围: [{np.min(train_prices):.6f}, {np.max(train_prices):.6f}]")
        
        # 添加训练数据并估计参数
        print("\n🔧 拟合GARCH(1,1)-GED模型...")
        calc.add_price_points(train_prices.tolist())
        print(f"数据点数量: {calc.get_data_size()}, 足够数据: {calc.has_enough_data()}")
        
        result_obj = calc.estimate_parameters()
        fit_time = time.time() - start_time
        
        print(f"✓ 模型拟合完成 (耗时: {fit_time:.4f}秒)")
        print(f"✓ 收敛状态: {result_obj.converged}")
        print(f"✓ 迭代次数: {result_obj.iterations}")
        
        if not result_obj.converged:
            print("⚠️  模型未完全收敛，但继续使用估计参数")
        
        params = result_obj.parameters
        
        # 样本内波动率预测
        start_vol_time = time.time()
        try:
            variance_series = calc.get_variance_series()
            if len(variance_series) > 0:
                insample_volatility = np.sqrt(variance_series)
            else:
                current_vol = calc.get_current_volatility()
                insample_volatility = np.full(len(train_prices), current_vol)
        except:
            current_vol = calc.get_current_volatility()
            insample_volatility = np.full(len(train_prices), current_vol)
        
        # 样本外预测
        forecast_volatility = []
        test_prices = np.zeros(len(test_returns) + 1)
        test_prices[0] = train_prices[-1]
        scaled_test_returns = test_returns * scale_factor
        
        for i in range(len(test_returns)):
            try:
                forecast_obj = calc.forecast_volatility(1)
                if forecast_obj.volatility > 0 and np.isfinite(forecast_obj.volatility):
                    forecast_volatility.append(forecast_obj.volatility)
                else:
                    current_vol = calc.get_current_volatility()
                    forecast_volatility.append(current_vol)
                    
                test_prices[i+1] = test_prices[i] * (1 + scaled_test_returns[i])
                if test_prices[i+1] <= 0:
                    test_prices[i+1] = test_prices[i] * 0.999
                calc.add_price_point(test_prices[i+1])
                calc.update_model()
                
            except Exception as e:
                print(f"⚠️  预测步骤 {i+1} 出错: {e}")
                try:
                    current_vol = calc.get_current_volatility()
                    forecast_volatility.append(current_vol)
                except:
                    forecast_volatility.append(np.std(scaled_returns))
                break
            
        forecast_volatility = np.array(forecast_volatility)
        vol_prediction_time = time.time() - start_vol_time
        
        # 计算实际波动率
        window_size = 10
        actual_volatility = []
        for i in range(len(test_returns)):
            if i < window_size:
                actual_vol = np.std(test_returns[:i+1]) if i > 0 else np.std(train_returns[-window_size:])
            else:
                actual_vol = np.std(test_returns[i-window_size:i])
            actual_volatility.append(actual_vol)
        actual_volatility = np.array(actual_volatility)
        
        result = {
            'library': 'garch_lib',
            'omega': params.omega,
            'alpha': params.alpha,
            'beta': params.beta,
            'nu': params.nu,
            'log_likelihood': result_obj.log_likelihood,
            'aic': result_obj.aic,
            'bic': result_obj.bic,
            'fit_time': fit_time,
            'vol_prediction_time': vol_prediction_time,
            'converged': result_obj.converged,
            'iterations': result_obj.iterations,
            'insample_volatility': insample_volatility,
            'forecast_volatility': forecast_volatility,
            'actual_volatility': actual_volatility,
            'train_size': len(train_returns),
            'test_size': len(test_returns)
        }
        
        # 计算预测精度
        if len(forecast_volatility) == len(actual_volatility):
            result['forecast_mse'] = mean_squared_error(actual_volatility, forecast_volatility)
            result['forecast_mae'] = mean_absolute_error(actual_volatility, forecast_volatility)
            result['forecast_rmse'] = np.sqrt(result['forecast_mse'])
        elif len(forecast_volatility) > 0 and len(actual_volatility) > 0:
            min_len = min(len(forecast_volatility), len(actual_volatility))
            print(f"⚠️  预测长度不匹配，使用前{min_len}个点进行评估")
            result['forecast_mse'] = mean_squared_error(actual_volatility[:min_len], forecast_volatility[:min_len])
            result['forecast_mae'] = mean_absolute_error(actual_volatility[:min_len], forecast_volatility[:min_len])
            result['forecast_rmse'] = np.sqrt(result['forecast_mse'])
        
        print(f"✓ 参数估计:")
        print(f"   ω (omega): {result['omega']:.8f}")
        print(f"   α (alpha): {result['alpha']:.6f}")
        print(f"   β (beta):  {result['beta']:.6f}")
        print(f"   ν (nu):    {result['nu']:.6f}")
        print(f"✓ 对数似然: {result['log_likelihood']:.6f}")
        print(f"✓ AIC: {result['aic']:.6f}")
        print(f"✓ BIC: {result['bic']:.6f}")
        if 'forecast_rmse' in result:
            print(f"✓ 波动率预测RMSE: {result['forecast_rmse']:.6f}")
        
        return result
            
    except Exception as e:
        print(f"❌ garch_lib测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_results(arch_result, garch_result):
    """比较两种实现的结果"""
    print("\n" + "="*80)
    print("🔍 结果对比分析")
    print("="*80)
    
    if arch_result is None and garch_result is None:
        print("❌ 两个库都未能成功运行")
        return
    elif arch_result is None:
        print("⚠️  只有garch_lib成功运行")
        return
    elif garch_result is None:
        print("⚠️  只有Python arch库成功运行")
        return
    
    # 参数对比
    print("\n📊 参数对比:")
    print(f"{'参数':<8} {'Python arch':<15} {'garch_lib':<15} {'绝对差异':<12} {'相对差异(%)':<12}")
    print("-" * 72)
    
    params = ['omega', 'alpha', 'beta', 'nu']
    param_errors = []
    
    for param in params:
        arch_val = arch_result[param]
        garch_val = garch_result[param]
        abs_diff = abs(garch_val - arch_val)
        rel_diff = abs_diff / abs(arch_val) * 100 if abs(arch_val) > 0 else 0
        param_errors.append(rel_diff)
        
        print(f"{param:<8} {arch_val:<15.8f} {garch_val:<15.8f} {abs_diff:<12.2e} {rel_diff:<12.2f}")
    
    avg_param_error = np.mean(param_errors)
    print(f"{'平均':<8} {'':<15} {'':<15} {'':<12} {avg_param_error:<12.2f}")
    
    # 模型拟合质量对比
    print(f"\n📈 模型拟合质量:")
    ll_diff = garch_result['log_likelihood'] - arch_result['log_likelihood']
    aic_diff = garch_result['aic'] - arch_result['aic']
    bic_diff = garch_result['bic'] - arch_result['bic']
    
    print(f"{'指标':<15} {'Python arch':<15} {'garch_lib':<15} {'差异':<15}")
    print("-" * 65)
    print(f"{'对数似然':<15} {arch_result['log_likelihood']:<15.6f} {garch_result['log_likelihood']:<15.6f} {ll_diff:<15.6f}")
    print(f"{'AIC':<15} {arch_result['aic']:<15.6f} {garch_result['aic']:<15.6f} {aic_diff:<15.6f}")
    print(f"{'BIC':<15} {arch_result['bic']:<15.6f} {garch_result['bic']:<15.6f} {bic_diff:<15.6f}")
    
    # 性能对比
    print(f"\n⚡ 性能对比:")
    fit_speedup = arch_result['fit_time'] / garch_result['fit_time'] if garch_result['fit_time'] > 0 else 0
    vol_speedup = arch_result['vol_prediction_time'] / garch_result['vol_prediction_time'] if garch_result['vol_prediction_time'] > 0 else 0
    
    print(f"{'指标':<20} {'Python arch':<15} {'garch_lib':<15} {'提升倍数':<15}")
    print("-" * 70)
    print(f"{'拟合时间(秒)':<20} {arch_result['fit_time']:<15.4f} {garch_result['fit_time']:<15.4f} {fit_speedup:<15.2f}")
    print(f"{'预测时间(秒)':<20} {arch_result['vol_prediction_time']:<15.4f} {garch_result['vol_prediction_time']:<15.4f} {vol_speedup:<15.2f}")
    
    # 预测精度对比
    if 'forecast_rmse' in arch_result and 'forecast_rmse' in garch_result:
        print(f"\n🎯 预测精度对比:")
        arch_rmse = arch_result['forecast_rmse']
        garch_rmse = garch_result['forecast_rmse']
        rmse_diff = garch_rmse - arch_rmse
        rmse_rel_diff = rmse_diff / arch_rmse * 100 if arch_rmse > 0 else 0
        
        arch_mae = arch_result['forecast_mae']
        garch_mae = garch_result['forecast_mae']
        mae_diff = garch_mae - arch_mae
        mae_rel_diff = mae_diff / arch_mae * 100 if arch_mae > 0 else 0
        
        print(f"{'指标':<15} {'Python arch':<15} {'garch_lib':<15} {'差异':<15} {'相对差异(%)':<15}")
        print("-" * 80)
        print(f"{'RMSE':<15} {arch_rmse:<15.6f} {garch_rmse:<15.6f} {rmse_diff:<15.6f} {rmse_rel_diff:<15.2f}")
        print(f"{'MAE':<15} {arch_mae:<15.6f} {garch_mae:<15.6f} {mae_diff:<15.6f} {mae_rel_diff:<15.2f}")
        
        if rmse_rel_diff < -1:
            print(f"✅ garch_lib的预测精度更好 (RMSE改善{-rmse_rel_diff:.1f}%)")
        elif rmse_rel_diff > 1:
            print(f"⚠️  arch的预测精度更好 (RMSE差异{rmse_rel_diff:.1f}%)")
        else:
            print(f"🤝 两个库的预测精度相近")
    
    # 收敛性对比
    print(f"\n🔄 收敛性:")
    print(f"Python arch收敛: {'✅' if arch_result['converged'] else '❌'}")
    print(f"garch_lib收敛:   {'✅' if garch_result['converged'] else '❌'}")
    if 'iterations' in garch_result:
        print(f"garch_lib迭代次数: {garch_result['iterations']}")
    
    # 总结
    print(f"\n📋 总结:")
    if avg_param_error < 5:
        print(f"✅ 参数估计高度一致 (平均误差: {avg_param_error:.2f}%)")
    elif avg_param_error < 10:
        print(f"🟡 参数估计基本一致 (平均误差: {avg_param_error:.2f}%)")
    else:
        print(f"⚠️  参数估计存在差异 (平均误差: {avg_param_error:.2f}%)")
    
    print(f"⚡ garch_lib拟合速度提升: {fit_speedup:.1f}倍")
    print(f"⚡ garch_lib预测速度提升: {vol_speedup:.1f}倍")

def save_results(arch_result, garch_result, stock_data):
    """保存结果到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存详细比较结果
    results_summary = {
        'timestamp': timestamp,
        'stock': 'GS',
        'data_period': f"{stock_data.index[0]} to {stock_data.index[-1]}",
        'total_points': len(stock_data),
        'arch_result': arch_result,
        'garch_result': garch_result
    }
    
    # 保存为CSV格式
    if arch_result and garch_result:
        comparison_data = {
            'metric': ['omega', 'alpha', 'beta', 'nu', 'log_likelihood', 'aic', 'bic', 'fit_time', 'vol_prediction_time'],
            'arch_value': [
                arch_result['omega'], arch_result['alpha'], arch_result['beta'], arch_result['nu'],
                arch_result['log_likelihood'], arch_result['aic'], arch_result['bic'],
                arch_result['fit_time'], arch_result['vol_prediction_time']
            ],
            'garch_lib_value': [
                garch_result['omega'], garch_result['alpha'], garch_result['beta'], garch_result['nu'],
                garch_result['log_likelihood'], garch_result['aic'], garch_result['bic'],
                garch_result['fit_time'], garch_result['vol_prediction_time']
            ]
        }
        
        df = pd.DataFrame(comparison_data)
        csv_file = f"gs_stock_validation_{timestamp}.csv"
        df.to_csv(csv_file, index=False)
        print(f"\n💾 结果已保存到: {csv_file}")

def main():
    """主函数"""
    print("=" * 80)
    print("🏦 高盛(GS)股票 GARCH(1,1)-GED 模型验证")
    print("=" * 80)
    print("比较 garch_lib 和 Python arch 库在真实股票数据上的表现")
    print()
    
    # 检查依赖
    if not HAS_ARCH and not HAS_GARCH_LIB:
        print("❌ 未检测到任何GARCH库，请安装arch或编译garch_lib")
        return
    
    try:
        # 下载股票数据
        stock_data = download_gs_data(period="2y", interval="1d")  # 2年的日数据
        if stock_data is None:
            return
        
        # 准备收益率数据
        returns = prepare_returns_data(stock_data, return_type="log")
        
        if len(returns) < 100:
            print(f"❌ 数据点太少 ({len(returns)}), 需要至少100个点")
            return
        
        # 运行两个库的测试
        arch_result = test_arch_lib(returns, test_ratio=0.2)
        garch_result = test_garch_lib(returns, test_ratio=0.2)
        
        # 比较结果
        compare_results(arch_result, garch_result)
        
        # 保存结果
        save_results(arch_result, garch_result, stock_data)
        
        print(f"\n✅ 高盛股票验证完成!")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  用户中断验证过程")
    except Exception as e:
        print(f"\n❌ 验证过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 