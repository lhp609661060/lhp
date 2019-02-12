# coding=utf-8

"""
遍历指定目录代码清单
"""

import os
import pandas


FILE_EXT = set(['.java', '.js', '.css', '.xml', '.properties', '.html', '.py', '.conf', '.scss'])


def get_path(path):
    """
    通过指定path获取目录下所有文件，文件相对目录，文件名，文件类型，代码行数
    return [{'file': 'xxx', 'ext':'xxx', 'path':'xxx', 'code_nm': 12}]
    """
    result = []

    for root, fl, fs in os.walk(path):
        if fs:
            for f in fs:
                f_info = get_file_info(os.path.join(root, f), f)
                f_info['path'] = f_info['path'].replace(path, '').replace('\\', '/')
                result.append(f_info)

    return result


def get_file_info(path, fname):
    """
    获取文件信息,文件名称，文件类型，代码行数
    """

    ext = os.path.splitext(path)[1]
    if ext not in FILE_EXT:
        return dict(file=fname, ext=ext, path=path, count=0)

    count = 0
    with open(path, 'r', encoding='gbk', errors='ignore') as f:
        for r in f.readlines():
            count += 1

    return dict(file=fname, ext=ext, path=path, count=count)


def statistics(data):
    """
    统计数据，模块，文件数，代码行数
    """

    # 过滤掉 .idea
    data = filter(lambda d: '/.idea' not in d['path'], data)

    # 过滤掉target
    data = filter(lambda d: '/target' not in d['path'], data)

    result = {}

    for d in data:
        mode = d['path'].split('/')[1]
        if mode not in result:
            result[mode] = dict(mode=mode, file_count=0, code_count=0)
        result[mode]['file_count'] += 1
        result[mode]['code_count'] += d['count']

    return result.values()


def statistics_file(data):
    """
    统计文件类型，文件个数，代码行数
    """

    # 过滤掉 .idea
    data = filter(lambda d: '/.idea' not in d['path'], data)

    # 过滤掉target
    data = filter(lambda d: '/target' not in d['path'], data)

    result = {}

    for d in data:
        ext = d['ext']
        if ext not in result:
            result[ext] = dict(ext=ext, file_count=0, code_count=0)
        result[ext]['file_count'] += 1
        result[ext]['code_count'] += d['count']

    return result.values()


def main(path):
    data = get_path(path)

    df = pandas.DataFrame.from_dict(data)
    df.to_excel(u'代码清单-明细.xlsx', index=False)

    statistics_data = statistics(data)
    statistics_df = pandas.DataFrame.from_dict(statistics_data)
    statistics_df.to_excel(u'代码清单-模块.xlsx', index=False)

    statistics_file_data = statistics_file(data)
    statistics_file_data_df = pandas.DataFrame.from_dict(statistics_file_data)
    statistics_file_data_df.to_excel(u'代码清单-文件类型.xlsx', index=False)

    


if __name__ == '__main__':
    main(u'E:/workspce/imp/rz/trunk')
