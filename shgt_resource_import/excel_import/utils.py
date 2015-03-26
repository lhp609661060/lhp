#coding=utf8
__author__ = 'lhp'

class ValueException(Exception):
    
    def __init__(self, message=None, code=None, params={}):
        super(ValueException, self).__init__(message)
        self.code = code
        self.params = params



if __name__ == '__main__':
    print 'this is test ....................'