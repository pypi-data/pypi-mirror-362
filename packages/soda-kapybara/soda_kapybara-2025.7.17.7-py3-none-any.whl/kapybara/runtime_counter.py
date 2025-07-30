class Counter:
    """一个简单的可变整数计数器。

    这避免了单例模式的复杂性，因为 Python 模块本身就是单例的。
    在模块级别创建该类的实例后，无论在哪里导入，都是同一个对象。
    """

    def __init__(self, initial_value=0):
        self.value = initial_value

    def __iadd__(self, other):
        """支持原地加法（例如：`counter += 1`）。"""
        self.value += other
        return self

    def __int__(self):
        """允许强制转换为 int，例如：`int(counter)`。"""
        return self.value

    def __repr__(self):
        """提供开发者友好的字符串表示。"""
        return f'Counter(value={self.value})'

    def __str__(self):
        """提供用户友好的字符串表示。"""
        return str(self.value)
