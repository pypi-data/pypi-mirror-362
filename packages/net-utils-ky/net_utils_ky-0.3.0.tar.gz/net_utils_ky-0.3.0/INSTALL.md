# 安装指南

## 从 PyPI 安装

### 基本安装

```bash
pip install net_utils_ky
```

### 安装开发依赖

```bash
pip install net_utils_ky[dev]
```

## 从源码安装

### 克隆仓库

```bash
git clone https://github.com/yourusername/net_utils_ky.git
cd net_utils_ky
```

### 安装开发版本

```bash
pip install -e .
```

### 安装开发依赖

```bash
pip install -e ".[dev]"
```

## 验证安装

### Python 中使用

```python
from net_utils_ky import NetworkUtils

# 创建实例
net_utils = NetworkUtils()

# 检查网络连接
if net_utils.is_connected():
    print("安装成功！网络连接正常")
else:
    print("安装成功！但网络连接有问题")
```

### 命令行使用

```bash
# 检查网络连接
net-utils check-connection

# 查看帮助
net-utils --help
```

## 依赖要求

### 必需依赖

- Python >= 3.7
- requests >= 2.25.0
- urllib3 >= 1.26.0

### 可选依赖

- aiohttp (用于异步功能)
- pytest (用于测试)
- black (用于代码格式化)
- flake8 (用于代码检查)
- mypy (用于类型检查)

## 故障排除

### 常见问题

1. **ImportError: No module named 'net_utils_ky'**

   - 确保已正确安装包
   - 检查 Python 环境

2. **ModuleNotFoundError: No module named 'requests'**

   - 安装 requests: `pip install requests`

3. **权限错误**
   - 使用虚拟环境
   - 或使用 `pip install --user net_utils_ky`

### 虚拟环境

推荐使用虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 安装包
pip install net_utils_ky
```

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/yourusername/net_utils_ky.git
cd net_utils_ky
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装开发依赖

```bash
pip install -e ".[dev]"
```

### 4. 运行测试

```bash
pytest
```

### 5. 代码格式化

```bash
black .
```

### 6. 类型检查

```bash
mypy net_utils_ky
```

## 构建和发布

### 构建包

```bash
python -m build
```

### 检查包

```bash
twine check dist/*
```

### 上传到 TestPyPI

```bash
twine upload --repository testpypi dist/*
```

### 上传到 PyPI

```bash
twine upload dist/*
```

### 使用构建脚本

```bash
python build_and_upload.py
```

## 版本兼容性

| Python 版本 | 支持状态    |
| ----------- | ----------- |
| 3.7         | ✅ 完全支持 |
| 3.8         | ✅ 完全支持 |
| 3.9         | ✅ 完全支持 |
| 3.10        | ✅ 完全支持 |
| 3.11        | ✅ 完全支持 |
| 3.12        | ✅ 完全支持 |

## 平台支持

- ✅ Windows
- ✅ Linux
- ✅ macOS
- ✅ 其他 Unix 系统

## 获取帮助

如果遇到安装问题，请：

1. 检查 Python 版本是否符合要求
2. 确保网络连接正常
3. 尝试使用虚拟环境
4. 查看错误信息并搜索解决方案
5. 在 GitHub 上提交 Issue
