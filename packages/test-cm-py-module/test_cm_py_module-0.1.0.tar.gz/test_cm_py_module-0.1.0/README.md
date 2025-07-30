# test-cm-py-module

一个简单的加法和减法计算模块

## 安装

```bash
pip install test-cm-py-module
```

## 使用方法

```python
from test_cm_py_module import add, subtract

# 加法运算
result = add(5, 3)
print(result)  # 输出: 8

# 减法运算
result = subtract(10, 4)
print(result)  # 输出: 6
```

## 功能

- `add(a, b)`: 计算两个数的和
- `subtract(a, b)`: 计算两个数的差

## 开发

```bash
# 克隆仓库
git clone https://github.com/yourusername/test-cm-py-module.git
cd test-cm-py-module

# 安装开发依赖
pip install -e .[dev]

# 运行测试
pytest
```

## 许可证

MIT License
