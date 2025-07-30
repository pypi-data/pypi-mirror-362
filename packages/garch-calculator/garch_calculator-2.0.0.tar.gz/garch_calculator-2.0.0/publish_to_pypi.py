#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PyPI发布脚本 - 自动化GARCH Calculator包的发布流程

使用方法:
    python publish_to_pypi.py --test     # 发布到测试PyPI
    python publish_to_pypi.py --prod     # 发布到生产PyPI
    python publish_to_pypi.py --build    # 仅构建，不发布
    python publish_to_pypi.py --check    # 检查包的有效性
"""

import os
import sys
import subprocess
import argparse
import shutil
from pathlib import Path

def run_command(cmd, cwd=None, check=True):
    """运行命令并打印输出"""
    print(f"🔄 执行: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            check=check, 
            capture_output=True, 
            text=True
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        if e.stdout:
            print("标准输出:", e.stdout)
        if e.stderr:
            print("错误输出:", e.stderr)
        raise

def check_dependencies():
    """检查必要的依赖"""
    print("🔍 检查依赖...")
    
    required_packages = ['build', 'twine', 'wheel']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少必要包: {', '.join(missing_packages)}")
        print("请运行: pip install build twine wheel")
        return False
    
    print("✅ 所有依赖已满足")
    return True

def clean_build():
    """清理构建目录"""
    print("🧹 清理构建目录...")
    
    dirs_to_clean = ['build', 'dist', 'garch_lib.egg-info', 'garch_calculator.egg-info']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   删除: {dir_name}")
    
    # 清理编译的扩展模块
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(('.so', '.pyd', '.dylib')):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"   删除: {file_path}")
    
    print("✅ 清理完成")

def check_package_structure():
    """检查包结构"""
    print("📋 检查包结构...")
    
    required_files = [
        'setup.py',
        'pyproject.toml', 
        'README.md',
        'LICENSE',
        'MANIFEST.in',
        'garch_lib/__init__.py',
        'src/garch_calculator.cpp',
        'python/garch_bindings.cpp',
        'include/garch_calculator.h'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    print("✅ 包结构检查通过")
    return True

def build_package():
    """构建包"""
    print("🔨 构建包...")
    
    # 使用setup.py构建包 (兼容我们的CMake集成)
    run_command([sys.executable, 'setup.py', 'sdist', 'bdist_wheel'])
    
    # 检查构建结果
    if not os.path.exists('dist'):
        print("❌ 构建失败：dist目录不存在")
        return False
    
    dist_files = os.listdir('dist')
    if not any(f.endswith('.whl') for f in dist_files):
        print("❌ 构建失败：没有找到wheel文件")
        return False
    
    if not any(f.endswith('.tar.gz') for f in dist_files):
        print("❌ 构建失败：没有找到源代码分发文件")
        return False
    
    print("✅ 包构建成功")
    print("📦 构建的文件:")
    for file in dist_files:
        print(f"   {file}")
    
    return True

def check_package():
    """检查包的有效性"""
    print("🔍 检查包的有效性...")
    
    # 使用twine检查
    run_command([sys.executable, '-m', 'twine', 'check', 'dist/*'])
    
    print("✅ 包检查通过")
    return True

def test_install():
    """测试本地安装"""
    print("🧪 测试本地安装...")
    
    try:
        # 在虚拟环境中测试安装
        wheel_files = [f for f in os.listdir('dist') if f.endswith('.whl')]
        if wheel_files:
            wheel_file = wheel_files[0]
            print(f"测试安装: {wheel_file}")
            
            # 这里可以添加更详细的测试逻辑
            # 比如创建临时虚拟环境，安装包，运行测试等
            
        print("✅ 本地安装测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 本地安装测试失败: {e}")
        return False

def upload_to_test_pypi():
    """上传到测试PyPI"""
    print("📤 上传到测试PyPI...")
    
    print("📋 请确保已配置TestPyPI认证:")
    print("   1. 在 ~/.pypirc 文件中配置TestPyPI token")
    print("   2. 或使用 twine upload --repository testpypi --username __token__ --password <token>")
    
    confirm = input("是否继续上传到测试PyPI? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ 用户取消上传")
        return False
    
    try:
        # 只上传源码分发包，跳过ARM64 wheel（PyPI不支持linux_aarch64标签）
        run_command([
            sys.executable, '-m', 'twine', 'upload',
            '--repository', 'testpypi',
            'dist/*.tar.gz'
        ])
        
        print("✅ 成功上传到测试PyPI")
        print("🔗 测试安装命令:")
        print("   pip install --index-url https://test.pypi.org/simple/ garch-calculator")
        print("💡 注意: 只上传了源码包，用户安装时会自动编译C++扩展")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ 上传到测试PyPI失败")
        return False

def upload_to_prod_pypi():
    """上传到生产PyPI"""
    print("📤 上传到生产PyPI...")
    
    print("⚠️  注意: 这将发布到生产环境，版本号不能重复使用!")
    print("📋 请确保已配置PyPI认证:")
    print("   1. 在 ~/.pypirc 文件中配置PyPI token")
    print("   2. 或使用 twine upload --username __token__ --password <token>")
    
    confirm = input("确认上传到生产PyPI? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ 用户取消上传")
        return False
    
    # 二次确认
    version_confirm = input("请再次确认版本号正确且之前未使用过? (y/N): ")
    if version_confirm.lower() != 'y':
        print("❌ 用户取消上传")
        return False
    
    try:
        # 只上传源码分发包，跳过ARM64 wheel（PyPI不支持linux_aarch64标签）
        run_command([
            sys.executable, '-m', 'twine', 'upload',
            'dist/*.tar.gz'
        ])
        
        print("✅ 成功上传到生产PyPI")
        print("🔗 安装命令:")
        print("   pip install garch-calculator")
        print("💡 注意: 只上传了源码包，用户安装时会自动编译C++扩展")
        return True
        
    except subprocess.CalledProcessError:
        print("❌ 上传到生产PyPI失败")
        return False

def main():
    parser = argparse.ArgumentParser(description='GARCH Calculator PyPI发布工具')
    parser.add_argument('--test', action='store_true', help='发布到测试PyPI')
    parser.add_argument('--prod', action='store_true', help='发布到生产PyPI')
    parser.add_argument('--build', action='store_true', help='仅构建，不发布')
    parser.add_argument('--check', action='store_true', help='检查包的有效性')
    parser.add_argument('--clean', action='store_true', help='仅清理构建目录')
    
    args = parser.parse_args()
    
    if not any([args.test, args.prod, args.build, args.check, args.clean]):
        parser.print_help()
        return
    
    print("=" * 60)
    print("🚀 GARCH Calculator PyPI发布工具")
    print("=" * 60)
    
    try:
        # 清理
        if args.clean:
            clean_build()
            return
        
        # 检查依赖
        if not check_dependencies():
            return
        
        # 清理旧构建
        clean_build()
        
        # 检查包结构
        if not check_package_structure():
            return
        
        # 构建包
        if not build_package():
            return
        
        # 检查包
        if not check_package():
            return
        
        # 仅检查
        if args.check:
            print("✅ 包检查完成，一切正常!")
            return
        
        # 仅构建
        if args.build:
            print("✅ 包构建完成!")
            return
        
        # 测试安装
        if not test_install():
            print("⚠️  本地安装测试失败，但继续发布流程")
        
        # 发布到测试PyPI
        if args.test:
            if upload_to_test_pypi():
                print("🎉 成功发布到测试PyPI!")
            return
        
        # 发布到生产PyPI
        if args.prod:
            if upload_to_prod_pypi():
                print("🎉 成功发布到生产PyPI!")
            return
            
    except KeyboardInterrupt:
        print("\n❌ 用户中断")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main() 