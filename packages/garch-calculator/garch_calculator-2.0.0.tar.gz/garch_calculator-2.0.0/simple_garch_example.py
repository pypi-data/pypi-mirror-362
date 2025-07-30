#!/usr/bin/env python3
"""
最简单的GARCH示例程序
使用yfinance获取股票数据，用garch_lib进行GARCH建模
现在直接使用收益率数据，与arch库保持一致
garch_lib内部自动使用改进的L-BFGS多起始点优化
"""

import numpy as np
import yfinance as yf
import garch_lib as gc

def main():
    # 1. 下载股票数据 (苹果股票，1年数据)
    print("📊 下载AAPL股票数据...")
    stock = yf.Ticker("AAPL")
    data = stock.history(period="1y")
    
    # 2. 计算对数收益率 (与arch库保持一致)
    print("📈 计算对数收益率...")
    prices = data['Close'].values
    returns = np.log(prices[1:] / prices[:-1])
    
    # 3. 去除均值 (中心化处理，与arch库保持一致)
    returns = returns - returns.mean()
    
    print(f"📋 数据统计:")
    print(f"   数据点数: {len(returns)}")
    print(f"   收益率均值: {returns.mean():.6f}")
    print(f"   收益率标准差: {returns.std():.6f}")
    
    # 4. 创建GARCH计算器并直接添加收益率数据
    print("⚡ 创建GARCH模型...")
    calc = gc.GarchCalculator(history_size=len(returns) + 10)
    
    # 直接使用收益率，不再需要价格转换
    calc.add_returns(returns.tolist())
    
    # 5. 显示初始状态
    print(f"\n🔧 初始状态:")
    print(f"   初始波动率: {calc.get_current_volatility():.6f}")
    print(f"   初始方差: {calc.get_current_variance():.6f}")
    
    # 6. 自动估计GARCH参数 (内部使用改进的L-BFGS多起始点优化)
    print(f"\n⚡ 估计GARCH参数...")
    print(f"   🔍 使用改进的L-BFGS多起始点优化算法...")
    
    result = calc.estimate_parameters()
    params = result.parameters
    
    print(f"\n✅ GARCH(1,1)模型结果:")
    print(f"   收敛状态: {'✅' if result.converged else '❌'}")
    print(f"   对数似然值: {result.log_likelihood:.6f}")
    print(f"   迭代次数: {result.iterations}")
    print(f"   优化时间: {result.convergence_time_ms:.2f} ms")
    print(f"   ω (omega): {params.omega:.6f}")
    print(f"   α (alpha): {params.alpha:.6f}")  
    print(f"   β (beta):  {params.beta:.6f}")
    print(f"   ν (nu):    {params.nu:.6f}")
    print(f"   持续性 (α+β): {params.alpha + params.beta:.6f}")
    
    # 7. 【关键步骤】更新模型状态，重新计算当前条件方差
    print(f"\n🔄 更新模型状态...")
    update_success = calc.update_model()
    print(f"   更新成功: {'✅' if update_success else '❌'}")
    
    # 8. 显示最终结果
    current_volatility = calc.get_current_volatility()
    current_variance = calc.get_current_variance()
    
    print(f"\n📊 最终结果:")
    print(f"   当前波动率: {current_volatility:.6f}")
    print(f"   当前方差: {current_variance:.6f}")
    print(f"   数据标准差: {returns.std():.6f}")
    print(f"   波动率 vs 标准差比率: {current_volatility / returns.std():.3f}")
    
    # 9. 预测未来1天的波动率
    forecast = calc.forecast_volatility(1)
    print(f"   明天预测波动率: {forecast.volatility:.6f}")
    print(f"   预测置信度: {forecast.confidence_score:.3f}")
    
    # 10. 计算信息准则
    aic = calc.calculate_aic()
    bic = calc.calculate_bic()
    print(f"   AIC: {aic:.2f}")
    print(f"   BIC: {bic:.2f}")
    
    # 11. 验证波动率是否会随不同股票而变化
    print(f"\n🔍 验证其他股票的波动率:")
    test_stocks = ["MSFT", "GOOGL", "TSLA"]
    
    for symbol in test_stocks:
        try:
            test_stock = yf.Ticker(symbol)
            test_data = test_stock.history(period="6mo")  # 6个月数据
            
            if test_data.empty:
                continue
                
            test_prices = test_data['Close'].values
            test_returns = np.log(test_prices[1:] / test_prices[:-1])
            test_returns = test_returns - test_returns.mean()
            
            # 创建新的计算器
            test_calc = gc.GarchCalculator()
            test_calc.add_returns(test_returns.tolist())
            
            # 自动估计参数 (内部使用L-BFGS)
            test_result = test_calc.estimate_parameters()
            test_calc.update_model()  # 关键步骤！
            
            test_volatility = test_calc.get_current_volatility()
            convergence = "✅" if test_result.converged else "❌"
            print(f"   {symbol}: 波动率={test_volatility:.6f}, 标准差={test_returns.std():.6f}, 收敛={convergence}")
            
        except Exception as e:
            print(f"   {symbol} 数据获取失败: {e}")
    
    # 12. 优化算法总结
    print(f"\n🎯 优化算法总结:")
    print(f"   ✅ 自动多起始点L-BFGS优化")
    print(f"   ✅ 智能起始点生成 (基于数据特征)")
    print(f"   ✅ 鲁棒参数变换 (对数空间优化)")
    print(f"   ✅ 改进的线搜索 (Wolfe条件)")
    print(f"   ✅ 高效内存管理 (L-BFGS历史)")
    
    print(f"\n✅ 分析完成！GARCH模型现在使用高级优化算法自动收敛。")

if __name__ == "__main__":
    main() 