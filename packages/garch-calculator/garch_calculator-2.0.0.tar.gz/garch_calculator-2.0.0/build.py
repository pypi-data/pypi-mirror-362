#!/usr/bin/env python3
"""
构建改进的 GARCH C++ 实现 (匹配 arch 库)
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, check=True):
    """运行命令并处理错误"""
    print(f"运行: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    try:
        result = subprocess.run(cmd, shell=isinstance(cmd, str), check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"错误: {e}")
        if e.stderr:
            print(f"错误输出: {e.stderr}")
        if check:
            sys.exit(1)
        return e

def build_improved_garch():
    """构建改进的 GARCH 实现"""
    
    print("=== 构建改进的 GARCH C++ 实现 ===\n")
    
    # 确保在正确的目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # 清理之前的构建
    print("1. 清理之前的构建...")
    if Path("build").exists():
        run_command("rm -rf build", check=False)
    
    if Path("garch_calculator.cpython*.so").exists():
        run_command("rm -f garch_calculator.cpython*.so", check=False)
    
    # 创建构建目录
    print("\n2. 创建构建目录...")
    os.makedirs("build", exist_ok=True)
    os.chdir("build")
    
    # 配置 CMake
    print("\n3. 配置 CMake...")
    cmake_cmd = [
        "cmake", "..",
        "-DCMAKE_BUILD_TYPE=Release",
        "-DBUILD_TESTS=ON"
    ]
    run_command(cmake_cmd)
    
    # 构建项目
    print("\n4. 构建项目...")
    run_command(["make", "-j", str(os.cpu_count() or 4)])
    
    # 复制 Python 模块到主目录
    print("\n5. 复制 Python 模块...")
    so_files = list(Path(".").glob("_garch_calculator.cpython*.so"))
    if so_files:
        so_file = so_files[0]
        # 复制到garch_lib包目录
        target_path = Path("../garch_lib") / so_file.name
        run_command(f"cp {so_file} {target_path}", check=False)
        print(f"已复制 {so_file} 到 garch_lib/ 目录")
    else:
        # 检查是否在build/lib目录中
        build_so_files = list(Path("../build/lib.linux-aarch64-cpython-312/garch_lib").glob("_garch_calculator.cpython*.so"))
        if build_so_files:
            so_file = build_so_files[0]
            target_path = Path("../garch_lib") / so_file.name
            run_command(f"cp {so_file} {target_path}", check=False)
            print(f"已从build目录复制 {so_file.name} 到 garch_lib/ 目录")
        else:
            print("警告: 未找到 _garch_calculator.cpython*.so 文件")
    
    # 返回主目录
    os.chdir("..")
    
    print("\n6. 验证构建...")
    
    # 测试 C++ 可执行文件 (如果存在)
    cpp_test = Path("build/test_garch")
    if cpp_test.exists():
        print("运行 C++ 测试...")
        run_command(["./build/test_garch"], check=False)
    
    # 测试 Python 导入
    print("\n测试 Python 模块导入...")
    test_import = """
import sys
sys.path.append('.')
try:
    import garch_lib
    print("✅ Python 包导入成功")
    
    # 简单测试
    calc = garch_lib.GarchCalculator(100, 20)
    print(f"✅ 创建 GarchCalculator 实例成功")
    
    # 测试参数设置
    params = garch_lib.GarchParameters(0.00001, 0.1, 0.8, 1.5)
    calc.set_parameters(params)
    retrieved = calc.get_parameters()
    print(f"✅ 参数设置和获取成功: ω={retrieved.omega}, α={retrieved.alpha}, β={retrieved.beta}, ν={retrieved.nu}")
    
except ImportError as e:
    print(f"❌ Python 包导入失败: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ 模块测试失败: {e}")
    sys.exit(1)
"""
    
    run_command([sys.executable, "-c", test_import])
    
    print("\n=== 构建完成 ===")
    print("\n下一步：")
    print("1. 运行兼容性测试: python test_arch_compatibility.py")
    print("2. 运行完整测试: python example_usage.py")
    print("3. 运行对比测试: python final_comparison.py")

if __name__ == "__main__":
    build_improved_garch() 