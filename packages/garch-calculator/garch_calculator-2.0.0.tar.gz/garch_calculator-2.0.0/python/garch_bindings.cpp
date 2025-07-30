#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include <pybind11/chrono.h>
#include "../include/garch_calculator.h"

namespace py = pybind11;

PYBIND11_MODULE(_garch_calculator, m) {
    m.doc() = "High-Performance GARCH Calculator with Incremental Updates";

    // === 数据结构绑定 ===
    
    py::class_<garch::GarchParameters>(m, "GarchParameters")
        .def(py::init<>())
        .def(py::init<double, double, double, double>(),
             py::arg("omega"), py::arg("alpha"), py::arg("beta"), py::arg("nu"))
        .def(py::init<double, double, double, double, double>(),
             py::arg("mu"), py::arg("omega"), py::arg("alpha"), py::arg("beta"), py::arg("nu"))
        .def_readwrite("mu", &garch::GarchParameters::mu, "Mean parameter (μ)")
        .def_readwrite("omega", &garch::GarchParameters::omega, "Constant term (ω)")
        .def_readwrite("alpha", &garch::GarchParameters::alpha, "ARCH parameter (α)")
        .def_readwrite("beta", &garch::GarchParameters::beta, "GARCH parameter (β)")
        .def_readwrite("nu", &garch::GarchParameters::nu, "GED shape parameter (ν)")
        .def("is_valid", &garch::GarchParameters::isValid, "Check if parameters are valid")
        .def("get_persistence", &garch::GarchParameters::getPersistence, "Get persistence (α + β)")
        .def("get_unconditional_variance", &garch::GarchParameters::getUnconditionalVariance,
             "Get unconditional variance")
        // === 预设参数静态方法 ===
        .def_static("create_brett_optimized", &garch::GarchParameters::createBrettOptimized,
                   "Create Brett-optimized parameters based on grid search results")
        .def_static("create_high_volatility", &garch::GarchParameters::createHighVolatility,
                   "Create parameters for high volatility periods")
        .def_static("create_stable_period", &garch::GarchParameters::createStablePeriod,
                   "Create parameters for stable periods")
        .def_static("create_arch_like", &garch::GarchParameters::createArchLike,
                   "Create parameters similar to arch library estimates")
        .def_static("create_adaptive", &garch::GarchParameters::createAdaptive,
                   py::arg("data_variance"), py::arg("data_mean") = 0.0,
                   "Create adaptive parameters based on data characteristics")
        .def_static("get_preset_names", &garch::GarchParameters::getPresetNames,
                   "Get list of available preset parameter names")
        .def_static("create_preset", &garch::GarchParameters::createPreset,
                   py::arg("preset_name"),
                   "Create parameters from preset name")
        .def("__repr__", [](const garch::GarchParameters& p) {
            return "GarchParameters(mu=" + std::to_string(p.mu) +
                   ", omega=" + std::to_string(p.omega) +
                   ", alpha=" + std::to_string(p.alpha) +
                   ", beta=" + std::to_string(p.beta) +
                   ", nu=" + std::to_string(p.nu) + ")";
        });

    py::class_<garch::PricePoint>(m, "PricePoint")
        .def(py::init<>())
        .def(py::init<int64_t, double, double>(),
             py::arg("timestamp"), py::arg("price"), py::arg("log_return"))
        .def_readwrite("timestamp", &garch::PricePoint::timestamp)
        .def_readwrite("price", &garch::PricePoint::price)
        .def_readwrite("log_return", &garch::PricePoint::log_return)
        .def("__repr__", [](const garch::PricePoint& p) {
            return "PricePoint(timestamp=" + std::to_string(p.timestamp) +
                   ", price=" + std::to_string(p.price) +
                   ", log_return=" + std::to_string(p.log_return) + ")";
        });

    py::class_<garch::VolatilityForecast>(m, "VolatilityForecast")
        .def(py::init<>())
        .def_readwrite("timestamp", &garch::VolatilityForecast::timestamp)
        .def_readwrite("volatility", &garch::VolatilityForecast::volatility)
        .def_readwrite("variance", &garch::VolatilityForecast::variance)
        .def_readwrite("confidence_score", &garch::VolatilityForecast::confidence_score)
        .def_readwrite("forecast_horizon", &garch::VolatilityForecast::forecast_horizon)
        .def("__repr__", [](const garch::VolatilityForecast& f) {
            return "VolatilityForecast(volatility=" + std::to_string(f.volatility) +
                   ", variance=" + std::to_string(f.variance) +
                   ", confidence=" + std::to_string(f.confidence_score) +
                   ", horizon=" + std::to_string(f.forecast_horizon) + ")";
        });

    py::class_<garch::EstimationResult>(m, "EstimationResult")
        .def(py::init<>())
        .def_readwrite("parameters", &garch::EstimationResult::parameters)
        .def_readwrite("log_likelihood", &garch::EstimationResult::log_likelihood)
        .def_readwrite("aic", &garch::EstimationResult::aic)
        .def_readwrite("bic", &garch::EstimationResult::bic)
        .def_readwrite("iterations", &garch::EstimationResult::iterations)
        .def_readwrite("convergence_time_ms", &garch::EstimationResult::convergence_time_ms)
        .def_readwrite("converged", &garch::EstimationResult::converged)
        .def("__repr__", [](const garch::EstimationResult& r) {
            return "EstimationResult(converged=" + std::to_string(r.converged) +
                   ", log_likelihood=" + std::to_string(r.log_likelihood) +
                   ", aic=" + std::to_string(r.aic) +
                   ", iterations=" + std::to_string(r.iterations) + ")";
        });

    py::class_<garch::BasicStats>(m, "BasicStats")
        .def(py::init<>())
        .def_readwrite("mean", &garch::BasicStats::mean)
        .def_readwrite("variance", &garch::BasicStats::variance)
        .def_readwrite("std_dev", &garch::BasicStats::std_dev)
        .def_readwrite("skewness", &garch::BasicStats::skewness)
        .def_readwrite("kurtosis", &garch::BasicStats::kurtosis)
        .def_readwrite("count", &garch::BasicStats::count);

    // === 主要的GARCH计算器类 ===
    
    py::class_<garch::GarchCalculator>(m, "GarchCalculator")
        .def(py::init<size_t, size_t>(),
             py::arg("history_size") = 1000, py::arg("min_samples") = 50,
             "Create GARCH Calculator with specified history size and minimum samples")
        
        // === 核心功能 ===
        .def("add_price_point", &garch::GarchCalculator::addPricePoint,
             py::arg("price"), py::arg("timestamp") = 0,
             "Add a single price point (incremental update)")
        .def("add_price_points", &garch::GarchCalculator::addPricePoints,
             py::arg("prices"), py::arg("timestamps") = std::vector<int64_t>{},
             "Add multiple price points")
        
        // === 新增：直接添加收益率数据（与arch库保持一致）===
        .def("add_return", &garch::GarchCalculator::addReturn,
             py::arg("return_value"), py::arg("timestamp") = 0,
             "Add a single return value (matches arch library input)")
        .def("add_returns", &garch::GarchCalculator::addReturns,
             py::arg("returns"), py::arg("timestamps") = std::vector<int64_t>{},
             "Add multiple return values")
        .def("update_model", &garch::GarchCalculator::updateModel,
             "Update GARCH model state based on latest return")
        .def("estimate_parameters", &garch::GarchCalculator::estimateParameters,
             "Estimate GARCH parameters using maximum likelihood")
        .def("forecast_volatility", &garch::GarchCalculator::forecastVolatility,
             py::arg("horizon") = 1,
             "Forecast future volatility")
        
        // === 参数管理 ===
        .def("set_parameters", &garch::GarchCalculator::setParameters,
             py::arg("params"),
             "Set GARCH parameters")
        .def("get_parameters", &garch::GarchCalculator::getParameters,
             "Get current GARCH parameters")
        .def("reset_parameters", &garch::GarchCalculator::resetParameters,
             "Reset parameters to default values")
        
        // === 状态查询 ===
        .def("get_current_variance", &garch::GarchCalculator::getCurrentVariance,
             "Get current variance estimate")
        .def("get_current_volatility", &garch::GarchCalculator::getCurrentVolatility,
             "Get current volatility estimate")
        .def("get_data_size", &garch::GarchCalculator::getDataSize,
             "Get number of historical data points")
        .def("get_log_returns", &garch::GarchCalculator::getLogReturns,
             "Get log returns series")
        .def("get_variance_series", &garch::GarchCalculator::getVarianceSeries,
             "Get variance series")
        .def("has_enough_data", &garch::GarchCalculator::hasEnoughData,
             "Check if there's enough data for estimation")
        
        // === 诊断和统计 ===
        .def("calculate_log_likelihood", 
             py::overload_cast<>(&garch::GarchCalculator::calculateLogLikelihood, py::const_),
             "Calculate log-likelihood with current parameters")
        .def("calculate_log_likelihood", 
             py::overload_cast<const garch::GarchParameters&>(&garch::GarchCalculator::calculateLogLikelihood, py::const_),
             py::arg("params"),
             "Calculate log-likelihood with specified parameters")
        .def("calculate_aic", &garch::GarchCalculator::calculateAIC,
             "Calculate Akaike Information Criterion")
        .def("calculate_bic", &garch::GarchCalculator::calculateBIC,
             "Calculate Bayesian Information Criterion")
        .def("calculate_confidence_score", &garch::GarchCalculator::calculateConfidenceScore,
             "Calculate confidence score")
        
        // === 配置管理 ===
        .def("set_history_size", &garch::GarchCalculator::setHistorySize,
             py::arg("size"),
             "Set history buffer size")
        .def("set_min_samples", &garch::GarchCalculator::setMinSamples,
             py::arg("min_samples"),
             "Set minimum samples required")
        .def("get_config_info", &garch::GarchCalculator::getConfigInfo,
             "Get configuration information")
        
        // === 线程安全和清理 ===
        .def("set_thread_safe", &garch::GarchCalculator::setThreadSafe,
             py::arg("enable"),
             "Enable/disable thread safety")
        .def("clear", &garch::GarchCalculator::clear,
             "Clear all data and reset state")
        
        // === Python特有的便利方法 ===
        .def("add_prices_numpy", [](garch::GarchCalculator& calc, py::array_t<double> prices) {
            py::buffer_info buf = prices.request();
            double* ptr = (double*) buf.ptr;
            std::vector<double> price_vec(ptr, ptr + buf.size);
            return calc.addPricePoints(price_vec);
        }, py::arg("prices"), "Add prices from numpy array")
        
        .def("add_returns_numpy", [](garch::GarchCalculator& calc, py::array_t<double> returns) {
            py::buffer_info buf = returns.request();
            double* ptr = (double*) buf.ptr;
            std::vector<double> return_vec(ptr, ptr + buf.size);
            return calc.addReturns(return_vec);
        }, py::arg("returns"), "Add returns from numpy array (matches arch library)")
        
        .def("get_log_returns_numpy", [](const garch::GarchCalculator& calc) {
            auto returns = calc.getLogReturns();
            return py::array_t<double>(
                returns.size(),
                returns.data(),
                py::cast(calc, py::return_value_policy::reference_internal)
            );
        }, "Get log returns as numpy array")
        
        .def("get_variance_series_numpy", [](const garch::GarchCalculator& calc) {
            auto variances = calc.getVarianceSeries();
            return py::array_t<double>(
                variances.size(),
                variances.data(),
                py::cast(calc, py::return_value_policy::reference_internal)
            );
        }, "Get variance series as numpy array")
        
        .def("__repr__", [](const garch::GarchCalculator& calc) {
            return "GarchCalculator(data_size=" + std::to_string(calc.getDataSize()) +
                   ", current_volatility=" + std::to_string(calc.getCurrentVolatility()) + ")";
        });

    // === 工具函数 ===
    
    m.def("calculate_basic_stats", &garch::calculateBasicStats,
          py::arg("data"),
          "Calculate basic statistics of a data series");
    
    m.def("calculate_autocorrelation", &garch::calculateAutocorrelation,
          py::arg("data"), py::arg("max_lag") = 20,
          "Calculate autocorrelation function");
    
    m.def("calculate_ljung_box_statistic", &garch::calculateLjungBoxStatistic,
          py::arg("residuals"), py::arg("lag") = 10,
          "Calculate Ljung-Box test statistic");
    
    m.def("calculate_var", &garch::calculateVaR,
          py::arg("volatility"), py::arg("confidence_level") = 0.05,
          "Calculate Value at Risk");
    
    m.def("calculate_expected_shortfall", &garch::calculateExpectedShortfall,
          py::arg("volatility"), py::arg("confidence_level") = 0.05,
          "Calculate Expected Shortfall");

    // === 模块信息 ===
    m.attr("__version__") = "1.0.6";
    m.attr("__author__") = "GARCH Library Team";
} 