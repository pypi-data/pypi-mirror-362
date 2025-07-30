#!/usr/bin/env python3
"""
快速测试脚本 - 验证GARCH Calculator包的构建和基本功能
"""

import sys
import os
import subprocess
import importlib.util

def test_import():
    """测试模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试从包目录导入
        sys.path.insert(0, '.')
        import garch_lib
        
        print(f"✅ 成功导入 garch_lib")
        print(f"   版本: {garch_lib.__version__}")
        print(f"   构建信息: {garch_lib.get_build_info()}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_extension_module():
    """测试C++扩展模块"""
    print("\n🔍 测试C++扩展模块...")
    
    try:
        # 检查是否有编译好的扩展模块
        import glob
        so_files = glob.glob("garch_lib/*.so") + glob.glob("*.so")
        
        if so_files:
            print(f"✅ 找到扩展模块: {so_files}")
            
            # 尝试导入和使用
            import garch_lib.garch_calculator as gc
            
            # 创建计算器实例
            calc = gc.GarchCalculator(100, 10)
            print(f"✅ 成功创建 GarchCalculator 实例")
            
            # 添加一些测试数据
            import numpy as np
            test_prices = np.random.lognormal(0, 0.02, 50) * 100
            calc.add_price_points(test_prices.tolist())
            
            print(f"✅ 成功添加测试数据: {len(test_prices)} 个价格点")
            print(f"   数据大小: {calc.get_data_size()}")
            print(f"   足够数据: {calc.has_enough_data()}")
            
            return True
        else:
            print("⚠️  未找到编译的扩展模块，请先运行 python build.py")
            return False
            
    except Exception as e:
        print(f"❌ 扩展模块测试失败: {e}")
        return False

def test_package_structure():
    """测试包结构"""
    print("\n🔍 测试包结构...")
    
    required_files = [
        'setup.py',
        'pyproject.toml',
        'LICENSE',
        'README.md',
        'MANIFEST.in',
        'garch_lib/__init__.py',
    ]
    
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print(f"❌ 缺少必要文件: {missing}")
        return False
    else:
        print("✅ 包结构完整")
        return True

def test_dependencies():
    """测试依赖"""
    print("\n🔍 测试依赖...")
    
    try:
        import numpy
        print(f"✅ NumPy: {numpy.__version__}")
        
        import pybind11
        print(f"✅ pybind11: {pybind11.__version__}")
        
        return True
        
    except ImportError as e:
        print(f"❌ 依赖检查失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 GARCH Calculator 包测试")
    print("=" * 60)
    
    tests = [
        ("包结构", test_package_structure),
        ("依赖检查", test_dependencies),
        ("模块导入", test_import),
        ("扩展模块", test_extension_module),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}测试:")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}测试出错: {e}")
            results.append((test_name, False))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<10}: {status}")
    
    print(f"\n总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！包准备就绪。")
        print("\n📋 下一步:")
        print("1. 运行 python publish_to_pypi.py --check 进行完整检查")
        print("2. 运行 python publish_to_pypi.py --test 发布到测试PyPI")
        print("3. 测试无误后运行 python publish_to_pypi.py --prod 发布到生产PyPI")
        return True
    else:
        print("⚠️  有测试失败，请修复后再尝试发布。")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 