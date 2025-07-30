#!/usr/bin/env python3
"""
多股票GARCH(1,1)-GED模型综合验证脚本
使用yfinance获取多只股票的长期历史数据，全面比较garch_lib和Python arch库的表现

🔄 更新：现在garch_lib与arch库使用完全一致的输入（直接使用收益率）
不再需要价格转换和缩放，提供更精确的比较结果
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
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

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
    import garch_lib as gc
    HAS_GARCH_LIB = True
    print("✓ Successfully imported garch_calculator")
except ImportError:
    HAS_GARCH_LIB = False
    print("❌ Failed to import garch_calculator")

# 定义要测试的股票列表（包含不同行业和波动率特征）
STOCK_SYMBOLS = {
    'GS': '高盛集团 (金融)',
    'AAPL': '苹果公司 (科技)',
    'MSFT': '微软公司 (科技)', 
    'JPM': '摩根大通 (金融)',
    'NVDA': '英伟达 (半导体)',
    'TSLA': '特斯拉 (汽车)',
    'META': 'Meta平台 (社交媒体)',
    'GOOGL': '谷歌 (科技)',
    'AMZN': '亚马逊 (电商)',
    'BAC': '美国银行 (金融)',
    'XOM': '埃克森美孚 (能源)',
    'JNJ': '强生公司 (医疗)',
    'V': 'Visa (金融服务)',
    'PG': '宝洁公司 (消费品)',
    'HD': '家得宝 (零售)'
}

class StockDataManager:
    """股票数据管理器"""
    
    def __init__(self, period="5y", interval="1d"):
        self.period = period
        self.interval = interval
        self.cache = {}
    
    def download_stock_data(self, symbol):
        """下载单只股票数据"""
        if symbol in self.cache:
            return self.cache[symbol]
        
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=self.period, interval=self.interval)
            
            if data.empty:
                print(f"❌ {symbol}: 未能获取到数据")
                return None
            
            # 数据清理
            data = data.dropna()
            if len(data) < 500:  # 至少需要500个数据点
                print(f"⚠️  {symbol}: 数据点不足 ({len(data)})")
                return None
            
            print(f"✓ {symbol}: {len(data)} 个数据点, 时间范围: {data.index[0].date()} 到 {data.index[-1].date()}")
            
            self.cache[symbol] = data
            return data
            
        except Exception as e:
            print(f"❌ {symbol}: 下载失败 - {e}")
            return None
    
    def prepare_returns(self, stock_data, return_type="log"):
        """准备收益率数据"""
        prices = stock_data['Close'].dropna()
        
        if return_type == "log":
            returns = np.log(prices / prices.shift(1)).dropna()
        else:
            returns = (prices / prices.shift(1) - 1).dropna()
        
        # 去除极端异常值（超过6个标准差）
        mean_return = returns.mean()
        std_return = returns.std()
        
        # 统计异常值
        outliers_mask = np.abs(returns - mean_return) > 6 * std_return
        outliers_count = outliers_mask.sum()
        
        if outliers_count > 0:
            print(f"   去除 {outliers_count} 个极端异常值")
            returns = returns[~outliers_mask]
        
        # 中心化处理
        returns = returns - returns.mean()
        
        return returns.values

class GarchModelTester:
    """GARCH模型测试器"""
    
    def __init__(self, test_ratio=0.15):  # 减少测试集比例，增加训练集
        self.test_ratio = test_ratio
    
    def test_arch_lib(self, returns, symbol="UNKNOWN"):
        """测试Python arch库"""
        if not HAS_ARCH:
            return None
            
        try:
            # 分割数据 - 85%训练，15%测试
            split_point = int(len(returns) * (1 - self.test_ratio))
            train_returns = returns[:split_point]
            test_returns = returns[split_point:]
            
            start_time = time.time()
            
            # 创建并拟合GARCH(1,1)-GED模型
            model = arch_model(train_returns, vol='GARCH', p=1, q=1, dist='ged', rescale=False)
            fitted_model = model.fit(disp='off', show_warning=False, options={'maxiter': 1000})
            fit_time = time.time() - start_time
            
            # 获取参数
            params = fitted_model.params
            
            # 样本内波动率
            start_vol_time = time.time()
            insample_volatility = fitted_model.conditional_volatility
            
            # 样本外预测
            forecast_horizon = len(test_returns)
            try:
                forecast = fitted_model.forecast(horizon=forecast_horizon, start=split_point)
                if forecast.variance.values.shape[0] > 0:
                    forecast_volatility = np.sqrt(forecast.variance.values[-1, :])
                else:
                    last_vol = insample_volatility[-1] if len(insample_volatility) > 0 else np.std(train_returns)
                    forecast_volatility = np.full(forecast_horizon, last_vol)
            except:
                last_vol = insample_volatility[-1] if len(insample_volatility) > 0 else np.std(train_returns)
                forecast_volatility = np.full(forecast_horizon, last_vol)
            
            vol_prediction_time = time.time() - start_vol_time
            
            # 计算实际波动率（滚动标准差）
            window_size = min(20, len(test_returns) // 3)  # 更大的窗口
            actual_volatility = []
            for i in range(len(test_returns)):
                if i < window_size:
                    actual_vol = np.std(test_returns[:i+1]) if i > 0 else np.std(train_returns[-window_size:])
                else:
                    actual_vol = np.std(test_returns[max(0, i-window_size):i+1])
                actual_volatility.append(actual_vol)
            actual_volatility = np.array(actual_volatility)
            
            result = {
                'library': 'arch',
                'symbol': symbol,
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
                'train_size': len(train_returns),
                'test_size': len(test_returns),
                'persistence': params['alpha[1]'] + params['beta[1]'],
                'unconditional_vol': np.sqrt(params['omega'] / (1 - params['alpha[1]'] - params['beta[1]'])),
                'insample_volatility': insample_volatility,
                'forecast_volatility': forecast_volatility,
                'actual_volatility': actual_volatility
            }
            
            # 计算预测精度指标
            if len(forecast_volatility) == len(actual_volatility):
                result['forecast_mse'] = mean_squared_error(actual_volatility, forecast_volatility)
                result['forecast_mae'] = mean_absolute_error(actual_volatility, forecast_volatility)
                result['forecast_rmse'] = np.sqrt(result['forecast_mse'])
                
                # 计算更多预测精度指标
                result['forecast_mape'] = np.mean(np.abs((actual_volatility - forecast_volatility) / actual_volatility)) * 100
                result['forecast_r2'] = 1 - (np.sum((actual_volatility - forecast_volatility)**2) / 
                                            np.sum((actual_volatility - np.mean(actual_volatility))**2))
            
            return result
            
        except Exception as e:
            print(f"❌ {symbol} arch库测试失败: {e}")
            return None
    
    def test_garch_lib(self, returns, symbol="UNKNOWN"):
        """测试garch_lib实现 - 现在与arch库使用完全一致的输入"""
        if not HAS_GARCH_LIB:
            return None
            
        try:
            # 分割数据 - 85%训练，15%测试
            split_point = int(len(returns) * (1 - self.test_ratio))
            train_returns = returns[:split_point]
            test_returns = returns[split_point:]
            
            start_time = time.time()
            
            # 创建计算器
            min_samples = min(100, len(train_returns) // 5)
            calc = gc.GarchCalculator(history_size=len(train_returns)+200, min_samples=min_samples)
            
            # 直接添加收益率数据 - 与arch库完全一致！
            calc.add_returns(train_returns.tolist())
            
            # 估计参数
            result_obj = calc.estimate_parameters()
            fit_time = time.time() - start_time
            
            params = result_obj.parameters
            
            # 样本内波动率预测
            start_vol_time = time.time()
            try:
                variance_series = calc.get_variance_series()
                if len(variance_series) > 0:
                    insample_volatility = np.sqrt(variance_series)
                else:
                    current_vol = calc.get_current_volatility()
                    insample_volatility = np.full(len(train_returns), current_vol)
            except:
                current_vol = calc.get_current_volatility()
                insample_volatility = np.full(len(train_returns), current_vol)
            
            # 样本外预测
            forecast_volatility = []
            
            for i in range(len(test_returns)):
                try:
                    # 预测下一期波动率
                    forecast_obj = calc.forecast_volatility(1)
                    if forecast_obj.volatility > 0 and np.isfinite(forecast_obj.volatility):
                        forecast_volatility.append(forecast_obj.volatility)
                    else:
                        current_vol = calc.get_current_volatility()
                        forecast_volatility.append(current_vol)
                    
                    # 添加实际收益率并更新模型（一步预测）
                    calc.add_return(test_returns[i])
                    calc.update_model()
                    
                except Exception as e:
                    try:
                        current_vol = calc.get_current_volatility()
                        forecast_volatility.append(current_vol)
                    except:
                        forecast_volatility.append(np.std(train_returns))
                    break
                
            forecast_volatility = np.array(forecast_volatility)
            vol_prediction_time = time.time() - start_vol_time
            
            # 计算实际波动率（滚动标准差）
            window_size = min(20, len(test_returns) // 3)
            actual_volatility = []
            for i in range(len(test_returns)):
                if i < window_size:
                    actual_vol = np.std(test_returns[:i+1]) if i > 0 else np.std(train_returns[-window_size:])
                else:
                    actual_vol = np.std(test_returns[max(0, i-window_size):i+1])
                actual_volatility.append(actual_vol)
            actual_volatility = np.array(actual_volatility)
            
            result = {
                'library': 'garch_lib',
                'symbol': symbol,
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
                'train_size': len(train_returns),
                'test_size': len(test_returns),
                'persistence': params.alpha + params.beta,
                'unconditional_vol': np.sqrt(params.omega / (1 - params.alpha - params.beta)) if (params.alpha + params.beta) < 1 else np.inf,
                'insample_volatility': insample_volatility,
                'forecast_volatility': forecast_volatility,
                'actual_volatility': actual_volatility
            }
            
            # 计算预测精度指标
            if len(forecast_volatility) == len(actual_volatility):
                result['forecast_mse'] = mean_squared_error(actual_volatility, forecast_volatility)
                result['forecast_mae'] = mean_absolute_error(actual_volatility, forecast_volatility)
                result['forecast_rmse'] = np.sqrt(result['forecast_mse'])
                result['forecast_mape'] = np.mean(np.abs((actual_volatility - forecast_volatility) / actual_volatility)) * 100
                result['forecast_r2'] = 1 - (np.sum((actual_volatility - forecast_volatility)**2) / 
                                            np.sum((actual_volatility - np.mean(actual_volatility))**2))
            elif len(forecast_volatility) > 0 and len(actual_volatility) > 0:
                min_len = min(len(forecast_volatility), len(actual_volatility))
                result['forecast_mse'] = mean_squared_error(actual_volatility[:min_len], forecast_volatility[:min_len])
                result['forecast_mae'] = mean_absolute_error(actual_volatility[:min_len], forecast_volatility[:min_len])
                result['forecast_rmse'] = np.sqrt(result['forecast_mse'])
                result['forecast_mape'] = np.mean(np.abs((actual_volatility[:min_len] - forecast_volatility[:min_len]) / actual_volatility[:min_len])) * 100
                result['forecast_r2'] = 1 - (np.sum((actual_volatility[:min_len] - forecast_volatility[:min_len])**2) / 
                                            np.sum((actual_volatility[:min_len] - np.mean(actual_volatility[:min_len]))**2))
            
            return result
                
        except Exception as e:
            print(f"❌ {symbol} garch_lib测试失败: {e}")
            return None

def test_single_stock(symbol, description, data_manager, tester):
    """测试单只股票"""
    print(f"\n{'='*80}")
    print(f"📈 {symbol} - {description}")
    print('='*80)
    
    # 下载数据
    stock_data = data_manager.download_stock_data(symbol)
    if stock_data is None:
        return None
    
    # 准备收益率数据
    returns = data_manager.prepare_returns(stock_data, return_type="log")
    
    if len(returns) < 500:
        print(f"❌ {symbol}: 数据点太少 ({len(returns)})")
        return None
    
    print(f"📊 收益率统计:")
    print(f"   数据点数: {len(returns)}")
    print(f"   均值: {returns.mean():.8f}")
    print(f"   标准差: {returns.std():.6f}")
    print(f"   偏度: {pd.Series(returns).skew():.4f}")
    print(f"   峰度: {pd.Series(returns).kurtosis():.4f}")
    print(f"   训练集: {int(len(returns) * 0.85)} 点")
    print(f"   测试集: {len(returns) - int(len(returns) * 0.85)} 点")
    
    # 测试两个库
    arch_result = tester.test_arch_lib(returns, symbol)
    garch_result = tester.test_garch_lib(returns, symbol)
    
    if arch_result:
        print(f"\n✅ {symbol} - Python arch库测试完成")
        print(f"   参数: ω={arch_result['omega']:.6f}, α={arch_result['alpha']:.4f}, β={arch_result['beta']:.4f}, ν={arch_result['nu']:.4f}")
        print(f"   收敛: {'是' if arch_result['converged'] else '否'}, 时间: {arch_result['fit_time']:.3f}秒")
        if 'forecast_rmse' in arch_result:
            print(f"   预测RMSE: {arch_result['forecast_rmse']:.6f}")
    
    if garch_result:
        print(f"\n✅ {symbol} - garch_lib测试完成 (使用收益率输入)")
        print(f"   参数: ω={garch_result['omega']:.6f}, α={garch_result['alpha']:.4f}, β={garch_result['beta']:.4f}, ν={garch_result['nu']:.4f}")
        print(f"   收敛: {'是' if garch_result['converged'] else '否'}, 迭代: {garch_result.get('iterations', 'N/A')}, 时间: {garch_result['fit_time']:.3f}秒")
        if 'forecast_rmse' in garch_result:
            print(f"   预测RMSE: {garch_result['forecast_rmse']:.6f}")
    
    return {
        'symbol': symbol,
        'description': description,
        'data_points': len(returns),
        'returns_stats': {
            'mean': returns.mean(),
            'std': returns.std(),
            'skewness': pd.Series(returns).skew(),
            'kurtosis': pd.Series(returns).kurtosis()
        },
        'arch_result': arch_result,
        'garch_result': garch_result
    }

def generate_comprehensive_report(all_results):
    """生成综合报告"""
    print(f"\n\n{'='*100}")
    print("📊 多股票GARCH模型综合验证报告")
    print('='*100)
    
    # 过滤有效结果
    valid_results = [r for r in all_results if r and r['arch_result'] and r['garch_result']]
    
    if not valid_results:
        print("❌ 没有有效的比较结果")
        return
    
    print(f"📈 成功测试的股票数量: {len(valid_results)}")
    print(f"📊 总数据点: {sum(r['data_points'] for r in valid_results):,}")
    
    # 1. 参数一致性分析
    print(f"\n{'='*60}")
    print("1. 参数估计一致性分析")
    print('='*60)
    
    param_errors = []
    convergence_stats = {'arch_converged': 0, 'garch_converged': 0, 'both_converged': 0}
    
    for result in valid_results:
        arch_res = result['arch_result']
        garch_res = result['garch_result']
        
        # 收敛性统计
        if arch_res['converged']:
            convergence_stats['arch_converged'] += 1
        if garch_res['converged']:
            convergence_stats['garch_converged'] += 1
        if arch_res['converged'] and garch_res['converged']:
            convergence_stats['both_converged'] += 1
        
        # 参数差异
        params = ['omega', 'alpha', 'beta', 'nu']
        stock_param_errors = []
        for param in params:
            arch_val = arch_res[param]
            garch_val = garch_res[param]
            rel_diff = abs(garch_val - arch_val) / abs(arch_val) * 100 if abs(arch_val) > 0 else 0
            stock_param_errors.append(rel_diff)
        
        param_errors.append({
            'symbol': result['symbol'],
            'omega_error': stock_param_errors[0],
            'alpha_error': stock_param_errors[1],
            'beta_error': stock_param_errors[2],
            'nu_error': stock_param_errors[3],
            'avg_error': np.mean(stock_param_errors)
        })
    
    # 参数误差统计
    df_errors = pd.DataFrame(param_errors)
    print(f"\n参数估计相对误差统计 (%):")
    print(f"{'参数':<8} {'平均':<8} {'中位数':<8} {'标准差':<8} {'最大值':<8}")
    print("-" * 48)
    for param in ['omega', 'alpha', 'beta', 'nu', 'avg']:
        col = f"{param}_error"
        print(f"{param:<8} {df_errors[col].mean():<8.2f} {df_errors[col].median():<8.2f} {df_errors[col].std():<8.2f} {df_errors[col].max():<8.2f}")
    
    # 收敛性统计
    print(f"\n收敛性统计:")
    print(f"arch库收敛率: {convergence_stats['arch_converged']}/{len(valid_results)} ({convergence_stats['arch_converged']/len(valid_results)*100:.1f}%)")
    print(f"garch_lib收敛率: {convergence_stats['garch_converged']}/{len(valid_results)} ({convergence_stats['garch_converged']/len(valid_results)*100:.1f}%)")
    print(f"两者都收敛: {convergence_stats['both_converged']}/{len(valid_results)} ({convergence_stats['both_converged']/len(valid_results)*100:.1f}%)")
    
    # 2. 预测精度分析
    print(f"\n{'='*60}")
    print("2. 预测精度对比分析")
    print('='*60)
    
    prediction_stats = []
    for result in valid_results:
        arch_res = result['arch_result']
        garch_res = result['garch_result']
        
        if 'forecast_rmse' in arch_res and 'forecast_rmse' in garch_res:
            rmse_improvement = (arch_res['forecast_rmse'] - garch_res['forecast_rmse']) / arch_res['forecast_rmse'] * 100
            mae_improvement = (arch_res['forecast_mae'] - garch_res['forecast_mae']) / arch_res['forecast_mae'] * 100
            
            prediction_stats.append({
                'symbol': result['symbol'],
                'arch_rmse': arch_res['forecast_rmse'],
                'garch_rmse': garch_res['forecast_rmse'],
                'rmse_improvement': rmse_improvement,
                'mae_improvement': mae_improvement,
                'arch_r2': arch_res.get('forecast_r2', 0),
                'garch_r2': garch_res.get('forecast_r2', 0)
            })
    
    if prediction_stats:
        df_pred = pd.DataFrame(prediction_stats)
        print(f"\n预测精度改善统计 (正数表示garch_lib更好):")
        print(f"RMSE改善 - 平均: {df_pred['rmse_improvement'].mean():.2f}%, 中位数: {df_pred['rmse_improvement'].median():.2f}%")
        print(f"MAE改善 - 平均: {df_pred['mae_improvement'].mean():.2f}%, 中位数: {df_pred['mae_improvement'].median():.2f}%")
        
        better_count = (df_pred['rmse_improvement'] > 0).sum()
        worse_count = (df_pred['rmse_improvement'] < -5).sum()
        similar_count = len(df_pred) - better_count - worse_count
        
        print(f"\ngarch_lib预测更好: {better_count}/{len(df_pred)} ({better_count/len(df_pred)*100:.1f}%)")
        print(f"预测精度相似: {similar_count}/{len(df_pred)} ({similar_count/len(df_pred)*100:.1f}%)")
        print(f"arch预测更好: {worse_count}/{len(df_pred)} ({worse_count/len(df_pred)*100:.1f}%)")
    
    # 3. 性能分析
    print(f"\n{'='*60}")
    print("3. 计算性能对比分析")
    print('='*60)
    
    performance_stats = []
    for result in valid_results:
        arch_res = result['arch_result']
        garch_res = result['garch_result']
        
        fit_speedup = arch_res['fit_time'] / garch_res['fit_time'] if garch_res['fit_time'] > 0 else 0
        vol_speedup = arch_res['vol_prediction_time'] / garch_res['vol_prediction_time'] if garch_res['vol_prediction_time'] > 0 else 0
        
        performance_stats.append({
            'symbol': result['symbol'],
            'arch_fit_time': arch_res['fit_time'],
            'garch_fit_time': garch_res['fit_time'],
            'fit_speedup': fit_speedup,
            'vol_speedup': vol_speedup
        })
    
    df_perf = pd.DataFrame(performance_stats)
    print(f"\n性能提升统计:")
    print(f"拟合速度提升 - 平均: {df_perf['fit_speedup'].mean():.2f}x, 中位数: {df_perf['fit_speedup'].median():.2f}x")
    print(f"预测速度提升 - 平均: {df_perf['vol_speedup'].mean():.2f}x, 中位数: {df_perf['vol_speedup'].median():.2f}x")
    
    # 4. 按行业分析
    print(f"\n{'='*60}")
    print("4. 按行业/特征分组分析")
    print('='*60)
    
    # 根据股票特征分组
    industry_groups = {
        '金融': ['GS', 'JPM', 'BAC', 'V'],
        '科技': ['AAPL', 'MSFT', 'GOOGL', 'META'],
        '高波动': ['NVDA', 'TSLA'],
        '消费/能源': ['AMZN', 'XOM', 'JNJ', 'PG', 'HD']
    }
    
    for industry, symbols in industry_groups.items():
        industry_results = [r for r in valid_results if r['symbol'] in symbols]
        if not industry_results:
            continue
        
        print(f"\n{industry}板块 ({len(industry_results)}只股票):")
        
        avg_param_error = np.mean([np.mean([
            abs(r['garch_result'][p] - r['arch_result'][p]) / abs(r['arch_result'][p]) * 100 
            if abs(r['arch_result'][p]) > 0 else 0
            for p in ['omega', 'alpha', 'beta', 'nu']
        ]) for r in industry_results])
        
        if any('forecast_rmse' in r['arch_result'] and 'forecast_rmse' in r['garch_result'] for r in industry_results):
            avg_rmse_improvement = np.mean([
                (r['arch_result']['forecast_rmse'] - r['garch_result']['forecast_rmse']) / r['arch_result']['forecast_rmse'] * 100
                for r in industry_results 
                if 'forecast_rmse' in r['arch_result'] and 'forecast_rmse' in r['garch_result']
            ])
            print(f"   平均参数误差: {avg_param_error:.2f}%")
            print(f"   平均RMSE改善: {avg_rmse_improvement:.2f}%")
        else:
            print(f"   平均参数误差: {avg_param_error:.2f}%")
    
    # 5. 详细对比表
    print(f"\n{'='*60}")
    print("5. 各股票详细对比表")
    print('='*60)
    
    print(f"{'股票':<6} {'参数误差%':<10} {'RMSE改善%':<10} {'拟合时间比':<10} {'收敛状态':<15}")
    print("-" * 65)
    
    for result in valid_results:
        arch_res = result['arch_result']
        garch_res = result['garch_result']
        
        avg_param_error = np.mean([
            abs(garch_res[p] - arch_res[p]) / abs(arch_res[p]) * 100 
            if abs(arch_res[p]) > 0 else 0
            for p in ['omega', 'alpha', 'beta', 'nu']
        ])
        
        if 'forecast_rmse' in arch_res and 'forecast_rmse' in garch_res:
            rmse_improvement = (arch_res['forecast_rmse'] - garch_res['forecast_rmse']) / arch_res['forecast_rmse'] * 100
        else:
            rmse_improvement = 0
        
        fit_ratio = garch_res['fit_time'] / arch_res['fit_time'] if arch_res['fit_time'] > 0 else 0
        
        convergence = f"{'A' if arch_res['converged'] else 'a'}{'G' if garch_res['converged'] else 'g'}"
        
        print(f"{result['symbol']:<6} {avg_param_error:<10.2f} {rmse_improvement:<10.2f} {fit_ratio:<10.2f} {convergence:<15}")
    
    return {
        'total_stocks': len(valid_results),
        'convergence_stats': convergence_stats,
        'param_errors': df_errors,
        'prediction_stats': df_pred if prediction_stats else None,
        'performance_stats': df_perf
    }

def save_comprehensive_results(all_results, summary_stats):
    """保存综合结果"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存详细结果
    detailed_results = []
    for result in all_results:
        if result and result['arch_result'] and result['garch_result']:
            detailed_results.append({
                'symbol': result['symbol'],
                'description': result['description'],
                'data_points': result['data_points'],
                'returns_mean': result['returns_stats']['mean'],
                'returns_std': result['returns_stats']['std'],
                'returns_skewness': result['returns_stats']['skewness'],
                'returns_kurtosis': result['returns_stats']['kurtosis'],
                
                # arch结果
                'arch_omega': result['arch_result']['omega'],
                'arch_alpha': result['arch_result']['alpha'],
                'arch_beta': result['arch_result']['beta'],
                'arch_nu': result['arch_result']['nu'],
                'arch_log_likelihood': result['arch_result']['log_likelihood'],
                'arch_aic': result['arch_result']['aic'],
                'arch_bic': result['arch_result']['bic'],
                'arch_fit_time': result['arch_result']['fit_time'],
                'arch_converged': result['arch_result']['converged'],
                'arch_forecast_rmse': result['arch_result'].get('forecast_rmse', np.nan),
                'arch_forecast_r2': result['arch_result'].get('forecast_r2', np.nan),
                
                # garch_lib结果
                'garch_omega': result['garch_result']['omega'],
                'garch_alpha': result['garch_result']['alpha'],
                'garch_beta': result['garch_result']['beta'],
                'garch_nu': result['garch_result']['nu'],
                'garch_log_likelihood': result['garch_result']['log_likelihood'],
                'garch_aic': result['garch_result']['aic'],
                'garch_bic': result['garch_result']['bic'],
                'garch_fit_time': result['garch_result']['fit_time'],
                'garch_converged': result['garch_result']['converged'],
                'garch_iterations': result['garch_result'].get('iterations', np.nan),
                'garch_forecast_rmse': result['garch_result'].get('forecast_rmse', np.nan),
                'garch_forecast_r2': result['garch_result'].get('forecast_r2', np.nan),
                
                # 比较指标
                'param_avg_error': np.mean([
                    abs(result['garch_result'][p] - result['arch_result'][p]) / abs(result['arch_result'][p]) * 100 
                    if abs(result['arch_result'][p]) > 0 else 0
                    for p in ['omega', 'alpha', 'beta', 'nu']
                ]),
                'rmse_improvement': (result['arch_result'].get('forecast_rmse', 0) - 
                                   result['garch_result'].get('forecast_rmse', 0)) / 
                                   result['arch_result'].get('forecast_rmse', 1) * 100,
                'fit_speedup': result['arch_result']['fit_time'] / result['garch_result']['fit_time'] 
                              if result['garch_result']['fit_time'] > 0 else 0
            })
    
    # 保存到CSV
    if detailed_results:
        df_detailed = pd.DataFrame(detailed_results)
        csv_file = f"multi_stock_garch_validation_{timestamp}.csv"
        df_detailed.to_csv(csv_file, index=False)
        print(f"\n💾 详细结果已保存到: {csv_file}")
    
    # 保存汇总统计
    summary_file = f"validation_summary_{timestamp}.json"
    with open(summary_file, 'w') as f:
        json.dump({
            'timestamp': timestamp,
            'total_stocks_tested': len(all_results),
            'successful_comparisons': len(detailed_results),
            'convergence_stats': summary_stats['convergence_stats'] if summary_stats else {},
            'param_error_stats': summary_stats['param_errors'].describe().to_dict() if summary_stats and 'param_errors' in summary_stats else {},
            'stocks_list': list(STOCK_SYMBOLS.keys())
        }, f, indent=2, default=str)
    
    print(f"💾 汇总统计已保存到: {summary_file}")

def main():
    """主函数"""
    print("=" * 100)
    print("🏦 多股票GARCH(1,1)-GED模型综合验证系统")
    print("🔄 更新：garch_lib现在与arch库使用完全一致的输入")
    print("=" * 100)
    print(f"测试股票数量: {len(STOCK_SYMBOLS)}")
    print(f"数据周期: 5年历史数据")
    print(f"训练/测试比例: 85%/15%")
    print(f"输入格式: 直接使用收益率数据 (与arch库一致)")
    print()
    
    # 检查依赖
    if not HAS_ARCH and not HAS_GARCH_LIB:
        print("❌ 未检测到任何GARCH库，请安装arch或编译garch_lib")
        return
    
    try:
        # 初始化管理器
        data_manager = StockDataManager(period="5y", interval="1d")
        tester = GarchModelTester(test_ratio=0.15)
        
        # 按批次测试股票（避免内存问题）
        all_results = []
        batch_size = 5
        stock_items = list(STOCK_SYMBOLS.items())
        
        for i in range(0, len(stock_items), batch_size):
            batch = stock_items[i:i+batch_size]
            print(f"\n🔄 处理批次 {i//batch_size + 1}/{(len(stock_items)-1)//batch_size + 1}")
            
            # 串行处理每只股票（避免并发问题）
            for symbol, description in batch:
                result = test_single_stock(symbol, description, data_manager, tester)
                all_results.append(result)
        
        # 生成综合报告
        summary_stats = generate_comprehensive_report(all_results)
        
        # 保存结果
        save_comprehensive_results(all_results, summary_stats)
        
        print(f"\n✅ 多股票验证完成! 总共测试了 {len([r for r in all_results if r])} 只股票")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  用户中断验证过程")
    except Exception as e:
        print(f"\n❌ 验证过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 