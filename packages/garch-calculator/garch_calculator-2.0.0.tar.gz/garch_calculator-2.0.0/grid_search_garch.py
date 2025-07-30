#!/usr/bin/env python3
"""
针对brett.csv数据的GARCH参数网格搜索工具
目标：找到与arch库尽可能接近的参数组合
"""

import garch_lib as gc
import pandas as pd
import numpy as np
from arch import arch_model
import itertools
import time
from typing import Dict, List, Tuple, Optional
import json

class GarchGridSearch:
    """GARCH参数网格搜索类"""
    
    def __init__(self, data: np.ndarray, verbose: bool = True):
        """
        初始化网格搜索
        
        Args:
            data: 收益率数据
            verbose: 是否显示详细输出
        """
        self.data = data
        self.verbose = verbose
        self.results = []
        
        # 首先用arch库估计基准参数
        self._estimate_arch_baseline()
        
    def _estimate_arch_baseline(self):
        """使用arch库估计基准参数"""
        try:
            arch_model_obj = arch_model(self.data, vol='Garch', p=1, q=1, dist='ged', rescale=False)
            arch_result = arch_model_obj.fit(disp='off', show_warning=False)
            
            self.arch_params = {
                'mu': arch_result.params['mu'],
                'omega': arch_result.params['omega'],
                'alpha': arch_result.params['alpha[1]'],
                'beta': arch_result.params['beta[1]'],
                'nu': arch_result.params['nu']
            }
            self.arch_likelihood = arch_result.loglikelihood
            
            if self.verbose:
                print("🎯 arch库基准参数:")
                print(f"  mu: {self.arch_params['mu']:.6f}")
                print(f"  omega: {self.arch_params['omega']:.6f}")
                print(f"  alpha: {self.arch_params['alpha']:.6f}")
                print(f"  beta: {self.arch_params['beta']:.6f}")
                print(f"  nu: {self.arch_params['nu']:.6f}")
                print(f"  似然值: {self.arch_likelihood:.6f}")
                
        except Exception as e:
            print(f"❌ arch库估计失败: {e}")
            # 使用默认参数
            self.arch_params = {'mu': 0.0, 'omega': 20.0, 'alpha': 0.3, 'beta': 0.6, 'nu': 2.0}
            self.arch_likelihood = -np.inf
    
    def define_search_ranges(self, range_type: str = 'coarse') -> Dict[str, np.ndarray]:
        """
        定义搜索范围
        
        Args:
            range_type: 'coarse' 粗搜索, 'fine' 精搜索, 'adaptive' 自适应
            
        Returns:
            参数搜索范围字典
        """
        if range_type == 'coarse':
            # 粗搜索：覆盖较大范围
            ranges = {
                'mu': np.linspace(self.arch_params['mu'] - 5.0, self.arch_params['mu'] + 5.0, 5),
                'omega': np.linspace(5.0, 60.0, 8),  # 基于brett.csv观察到的范围
                'alpha': np.linspace(0.05, 0.8, 8),
                'beta': np.linspace(0.05, 0.8, 8),
                'nu': np.linspace(1.2, 4.0, 6)
            }
        elif range_type == 'fine':
            # 精搜索：围绕arch参数的细致搜索
            mu_range = max(3.0, abs(self.arch_params['mu']) * 0.2)
            omega_range = max(5.0, self.arch_params['omega'] * 0.3)
            
            ranges = {
                'mu': np.linspace(self.arch_params['mu'] - mu_range, 
                                self.arch_params['mu'] + mu_range, 7),
                'omega': np.linspace(max(1.0, self.arch_params['omega'] - omega_range),
                                   self.arch_params['omega'] + omega_range, 9),
                'alpha': np.linspace(max(0.01, self.arch_params['alpha'] - 0.2),
                                   min(0.9, self.arch_params['alpha'] + 0.2), 9),
                'beta': np.linspace(max(0.01, self.arch_params['beta'] - 0.2),
                                  min(0.9, self.arch_params['beta'] + 0.2), 9),
                'nu': np.linspace(max(1.1, self.arch_params['nu'] - 0.8),
                                min(5.0, self.arch_params['nu'] + 0.8), 7)
            }
        else:  # adaptive
            # 自适应：基于数据特征调整范围
            data_var = np.var(self.data)
            data_mean = np.mean(self.data)
            
            ranges = {
                'mu': np.linspace(data_mean - 3*np.sqrt(data_var), 
                                data_mean + 3*np.sqrt(data_var), 6),
                'omega': np.linspace(1.0, data_var * 2, 10),
                'alpha': np.linspace(0.02, 0.85, 12),
                'beta': np.linspace(0.02, 0.85, 12), 
                'nu': np.linspace(1.2, 4.0, 8)
            }
            
        # 确保平稳性约束在搜索过程中得到考虑
        # 我们在评估时检查 alpha + beta < 1
        
        return ranges
    
    def _evaluate_parameters(self, mu: float, omega: float, alpha: float, 
                           beta: float, nu: float) -> Optional[float]:
        """
        评估给定参数组合的似然值
        
        Returns:
            似然值，如果参数无效则返回None
        """
        # 检查参数约束
        if not (omega > 0 and alpha >= 0 and beta >= 0 and nu > 1.0):
            return None
            
        # 平稳性约束
        if alpha + beta >= 0.999:
            return None
            
        try:
            # 使用garch_lib计算似然值
            calc = gc.GarchCalculator(history_size=len(self.data) + 10)
            calc.add_returns(self.data.tolist())
            
            params = gc.GarchParameters()
            params.mu = mu
            params.omega = omega
            params.alpha = alpha
            params.beta = beta
            params.nu = nu
            
            calc.set_parameters(params)
            likelihood = calc.calculate_log_likelihood()
            
            if np.isfinite(likelihood) and likelihood > -1e6:
                return likelihood
            else:
                return None
                
        except Exception:
            return None
    
    def grid_search(self, range_type: str = 'coarse', max_combinations: int = 50000) -> Dict:
        """
        执行网格搜索
        
        Args:
            range_type: 搜索范围类型
            max_combinations: 最大搜索组合数
            
        Returns:
            搜索结果字典
        """
        ranges = self.define_search_ranges(range_type)
        
        # 计算总组合数
        total_combinations = np.prod([len(r) for r in ranges.values()])
        
        if self.verbose:
            print(f"\n🔍 开始{range_type}网格搜索")
            print(f"  搜索范围: {range_type}")
            print(f"  总组合数: {total_combinations:,}")
            for param, values in ranges.items():
                print(f"  {param}: [{values.min():.3f}, {values.max():.3f}] ({len(values)}个点)")
            
        if total_combinations > max_combinations:
            print(f"⚠️  组合数过多，自动降采样到 {max_combinations:,} 个组合")
            # 随机采样
            sample_indices = np.random.choice(total_combinations, max_combinations, replace=False)
        else:
            sample_indices = None
            
        # 执行搜索
        best_likelihood = -np.inf
        best_params = None
        current_combination = 0
        start_time = time.time()
        
        param_combinations = itertools.product(*ranges.values())
        
        for i, (mu, omega, alpha, beta, nu) in enumerate(param_combinations):
            if sample_indices is not None and i not in sample_indices:
                continue
                
            likelihood = self._evaluate_parameters(mu, omega, alpha, beta, nu)
            
            if likelihood is not None:
                result = {
                    'mu': mu, 'omega': omega, 'alpha': alpha, 'beta': beta, 'nu': nu,
                    'likelihood': likelihood,
                    'param_distance': self._calculate_param_distance(mu, omega, alpha, beta, nu)
                }
                self.results.append(result)
                
                if likelihood > best_likelihood:
                    best_likelihood = likelihood
                    best_params = result.copy()
                    
            current_combination += 1
            
            # 进度显示
            if self.verbose and current_combination % 1000 == 0:
                elapsed = time.time() - start_time
                rate = current_combination / elapsed
                eta = (max_combinations - current_combination) / rate if rate > 0 else 0
                print(f"  进度: {current_combination:,}/{max_combinations:,} "
                      f"({current_combination/max_combinations*100:.1f}%) "
                      f"ETA: {eta:.1f}s")
                
        elapsed_time = time.time() - start_time
        
        if self.verbose:
            print(f"\n✅ 网格搜索完成!")
            print(f"  耗时: {elapsed_time:.2f}秒")
            print(f"  有效组合: {len(self.results):,}")
            
        return {
            'best_params': best_params,
            'best_likelihood': best_likelihood,
            'total_evaluated': len(self.results),
            'search_time': elapsed_time,
            'arch_likelihood': self.arch_likelihood
        }
    
    def _calculate_param_distance(self, mu: float, omega: float, alpha: float, 
                                beta: float, nu: float) -> float:
        """计算与arch库参数的距离"""
        distances = [
            abs(mu - self.arch_params['mu']) / max(abs(self.arch_params['mu']), 1.0),
            abs(omega - self.arch_params['omega']) / self.arch_params['omega'],
            abs(alpha - self.arch_params['alpha']) / self.arch_params['alpha'],
            abs(beta - self.arch_params['beta']) / max(self.arch_params['beta'], 0.1),
            abs(nu - self.arch_params['nu']) / self.arch_params['nu']
        ]
        return np.mean(distances)
    
    def get_top_results(self, n: int = 10, sort_by: str = 'likelihood') -> List[Dict]:
        """
        获取最佳结果
        
        Args:
            n: 返回前n个结果
            sort_by: 排序依据 ('likelihood' 或 'param_distance')
            
        Returns:
            最佳结果列表
        """
        if not self.results:
            return []
            
        if sort_by == 'likelihood':
            sorted_results = sorted(self.results, key=lambda x: x['likelihood'], reverse=True)
        else:  # param_distance
            sorted_results = sorted(self.results, key=lambda x: x['param_distance'])
            
        return sorted_results[:n]
    
    def analyze_results(self) -> None:
        """分析搜索结果"""
        if not self.results:
            print("❌ 没有有效的搜索结果")
            return
            
        print("\n📊 搜索结果分析")
        print("=" * 80)
        
        # 最佳似然值结果
        best_likelihood_result = max(self.results, key=lambda x: x['likelihood'])
        print(f"\n🎯 最佳似然值参数:")
        print(f"  mu: {best_likelihood_result['mu']:.6f}")
        print(f"  omega: {best_likelihood_result['omega']:.6f}")
        print(f"  alpha: {best_likelihood_result['alpha']:.6f}")
        print(f"  beta: {best_likelihood_result['beta']:.6f}")
        print(f"  nu: {best_likelihood_result['nu']:.6f}")
        print(f"  似然值: {best_likelihood_result['likelihood']:.6f}")
        print(f"  与arch库似然值差异: {abs(best_likelihood_result['likelihood'] - self.arch_likelihood):.6f}")
        
        # 最接近arch参数的结果
        closest_param_result = min(self.results, key=lambda x: x['param_distance'])
        print(f"\n🎯 最接近arch库的参数:")
        print(f"  mu: {closest_param_result['mu']:.6f}")
        print(f"  omega: {closest_param_result['omega']:.6f}")
        print(f"  alpha: {closest_param_result['alpha']:.6f}")
        print(f"  beta: {closest_param_result['beta']:.6f}")
        print(f"  nu: {closest_param_result['nu']:.6f}")
        print(f"  似然值: {closest_param_result['likelihood']:.6f}")
        print(f"  参数距离: {closest_param_result['param_distance']:.6f}")
        
        # 统计分析
        likelihoods = [r['likelihood'] for r in self.results]
        distances = [r['param_distance'] for r in self.results]
        
        print(f"\n📈 统计信息:")
        print(f"  似然值范围: [{min(likelihoods):.3f}, {max(likelihoods):.3f}]")
        print(f"  似然值均值: {np.mean(likelihoods):.3f}")
        print(f"  参数距离均值: {np.mean(distances):.3f}")
        print(f"  在arch似然值±1.0内的参数组合: {sum(1 for ll in likelihoods if abs(ll - self.arch_likelihood) <= 1.0)}")
        
    def save_results(self, filename: str) -> None:
        """保存搜索结果到文件"""
        result_data = {
            'arch_params': self.arch_params,
            'arch_likelihood': self.arch_likelihood,
            'search_results': self.results,
            'best_likelihood': max(self.results, key=lambda x: x['likelihood']) if self.results else None,
            'closest_params': min(self.results, key=lambda x: x['param_distance']) if self.results else None
        }
        
        with open(filename, 'w') as f:
            json.dump(result_data, f, indent=2)
            
        print(f"💾 结果已保存到: {filename}")


def main():
    """主函数：针对brett.csv进行网格搜索"""
    
    print("🚀 brett.csv GARCH参数网格搜索")
    print("=" * 60)
    
    # 读取数据
    df = pd.read_csv('brett.csv')
    returns = df['c_scaled'].values[:500]  # 使用前500个数据点
    
    print(f"📊 数据信息:")
    print(f"  数据点数: {len(returns)}")
    print(f"  均值: {returns.mean():.6f}")
    print(f"  标准差: {returns.std():.6f}")
    
    # 创建网格搜索对象
    grid_search = GarchGridSearch(returns, verbose=True)
    
    # 执行粗搜索
    print("\n" + "="*60)
    coarse_result = grid_search.grid_search(range_type='coarse', max_combinations=20000)
    grid_search.analyze_results()
    
    # 基于粗搜索结果进行精搜索
    if coarse_result['best_params']:
        print("\n" + "="*60)
        print("🔍 基于最佳结果进行精细搜索...")
        
        # 更新arch_params为粗搜索的最佳结果，用于精搜索
        best = coarse_result['best_params']
        grid_search.arch_params = {
            'mu': best['mu'],
            'omega': best['omega'], 
            'alpha': best['alpha'],
            'beta': best['beta'],
            'nu': best['nu']
        }
        
        # 清空之前的结果
        grid_search.results = []
        
        fine_result = grid_search.grid_search(range_type='fine', max_combinations=15000)
        grid_search.analyze_results()
    
    # 保存结果
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    grid_search.save_results(f'brett_garch_grid_search_{timestamp}.json')
    
    # 显示最佳参数的推荐使用方式
    if grid_search.results:
        best = max(grid_search.results, key=lambda x: x['likelihood'])
        print(f"\n💡 推荐的GARCH参数（基于网格搜索）:")
        print(f"   omega = {best['omega']:.6f}")
        print(f"   alpha = {best['alpha']:.6f}")
        print(f"   beta = {best['beta']:.6f}")
        print(f"   nu = {best['nu']:.6f}")
        print(f"   似然值 = {best['likelihood']:.6f}")
        
        print(f"\n📝 使用示例:")
        print(f"   params = gc.GarchParameters()")
        print(f"   params.mu = {best['mu']:.6f}")
        print(f"   params.omega = {best['omega']:.6f}")
        print(f"   params.alpha = {best['alpha']:.6f}")
        print(f"   params.beta = {best['beta']:.6f}")
        print(f"   params.nu = {best['nu']:.6f}")
        print(f"   calc.set_parameters(params)")


if __name__ == "__main__":
    main() 