#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


def test_iter():
    """
    实际调的是下面两个方法
    __iter__
    __next__
    """
    items = [1, 2, 3]
    it = iter(items) # 调用的是 items.__iter__()
    i = next(it) # 调用的是 it.__next__()
    assert i == 1


def test_iter2():
    """
    自己定义了类，想迭代类里的数组. 用 __iter__
    """
    class Node():
        def __init__(self, value):
            self._value = value
            self._children = []

        # str()
        def __repr__(self):
            return 'Node({!r})'.format(self._value)

        def add_child(self, node):
            self._children.append(node)

        def __iter__(self):
            return iter(self._children)

    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)

    for s, ch in zip(["Node(1)", "Node(2)"], root):
        assert s == str(ch)


def test_yield():
    """
    使用 yield 将函数转换成生成器
    """
    class Node():
        def __init__(self, value):
            self._value = value
            self._children = []

        # str()
        def __repr__(self):
            return 'Node({!r})'.format(self._value)

        def add_child(self, node):
            self._children.append(node)

        def __iter__(self):
            return iter(self._children)

        # 用 yield 将函数转换成生成器
        def depth_first(self):
            yield self
            for c in self:
                yield from c.depth_first()

    root = Node(0)
    child1 = Node(1)
    child2 = Node(2)
    root.add_child(child1)
    root.add_child(child2)
    child1.add_child(Node(3))
    child1.add_child(Node(4))
    child2.add_child(Node(5))

    for s, ch in zip(["Node(0)", "Node(1)", "Node(3)", "Node(4)", "Node(2)", "Node(5)"], root.depth_first()):
        assert s == str(ch)


def test_yield_from():
    """
    yield from 返回生成器，迭代器
    """
    from collections.abc import Iterable
    def flatten(items , ignore_types =(str , bytes )):
        for x in items:
            if isinstance(x, Iterable) and not isinstance(x, ignore_types):
                yield from flatten (x)
            else:
                yield x
                
    items = [1, 2, [3, 4, [5, 6],7],8]
    # Produces 1 2 3 4 5 6 7 8
    for i, x in zip(range(1, 9), flatten(items)):
        print(x)
        assert i == x


def test_heapq_merge():
    """
    heapq.merge()
    需要本身是有序的，不会立马读取所有序列
    """
    import heapq
    a = [1, 4, 7, 10]
    b = [2, 5, 6, 11]
    for i, c in zip([1, 2, 4, 5, 6, 7, 10, 11], heapq.merge(a, b)):
        print(c)
        assert i == c
        