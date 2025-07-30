#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

from .rediscache import RedisCache


# 使用示例
def test_rediscache1(del_key=1):
    ''' 单元测试
    '''
    import time

    host='192.168.15.111'
    host='localhost'
    host='127.0.0.1'
    port = 6379

    print(f'正在连接Redis:{host}...')
    rc = RedisCache(host=host, port=port)

    def get_value(a, b, c):
        print('in get_value method...')
        #ret = a*b+c
        #ret = '%s_%s_%s' % (a,b,c)
        #ret = (a,b,c)
        #ret = dict(zip('abc', (a,b,c)))

        # 测试key带中文的情况
        # ret = dict(zip('老司机', (a, b, c+int(time.time()))))
        ret = dict(zip('老司机', (a, b, c)))
        return ret


    a,b,c = 2, 3, 4 #int(time.time())
    keyname = '%s_%s_%s' % (a,b,c)
    print(f'keyname:{keyname}...')
    print('a,b,c:', (a,b,c))

    # 使用下面这句是错误的，会直接先去调用get_value
    # ret = rc.cache(keyname, get_value(a,b,c))

    # 正确的方式是先构造一个lambda函数，再传递
    tfun = lambda: get_value(a,b,c)

    # 自动缓存
    print('正在读取缓存...')

    ret = rc.cache(keyname, tfun, tojson=1)
    print('result:', ret)
    print('-'*40)
    assert ret == {'老': 2, '司': 3, '机': 4}

    # 再读一次，肯定是命中缓存
    print('再读一次缓存...')
    ret = rc.cache(keyname, tfun, tojson=1)
    print('result:', ret)
    # result: {'老': 2, '司': 3, '机': 4}
    assert ret == {'老': 2, '司': 3, '机': 4}

    # 删除缓存，如果删除那么每次运行 首先是未命中，然后再命中；
    # rand_key = int(time.time()) % 2
    if del_key:
        print('正在删除缓存...')
        rc.delkey(keyname)


# 使用示例
def test_rediscache(host='127.0.0.1', port=6379, del_key=0):
    ''' 单元测试
    '''
    import time

    print(f'正在连接Redis:{host}...')
    rc = RedisCache(host=host, port=port)

    def get_value(a, b, c):
        print('in get_value method...')
        #ret = a*b+c
        #ret = '%s_%s_%s' % (a,b,c)
        #ret = (a,b,c)
        #ret = dict(zip('abc', (a,b,c)))

        # 测试key带中文的情况
        ret = dict(zip('老司机', (a, b, c+int(time.time()))))
        return ret

    a,b,c = 2, 3, 4 #int(time.time())
    keyname = '%s_%s_%s' % (a,b,c)
    print(f'keyname:{keyname}...')
    print('a,b,c:', (a,b,c))

    # 使用下面这句是错误的，会直接先去调用get_value
    # ret = rc.cache(keyname, get_value(a,b,c))

    # 正确的方式是先构造一个lambda函数，再传递
    tfun = lambda: get_value(a,b,c)

    # 自动缓存
    print('正在读取缓存...')

    ret = rc.cache(keyname, tfun, tojson=1)
    print('result:', ret)
    print('-'*40)

    # 再读一次，肯定是命中缓存
    print('再读一次缓存...')
    ret = rc.cache(keyname, tfun, tojson=1)
    print('result:', ret)

    # 删除缓存，如果删除那么每次运行 首先是未命中，然后再命中；
    # rand_key = int(time.time()) % 2
    if del_key:
        print('正在删除缓存...')
        rc.delkey(keyname)

def main_cli(host='127.0.0.1', port=6379):
    ''' 命令行测试
    '''
    import time

    print(f'正在连接Redis:{host}...')
    rc = RedisCache(host=host, port=port)
    while 1:
        query = input('请输入命令:').strip()
        # 退出
        if query.lower() in ['q', 'quit', 'bye', 'exit']: break
        if query in ['clear', 'restart']:
            pass
        # 拆分命令
        cmdtxt, keyname, value = ['']*3
        cmds = query.split(" ")
        if len(cmds)==2:
            cmdtxt, value = cmds
        elif len(cmds)==3:
            cmdtxt, keyname, value = cmds
        else:
            print('无法识别的命令!')
            continue;
        cmdtxt = cmdtxt.lower()
        if cmdtxt == "delkey":
            keyname = value
            if keyname:
                print(f'正在删除缓存，key={keyname}')
                ret = rc.delkey(keyname)
                print(f'删除结果: {ret}')
        elif cmdtxt == "setkey" :
            print(f'正在设置缓存，key={keyname}')
            ret = rc.setkey(keyname, value)
            print(f'设置结果: {ret}')
        elif cmdtxt == "query":
            keyname = value
            if keyname:
                print(f'正在读取缓存，key={keyname}')
                ret = rc.getkey(keyname)
                print(f'读取结果: {ret}')
        else:
            print('无法识别的命令!')
if __name__ == '__main__':
    pass
    test_rediscache()
