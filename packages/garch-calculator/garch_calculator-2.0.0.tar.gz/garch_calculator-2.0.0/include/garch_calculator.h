#ifndef GARCH_CALCULATOR_H
#define GARCH_CALCULATOR_H

#include <vector>
#include <string>
#include <memory>
#include <unordered_map>
#include <mutex>
#include <cstdint>
#include <cmath>
#include <limits>
#include <boost/circular_buffer.hpp>

namespace garch {

// GARCH模型参数结构
struct GarchParameters {
    double mu;                  // 均值参数 (μ) - 匹配arch库
    double omega;               // 常数项 (ω)
    double alpha;               // ARCH参数 (α) 
    double beta;                // GARCH参数 (β)
    double nu;                  // GED形状参数 (ν)
    
    // 默认构造函数 - 使用更合理的初始值
    GarchParameters() : mu(0.0), omega(10.0), alpha(0.1), beta(0.8), nu(2.0) {}
    
    // 带参数构造函数
    GarchParameters(double mu_, double omega_, double alpha_, double beta_, double nu_)
        : mu(mu_), omega(omega_), alpha(alpha_), beta(beta_), nu(nu_) {}
        
    // 兼容旧版本的构造函数（不包含mu）
    GarchParameters(double omega_, double alpha_, double beta_, double nu_)
        : mu(0.0), omega(omega_), alpha(alpha_), beta(beta_), nu(nu_) {}
        
    // 检查参数有效性 (匹配 arch 库约束)
    bool isValid() const {
        return omega > 0.0 && alpha >= 0.0 && beta >= 0.0 && 
               (alpha + beta) < 1.0 && nu > 1.0 && 
               std::isfinite(omega) && std::isfinite(alpha) && 
               std::isfinite(beta) && std::isfinite(nu);
    }
    
    // 计算持续性 (persistence)
    double getPersistence() const { return alpha + beta; }
    
    // 计算无条件方差
    double getUnconditionalVariance() const {
        return omega / (1.0 - alpha - beta);
    }
    
    // === 预设参数功能 ===
    
    // 创建Brett数据优化的默认参数（基于网格搜索结果）
    static GarchParameters createBrettOptimized();
    
    // 创建高波动率期间的参数
    static GarchParameters createHighVolatility();
    
    // 创建稳定期间的参数
    static GarchParameters createStablePeriod();
    
    // 创建接近arch库的参数
    static GarchParameters createArchLike();
    
    // 创建基于数据特征的自适应参数
    static GarchParameters createAdaptive(double data_variance, double data_mean = 0.0);
    
    // 获取所有可用的预设参数名称
    static std::vector<std::string> getPresetNames();
    
    // 根据名称创建预设参数
    static GarchParameters createPreset(const std::string& preset_name);
};

// 价格数据点结构
struct PricePoint {
    int64_t timestamp;          // 时间戳
    double price;               // 价格
    double log_return;          // 对数收益率
    
    PricePoint() : timestamp(0), price(0.0), log_return(0.0) {}
    PricePoint(int64_t ts, double p, double lr) 
        : timestamp(ts), price(p), log_return(lr) {}
};

// 波动率预测结果结构
struct VolatilityForecast {
    int64_t timestamp;          // 预测时间戳
    double volatility;          // 预测波动率 (标准差)
    double variance;            // 预测方差
    double confidence_score;    // 置信度 (0-1)
    int forecast_horizon;       // 预测步数
    
    VolatilityForecast() : timestamp(0), volatility(0.0), variance(0.0), 
                          confidence_score(0.0), forecast_horizon(0) {}
};

// 模型估计结果结构
struct EstimationResult {
    GarchParameters parameters;  // 估计的参数
    double log_likelihood;       // 对数似然值
    double aic;                  // 赤池信息准则
    double bic;                  // 贝叶斯信息准则
    int iterations;              // 优化迭代次数
    double convergence_time_ms;  // 收敛时间(毫秒)
    bool converged;              // 是否收敛
    
    EstimationResult() : log_likelihood(-std::numeric_limits<double>::infinity()),
                        aic(std::numeric_limits<double>::infinity()),
                        bic(std::numeric_limits<double>::infinity()),
                        iterations(0), convergence_time_ms(0.0), converged(false) {}
};

// 主要的GARCH计算器类
class GarchCalculator {
public:
    // 构造函数
    explicit GarchCalculator(size_t history_size = 1000, size_t min_samples = 50);
    
    // 析构函数
    ~GarchCalculator() = default;
    
    // 禁用拷贝，允许移动
    GarchCalculator(const GarchCalculator&) = delete;
    GarchCalculator& operator=(const GarchCalculator&) = delete;
    GarchCalculator(GarchCalculator&&) = default;
    GarchCalculator& operator=(GarchCalculator&&) = default;
    
    // === 核心功能接口 ===
    
    // 添加新的价格数据点 (增量计算)
    bool addPricePoint(double price, int64_t timestamp = 0);
    
    // 批量添加价格数据
    bool addPricePoints(const std::vector<double>& prices, 
                       const std::vector<int64_t>& timestamps = {});
    
    // === 新增：直接添加收益率数据（与arch库保持一致）===
    
    // 添加单个收益率数据点
    bool addReturn(double return_value, int64_t timestamp = 0);
    
    // 批量添加收益率数据
    bool addReturns(const std::vector<double>& returns, 
                   const std::vector<int64_t>& timestamps = {});
    
    // 更新GARCH模型状态 (基于最新收益率)
    bool updateModel();
    
    // 估计GARCH参数 (使用最大似然估计)
    EstimationResult estimateParameters();
    
    // 预测未来波动率
    VolatilityForecast forecastVolatility(int horizon = 1) const;
    
    // === 参数管理 ===
    
    // 设置GARCH参数
    void setParameters(const GarchParameters& params);
    
    // 获取当前参数
    GarchParameters getParameters() const;
    
    // 重置参数为默认值
    void resetParameters();
    
    // === 状态查询 ===
    
    // 获取当前方差
    double getCurrentVariance() const;
    
    // 获取当前波动率 (标准差)
    double getCurrentVolatility() const;
    
    // 获取历史数据点数量
    size_t getDataSize() const;
    
    // 获取对数收益率序列
    std::vector<double> getLogReturns() const;
    
    // 获取方差序列
    std::vector<double> getVarianceSeries() const;
    
    // 检查是否有足够数据进行估计
    bool hasEnoughData() const;
    
    // === 诊断和统计 ===
    
    // 计算对数似然值
    double calculateLogLikelihood() const;
    double calculateLogLikelihood(const GarchParameters& params) const;
    
    // === 新增：匹配 arch 库的核心计算方法 ===
    
    // 计算 GED 对数似然 (匹配 arch 库实现)
    double calculateGedLogLikelihood(const std::vector<double>& residuals,
                                    const std::vector<double>& sigma_t,
                                    double nu) const;
    
    // 计算条件方差序列 (匹配 arch 库)
    std::vector<double> calculateConditionalVariances(const std::vector<double>& residuals, 
                                                      const GarchParameters& params) const;
    
    // 计算信息准则
    double calculateAIC() const;
    double calculateBIC() const;
    
    // 计算置信度分数
    double calculateConfidenceScore() const;
    
    // === 配置管理 ===
    
    // 设置历史数据大小
    void setHistorySize(size_t size);
    
    // 设置最小样本数要求
    void setMinSamples(size_t min_samples);
    
    // 获取配置信息
    std::string getConfigInfo() const;
    
    // === 线程安全 ===
    
    // 启用/禁用线程安全模式
    void setThreadSafe(bool enable);
    
    // 清除所有数据
    void clear();

private:
    // === 内部计算方法 ===
    
    // 计算对数收益率
    static double calculateLogReturn(double current_price, double previous_price);
    
    // 计算GED密度函数
    static double calculateGedDensity(double x, double sigma, double nu);
    
    // 数值优化求解参数
    EstimationResult optimizeParameters();
    
    // 计算梯度
    void calculateGradient(const std::vector<double>& log_returns,
                          const GarchParameters& params,
                          std::vector<double>& gradient) const;
    
    // === BFGS优化算法相关方法 ===
    
    // BFGS优化主函数
    EstimationResult optimizeWithBFGS(const GarchParameters& initial_params);
    
    // 改进的L-BFGS多起始点优化方法
    EstimationResult optimizeWithAdvancedLBFGS(double sample_variance, const std::vector<double>& log_returns);
    
    // L-BFGS核心优化器
    EstimationResult optimizeWithLBFGS(const GarchParameters& initial_params, int memory_size = 10);
    
    // 智能起始点生成
    std::vector<GarchParameters> generateSmartStartingPoints(double sample_variance, const std::vector<double>& log_returns);
    
    // 鲁棒参数变换（对数空间）
    std::vector<double> transformToUnconstrainedSpace(const GarchParameters& params) const;
    GarchParameters transformFromUnconstrainedSpace(const std::vector<double>& unconstrained_params) const;
    
    // 改进的线搜索（更强的Wolfe条件）
    double robustLineSearch(const GarchParameters& current_params,
                           const std::vector<double>& gradient,
                           const std::vector<double>& direction,
                           double initial_step = 1.0) const;
    
    // L-BFGS方向计算
    std::vector<double> computeLBFGSDirection(
        const std::vector<double>& grad,
        const std::vector<std::vector<double>>& s_history,
        const std::vector<std::vector<double>>& y_history,
        const std::vector<double>& rho_history,
        int memory_size) const;
    
    // 计算分析梯度 (匹配 arch 库)
    void calculateAnalyticalGradient(const GarchParameters& params, 
                                    std::vector<double>& gradient) const;
    
    // 线搜索算法（Wolfe条件）
    double lineSearch(const GarchParameters& current_params,
                     const std::vector<double>& gradient,
                     const std::vector<double>& direction,
                     double initial_step = 1.0) const;
    
    // 更新BFGS Hessian近似
    void updateBFGSHessian(std::vector<std::vector<double>>& H,
                          const std::vector<double>& s,
                          const std::vector<double>& y) const;
    
    // 参数向量转换工具
    std::vector<double> parametersToVector(const GarchParameters& params) const;
    GarchParameters vectorToParameters(const std::vector<double>& vec) const;
    
    // 约束优化：将参数投影到可行域
    std::vector<double> projectToFeasibleRegion(const std::vector<double>& params) const;
    
    // 验证参数边界
    GarchParameters constrainParameters(const GarchParameters& params) const;
    
    // 获取当前时间戳
    static int64_t getCurrentTimestamp();
    
    // === 私有数据成员 ===
    
    // 历史价格数据 (使用循环缓冲区提高性能)
    boost::circular_buffer<PricePoint> price_history_;
    
    // GARCH模型参数
    GarchParameters parameters_;
    
    // 当前方差估计
    double current_variance_;
    
    // 方差历史序列 (用于预测)
    std::vector<double> variance_history_;
    
    // 配置参数
    size_t min_samples_;
    
    // 线程安全
    mutable std::mutex mutex_;
    bool thread_safe_;
    
    // 缓存和优化
    mutable std::unordered_map<std::string, double> density_cache_;
    
    // 统计信息
    int64_t last_update_time_;
    size_t update_count_;
};

// === 工具函数 ===

// 计算序列的基本统计量
struct BasicStats {
    double mean;
    double variance;
    double std_dev;
    double skewness;
    double kurtosis;
    size_t count;
    
    BasicStats() : mean(0), variance(0), std_dev(0), skewness(0), kurtosis(0), count(0) {}
};

// 计算基本统计量
BasicStats calculateBasicStats(const std::vector<double>& data);

// 计算自相关函数
std::vector<double> calculateAutocorrelation(const std::vector<double>& data, int max_lag = 20);

// Ljung-Box检验统计量 (用于检验序列相关性)
double calculateLjungBoxStatistic(const std::vector<double>& residuals, int lag = 10);

// 计算VaR (风险价值)
double calculateVaR(double volatility, double confidence_level = 0.05);

// 计算ES (期望损失)
double calculateExpectedShortfall(double volatility, double confidence_level = 0.05);

} // namespace garch

#endif // GARCH_CALCULATOR_H 