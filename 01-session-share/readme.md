# 01 Session 共享

## 专题

创建一个网站之后，对于有些API可能需要优化，甚至是用其它语言优化，举个例子: python 实现的API响应速度慢，需要优化，又由于时间紧，不会重写所有API,只用 Go 重写部分的API, 这里面就要涉及到一个原有 Python 中的session 如何在Go中共享

## 想法

利用 Redis 存储Session 状态

## 参考