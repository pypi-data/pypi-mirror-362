import time
import sys
import os
import psutil
import functools
from threading import Thread, Event, Lock
from typing import Callable, Any, Union, Tuple, Dict, List, Optional




# ================================================== 线程控制器 ==================================================
class _ThreadController:
    # 循环定时器控制器(用于停止定时任务)
    def __init__(self):
        self._stopEvent = Event()  # 停止事件标志
        self._thread: Optional[Thread] = None  # 工作线程引用
        self._value: Any = None  # 存储结果

    # 停止定时循环
    def stop(self): self._stopEvent.set()

    # 检查定时器是否在运行
    def isRun(self) -> bool: return not self._stopEvent.is_set()

    # 只读属性
    @property
    def thread(self): return self._thread
    @property
    def stopEvent(self): return self._stopEvent
    @property
    def value(self): return self._value

    # 修改属性
    @thread.setter
    def thread(self, value): self._thread = value
    @value.setter
    def value(self, value): self._value = value




# ================================================== 单次定时器 ==================================================
def setTimeout(sleep: float) -> Callable:
    """
    单次定时器装饰器工厂
    :param sleep: 延迟时间(秒)
    :returns: 返回 ThreadController 对象,
    提供 stop() 停止定时器,
    isRun() 检查定时器是否在运行,
    value 属性获取定时器执行结果
    """

    # 校验参数
    if sleep < 0: raise ValueError("延迟时间不能为负数")

    # 定义装饰器
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> _ThreadController:
            # 创建控制器对象
            controller = _ThreadController()

            # 定义任务函数
            def task():
                try:
                    controller.stopEvent.wait(sleep)  # 带停止检测的等待
                    if not controller.isRun(): return  # 停止事件
                    controller.value = func(*args, **kwargs)  # 将结果存储到控制器对象
                except Exception as e: print(f"定时任务执行失败: {str(e)}")

            # 启动任务线程
            controller.thread = Thread(target=task)
            controller.thread.start()

            # 返回任务线程对象
            return controller
        return wrapper
    return decorator




# ================================================== 循环定时器 ==================================================
def setInterval(interval: float, end: float = 0) -> Callable:
    """
    循环定时器装饰器工厂
    :param interval: 执行间隔 (秒)
    :param end: 最大持续时间 (秒)，0表示无限
    :returns: 返回 ThreadController 对象,
    提供 stop() 停止定时器,
    isRun() 检查定时器是否在运行,
    value 属性获取定时器执行结果
    """

    # 校验参数
    if interval < 0 or end < 0: raise ValueError("时间参数不能为负数")

    # 定义装饰器
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> _ThreadController:
            # 创建控制器对象
            controller = _ThreadController()
            endTime = time.time() + end if end > interval else float('inf')  # 计算结束时间戳
            controller._value = []  # 存储结果

            # 定义任务函数
            def task():
                while True:
                    # 带停止检测的等待
                    controller.stopEvent.wait(interval)
                    if time.time() >= endTime or controller.isRun() is False: return  # 停止事件: break

                    # 执行目标函数
                    try: controller.value.append(func(*args, **kwargs))
                    except Exception as e: print(f"函数：{func.__name__} 定时任务执行失败: {str(e)}")

            # 启动任务线程
            controller.thread = Thread(target=task)
            controller.thread.start()

            # 返回控制器对象
            return controller
        return wrapper
    return decorator




# ================================================== 创建多线程 ==================================================
def createThread(inherit: bool = False) -> Callable:
    """
    创建线程装饰器工厂
    :param inherit: 是否要随着主线程结束而结束
    :returns: 返回 ThreadController 对象
    提供 isRun() 检查线程是否在运行,
    value 属性获取线程执行结果
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> _ThreadController:
            # 创建控制器对象
            controller = _ThreadController()

            # 定义任务函数
            def task():
                try: controller.value = func(*args, **kwargs)  # 执行目标函数
                except Exception as e: print(f"线程执行失败: {str(e)}")

            # 创建线程对象
            controller.thread = Thread(target=task, daemon=inherit)
            controller.thread.start()  # 启动线程

            # 返回线程对象
            return controller
        return wrapper
    return decorator




# ================================================== 耗时计算 ==================================================
def timeIt(num: int = 1, show: bool = True, info: bool = False) -> Callable:
    """
    耗时统计装饰器工厂
    :param num: 执行次数
    :param show: 是否直接打印耗时信息
    :param info: 是否返回统计信息
    :return: 返回(原函数返回值, 耗时信息)元组
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Union[Tuple[Any, Dict], Any]:
            result = None  # 存储结果
            tempElapsed = []  # 存储耗时

            # 循环执行目标函数
            for _ in range(num):
                start = time.perf_counter()  # 高精度计时开始
                result = func(*args, **kwargs)
                tempElapsed.append(time.perf_counter() - start)  # 计算耗时

            # 计算统计信息
            elapsed = {"avg": sum(tempElapsed) / num, "min": min(tempElapsed), "max": max(tempElapsed), "sum": sum(tempElapsed)}  # 计算平均耗时
            if num > 1: elapsed["median"] = sorted(tempElapsed)[len(tempElapsed) // 2]  # 计算中位数耗时
            elapsed = {k: f"{v:.5f}" for k, v in elapsed.items()}  # 格式化耗时信息

            # 判断是否显示耗时信息
            if show:
                print(f"函数：{func.__name__} 耗时统计信息:")
                for k, v in elapsed.items(): print(f"{k}: {v}s", end="\t")
                print()

            if info: return result, elapsed
            return result
        return wrapper
    return decorator




# ================================================== 异常处理 ==================================================
def catch(exc: Tuple[Any] = (Exception,), value: Tuple = None, reRaise: bool = False, show: bool = True) -> Callable:
    """
    异常捕获装饰器工厂
    :param exc: 要捕获的异常类型
    :param value: 异常发生时返回的默认值
    :param reRaise: 是否重新抛出异常
    :param show: 是否显示错误信息
    :return: 返回 (默认值, 异常对象)元组
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Tuple[Any, Any]:
            # 捕获异常并返回默认值
            try: return func(*args, **kwargs)  # 正常执行
            except exc as e:
                if show: print(f"[异常捕获 {func.__name__}], 错误信息: [{str(e)}]")
                if reRaise: raise e  # 重新抛出异常开关
                if value is None: return None, e  # 返回 None
                if len(value) == 1: return value[0]  # 返回元组
                return value[0], e  # 返回元组
        return wrapper
    return decorator




# ================================================== 全局异常捕获 ==================================================
def _catchAllErrors(func: Callable, exc: Tuple[Any], value: Tuple, reRaise: bool, show: bool) -> Callable:
    """
    内部实现的全局异常捕获装饰器
    :param func: 需要装饰的目标函数
    :param exc: 要捕获的异常类型
    :param value: 异常发生时返回的默认值
    :param reRaise: 是否重新抛出异常
    :param show: 是否显示错误信息
    :return: 返回 (默认值, 异常对象)元组
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Tuple[Any, Any]:
        # 捕获异常并返回默认值
        try: return func(*args, **kwargs)  # 正常执行
        except exc as e:
            if show: print(f"[异常捕获 {func.__name__}], 错误信息: [{str(e)}]")
            if reRaise: raise e  # 重新抛出异常开关
            if value is None: return None, e  # 返回 None
            if len(value) == 1: return value[0]  # 返回元组
            return value[0], e  # 返回元组
    return wrapper


def catchAll(name: str, exc: Tuple[Any] = (Exception,), value: Tuple = None, reRaise: bool = False, show: bool = True) -> None:
    """
    模块级全局异常捕获
    :param name: 需要处理的模块名称
    :param exc: 要捕获的异常类型
    :param value: 异常发生时返回的默认值
    :param reRaise: 是否重新抛出异常
    :param show: 是否显示错误信息
    :raise: 抛出异常
    """
    # 获取模块对象
    targetModule = sys.modules.get(name)
    if not targetModule: raise ValueError(f"找不到模块: {name}")

    # 遍历模块所有成员
    for attrName in dir(targetModule):
        # 获取成员对象
        attr = getattr(targetModule, attrName)

        # 仅处理用户定义的函数
        if callable(attr) and not isinstance(attr, type):
            try:
                # 添加异常捕获装饰器
                wrappedFunc = _catchAllErrors(attr, exc, value, reRaise, show)
                setattr(targetModule, attrName, wrappedFunc)
            except Exception as e: raise ValueError(f"处理函数 {attrName} 时发生错误: {str(e)}")




# ================================================== 调用限制 ==================================================
def callLimit(num: int = 1, value: Any = None) -> Callable:
    """
    调用次数限制装饰器工厂(线程安全版)
    :param num: 最大允许调用次数
    :param value: 超限后返回值
    :return: 返回默认值或目标函数返回值
    """

    def decorator(func: Callable) -> Callable:
        lock = Lock()  # 线程锁
        callCount = 0  # 调用计数器

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            # 保证原子操作
            nonlocal callCount

            # 循环计数器
            with lock:
                if callCount >= num: return value  # 超限
                callCount += 1  # 计数加1

            # 执行目标函数
            return func(*args, **kwargs)
        return wrapper
    return decorator




# ================================================== 失败重试 ==================================================
def retry(num: int = 3, delay: float = 0, exc: Tuple[Any] = (Exception,), show: bool = True) -> Callable:
    """
    失败重试装饰器工厂
    :param num: 最大尝试次数
    :param delay: 重试延迟时间(秒)
    :param exc: 要捕获的异常类型
    :param show: 是否显示错误信息
    :return: 返回目标函数返回值或异常对象
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            # 尝试执行目标函数
            for attempt in range(1, num + 1):
                # 捕获异常并重试
                try: return func(*args, **kwargs)
                except exc as e:
                    if show: print(f"第 {attempt} 次尝试失败: {str(e)}")
                    if attempt == num: return e # 最后一次尝试失败后抛出异常
                    time.sleep(delay)  # 重试前等待

            # 最后一次尝试
            return func(*args, **kwargs)
        return wrapper
    return decorator




# ================================================== 缓存装饰器 ==================================================
def memoize(num: int = 128, ttl: float = 0) -> Callable:
    """
    缓存装饰器工厂(线程安全+TTL支持)
    :param num: 最大缓存条目数 (LRU淘汰)
    :param ttl: 缓存有效期(秒)，0表示永久
    :return: 返回目标函数返回值
    """

    def decorator(func: Callable) -> Callable:
        cache = {}
        lock = Lock()
        lruKeys = []  # LRU队列

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Callable:
            nonlocal lruKeys
            # 生成唯一缓存键(排除self参数)
            key = (args[1:] if args and hasattr(args[0], '__dict__') else args, tuple(sorted(kwargs.items())))

            with lock:
                # 检查缓存有效性
                if key in cache:
                    entry = cache[key]
                    if ttl == 0 or time.time() - entry['time'] < ttl:
                        # 更新LRU队列
                        lruKeys.remove(key)
                        lruKeys.append(key)
                        return entry['value']
                    del cache[key]
                    lruKeys.remove(key)

                # 执行函数并缓存结果
                result = func(*args, **kwargs)
                cache[key] = {'value': result, 'time': time.time()}
                lruKeys.append(key)

                # LRU淘汰机制
                if len(cache) > num:
                    delKey = lruKeys.pop(0)
                    del cache[delKey]

                # 返回结果
                return result
        return wrapper
    return decorator




# ================================================== 速率限制装饰器 ==================================================
class _RateLimiter:
    """速率限制控制器"""

    def __init__(self, maxCalls: int, period: float, value: Any):
        self.maxCalls = maxCalls
        self.period = period
        self.value = value
        self.timestamps = []
        self.lock = Lock()

    def __call__(self, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            with self.lock:
                now = time.time()
                # 清除过期时间戳
                self.timestamps = [t for t in self.timestamps if t > now - self.period]

                # 检查是否超限
                if len(self.timestamps) >= self.maxCalls: return self.value

                # 记录本次调用
                self.timestamps = [t for t in self.timestamps if t > now - self.period]
                self.timestamps.append(now)
            return func(*args, **kwargs)
        return wrapper


def rateLimit(num: int = 1, period: float = 1, value: Any = None) -> _RateLimiter:
    """
    速率限制装饰器工厂
    :param num: 周期内最大调用次数
    :param period: 时间周期(秒)
    :param value: 超限后返回值
    :return: 返回速率限制控制器对象
    """
    return _RateLimiter(num, period, value)




# ================================================== 性能分析装饰器 ==================================================
def _calculateStats(data: List[float]) -> Dict[str, float]:
    """
    计算数据集的统计信息。
    :param data: 数据集
    :return: 统计信息字典
    """

    # 去除空值
    if not data: return {"max": 0, "min": 0, "median": 0, "average": 0}
    
    # 计算平均值
    average = sum(data) / len(data)
    
    # 计算最大值和最小值
    maxVal = max(data)
    minVal = min(data)
    
    # 计算中位数
    sortedData = sorted(data)
    n = len(sortedData)
    if n == 0: median = 0
    elif n % 2 == 0: median = (sortedData[n//2 - 1] + sortedData[n//2]) / 2
    else: median = sortedData[n//2]
    
    # 返回统计信息字典
    return {"max": maxVal, "min": minVal, "median": median, "average": average }


def analyse(sampling: float = 0.1, cpuSampling: float = 0.1, show: bool = True, info: bool = False) -> Callable:
    """
    性能监控装饰器。
    :param sampling: 监控间隔(秒) 默认0.1
    :param cpuSampling: CPU监控间隔(秒) 默认0.1
    :param info: 是否返回统计信息, 默认True是返回
    :param show: 是否显示统计信息, 默认True是显示
    :param info: 是否返回统计信息
    :return: 装饰器 或 统计数据元组
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Tuple[Any, Dict]:
            # 获取当前进程
            process = psutil.Process(os.getpid())
            
            # 记录初始内存占用
            initialMemory = process.memory_info().rss / 1024 / 1024
            
            # 存储内存和CPU使用情况的列表
            memoryUsage: List[float] = []
            cpuUsage: List[float] = []
            
            # 记录开始时间
            startTime = time.time()
            
            # 监控函数执行期间的内存和CPU使用情况
            def monitor() -> None:
                nonlocal memoryUsage, cpuUsage
                while True:
                    # 获取当前内存使用情况（MB），并减去初始内存
                    memInfo = process.memory_info()
                    memoryMb = memInfo.rss / 1024 / 1024 - initialMemory
                    memoryUsage.append(memoryMb)
                    
                    # 获取当前CPU使用情况（百分比）
                    cpuPercent = process.cpu_percent(interval=cpuSampling)
                    cpuUsage.append(cpuPercent)
                    
                    # 如果函数已经执行完毕，则退出监控循环
                    if not running: break
                    time.sleep(sampling)
            
            # 设置运行标志并启动监控线程
            running: bool = True
            monitorThread = Thread(target=monitor)
            monitorThread.daemon = True
            monitorThread.start()
            
            # 执行被装饰的函数
            try: result = func(*args, **kwargs)
            finally:
                # 函数执行完毕，停止监控
                running = False
                monitorThread.join()
            
            # 计算函数执行时间
            executionTime = time.time() - startTime
            
            # 计算内存和CPU使用的统计信息
            memoryStats = _calculateStats(memoryUsage)
            cpuStats = _calculateStats(cpuUsage)

            # 统计数据
            infos = {
                "execTime": executionTime,
                "initMem": initialMemory,
                "maxMem": memoryStats['max'],
                "minMem": memoryStats['min'],
                "medMem": memoryStats['median'],
                "avgMem": memoryStats['average'],
                "maxCpu": cpuStats['max'],
                "minCpu": cpuStats['min'],
                "medCpu": cpuStats['median'],
                "avgCpu": cpuStats['average']
            }

            # 打印统计信息
            if show:
                print(f"\n函数 {func.__name__} 的性能统计:")
                print(f"执行时间: {executionTime:.2f} 秒")
                print(f"初始内存占用: {initialMemory:.2f} MB")
                print("\n内存使用增量 (MB):")
                print(f"  最大值: {memoryStats['max']:.2f}")
                print(f"  最小值: {memoryStats['min']:.2f}")
                print(f"  中位数: {memoryStats['median']:.2f}")
                print(f"  平均值: {memoryStats['average']:.2f}")  
                print("\nCPU 使用 (%):")
                print(f"  最大值: {cpuStats['max']:.2f}")
                print(f"  最小值: {cpuStats['min']:.2f}")
                print(f"  中位数: {cpuStats['median']:.2f}")
                print(f"  平均值: {cpuStats['average']:.2f}")

            # 返回函数执行结果
            if info: return result, infos
            return result
        return wrapper
    return decorator

