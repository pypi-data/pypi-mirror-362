#!/usr/bin/env python3
"""
为brett.csv数据优化的GARCH参数预设工具
基于网格搜索找到的最优参数组合
"""

import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
from typing import Dict, List, Tuple

class BrettOptimizedGarch:
    """为brett.csv数据优化的GARCH参数类"""
    
    # 基于网格搜索得到的最优参数预设
    OPTIMIZED_PARAMS = {
        'default': {
            'mu': 0.883802,
            'omega': 16.607143,
            'alpha': 0.214286,
            'beta': 0.692857,
            'nu': 1.830000,
            'likelihood': -1974.905295,
            'description': '基于500个数据点的网格搜索最优参数'
        },
        'high_volatility': {
            'mu': 0.883802,
            'omega': 20.0,
            'alpha': 0.25,
            'beta': 0.68,
            'nu': 1.8,
            'description': '适用于高波动率期间的参数'
        },
        'stable_period': {
            'mu': 0.883802,
            'omega': 12.0,
            'alpha': 0.18,
            'beta': 0.75,
            'nu': 2.0,
            'description': '适用于稳定期间的参数'
        },
        'arch_like': {
            'mu': 0.883802,
            'omega': 16.303085,
            'alpha': 0.243217,
            'beta': 0.685985,
            'nu': 1.858213,
            'description': 'arch库估计的参数（作为基准）'
        }
    }
    
    @classmethod
    def create_calculator(cls, param_set: str = 'default', 
                         history_size: int = 500) -> gc.GarchCalculator:
        """
        创建预配置的GARCH计算器
        
        Args:
            param_set: 参数集名称 ('default', 'high_volatility', 'stable_period', 'arch_like')
            history_size: 历史数据大小
            
        Returns:
            配置好的GarchCalculator实例
        """
        if param_set not in cls.OPTIMIZED_PARAMS:
            raise ValueError(f"未知的参数集: {param_set}. 可用选项: {list(cls.OPTIMIZED_PARAMS.keys())}")
        
        # 创建计算器
        calc = gc.GarchCalculator(history_size=history_size)
        
        # 设置优化参数
        params_dict = cls.OPTIMIZED_PARAMS[param_set]
        params = gc.GarchParameters()
        params.mu = params_dict['mu']
        params.omega = params_dict['omega']
        params.alpha = params_dict['alpha']
        params.beta = params_dict['beta']
        params.nu = params_dict['nu']
        
        calc.set_parameters(params)
        
        return calc
    
    @classmethod
    def get_parameters(cls, param_set: str = 'default') -> gc.GarchParameters:
        """
        获取参数对象
        
        Args:
            param_set: 参数集名称
            
        Returns:
            GarchParameters对象
        """
        if param_set not in cls.OPTIMIZED_PARAMS:
            raise ValueError(f"未知的参数集: {param_set}. 可用选项: {list(cls.OPTIMIZED_PARAMS.keys())}")
        
        params_dict = cls.OPTIMIZED_PARAMS[param_set]
        params = gc.GarchParameters()
        params.mu = params_dict['mu']
        params.omega = params_dict['omega']
        params.alpha = params_dict['alpha']
        params.beta = params_dict['beta']
        params.nu = params_dict['nu']
        
        return params
    
    @classmethod
    def compare_with_arch(cls, data: np.ndarray, param_set: str = 'default') -> Dict:
        """
        与arch库进行对比验证
        
        Args:
            data: 收益率数据
            param_set: 参数集名称
            
        Returns:
            对比结果字典
        """
        # arch库估计
        try:
            arch_model_obj = arch_model(data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
            arch_result = arch_model_obj.fit(disp='off', show_warning=False)
            arch_likelihood = arch_result.loglikelihood
            arch_params = {
                'mu': arch_result.params['mu'],
                'omega': arch_result.params['omega'],
                'alpha': arch_result.params['alpha[1]'],
                'beta': arch_result.params['beta[1]'],
                'nu': arch_result.params['nu']
            }
        except Exception as e:
            return {'error': f'arch库估计失败: {e}'}
        
        # garch_lib计算
        calc = cls.create_calculator(param_set)
        calc.add_returns(data.tolist())
        
        garch_params = cls.OPTIMIZED_PARAMS[param_set]
        garch_likelihood = calc.calculate_log_likelihood()
        
        # 计算差异
        param_diffs = {
            'mu': abs(garch_params['mu'] - arch_params['mu']),
            'omega': abs(garch_params['omega'] - arch_params['omega']),
            'alpha': abs(garch_params['alpha'] - arch_params['alpha']),
            'beta': abs(garch_params['beta'] - arch_params['beta']),
            'nu': abs(garch_params['nu'] - arch_params['nu'])
        }
        
        likelihood_diff = abs(garch_likelihood - arch_likelihood)
        
        return {
            'arch_params': arch_params,
            'arch_likelihood': arch_likelihood,
            'garch_params': garch_params,
            'garch_likelihood': garch_likelihood,
            'param_differences': param_diffs,
            'likelihood_difference': likelihood_diff,
            'improvement_over_arch': garch_likelihood > arch_likelihood
        }
    
    @classmethod
    def rolling_forecast_brett(cls, param_set: str = 'default', 
                              window_size: int = 200,
                              data_points: int = 500) -> Dict:
        """
        针对brett.csv的滚动预测
        
        Args:
            param_set: 参数集名称
            window_size: 滚动窗口大小
            data_points: 使用的数据点数
            
        Returns:
            预测结果字典
        """
        # 读取brett.csv数据
        df = pd.read_csv('brett.csv')
        returns = df['c_scaled'].values[:data_points]
        
        garch_predictions = []
        arch_predictions = []
        prediction_indices = []
        
        print(f"🔄 使用{param_set}参数集进行滚动预测")
        print(f"   数据点: {len(returns)}, 窗口大小: {window_size}")
        
        success_count = 0
        total_attempts = 0
        
        for i in range(window_size, len(returns)):
            total_attempts += 1
            window_data = returns[i-window_size:i]
            
            try:
                # 使用优化参数的garch_lib预测
                calc = cls.create_calculator(param_set, window_size + 10)
                calc.add_returns(window_data.tolist())
                
                garch_forecast = calc.forecast_volatility(1)
                garch_vol = garch_forecast.volatility
                garch_predictions.append(garch_vol)
                
                # arch库预测（作为基准）
                arch_model_obj = arch_model(window_data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
                arch_result = arch_model_obj.fit(disp='off', show_warning=False)
                arch_forecast = arch_result.forecast(horizon=1, reindex=False)
                arch_vol = np.sqrt(arch_forecast.variance.values[-1, 0])
                arch_predictions.append(arch_vol)
                
                prediction_indices.append(i)
                success_count += 1
                
                # 进度显示
                if total_attempts % 50 == 0:
                    progress = total_attempts / (len(returns) - window_size) * 100
                    print(f"   进度: {progress:.1f}% - garch_lib: {garch_vol:.4f}, arch: {arch_vol:.4f}")
                    
            except Exception as e:
                print(f"   预测失败 at index {i}: {str(e)}")
                continue
        
        # 计算统计指标
        if len(garch_predictions) > 0:
            garch_arr = np.array(garch_predictions)
            arch_arr = np.array(arch_predictions)
            
            correlation = np.corrcoef(garch_arr, arch_arr)[0, 1] if len(garch_arr) > 1 else 0
            mae = np.mean(np.abs(garch_arr - arch_arr))
            rmse = np.sqrt(np.mean((garch_arr - arch_arr)**2))
            mape = np.mean(np.abs((garch_arr - arch_arr) / arch_arr)) * 100
            
            return {
                'param_set': param_set,
                'success_count': success_count,
                'total_attempts': total_attempts,
                'success_rate': success_count / total_attempts,
                'garch_predictions': garch_predictions,
                'arch_predictions': arch_predictions,
                'prediction_indices': prediction_indices,
                'correlation': correlation,
                'mae': mae,
                'rmse': rmse,
                'mape': mape,
                'garch_mean': garch_arr.mean(),
                'arch_mean': arch_arr.mean(),
                'garch_std': garch_arr.std(),
                'arch_std': arch_arr.std()
            }
        else:
            return {'error': '没有成功的预测'}
    
    @classmethod
    def quick_grid_search(cls, data: np.ndarray, 
                         omega_range: Tuple[float, float] = (10.0, 25.0),
                         alpha_range: Tuple[float, float] = (0.15, 0.35),
                         beta_range: Tuple[float, float] = (0.60, 0.80),
                         grid_points: int = 5) -> Dict:
        """
        快速网格搜索（用于微调参数）
        
        Args:
            data: 收益率数据
            omega_range: omega参数范围
            alpha_range: alpha参数范围
            beta_range: beta参数范围
            grid_points: 每个参数的网格点数
            
        Returns:
            搜索结果
        """
        # 先用arch库估计mu和nu
        try:
            arch_model_obj = arch_model(data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
            arch_result = arch_model_obj.fit(disp='off', show_warning=False)
            mu = arch_result.params['mu']
            nu = arch_result.params['nu']
            arch_likelihood = arch_result.loglikelihood
        except:
            mu = data.mean()
            nu = 2.0
            arch_likelihood = -np.inf
        
        # 网格搜索
        omega_values = np.linspace(omega_range[0], omega_range[1], grid_points)
        alpha_values = np.linspace(alpha_range[0], alpha_range[1], grid_points)
        beta_values = np.linspace(beta_range[0], beta_range[1], grid_points)
        
        best_likelihood = -np.inf
        best_params = None
        results = []
        
        print(f"🔍 快速网格搜索: {grid_points}³ = {grid_points**3} 组合")
        
        total_combinations = grid_points ** 3
        combination_count = 0
        
        for omega in omega_values:
            for alpha in alpha_values:
                for beta in beta_values:
                    combination_count += 1
                    
                    # 检查平稳性约束
                    if alpha + beta >= 0.999:
                        continue
                    
                    try:
                        calc = gc.GarchCalculator(history_size=len(data) + 10)
                        calc.add_returns(data.tolist())
                        
                        params = gc.GarchParameters()
                        params.mu = mu
                        params.omega = omega
                        params.alpha = alpha
                        params.beta = beta
                        params.nu = nu
                        
                        calc.set_parameters(params)
                        likelihood = calc.calculate_log_likelihood()
                        
                        if np.isfinite(likelihood):
                            result = {
                                'omega': omega, 'alpha': alpha, 'beta': beta,
                                'mu': mu, 'nu': nu, 'likelihood': likelihood
                            }
                            results.append(result)
                            
                            if likelihood > best_likelihood:
                                best_likelihood = likelihood
                                best_params = result.copy()
                                
                    except:
                        continue
                    
                    if combination_count % 25 == 0:
                        progress = combination_count / total_combinations * 100
                        print(f"   进度: {progress:.1f}%")
        
        return {
            'best_params': best_params,
            'best_likelihood': best_likelihood,
            'arch_likelihood': arch_likelihood,
            'total_results': len(results),
            'improvement': best_likelihood > arch_likelihood if arch_likelihood != -np.inf else True
        }
    
    @classmethod
    def show_available_params(cls) -> None:
        """显示所有可用的参数集"""
        print("📋 可用的参数集:")
        print("=" * 60)
        
        for name, params in cls.OPTIMIZED_PARAMS.items():
            print(f"\n🎯 {name}:")
            print(f"   omega: {params['omega']:.6f}")
            print(f"   alpha: {params['alpha']:.6f}")
            print(f"   beta: {params['beta']:.6f}")
            print(f"   nu: {params['nu']:.6f}")
            if 'likelihood' in params:
                print(f"   似然值: {params['likelihood']:.6f}")
            print(f"   说明: {params['description']}")


def main():
    """演示使用方法"""
    print("🚀 Brett优化GARCH参数工具演示")
    print("=" * 60)
    
    # 显示可用参数集
    BrettOptimizedGarch.show_available_params()
    
    # 读取数据
    df = pd.read_csv('brett.csv')
    returns = df['c_scaled'].values[:300]
    
    print(f"\n📊 使用数据: {len(returns)} 个点")
    
    # 测试默认参数与arch库的对比
    print(f"\n🔍 默认参数与arch库对比:")
    comparison = BrettOptimizedGarch.compare_with_arch(returns, 'default')
    
    if 'error' not in comparison:
        print(f"   似然值差异: {comparison['likelihood_difference']:.6f}")
        print(f"   参数差异:")
        for param, diff in comparison['param_differences'].items():
            print(f"     {param}: {diff:.6f}")
        print(f"   garch_lib是否更优: {comparison['improvement_over_arch']}")
    
    # 快速网格搜索微调
    print(f"\n🔍 快速网格搜索微调:")
    grid_result = BrettOptimizedGarch.quick_grid_search(returns, grid_points=4)
    
    if grid_result['best_params']:
        best = grid_result['best_params']
        print(f"   最优参数: ω={best['omega']:.4f}, α={best['alpha']:.4f}, β={best['beta']:.4f}")
        print(f"   似然值: {best['likelihood']:.6f}")
        print(f"   改进程度: {grid_result['improvement']}")


if __name__ == "__main__":
    main() 