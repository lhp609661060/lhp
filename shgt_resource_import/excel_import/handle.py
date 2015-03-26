#coding=utf8
__author__ = 'lhp'


"""
excel 数据
"""

import field


class BaseItem(object):

    def __init__(self, item):
        self.item = item
        self.__fields = []
        self.errors = []
        for k in dir(self):
            v = getattr(self, k)
            if isinstance(v, field.Field):
                self.__fields.append((k, v))

    def init(self):
        pass

    def always(self):
        pass

    def fail(self):
        pass

    def items(self):
        self.init()

        for k, fieldObject in self.__fields:
            value = self.item.get(k)
            self.item[k] = fieldObject.clean(value)
            self.errors += fieldObject.errors

        if self.errors:
            self.fail()

        self.always()

        return self.item

class TestItem(BaseItem):

    name = field.CharField(default_value='')

    def fail(self):
        print 'this item error->', [e.message for e in self.errors]

if __name__ == '__main__':
    print 'test excel datas'
    item = TestItem({})
    print item.items()
    print item.errors