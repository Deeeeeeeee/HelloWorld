#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


def test_format():
    """
    自定义格式化输出
    __format__
    """
    _formats = {
        'ymd': '{d.year}-{d.month}-{d.day}',
        'mdy': '{d.month}/{d.day}/{d.year}',
        'dmy': '{d.day}/{d.month}/{d.year}'
    }

    class Date:
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day

        def __format__(self, code):
            if code == '':
                code = 'ymd'
            fmt = _formats[code]
            return fmt.format(d=self)

    d = Date(2012, 12, 21)
    assert format(d) == '2012-12-21'

    assert format(d, 'mdy') == '12/21/2012'


def test_slots():
    """
    __slots__ 可以节省内存，但只能使用这些属性
    """
    class Date:
        __slots__ = ['year', 'month', 'day']
        def __init__(self, year, month, day):
            self.year = year
            self.month = month
            self.day = day