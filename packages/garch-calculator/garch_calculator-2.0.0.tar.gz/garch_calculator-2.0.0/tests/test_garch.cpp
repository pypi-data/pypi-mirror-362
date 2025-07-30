#include "../include/garch_calculator.h"
#include <iostream>
#include <vector>
#include <random>
#include <cassert>

using namespace garch;

int main() {
    std::cout << "=== C++ GARCH Calculator 基本测试 ===" << std::endl;
    
    try {
        // 1. 测试基本构造
        GarchCalculator calculator(100, 20);
        std::cout << "✓ GarchCalculator 构造成功" << std::endl;
        
        // 2. 测试参数设置
        GarchParameters params(0.00001, 0.1, 0.8, 1.5);
        calculator.setParameters(params);
        auto retrieved = calculator.getParameters();
        
        assert(std::abs(retrieved.omega - 0.00001) < 1e-8);
        assert(std::abs(retrieved.alpha - 0.1) < 1e-8);
        assert(std::abs(retrieved.beta - 0.8) < 1e-8);
        assert(std::abs(retrieved.nu - 1.5) < 1e-8);
        std::cout << "✓ 参数设置和获取测试通过" << std::endl;
        
        // 3. 测试数据添加
        std::vector<double> prices = {100.0, 100.1, 99.9, 100.2, 99.8, 100.5};
        bool success = calculator.addPricePoints(prices);
        assert(success);
        assert(calculator.getDataSize() == prices.size());
        std::cout << "✓ 价格数据添加测试通过" << std::endl;
        
        // 4. 测试对数收益率计算
        auto returns = calculator.getLogReturns();
        assert(returns.size() == prices.size() - 1);
        std::cout << "✓ 对数收益率计算测试通过" << std::endl;
        
        // 5. 测试波动率预测
        auto forecast = calculator.forecastVolatility(1);
        assert(forecast.volatility > 0);
        assert(forecast.variance > 0);
        std::cout << "✓ 波动率预测测试通过" << std::endl;
        
        // 6. 测试参数有效性检查
        GarchParameters invalid_params(0.0, 0.1, 0.8, 1.5); // omega = 0 无效
        assert(!invalid_params.isValid());
        
        GarchParameters valid_params(0.00001, 0.1, 0.85, 1.8);
        assert(valid_params.isValid());
        std::cout << "✓ 参数有效性检查测试通过" << std::endl;
        
        std::cout << "\n🎉 所有基本测试通过！" << std::endl;
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "❌ 测试失败: " << e.what() << std::endl;
        return 1;
    } catch (...) {
        std::cerr << "❌ 未知错误" << std::endl;
        return 1;
    }
} 