# FunKit - 功能强大的装饰器工具包

## 简介
`FunKit` 是一个Python装饰器工具包，提供了多种实用的装饰器，包括定时器、线程管理、耗时统计、异常处理、调用限制、失败重试、缓存和速率限制等功能。这些装饰器可以帮助开发者更方便地实现复杂的功能，提高代码的可读性和可维护性。

## 安装
你可以通过以下命令安装 `FunKit`：
```bash
pip install FunKit
```

## 使用方法

### 1. 单次定时器 (`setTimeout`)
`setTimeout` 装饰器用于在指定的延迟时间后执行函数。

**参数**：
- `sleep`：延迟时间（秒），必须为非负数。

**返回值**：
返回一个 `_ThreadController` 对象，该对象提供以下方法和属性：
- `stop()`：停止定时器。
- `isRun()`：检查定时器是否在运行。
- `value`：获取定时器执行结果。

**示例代码**：
```python
from FunKit import setTimeout

@setTimeout(sleep=2)
def my_function():
    print("这是延迟2秒后执行的函数。")

controller = my_function()
# 如果你想停止定时器，可以调用 controller.stop()
```

### 2. 循环定时器 (`setInterval`)
`setInterval` 装饰器用于按指定的时间间隔循环执行函数。

**参数**：
- `interval`：执行间隔（秒），必须为非负数。
- `end`：最大持续时间（秒），0 表示无限，必须为非负数。

**返回值**：
返回一个 `_ThreadController` 对象，该对象提供以下方法和属性：
- `stop()`：停止定时器。
- `isRun()`：检查定时器是否在运行。
- `value`：获取定时器执行结果，结果存储在列表中。

**示例代码**：
```python
from FunKit import setInterval

@setInterval(interval=1, end=5)
def my_function():
    print("这是每秒执行一次，持续5秒的函数。")

controller = my_function()
# 如果你想提前停止定时器，可以调用 controller.stop()
```

### 3. 创建多线程 (`createThread`)
`createThread` 装饰器用于将函数封装成线程执行。

**参数**：
- `inherit`：是否要随着主线程结束而结束，默认为 `False`。

**返回值**：
返回一个 `_ThreadController` 对象，该对象提供以下方法和属性：
- `isRun()`：检查线程是否在运行。
- `value`：获取线程执行结果。

**示例代码**：
```python
from FunKit import createThread

@createThread(inherit=True)
def my_function():
    print("这是在新线程中执行的函数。")

controller = my_function()
```

### 4. 耗时计算 (`timeIt`)
`timeIt` 装饰器用于统计函数的执行耗时。

**参数**：
- `num`：执行次数，默认为 1。
- `show`：是否直接打印耗时信息，默认为 `True`。
- `info`：是否返回耗时信息，默认为 `False`。
- 
**返回值**：
返回一个元组 `(原函数返回值, 耗时信息)` 或 `原函数返回值`，其中耗时信息是一个字典，包含平均耗时、最小耗时、最大耗时、总耗时等信息。

**示例代码**：
```python
from FunKit import timeIt

@timeIt(num=3)
def my_function():
    # 模拟耗时操作
    import time
    time.sleep(1)
    return "函数执行完成"

result, elapsed = my_function()
print(f"函数返回值: {result}")
print(f"耗时信息: {elapsed}")
```

### 5. 异常处理 (`catch`)
`catch` 装饰器用于捕获函数执行过程中的异常。

**参数**：
- `exc`：要捕获的异常类型，默认为 `Exception`。
- `value`：异常发生时返回的默认值，默认为 `None`。
- `reRaise`：是否重新抛出异常，默认为 `False`。
- `show`：是否显示错误信息，默认为 `True`。

**返回值**：
返回一个元组 `(默认值, 异常对象)`。

**示例代码**：
```python
from FunKit import catch

@catch(exc=ZeroDivisionError, value="发生除零错误")
def my_function():
    return 1 / 0

result, error = my_function()
print(f"结果: {result}")
print(f"异常对象: {error}")
```

### 6. 全局异常捕获 (`catchAll`)
`catchAll` 装饰器用于对指定模块中的所有用户定义函数进行全局异常捕获。

**参数**：
- `name`：需要处理的模块名称。
- `exc`：要捕获的异常类型，默认为 `Exception`。
- `value`：异常发生时返回的默认值，默认为 `None`。
- `reRaise`：是否重新抛出异常，默认为 `False`。
- `show`：是否显示错误信息，默认为 `True`。

**返回值**：
返回一个元组 `(默认值, 异常对象)`。

**示例代码**：
```python
import FunKit
from FunKit import catchAll

def my_function():
    return 1 / 0

catchAll(name=__name__)
try:
    result = my_function()
except Exception as e:
    print(f"捕获到异常: {e}")
```

### 7. 调用限制 (`callLimit`)
`callLimit` 装饰器用于限制函数的调用次数。

**参数**：
- `num`：最大允许调用次数，默认为 1。
- `value`：超限后返回值，默认为 `None`。

**返回值**：
返回默认值或目标函数返回值。

**示例代码**：
```python
from FunKit import callLimit

@callLimit(num=2, value="调用次数已超限")
def my_function():
    return "函数正常执行"

print(my_function())
print(my_function())
print(my_function())
```

### 8. 失败重试 (`retry`)
`retry` 装饰器用于在函数执行失败时进行重试。

**参数**：
- `num`：最大尝试次数，默认为 3。
- `delay`：重试延迟时间（秒），默认为 0。
- `exc`：要捕获的异常类型，默认为 `Exception`。
- `show`：是否显示错误信息，默认为 `True`。

**返回值**：
返回目标函数返回值或异常对象。

**示例代码**：
```python
from FunKit import retry

@retry(num=3, delay=1)
def my_function():
    import random
    if random.random() < 0.5:
        raise ValueError("模拟错误")
    return "函数执行成功"

result = my_function()
print(f"结果: {result}")
```

### 9. 缓存装饰器 (`memoize`)
`memoize` 装饰器用于缓存函数的执行结果，避免重复计算。

**参数**：
- `num`：最大缓存条目数（LRU 淘汰），默认为 128。
- `ttl`：缓存有效期（秒），0 表示永久，默认为 0。

**返回值**：
返回目标函数返回值。

**示例代码**：
```python
from FunKit import memoize

@memoize(num=2, ttl=2)
def my_function(x):
    import time
    time.sleep(1)
    return x * 2

print(my_function(2))  # 第一次调用，会进行计算
print(my_function(2))  # 第二次调用，会使用缓存结果
```

### 10. 速率限制装饰器 (`rateLimit`)
`rateLimit` 装饰器用于限制函数在指定时间周期内的调用次数。

**参数**：
- `num`：周期内最大调用次数，默认为 1。
- `period`：时间周期（秒），默认为 1。
- `value`：超限后返回值，默认为 `None`。

**返回值**：
返回速率限制控制器对象。

**示例代码**：
```python
from FunKit import rateLimit

@rateLimit(num=2, period=1, value="调用速率已超限")
def my_function():
    return "函数正常执行"

print(my_function())
print(my_function())
print(my_function())
```

### 11. 性能分析装饰器 (`analyse`)
`analyse` 装饰器用于分析函数的执行性能，包括 CPU 和内存使用情况。

**参数**：
- `sampling`：采样率，默认为 0.1。
- `cpuSampling`：CPU 采样率，默认为 0.1。
- `show`：是否直接打印分析结果，默认为 `True`。
- `info`：是否返回统计信息，默认为 `False`。

**返回值**：
返回一个`元组(原函数返回值, 统计信息)` 或 `原函数返回值`，统计信息包含 CPU 和内存使用情况的分析结果和函数执行结果。

**示例代码**：
```python
from FunKit import analyse

@analyse(sampling=0.1, cpuSampling=0.1)
def intensiveFunction() -> int:
    import time
    result = 0
    for i in range(10000000):
        result += i * i
    time.sleep(1)  # 为了更好地观察内存变化
    return result
    
result = intensiveFunction()
print(f"\n函数返回结果: {result}")
```    


## 贡献
如果你发现了 bug 或者有新的功能需求，欢迎联系QQ邮箱：2449579731@qq.com

## 许可证
本项目采用 [MIT 许可证](../../Downloads/FunKit-0.1.7/LICENSE)。