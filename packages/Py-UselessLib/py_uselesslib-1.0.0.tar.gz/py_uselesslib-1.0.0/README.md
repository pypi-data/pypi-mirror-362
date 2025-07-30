
# UselessLib 技术文档

## 1. 概述

UselessLib 是一个Python工具库，提供了一系列工具函数。本库采用模块化设计，包含对布尔值、整数、字符串等基础数据类型的判断操作，以及高阶函数执行和系统工具等功能。

## 2. 功能模块

### 2.1 布尔(Bool)操作模块

提供全面的布尔值判断和操作功能：

- 判断布尔值的真伪状态
- 生成随机布尔值
- 获取基础布尔常量

#### 核心功能示例

```python
from cn.xiuxius.uselesslib.bool import is_true, is_false, random_bool

print(is_true(True))  # True
print(random_bool())  # 随机True或False
```

| 函数                  | 描述         | 返回值  |
|---------------------|------------|------|
| `is_true(n: bool)`  | 判断是否为True  | bool |
| `is_false(n: bool)` | 判断是否为False | bool |
| `random_bool()`     | 生成随机布尔值    | bool |

### 2.2 整数(Int)操作模块

提供0-100整数的精确判断功能，支持自定义数字匹配：

#### 核心功能示例

```python
from cn.xiuxius.uselesslib.int import is_zero, is_twenty, is_custom_number

print(is_zero(0))  # True
print(is_custom_number(30, 30))  # True
```

注意：本模块包含从0到100的精确判断函数，如 `is_one()` 到 `is_one_hundred()`。

### 2.3 字符串(Str)操作模块

提供字母a-z的大小写敏感/不敏感匹配，支持自定义字符串匹配：

#### 核心功能示例

```python
from cn.xiuxius.uselesslib.str import is_a, is_z_ignore_case, is_custom_str

print(is_a("a"))  # True
print(is_custom_str("Test", "test"))  # False
```

| 函数命名规则            | 示例               |
|-------------------------|--------------------|
| `is_[a-z]`              | 区分大小写的匹配   |
| `is_[a-z]_ignore_case` | 不区分大小写的匹配 |

### 2.4 函数(Fun)操作模块

提供安全的函数执行机制：

- 带参数/关键字参数执行
- 带异常概率的执行
- 多种执行方式封装

#### 核心功能示例

```python
from cn.xiuxius.uselesslib.fun import execute_fun_with_args, execute_fun_with_random_exception

def add(a, b):
    return a + b

execute_fun_with_args(add, 1, 2)  # 3

try:
    execute_fun_with_random_exception(lambda: 1/1, probability=0.1)
except Exception as e:
    print(f"捕获异常: {e}")
```


### 2.5 工具(Util)模块

提供系统级功能：

- 随机字符串生成
- 异步崩溃机制（用于测试场景）

#### 核心功能示例

```python
from cn.xiuxius.uselesslib.util import random_print_str, async_crash_with_random_time_in_1_minute

random_print_str()  # 输出随机字符串
# async_crash_with_random_time_in_1_minute()  # 谨慎使用
```

## 3. 安装与使用

### 3.1 安装方式

```bash
pip install uselesslib
```

### 3.2 基础导入

```python
from cn.xiuxius.uselesslib import bool, int, str, fun, util
```

## 4. 最佳实践

### 4.1 布尔运算

```python
from cn.xiuxius.uselesslib.bool import is_true_or_false

result = is_true_or_false(False)  # 安全的布尔判断
```

### 4.2 安全性执行

```python
from cn.xiuxius.uselesslib.fun import execute_fun_with_random_exception

try:
    execute_fun_with_random_exception(lambda: 1/1, probability=0.1)
except Exception as e:
    print(f"安全捕获异常: {e}")
```

### 4.3 自定义匹配

```python
from cn.xiuxius.uselesslib.str import is_custom_str_ignore_case

match = is_custom_str_ignore_case("Hello", "hello")  # True
```

## 6. 许可证

UselessLib 使用 MIT 许可证开放源代码，详情见 LICENSE 文件。
