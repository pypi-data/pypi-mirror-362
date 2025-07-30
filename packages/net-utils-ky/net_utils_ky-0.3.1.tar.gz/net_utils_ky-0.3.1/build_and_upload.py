#!/usr/bin/env python3
"""
构建和上传到PyPI的脚本
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description):
    """运行命令并处理错误"""
    print(f"正在{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description}成功")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description}失败: {e}")
        print(f"错误输出: {e.stderr}")
        return None


def clean_build():
    """清理构建文件"""
    print("正在清理构建文件...")
    dirs_to_clean = ['build', 'dist', '*.egg-info']
    
    for pattern in dirs_to_clean:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"已删除目录: {path}")
            elif path.is_file():
                path.unlink()
                print(f"已删除文件: {path}")
    
    print("✅ 清理完成")


def check_dependencies():
    """检查必要的依赖"""
    print("正在检查依赖...")
    
    required_tools = ['python', 'pip', 'twine']
    missing_tools = []
    
    for tool in required_tools:
        if shutil.which(tool) is None:
            missing_tools.append(tool)
    
    if missing_tools:
        print(f"❌ 缺少必要的工具: {', '.join(missing_tools)}")
        print("请安装缺少的工具:")
        print("pip install twine")
        return False
    
    print("✅ 依赖检查通过")
    return True


def build_package():
    """构建包"""
    print("正在构建包...")
    
    # 安装构建依赖
    run_command("pip install --upgrade build", "安装构建工具")
    
    # 构建包
    result = run_command("python -m build", "构建包")
    
    if result is None:
        return False
    
    # 检查构建结果
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ 构建失败: dist目录不存在")
        return False
    
    files = list(dist_dir.glob('*'))
    if not files:
        print("❌ 构建失败: dist目录为空")
        return False
    
    print(f"✅ 构建成功，生成文件: {[f.name for f in files]}")
    return True


def check_package():
    """检查包"""
    print("正在检查包...")
    
    # 检查源代码分发
    result = run_command("twine check dist/*", "检查包格式")
    
    if result is None:
        return False
    
    print("✅ 包检查通过")
    return True


def upload_to_test_pypi():
    """上传到TestPyPI"""
    print("正在上传到TestPyPI...")
    
    # 检查是否有TWINE_USERNAME和TWINE_PASSWORD环境变量
    username = os.getenv('TWINE_USERNAME')
    password = os.getenv('TWINE_PASSWORD')
    
    if not username or not password:
        print("❌ 请设置环境变量 TWINE_USERNAME 和 TWINE_PASSWORD")
        print("或者使用交互式登录")
        return False
    
    result = run_command(
        "twine upload --repository testpypi dist/*",
        "上传到TestPyPI"
    )
    
    if result is None:
        return False
    
    print("✅ 上传到TestPyPI成功")
    print("您可以在 https://test.pypi.org/project/net_utils_ky/ 查看您的包")
    return True


def upload_to_pypi():
    """上传到PyPI"""
    print("正在上传到PyPI...")
    
    # 检查是否有TWINE_USERNAME和TWINE_PASSWORD环境变量
    username = os.getenv('TWINE_USERNAME')
    password = os.getenv('TWINE_PASSWORD')
    
    if not username or not password:
        print("❌ 请设置环境变量 TWINE_USERNAME 和 TWINE_PASSWORD")
        print("或者使用交互式登录")
        return False
    
    result = run_command(
        "twine upload dist/*",
        "上传到PyPI"
    )
    
    if result is None:
        return False
    
    print("✅ 上传到PyPI成功")
    print("您可以在 https://pypi.org/project/net_utils_ky/ 查看您的包")
    return True


def main():
    """主函数"""
    print("🚀 Net Utils KY - 构建和上传脚本")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 清理构建文件
    clean_build()
    
    # 构建包
    if not build_package():
        sys.exit(1)
    
    # 检查包
    if not check_package():
        sys.exit(1)
    
    # 询问上传目标
    print("\n请选择上传目标:")
    print("1. TestPyPI (测试)")
    print("2. PyPI (正式)")
    print("3. 仅构建，不上传")
    
    choice = input("请输入选择 (1/2/3): ").strip()
    
    if choice == "1":
        upload_to_test_pypi()
    elif choice == "2":
        upload_to_pypi()
    elif choice == "3":
        print("✅ 构建完成，未上传")
    else:
        print("❌ 无效选择")
        sys.exit(1)


if __name__ == "__main__":
    main() 