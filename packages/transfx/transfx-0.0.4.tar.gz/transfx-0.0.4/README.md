# transFX

一个简单易用的 Python 数学变换和工具包。

## 安装

```bash
pip install transfx
```

或者使用 uv：

```bash
uv pip install transfx
```

## 快速开始

```python
import transfx

# 创建 TransFX 实例
fx = transfx.TransFX()
print(f"版本: {fx.get_version()}")

# 数学运算
print(transfx.add(1, 2, 3))      # 6
print(transfx.sum(10, 20, 30))   # 60
print(transfx.sub(100, 25, 15))  # 60
print(transfx.mul(2, 3, 4))      # 24
print(transfx.div(120, 2, 3))    # 20.0

# 欢迎消息
transfx.hello()  # Hello, World! This is from transFX Welcom Package.
```

## 功能特性

- **数学运算**: 支持加法、减法、乘法、除法运算
- **类型安全**: 严格的类型检查和错误处理
- **简单易用**: 直观的 API 设计
- **轻量级**: 无外部依赖

## API 文档

### 数学函数

- `add(*args)`: 计算所有参数的和
- `sum(*args)`: 计算所有参数的和（与 add 相同）
- `sub(*args)`: 从第一个参数中依次减去后面的参数
- `mul(*args)`: 计算所有参数的乘积
- `div(*args)`: 从第一个参数开始依次除以后面的参数

### 工具函数

- `hello()`: 显示欢迎消息

### 主类

- `TransFX()`: 主要的 TransFX 类
  - `get_version()`: 获取版本信息

## 许可证

GPL-3.0 License
