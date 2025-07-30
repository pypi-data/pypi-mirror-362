#!/usr/bin/env python3
import os
import glob
import pandas as pd
import numpy as np
import time
from datetime import datetime
import sys
import traceback

# 导入验证模块
from validate_aave import main as validate_single

def find_data_files():
    """查找所有数据文件"""
    pattern = "../garch_pro_service/backtest_data/bitget_*_USDT_*_data.npz"
    files = glob.glob(pattern)
    
    if not files:
        # 尝试其他可能的路径
        pattern = "./garch_pro_service/backtest_data/bitget_*_USDT_*_data.npz"
        files = glob.glob(pattern)
    
    print(f"找到 {len(files)} 个数据文件")
    return sorted(files)

def extract_symbol_from_path(file_path):
    """从文件路径提取币种名称"""
    basename = os.path.basename(file_path)
    parts = basename.split('_')
    if len(parts) >= 2:
        return parts[1]
    return "UNKNOWN"

def run_batch_validation():
    """批量运行验证"""
    print("🚀 开始批量验证所有数据文件")
    print("=" * 80)
    
    data_files = find_data_files()
    if not data_files:
        print("❌ 未找到任何数据文件")
        return
    
    results = []
    failed_files = []
    total_start_time = time.time()
    
    for i, file_path in enumerate(data_files, 1):
        symbol = extract_symbol_from_path(file_path)
        print(f"\n📋 [{i}/{len(data_files)}] 处理 {symbol}")
        print("-" * 60)
        
        try:
            file_start_time = time.time()
            arch_result, garch_result = validate_single(file_path)
            file_time = time.time() - file_start_time
            
            if arch_result and garch_result:
                # 计算各种指标
                param_errors = []
                params = ['omega', 'alpha', 'beta', 'nu']
                for param in params:
                    arch_val = arch_result[param]
                    garch_val = garch_result[param]
                    rel_diff = abs(garch_val - arch_val) / abs(arch_val) * 100 if abs(arch_val) > 0 else 0
                    param_errors.append(rel_diff)
                
                avg_param_error = np.mean(param_errors)
                ll_diff = garch_result['log_likelihood'] - arch_result['log_likelihood']
                
                # 预测精度比较
                forecast_comparison = {}
                if 'forecast_rmse' in arch_result and 'forecast_rmse' in garch_result:
                    arch_rmse = arch_result['forecast_rmse']
                    garch_rmse = garch_result['forecast_rmse']
                    rmse_diff = garch_rmse - arch_rmse
                    rmse_rel_diff = rmse_diff / arch_rmse * 100 if arch_rmse > 0 else 0
                    
                    arch_mae = arch_result['forecast_mae']
                    garch_mae = garch_result['forecast_mae']
                    mae_diff = garch_mae - arch_mae
                    mae_rel_diff = mae_diff / arch_mae * 100 if arch_mae > 0 else 0
                    
                    forecast_comparison = {
                        'arch_rmse': arch_rmse,
                        'garch_rmse': garch_rmse,
                        'rmse_diff': rmse_diff,
                        'rmse_rel_diff': rmse_rel_diff,
                        'arch_mae': arch_mae,
                        'garch_mae': garch_mae,
                        'mae_diff': mae_diff,
                        'mae_rel_diff': mae_rel_diff
                    }
                
                result_record = {
                    'symbol': symbol,
                    'file_path': file_path,
                    'success': True,
                    'file_time': file_time,
                    'arch_converged': arch_result['converged'],
                    'garch_converged': garch_result['converged'],
                    'arch_fit_time': arch_result['fit_time'],
                    'garch_fit_time': garch_result['fit_time'],
                    'arch_vol_time': arch_result['vol_prediction_time'],
                    'garch_vol_time': garch_result['vol_prediction_time'],
                    'fit_speedup': arch_result['fit_time'] / garch_result['fit_time'] if garch_result['fit_time'] > 0 else 0,
                    'vol_speedup': arch_result['vol_prediction_time'] / garch_result['vol_prediction_time'] if garch_result['vol_prediction_time'] > 0 else 0,
                    'avg_param_error': avg_param_error,
                    'll_diff': ll_diff,
                    'arch_omega': arch_result['omega'],
                    'garch_omega': garch_result['omega'],
                    'arch_alpha': arch_result['alpha'],
                    'garch_alpha': garch_result['alpha'],
                    'arch_beta': arch_result['beta'],
                    'garch_beta': garch_result['beta'],
                    'arch_nu': arch_result['nu'],
                    'garch_nu': garch_result['nu'],
                    'train_size': arch_result['train_size'],
                    'test_size': arch_result['test_size'],
                    **forecast_comparison
                }
                
                results.append(result_record)
                print(f"✅ {symbol} 验证成功 (耗时: {file_time:.2f}秒)")
                
            else:
                failed_files.append((symbol, file_path, "模型未收敛或运行失败"))
                print(f"❌ {symbol} 验证失败")
                
        except Exception as e:
            error_msg = str(e)
            failed_files.append((symbol, file_path, error_msg))
            print(f"❌ {symbol} 验证出错: {error_msg}")
            # print(traceback.format_exc())
    
    total_time = time.time() - total_start_time
    
    # 生成汇总报告
    generate_summary_report(results, failed_files, total_time)
    
    # 保存详细结果
    save_detailed_results(results, failed_files)

def generate_summary_report(results, failed_files, total_time):
    """生成汇总报告"""
    print("\n\n" + "="*100)
    print("📊 批量验证汇总报告")
    print("="*100)
    
    total_files = len(results) + len(failed_files)
    success_rate = len(results) / total_files * 100 if total_files > 0 else 0
    
    print(f"总文件数: {total_files}")
    print(f"成功验证: {len(results)} ({success_rate:.1f}%)")
    print(f"失败文件: {len(failed_files)}")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"平均每文件: {total_time/total_files:.2f}秒" if total_files > 0 else "")
    
    if failed_files:
        print(f"\n❌ 失败的文件:")
        for symbol, file_path, error in failed_files:
            print(f"  - {symbol}: {error}")
    
    if not results:
        print("\n❌ 没有成功的验证结果")
        return
    
    # 转换为DataFrame进行统计
    df = pd.DataFrame(results)
    
    print(f"\n📈 性能统计:")
    print(f"  平均拟合速度提升: {df['fit_speedup'].mean():.2f}x")
    print(f"  平均预测速度提升: {df['vol_speedup'].mean():.2f}x" if 'vol_speedup' in df.columns else "  预测速度: N/A")
    print(f"  平均参数误差: {df['avg_param_error'].mean():.2f}%")
    
    if 'rmse_rel_diff' in df.columns:
        print(f"\n🎯 预测精度统计:")
        better_count = (df['rmse_rel_diff'] < 0).sum()
        worse_count = (df['rmse_rel_diff'] > 5).sum()  # 超过5%认为明显更差
        similar_count = len(df) - better_count - worse_count
        
        print(f"  garch_lib预测更好: {better_count} ({better_count/len(df)*100:.1f}%)")
        print(f"  预测精度相似: {similar_count} ({similar_count/len(df)*100:.1f}%)")
        print(f"  arch预测更好: {worse_count} ({worse_count/len(df)*100:.1f}%)")
        print(f"  平均RMSE相对差异: {df['rmse_rel_diff'].mean():.2f}%")
    
    print(f"\n🔧 参数一致性:")
    consistency_levels = {
        'high': (df['avg_param_error'] < 5).sum(),
        'medium': ((df['avg_param_error'] >= 5) & (df['avg_param_error'] < 10)).sum(),
        'low': (df['avg_param_error'] >= 10).sum()
    }
    
    print(f"  高度一致(<5%): {consistency_levels['high']} ({consistency_levels['high']/len(df)*100:.1f}%)")
    print(f"  基本一致(5-10%): {consistency_levels['medium']} ({consistency_levels['medium']/len(df)*100:.1f}%)")
    print(f"  有差异(>10%): {consistency_levels['low']} ({consistency_levels['low']/len(df)*100:.1f}%)")
    
    # 找出最好和最差的案例
    if len(df) > 0:
        print(f"\n🏆 表现最好的币种:")
        if 'rmse_rel_diff' in df.columns:
            best_forecast = df.loc[df['rmse_rel_diff'].idxmin()]
            print(f"  预测精度最佳: {best_forecast['symbol']} (RMSE改善: {best_forecast['rmse_rel_diff']:.2f}%)")
        
        fastest = df.loc[df['fit_speedup'].idxmax()]
        print(f"  拟合速度最快: {fastest['symbol']} (提升: {fastest['fit_speedup']:.2f}x)")
        
        most_consistent = df.loc[df['avg_param_error'].idxmin()]
        print(f"  参数最一致: {most_consistent['symbol']} (误差: {most_consistent['avg_param_error']:.2f}%)")
        
        print(f"\n⚠️  需要关注的币种:")
        if 'rmse_rel_diff' in df.columns:
            worst_forecast = df.loc[df['rmse_rel_diff'].idxmax()]
            print(f"  预测精度最差: {worst_forecast['symbol']} (RMSE差异: {worst_forecast['rmse_rel_diff']:.2f}%)")
        
        least_consistent = df.loc[df['avg_param_error'].idxmax()]
        print(f"  参数差异最大: {least_consistent['symbol']} (误差: {least_consistent['avg_param_error']:.2f}%)")

def save_detailed_results(results, failed_files):
    """保存详细结果到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # 保存成功的结果
    if results:
        df = pd.DataFrame(results)
        csv_file = f"batch_validation_results_{timestamp}.csv"
        df.to_csv(csv_file, index=False)
        print(f"\n💾 详细结果已保存到: {csv_file}")
    
    # 保存失败的文件列表
    if failed_files:
        failed_df = pd.DataFrame(failed_files, columns=['symbol', 'file_path', 'error'])
        failed_csv = f"batch_validation_failed_{timestamp}.csv"
        failed_df.to_csv(failed_csv, index=False)
        print(f"💾 失败文件列表已保存到: {failed_csv}")

def main():
    """主函数"""
    print("🔍 GARCH库批量验证工具")
    print("对比garch_lib和Python arch库在所有可用数据上的表现")
    print()
    
    try:
        run_batch_validation()
        print(f"\n✅ 批量验证完成!")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  用户中断验证过程")
    except Exception as e:
        print(f"\n❌ 批量验证过程中出现严重错误: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 