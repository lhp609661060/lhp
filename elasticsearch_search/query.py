#coding=utf8
__author__ = 'lhp'

"""
引用同事kok 写的一段代码
"""

class QueryDict(object):

    def __init__(self, keyword='', start=0, count=10):
        self._query_dict = {
            'query': {
                'bool': {
                    'must': []
                }
            },
            'sort': [],
            'facets': {},
            'aggs': {}
        }


    def limit(self, start, count):
        self._query_dict.update({
            'from': start,
            'size': count
        })


    def sort(self, field, order='desc'):
        self._query_dict.append({
            field: order
        })


    def aggs(self, field):
        self._query_dict['aggs'][field] = {'sum': {'field': field}}


    def keyword(self, keyword, *fields):
        query = {
            'query_string': {
                'query': '%s' % keyword if keyword else '*',
                'default_operator': "and"
            }
        }
        if fields:
            query['query_string']['fields'] = fields

        self._query_dict['query']['bool']['must'].append(query)


    def range(self, field, value):
        if value.count('-') == 1:
            low, high = value.split('-')

            self._query_dict['query']['bool']['must'].append({
                'range': {
                    field: {
                        'gte': low if low else 0.0,
                        'lte': high if high else 99999.0
                    }
                }
            })
        else:
            create_date = value.split('-')
            create_date_begin = '-'.join(create_date[0:3])
            create_date_end = '-'.join(create_date[3:])

            self._query_dict['query']['bool']['must'].append({
                'range': {
                    field: {
                        'gte': create_date_begin if create_date_begin else '',
                        'lte': create_date_end if create_date_end else 'now'
                    }
                }
            })


    def terms(self, field, values):
        self._query_dict['query']['bool']['must'].append({
            'terms': {
                field: values
            }
        })


    def facet(self, field):
        self._query_dict['facets'][field] = {
            'terms': {
                'field': field
            }
        }


    def dict(self):
        return self._query_dict


    def __str__(self):
        return json.dumps(self._query_dict, indent=2)