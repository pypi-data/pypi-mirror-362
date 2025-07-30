from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# 读取requirements文件
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="net_utils_ky",
    version="0.3.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个实用的网络工具包，提供各种网络相关的功能",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/net_utils_ky",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",

        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "net-utils=net_utils_ky.cli:main",
            "kyanos=net_utils_ky.kyanos_entry:main",
        ],
    },
    include_package_data=True,
    package_data={
        'net_utils_ky': [
            'libs/*',  # 包含所有二进制
        ],
    },
    zip_safe=False,
) 