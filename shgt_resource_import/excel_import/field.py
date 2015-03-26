#coding=utf8
__author__ = 'lhp'

import sys
import datetime
import time
import re
from utils import ValueException


"""
拓展django forms.Field
"""



class Field(object):

    empty_value = [None, '', [], {}]
    default_validators  = []
    errors = []
    default_message = {'invalid': u''}
    default_value = ''

    def __init__(self, required=True, validators=[], error_message=None, default_value=None):
        self.required = required
        self.default_validators += validators
        self.default_value = default_value
        if error_message: self.default_message.update(**error_message)

    def to_value(self, value):
        if value in self.empty_value:
            return ''
        return value

    def to_validator(self, value):
        pass

    def __to_validator(self, value):
        for v in self.default_validators:
            try:
                v(value)
            except Exception, e:
                raise ValueException(unicode(e.message))

    def to_required(self, value):
        if value in self.empty_value and self.required:
            raise ValueException(self.default_message['invalid'], 'invalid', {'value': value})

    def clean(self, value):
        try:
            self.to_required(value)
            value = self.to_value(value)
            self.to_validator(value)
            self.__to_validator(value)
            return value
        except ValueException, e:
            self.errors.append(e)
        return self.default_value



class CharField(Field):
    default_message = {
        'invalid': u'请输入值',
        'max_length': u'最多只能输入 ({max_length}) 个字符',
        'min_length': u'最少只能输入 ({min_length}) 个字符'
    }

    def __init__(self, required=True, max_length=None, min_length=None, validators=[], error_message=None, default_value=None):
        super(CharField, self).__init__(required=required, validators=validators, error_message=error_message, default_value=default_value)
        self.max_length = max_length
        self.min_length = min_length

    def to_value(self, value):
        value = super(CharField, self).to_value(value)
        if isinstance(value, float) and value % 1 == 0:
            value = '{:.0f}'.format(value)
        return unicode(value)

    def to_validator(self, value):
        if self.max_length and len(value) > self.max_length:
            raise ValueException(self.default_message['max_length'].format(max_length=self.max_length), 'max_length', {'max_length': self.max_length, 'value': value})

        if ((not self.required and value != '') or self.required) and self.min_length and len(value) < self.min_length:
            raise ValueException(self.default_message['min_length'].format(min_length=self.min_length), 'min_length', {'min_length': self.min_length, 'value': value})


class FloatField(Field):
    default_message = {
        'invalid': 'please a number', #u'请输入数字',
        'gte': 'aaaa{gte}',#u'请输入大于等于 {gte} 的数字',
        'lte': u'请输入小于等于 {lte} 的数字',
        'gt': u'请输入大于 {gt} 的数字',
        'lt': u'请输入小于 {lt} 的数字'
    }

    def __init__(self, required=True, gte=None, lte=None, gt=None, lt=None, validators=[], error_message=None, default_value=None):
        super(FloatField, self).__init__(required=required, validators=validators, error_message=error_message, default_value=default_value)
        self.gte, self.gt, self.lte, self.lt = gte, gt, lte, lt

    def to_value(self, value):
        print 'value->', value
        if value == '':
            return 0.0

        try:
            return float(value)
        except (ValueError, TypeError):
            raise ValueException(self.default_message['invalid'], 'invalid', {'value': value})

    _gte = lambda s, a, b: a >= b
    _lte = lambda s, a, b: a <= b
    _gt = lambda s, a, b: a > b
    _lt = lambda s, a, b: a < b

    def to_validator(self, value):

        for k in ['gte', 'gt', 'lte', 'lt']:
            v = getattr(self, k)
            if v and getattr(self, '_{}'.format(k))(value, v):
                raise ValueException(self.default_message[k].format(**{k: v}))

class DateTimeField(Field):
    default_message = {
        'invalid': 'please a date', #u'请输入日期',
    }

    formats = ['%Y-%m-%d', '%Y/%m/%d', '%Y%m%d','%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f',
               '%Y-%m-%d %H:%M', '%m/%d/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S.%f',
               '%m/%d/%Y %H:%M', '%m/%d/%Y', '%m/%d/%y %H:%M:%S', '%m/%d/%y %H:%M:%S.%f',
               '%m/%d/%y %H:%M', '%m/%d/%y']

    def __init__(self, required=True, strptime=None, validators=[], error_message=None, default_value=None):
        super(DateTimeField, self).__init__(required=required, validators=validators, error_message=error_message, default_value=default_value)
        self.strptime = strptime

    def to_value(self, value):
        value = super(DateTimeField, self).to_value(value)

        if isinstance(value, (datetime.datetime, datetime.date)):
            return value

        if isinstance(value, float):
            try:
                s_date = datetime.date(1899, 12, 31).toordinal() - 1
                return datetime.date.fromordinal(s_date + int(value))
            except:
                raise ValueException(self.default_message['invalid'], 'invalid', {'value': value, 'strptime': ['%Y-%m-%d']})

        if isinstance(value, (str, unicode)):
            formats = []
            if self.strptime is None:
                formats = self.formats
            elif isinstance(self.strptime, (str, unicode)):
                formats = [self.strptime]
            elif isinstance(self.strptime, list):
                formats = self.strptime

            for _ in formats:
                try:
                    return datetime.datetime.strptime(value, _)
                except: pass
            raise ValueException(self.default_message['invalid'], 'invalid', {'value': value, 'strptime': formats})

        raise ValueException(self.default_message['invalid'], 'invalid', {'value': value, 'strptime': ['%Y-%m-%d']})

class SpecField(CharField):
    default_message = {
        'invalid': 'please a value', #u'请输入值',
    }

    re_g = '[*Xx×]'

    def __init__(self, spec_format=[], spec_required=[], error_message=None, default_value=None):
        super(SpecField, self).__init__(required=True, validators=[], error_message=error_message, default_value=default_value)
        self.spec_format = spec_format
        self.spec_required = spec_required
        
    def to_value(self, value):
        value = super(SpecField, self).to_value(value)

        l = []
        for s in re.split(self.re_g, value):
            spec = re.findall('\d*\.?\d+|[cC]', s)
            if len(spec) == 0:
                l.append(0)
            elif len(spec) == 1:
                l.append(float(spec[0]))
            elif len(spec) == 2:
                if spec[0] in 'Cc':
                    l.append(float(spec[0]))
                else:
                    l.append(float(spec[-1]))
            else:
                l.append(0)

        return self.__format(l, self.spec_format)

    def to_validator(self, value):
        for k in self.spec_required:
            if k not in value or value[k] <= 0:
                raise ValueException(self.default_message['invalid'], 'invalid', {'value': value, 'spec_required': self.spec_required})
        
    def __format(self, specs, spec_format):
        s_l = len(specs)
        d = {}
        for formats in spec_format:
            f_l = len(formats)
            if f_l == s_l:
                d = dict(zip(formats, specs))
                break

        if 'act_length' in d in d['act_length'] in 'Cc':
            d['act_length'] = 0
        return d



def test(field, value):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    value = field.clean(value)
    for error in field.errors:
        print error.message

    print 'value -> {value}: type -> {typ}'.format(value=value, typ=type(value))


if __name__ == '__main__':
    print 'test ......................'
    a = CharField(max_length=10, min_length=3, required=False)
    b = FloatField(gte=3)
    c = DateTimeField(default_value=datetime.datetime.now())
    test(c, '2015/09/09s')

