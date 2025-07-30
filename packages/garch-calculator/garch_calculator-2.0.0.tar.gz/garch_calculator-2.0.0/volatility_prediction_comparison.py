#!/usr/bin/env python3
"""
网格搜索参数 vs arch库GARCH(1,1)-GED 波动率预测对比程序
专门针对brett.csv数据进行详细的预测性能评估
"""

import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple
import json
import time
from brett_optimized_garch import BrettOptimizedGarch

class VolatilityPredictionComparison:
    """波动率预测对比类"""
    
    def __init__(self, data: np.ndarray, test_name: str = "brett_comparison"):
        """
        初始化对比测试
        
        Args:
            data: 收益率数据
            test_name: 测试名称
        """
        self.data = data
        self.test_name = test_name
        self.results = {}
        
    def run_grid_search_optimization(self, grid_points: int = 6) -> Dict:
        """
        运行网格搜索找到最优参数
        
        Args:
            grid_points: 网格搜索点数
            
        Returns:
            网格搜索结果
        """
        print("🔍 执行网格搜索参数优化...")
        
        # 使用更精细的网格搜索
        grid_result = BrettOptimizedGarch.quick_grid_search(
            self.data, 
            omega_range=(10.0, 30.0),
            alpha_range=(0.10, 0.40), 
            beta_range=(0.55, 0.85),
            grid_points=grid_points
        )
        
        if grid_result['best_params']:
            print(f"✅ 网格搜索完成")
            print(f"   最优参数: ω={grid_result['best_params']['omega']:.4f}, "
                  f"α={grid_result['best_params']['alpha']:.4f}, "
                  f"β={grid_result['best_params']['beta']:.4f}")
            print(f"   最优似然值: {grid_result['best_likelihood']:.6f}")
            
            if grid_result['arch_likelihood'] != -np.inf:
                improvement = grid_result['best_likelihood'] - grid_result['arch_likelihood']
                print(f"   相对arch库改进: {improvement:.6f}")
        
        return grid_result
    
    def rolling_forecast_comparison(self, window_size: int = 200, 
                                  forecast_horizon: int = 1,
                                  use_optimized_params: bool = True) -> Dict:
        """
        滚动窗口预测对比
        
        Args:
            window_size: 滚动窗口大小
            forecast_horizon: 预测步长
            use_optimized_params: 是否使用网格搜索优化的参数
            
        Returns:
            对比结果字典
        """
        print(f"\n🔄 滚动窗口预测对比")
        print(f"   窗口大小: {window_size}, 预测步长: {forecast_horizon}")
        print(f"   数据总长度: {len(self.data)}")
        
        # 如果使用优化参数，先进行网格搜索
        if use_optimized_params:
            grid_result = self.run_grid_search_optimization()
            if not grid_result['best_params']:
                print("❌ 网格搜索失败，使用默认参数")
                use_optimized_params = False
        
        # 存储预测结果
        garch_lib_predictions = []
        arch_lib_predictions = []
        prediction_indices = []
        garch_lib_likelihoods = []
        arch_lib_likelihoods = []
        
        # 存储参数演化（如果不使用固定优化参数）
        garch_lib_params_history = []
        arch_lib_params_history = []
        
        successful_predictions = 0
        total_attempts = 0
        
        start_time = time.time()
        
        for i in range(window_size, len(self.data)):
            total_attempts += 1
            window_data = self.data[i-window_size:i]
            
            try:
                # === ARCH库预测（基准） ===
                arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
                arch_result = arch_model_obj.fit(disp='off', show_warning=False)
                
                # 检查收敛
                if arch_result.convergence_flag != 0:
                    continue
                    
                # arch库预测
                arch_forecast = arch_result.forecast(horizon=forecast_horizon, reindex=False)
                arch_vol = np.sqrt(arch_forecast.variance.values[-1, 0])
                arch_lib_predictions.append(arch_vol)
                arch_lib_likelihoods.append(arch_result.loglikelihood)
                
                # 记录arch库参数
                arch_params = {
                    'omega': arch_result.params['omega'],
                    'alpha': arch_result.params['alpha[1]'],
                    'beta': arch_result.params['beta[1]'],
                    'nu': arch_result.params['nu']
                }
                arch_lib_params_history.append(arch_params)
                
                # === GARCH_LIB预测 ===
                calc = gc.GarchCalculator(history_size=window_size + 10)
                calc.add_returns(window_data.tolist())
                
                if use_optimized_params:
                    # 使用网格搜索的最优参数
                    best_params = grid_result['best_params']
                    params = gc.GarchParameters()
                    params.mu = best_params['mu']
                    params.omega = best_params['omega']
                    params.alpha = best_params['alpha']
                    params.beta = best_params['beta']
                    params.nu = best_params['nu']
                    calc.set_parameters(params)
                    
                    # 记录使用的参数
                    garch_params = {
                        'omega': best_params['omega'],
                        'alpha': best_params['alpha'],
                        'beta': best_params['beta'],
                        'nu': best_params['nu']
                    }
                else:
                    # 让garch_lib自己估计参数
                    estimation_result = calc.estimate_parameters()
                    if not estimation_result.converged:
                        continue
                    garch_params = {
                        'omega': estimation_result.parameters.omega,
                        'alpha': estimation_result.parameters.alpha,
                        'beta': estimation_result.parameters.beta,
                        'nu': estimation_result.parameters.nu
                    }
                
                garch_lib_params_history.append(garch_params)
                
                # garch_lib预测
                garch_forecast = calc.forecast_volatility(forecast_horizon)
                garch_vol = garch_forecast.volatility
                garch_lib_predictions.append(garch_vol)
                
                # 计算似然值
                garch_likelihood = calc.calculate_log_likelihood()
                garch_lib_likelihoods.append(garch_likelihood)
                
                prediction_indices.append(i)
                successful_predictions += 1
                
                # 进度显示
                if total_attempts % 50 == 0:
                    progress = total_attempts / (len(self.data) - window_size) * 100
                    elapsed = time.time() - start_time
                    eta = elapsed * (len(self.data) - window_size - total_attempts) / total_attempts
                    print(f"   进度: {progress:.1f}% (ETA: {eta:.1f}s) - "
                          f"garch_lib: {garch_vol:.4f}, arch: {arch_vol:.4f}, "
                          f"差异: {abs(garch_vol - arch_vol):.4f}")
                
            except Exception as e:
                if total_attempts <= 5:  # 只显示前几个错误
                    print(f"   预测失败 at index {i}: {str(e)}")
                continue
        
        elapsed_time = time.time() - start_time
        
        print(f"\n✅ 滚动预测完成!")
        print(f"   耗时: {elapsed_time:.2f}秒")
        print(f"   成功预测: {successful_predictions}/{total_attempts} ({successful_predictions/total_attempts:.2%})")
        
        return {
            'garch_lib_predictions': garch_lib_predictions,
            'arch_lib_predictions': arch_lib_predictions,
            'prediction_indices': prediction_indices,
            'garch_lib_likelihoods': garch_lib_likelihoods,
            'arch_lib_likelihoods': arch_lib_likelihoods,
            'garch_lib_params_history': garch_lib_params_history,
            'arch_lib_params_history': arch_lib_params_history,
            'successful_predictions': successful_predictions,
            'total_attempts': total_attempts,
            'success_rate': successful_predictions / total_attempts,
            'elapsed_time': elapsed_time,
            'use_optimized_params': use_optimized_params,
            'grid_search_result': grid_result if use_optimized_params else None
        }
    
    def calculate_comparison_metrics(self, forecast_results: Dict) -> Dict:
        """
        计算详细的对比指标
        
        Args:
            forecast_results: 预测结果
            
        Returns:
            对比指标字典
        """
        garch_preds = np.array(forecast_results['garch_lib_predictions'])
        arch_preds = np.array(forecast_results['arch_lib_predictions'])
        
        # 基本统计指标
        metrics = {
            # 预测性能指标
            'correlation': np.corrcoef(garch_preds, arch_preds)[0, 1],
            'mae': np.mean(np.abs(garch_preds - arch_preds)),
            'rmse': np.sqrt(np.mean((garch_preds - arch_preds)**2)),
            'mape': np.mean(np.abs((garch_preds - arch_preds) / arch_preds)) * 100,
            'bias': np.mean(garch_preds - arch_preds),
            
            # 分布特征
            'garch_lib_mean': garch_preds.mean(),
            'arch_lib_mean': arch_preds.mean(),
            'garch_lib_std': garch_preds.std(),
            'arch_lib_std': arch_preds.std(),
            'garch_lib_min': garch_preds.min(),
            'arch_lib_min': arch_preds.min(),
            'garch_lib_max': garch_preds.max(),
            'arch_lib_max': arch_preds.max(),
            
            # 似然值对比
            'garch_lib_avg_likelihood': np.mean(forecast_results['garch_lib_likelihoods']),
            'arch_lib_avg_likelihood': np.mean(forecast_results['arch_lib_likelihoods']),
            
            # 相对性能
            'mean_relative_error': np.mean((garch_preds - arch_preds) / arch_preds) * 100,
            'accuracy_within_5pct': np.mean(np.abs((garch_preds - arch_preds) / arch_preds) < 0.05) * 100,
            'accuracy_within_10pct': np.mean(np.abs((garch_preds - arch_preds) / arch_preds) < 0.10) * 100,
            'accuracy_within_20pct': np.mean(np.abs((garch_preds - arch_preds) / arch_preds) < 0.20) * 100,
        }
        
        # 添加分位数对比
        for q in [0.05, 0.25, 0.5, 0.75, 0.95]:
            metrics[f'garch_lib_q{int(q*100)}'] = np.quantile(garch_preds, q)
            metrics[f'arch_lib_q{int(q*100)}'] = np.quantile(arch_preds, q)
        
        return metrics
    
    def analyze_parameter_differences(self, forecast_results: Dict) -> Dict:
        """
        分析参数差异
        
        Args:
            forecast_results: 预测结果
            
        Returns:
            参数分析结果
        """
        if not forecast_results['use_optimized_params']:
            # 如果使用动态参数估计，分析参数演化
            garch_params = forecast_results['garch_lib_params_history']
            arch_params = forecast_results['arch_lib_params_history']
            
            param_analysis = {}
            for param_name in ['omega', 'alpha', 'beta', 'nu']:
                garch_values = [p[param_name] for p in garch_params]
                arch_values = [p[param_name] for p in arch_params]
                
                param_analysis[param_name] = {
                    'garch_lib_mean': np.mean(garch_values),
                    'arch_lib_mean': np.mean(arch_values),
                    'garch_lib_std': np.std(garch_values),
                    'arch_lib_std': np.std(arch_values),
                    'mean_difference': np.mean(garch_values) - np.mean(arch_values),
                    'correlation': np.corrcoef(garch_values, arch_values)[0, 1] if len(garch_values) > 1 else 0
                }
            
            return param_analysis
        else:
            # 如果使用固定优化参数，与arch库平均参数对比
            grid_params = forecast_results['grid_search_result']['best_params']
            arch_params = forecast_results['arch_lib_params_history']
            
            param_analysis = {}
            for param_name in ['omega', 'alpha', 'beta', 'nu']:
                arch_values = [p[param_name] for p in arch_params]
                arch_mean = np.mean(arch_values)
                
                param_analysis[param_name] = {
                    'grid_search_value': grid_params[param_name],
                    'arch_lib_mean': arch_mean,
                    'arch_lib_std': np.std(arch_values),
                    'difference': grid_params[param_name] - arch_mean,
                    'relative_difference': (grid_params[param_name] - arch_mean) / arch_mean * 100
                }
            
            return param_analysis
    
    def generate_report(self, forecast_results: Dict, metrics: Dict, param_analysis: Dict) -> None:
        """
        生成详细报告
        
        Args:
            forecast_results: 预测结果
            metrics: 对比指标
            param_analysis: 参数分析
        """
        print(f"\n📊 波动率预测对比报告")
        print("=" * 80)
        
        # 基本信息
        print(f"\n🔧 测试配置:")
        print(f"   数据集: {self.test_name}")
        print(f"   数据点数: {len(self.data)}")
        print(f"   成功预测: {forecast_results['successful_predictions']}")
        print(f"   使用优化参数: {'是' if forecast_results['use_optimized_params'] else '否'}")
        
        # 预测性能对比
        print(f"\n📈 预测性能对比:")
        print(f"   相关系数: {metrics['correlation']:.4f}")
        print(f"   平均绝对误差: {metrics['mae']:.6f}")
        print(f"   均方根误差: {metrics['rmse']:.6f}")
        print(f"   平均绝对百分比误差: {metrics['mape']:.2f}%")
        print(f"   偏差 (garch_lib - arch): {metrics['bias']:.6f}")
        print(f"   平均相对误差: {metrics['mean_relative_error']:.2f}%")
        
        # 精度统计
        print(f"\n🎯 精度统计:")
        print(f"   5%以内精度: {metrics['accuracy_within_5pct']:.1f}%")
        print(f"   10%以内精度: {metrics['accuracy_within_10pct']:.1f}%")
        print(f"   20%以内精度: {metrics['accuracy_within_20pct']:.1f}%")
        
        # 分布对比
        print(f"\n📊 分布特征对比:")
        print(f"   {'统计量':<15} {'garch_lib':<12} {'arch库':<12} {'差异':<10}")
        print("-" * 55)
        stats = ['mean', 'std', 'min', 'max']
        for stat in stats:
            garch_val = metrics[f'garch_lib_{stat}']
            arch_val = metrics[f'arch_lib_{stat}']
            diff = garch_val - arch_val
            print(f"   {stat:<15} {garch_val:<12.4f} {arch_val:<12.4f} {diff:<10.4f}")
        
        # 分位数对比
        print(f"\n📈 分位数对比:")
        print(f"   {'分位数':<10} {'garch_lib':<12} {'arch库':<12} {'差异':<10}")
        print("-" * 50)
        for q in [5, 25, 50, 75, 95]:
            garch_val = metrics[f'garch_lib_q{q}']
            arch_val = metrics[f'arch_lib_q{q}']
            diff = garch_val - arch_val
            print(f"   Q{q}%{'':<7} {garch_val:<12.4f} {arch_val:<12.4f} {diff:<10.4f}")
        
        # 似然值对比
        print(f"\n🔍 似然值对比:")
        print(f"   garch_lib平均似然值: {metrics['garch_lib_avg_likelihood']:.4f}")
        print(f"   arch库平均似然值: {metrics['arch_lib_avg_likelihood']:.4f}")
        print(f"   似然值差异: {metrics['garch_lib_avg_likelihood'] - metrics['arch_lib_avg_likelihood']:.4f}")
        
        # 参数分析
        print(f"\n⚙️  参数分析:")
        if forecast_results['use_optimized_params']:
            print(f"   使用网格搜索固定参数 vs arch库动态参数:")
            for param, analysis in param_analysis.items():
                print(f"   {param}:")
                print(f"      网格搜索值: {analysis['grid_search_value']:.6f}")
                print(f"      arch库均值: {analysis['arch_lib_mean']:.6f}")
                print(f"      差异: {analysis['difference']:.6f} ({analysis['relative_difference']:.2f}%)")
        else:
            print(f"   garch_lib动态参数 vs arch库动态参数:")
            for param, analysis in param_analysis.items():
                print(f"   {param}: garch_lib={analysis['garch_lib_mean']:.4f}±{analysis['garch_lib_std']:.4f}, "
                      f"arch={analysis['arch_lib_mean']:.4f}±{analysis['arch_lib_std']:.4f}, "
                      f"相关性={analysis['correlation']:.3f}")
    
    def save_results(self, forecast_results: Dict, metrics: Dict, param_analysis: Dict) -> None:
        """保存结果到文件"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f'volatility_prediction_comparison_{self.test_name}_{timestamp}.json'
        
        # 转换numpy数组为列表以便JSON序列化
        results_to_save = {
            'test_name': self.test_name,
            'test_timestamp': timestamp,
            'forecast_results': {
                'garch_lib_predictions': forecast_results['garch_lib_predictions'],
                'arch_lib_predictions': forecast_results['arch_lib_predictions'],
                'prediction_indices': forecast_results['prediction_indices'],
                'garch_lib_likelihoods': forecast_results['garch_lib_likelihoods'],
                'arch_lib_likelihoods': forecast_results['arch_lib_likelihoods'],
                'successful_predictions': forecast_results['successful_predictions'],
                'total_attempts': forecast_results['total_attempts'],
                'success_rate': forecast_results['success_rate'],
                'elapsed_time': forecast_results['elapsed_time'],
                'use_optimized_params': forecast_results['use_optimized_params']
            },
            'comparison_metrics': metrics,
            'parameter_analysis': param_analysis
        }
        
        with open(filename, 'w') as f:
            json.dump(results_to_save, f, indent=2)
        
        print(f"\n💾 结果已保存到: {filename}")


def main():
    """主函数：执行完整的对比测试"""
    print("🚀 网格搜索参数 vs arch库GARCH(1,1)-GED 波动率预测对比")
    print("=" * 80)
    
    # 读取brett.csv数据
    df = pd.read_csv('brett.csv')
    
    # 使用不同的数据子集进行测试
    test_configs = [
        {
            'name': 'brett_full_500',
            'data': df['c_scaled'].values[:500],
            'window_size': 200,
            'description': '前500个数据点，窗口200'
        },
        {
            'name': 'brett_recent_300', 
            'data': df['c_scaled'].values[200:500],
            'window_size': 150,
            'description': '中间300个数据点，窗口150'
        }
    ]
    
    for config in test_configs:
        print(f"\n{'='*60}")
        print(f"🔍 测试配置: {config['name']}")
        print(f"   描述: {config['description']}")
        print(f"   数据长度: {len(config['data'])}")
        
        # 创建对比测试实例
        comparison = VolatilityPredictionComparison(config['data'], config['name'])
        
        # 测试1: 使用网格搜索优化参数
        print(f"\n🎯 测试1: 网格搜索优化参数 vs arch库")
        forecast_results_opt = comparison.rolling_forecast_comparison(
            window_size=config['window_size'],
            use_optimized_params=True
        )
        
        if forecast_results_opt['successful_predictions'] > 0:
            metrics_opt = comparison.calculate_comparison_metrics(forecast_results_opt)
            param_analysis_opt = comparison.analyze_parameter_differences(forecast_results_opt)
            comparison.generate_report(forecast_results_opt, metrics_opt, param_analysis_opt)
            comparison.save_results(forecast_results_opt, metrics_opt, param_analysis_opt)
        
        print(f"\n" + "="*60)
        print(f"🎯 测试2: garch_lib动态参数估计 vs arch库")
        
        # 测试2: 使用garch_lib动态参数估计
        forecast_results_dyn = comparison.rolling_forecast_comparison(
            window_size=config['window_size'],
            use_optimized_params=False
        )
        
        if forecast_results_dyn['successful_predictions'] > 0:
            metrics_dyn = comparison.calculate_comparison_metrics(forecast_results_dyn)
            param_analysis_dyn = comparison.analyze_parameter_differences(forecast_results_dyn)
            comparison.generate_report(forecast_results_dyn, metrics_dyn, param_analysis_dyn)
            comparison.save_results(forecast_results_dyn, metrics_dyn, param_analysis_dyn)
        
        # 对比两种方法
        if (forecast_results_opt['successful_predictions'] > 0 and 
            forecast_results_dyn['successful_predictions'] > 0):
            
            print(f"\n🏆 两种方法性能对比:")
            print(f"   {'指标':<20} {'网格搜索':<12} {'动态估计':<12} {'优势':<10}")
            print("-" * 60)
            
            comparisons = [
                ('相关系数', metrics_opt['correlation'], metrics_dyn['correlation']),
                ('MAE', metrics_opt['mae'], metrics_dyn['mae']),
                ('RMSE', metrics_opt['rmse'], metrics_dyn['rmse']),
                ('MAPE (%)', metrics_opt['mape'], metrics_dyn['mape']),
                ('10%内精度 (%)', metrics_opt['accuracy_within_10pct'], metrics_dyn['accuracy_within_10pct'])
            ]
            
            for metric_name, opt_val, dyn_val in comparisons:
                if metric_name == '相关系数' or '精度' in metric_name:
                    better = "网格搜索" if opt_val > dyn_val else "动态估计"
                else:
                    better = "网格搜索" if opt_val < dyn_val else "动态估计"
                
                print(f"   {metric_name:<20} {opt_val:<12.4f} {dyn_val:<12.4f} {better:<10}")


if __name__ == "__main__":
    main() 