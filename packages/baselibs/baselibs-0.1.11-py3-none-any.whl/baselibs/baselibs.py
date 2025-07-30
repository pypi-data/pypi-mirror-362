#!/usr/bin/env python3
#coding:utf-8
# update: 2024/11/25
'''
通用基础库 版本: v0.1.10
'''

__author__ = 'xmxoxo'

import argparse
import sys
import os
import re
import json
import hashlib
import random
import time
import string
import traceback
import logging
import pandas as pd
import numpy as np
import requests

pl = lambda x='', y='-', l=40: print(y*l) if x=='' else print(str(x)) if x[-3:]=='...' or y=='' else print(str(x).center(l, y))
pr = lambda x: print('%s:%s' % (x, eval(x)))
pt = lambda x, y=60: (print('\r%s'% (' '*y), end=''), print('\r%s'%x, end=''))

# 格式转换
format_json = lambda dat: json.dumps(dat, ensure_ascii=False, indent=4)
format_time = lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x))

def wlog(txt:str, work_path="./logs"):
    ''' 写入日志
    '''
    mkfold(work_path)
    today = time.strftime('%Y%m%d', time.localtime())
    fname = os.path.join(work_path, f"server_log_{today}.txt")
    tm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    log_txt = f"[{tm}] {txt}\n"
    savetofile(log_txt, fname, method="a+")

def rand_taskid(pre='', ext=''):
    ''' 按时间随机生成任务序列号
    '''
    nowtime = time.time()
    fmttxt = time.strftime('%Y%m%d%H%M%S', time.localtime(nowtime))
    dt = int((nowtime - int(nowtime))*1000)
    rndnum = random.randint(100, 999)
    ret = pre + fmttxt + str(dt)+ str(rndnum) + ext
    return ret

def rand_filename(path='', pre='', ext=''):
    '''按时间戳生成文件名'''

    nowtime = time.time()
    fmttxt = time.strftime('%Y%m%d%H%M%S', time.localtime(nowtime))

    '''
    dt = int((nowtime - int(nowtime))*1000000)
    filename = '%s%s%03d%s' % (pre, fmttxt, dt, ext)
    '''

    dt = int((nowtime - int(nowtime))*1000)
    rndnum = random.randint(100, 999)
    filename = '%s%s%03d%03d%s' % (pre, fmttxt, dt, rndnum, ext)
    if path:
        mkfold(path)
    fname = os.path.join(path, filename)
    return fname

def mkfold(new_dir):
    '''创建目录，支持多级子目录
    '''
    try:
        if new_dir == '': return
        if not os.path.exists(new_dir):
            os.makedirs(new_dir, exist_ok=True)
    except Exception as e:
        pass

def readtxtfile(fname, encoding='utf-8'):
    ''' 读取文本文件, 自动识别编码 '''

    try:
        with open(fname, 'r', encoding=encoding) as f:
            data = f.read()
        return data
    except UnicodeDecodeError as e:
        try:
            with open(fname,'r', encoding='gb2312') as f:
                data = f.read()
            return data
        except Exception as e:
            return ''
    except Exception as e:
        return ''

def readtxt(fname, encoding='utf-8'):
    ''' 读入文件   '''
    try:
        with open(fname, 'r', encoding=encoding) as f:
            data = f.read()
        return data
    except Exception as e:
        return ''

def readjson(fname):
    try:
        txt = readtxtfile(fname)
        jdat = json.loads(txt)
        return jdat
    except Exception as e:
        return None

def readjsonp(fname):
    try:
        txt = readtxtfile(fname)
        jdat = [json.loads(x) for x in txt.splitlines() if x]
        return jdat
    except Exception as e:
        return None

def readbin(fname):
    '''读取二进制文件'''

    try:# 保存文本信息到文件
        with open(fname, "rb") as f:
            byte_data = f.read()
        return byte_data
    except Exception as e:
        return b''

def savetxt(txt, filename, encoding='utf-8', method='w'):
    return savetofile(txt, filename, encoding, method)

def savetofile(txt, filename, encoding='utf-8', method='w'):
    '''保存文本信息到文件'''

    try:
        # 自动创建目录
        mkfold(os.path.dirname(filename))

        with open(filename, method, encoding=encoding) as f:
            f.write(str(txt))
        return 1
    except Exception as e:
        print(e)
        return 0

def savetobin(dat, filename, method='wb'):
    '''按二进制保存文件
    '''
    try:
        # 自动创建目录
        mkfold(os.path.dirname(filename))

        with open(filename, method) as f:
            f.write(dat)
        return 1
    except Exception as e:
        return 0

def savejson(dat, outfile, indent=4, method='w'):
    ''' 将json数据保存成文件
    '''
    dat_txt = json.dumps(dat, ensure_ascii=False, indent=indent)
    return savetofile(dat_txt, outfile, method=method)

def savejsonp(dat, outfile, method='w'):
    ''' 将数据保存为jsonp格式，一行一条记录
    '''
    try:
        lines = [json.dumps(x, ensure_ascii=False, indent=None) for x in dat]
        dat_txt = '\n'.join(lines) + "\n"
        return savetofile(dat_txt, outfile, method=method)
    except Exception as e:
        print(e)
        return 0

def templace_replace(template:str, fields:dict):
    ''' 按模板替换
    template: 模板，形如:"这是一个$count模板"
    fields: 变量字典，形如{'count':2,'secret':'abc'}
    '''

    ret = template
    for field, value in fields.items():
        field = field.strip()
        key = '$%s' % field
        if type(value) == list:
            value = "','".join(map(str, value))
        else:
            value = str(value)

        ret = ret.replace(key, str(value))
    return ret

def pathsplit (fullpath):
    '''将路径拆分为目录，文件，扩展名三个部分, 扩展名自动小写'''

    try:
        (filepath, tempfilename) = os.path.split(fullpath)
        (filename, extension) = os.path.splitext(tempfilename)
        extension = extension.lower()
        return filepath, filename, extension
    except Exception as e:
        return '', '' , ''

def replace_ext (filename:str, new_ext:str):
    ''' 替换新的扩展名
    '''
    p, f, e = pathsplit(filename)
    new_filename = os.path.join(p, f+new_ext)
    return new_filename

def replace_dict (txt:str, dictKey:dict, isreg:bool=False):
    '''按字典进行批量替换
    isreg: 是否启用正则
    '''
    try:

        tmptxt = txt
        for k, v in dictKey.items():
            if type(v) in [dict, tuple, list]:
                v = json.dumps(v, ensure_ascii=False)
            else:
                v = str(v)
                
            if isreg:
                tmptxt = re.sub(k, v, tmptxt)
            else:
                tmptxt = tmptxt.replace(k, v)
        return tmptxt
    except Exception as e:
        print(e)
        return tmptxt
    
def fmtText (txt):
    '''文本内容清洗（含HTML）
    '''
    # 删除HTML标签
    p = re.compile(r'(<(style|script)[^>]*?>[^>]+</\2>)|(<!--.+?-->)|(<[^>]+>)', re.S)
    txt = re.sub(p, r"", txt)

    # HTML实体替换
    dictKey = {
            '&nbsp;': ' ',
            '&quot;': '"',
            '&#034;': '"',
            '&apos;': '\'',
            '&amp;': '&',
            '&lt;':'<',
            '&gt;':'>',
            }
    txt = replace_dict(txt, dictKey)
    # 删除其它HTML实体
    txt = re.sub(r'(&[#\w\d]+;)',r"",txt)
    # 空格，制表符换成半角空格
    txt = re.sub('([　\t]+)',r" ",txt)
    # 多个连续的空格换成一个空格
    txt = re.sub(r'([ "?\t]{2,})',r" ", txt)
    # 删除空行
    txt = re.sub(r'(\n\s+)',r"\n",txt)
    # 中文之间的空格 [\u4e00-\u9fa5]
    #txt = re.sub(r'(\n\s+)',r"\1\2",txt)
    return txt

def cut_sent1(txt):
    '''切分句子，多种符号分割。'''

    txt = re.sub(r'([　\t]+)',r" ",txt)  #去掉特殊字符
    txt = re.sub(r'([ "?\t]{2,})',r" ",txt)  #多个连续的空格换成一个空格
    txt = re.sub(r'(\n\s*\n)',r"\n",txt)  # blank line

    txt = re.sub(r'([;；。！？\?])([^”])',r"\1\n\2", txt) # 单字符断句符，加入中英文分号
    txt = re.sub(r'(\.{6})([^”])',r"\1\n\2",txt) # 英文省略号
    txt = re.sub(r'(\…{2})([^”])',r"\1\n\2",txt) # 中文省略号
    # txt = re.sub('(”)','”\n',txt)   # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    txt = txt.rstrip()       # 段尾如果有多余的\n就去掉它
    nlist = txt.split("\n")
    nnlist = [x for x in nlist if x.strip()!='']  # 过滤掉空行
    return nnlist

def delspace(txt):
    '''预处理: 去空行 空格
    '''
    txt = re.sub(r'([　\t]+)',r" ",txt)  #去掉特殊字符
    txt = re.sub(r'([ "?\t]{2,})',r" ",txt)  #多个连续的空格换成一个空格
    txt = re.sub(r'(\n\s*\n)',r"\n",txt)  # blank line
    #全角替换
    #txt = txt.replace('％','%')
    #txt = txt.replace('、','')
    return txt

def cut_sent(txt):
    ''' 切分句子，仅按句号分割。
    '''
    txt = delspace(txt)
    txt = re.sub('([。])',r"\1\n",txt) # 单字符断句符，加入中英文分号
    # txt = re.sub('(\.{6})([^”])',r"\1\n\2",txt) # 英文省略号
    # txt = re.sub('(\…{2})([^”])',r"\1\n\2",txt) # 中文省略号
    # txt = re.sub('(”)','”\n',txt)   # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    txt = txt.rstrip()       # 段尾如果有多余的\n就去掉它
    # txt = re.sub('(\n"|"\n)',r"\n",txt)  #行开头与行结尾的引号去掉
    # txt = re.sub('(["])',r'""',txt)    #剩下的引号换成2个
    # nlist = txt.split("\n")
    nlist = txt.splitlines()
    nlist = [x for x in nlist if x.strip()!='']  # 过滤掉空行
    return nlist

def cut_segment_text(text, ret_length=512, segment=4):
    '''从长文本中分段截取并合返回指定长度的文本；
    参数：
        text：待处理的文本；
        ret_length：返回的最大长度；
        segment： 分段数量，分成几段提取；
    返回：字符串，总长度不超过 ret_length
    '''

    # 计算文本总长
    total = len(text)
    # 实际长度小于返回长度时 直接返回
    if total < ret_length:
        return text

    # 实际长度小于返回长度2倍，直接从前面截断
    if total < ret_length * 2:
        ret = text[:ret_length]
        return ret

    seg_len = ret_length // segment
    segs = (total - seg_len) // (segment -1)
    # 分段截取
    cut_txt = [text[i: i+seg_len] for i in range(0, total, segs)]

    # 组合
    ret = ';'.join(cut_txt)
    return ret


# -----------------------------------------

# 长文本智能拆分
def find_char_pos(txt, start, chars='。；，', maxlen=256):
    ''' 从文本的start位置向左右两边寻找，找到最近的chars符号，
    返回: 拆分的位置索引
    '''
    txt_length = len(txt)
    if txt_length <= maxlen:
        return txt_length

    pos = start     # 起点
    dire = 1        # 1向右，-1向左
    dist = 0        # 距离
    # 返回的结果
    cut_pos = 0
    while 1:
        # 找到指针位置的字符
        # print('pos:', pos)
        char = txt[pos]
        # 判断是否特定字符
        if char in chars:
            # 找到后退出
            #print('char:', char)
            cut_pos = pos+1
            break;
        # 没找到则继续下一个位置
        dire = -dire
        # 每到1方向时，距离增加
        if dire == -1:
            dist += 1
        pos = start + dire * dist

        # 超出位置判断
        if dist > maxlen:
            break; # 左右各找了maxlen都没有找到符号
        if pos<0 or pos>=txt_length:
            break # 超出了字符边界
    return cut_pos

def text_split_pos(txt, chars='。；', maxlen=256):
    ''' 文本智能拆分。把文本拆分成多段，分隔符为chars, 且保证每段的最大长度不超过maxlen
    返回：拆分后的列表
    '''
    # import math
    # print('文本长度:', len(txt))
    length = len(txt)
    if length <= maxlen:
        return [txt]

    ret_list = []
    tmp_txt = txt
    while 1:
        txt_length = len(tmp_txt)
        # 如果长度小于最大长度，退出
        if txt_length <= maxlen:
            ret_list.append(tmp_txt)
            break
        # 计算要分几段
        segs = math.ceil( txt_length / maxlen)
        # print('分段数：%d'%segs)
        start = txt_length // segs
        # 计算位置
        cut_pos = find_char_pos(tmp_txt, start, chars=chars, maxlen=maxlen)
        if cut_pos <= 0:
            # 没找到的情况：直接按start的位置切
            cut_pos = start

        #print('cut_pos:', cut_pos)
        sub_txt = tmp_txt[:cut_pos]
        #print('sub_txt:', sub_txt)
        ret_list.append(sub_txt)
        # 截取剩下的
        tmp_txt = tmp_txt[cut_pos:]
    return ret_list

def text_split(txt, chars='。；', maxlen=256):
    ''' 文本智能拆分。把文本拆分成多段，分隔符为chars,且保证每段的最大长度不超过maxlen
    返回：拆分后的列表
    '''
    result = []
    current_segment = ''

    for char in txt:
        if char in chars:
            if len(current_segment) + 1 > maxlen:
                result.append(current_segment)
                current_segment = char
            else:
                current_segment += char
                result.append(current_segment)
                current_segment = ''
        else:
            if len(current_segment) >= maxlen:
                result.append(current_segment)
                current_segment = char
            else:
                current_segment += char

    if current_segment:
        result.append(current_segment)

    return result

def text_split_with_regex(txt, chars='。；', maxlen=256):
    ''' 文本智能拆分。把文本拆分成多段，分隔符为chars,且保证每段的最大长度不超过maxlen
    返回：拆分后的列表，保留分隔符
    '''

    # 创建正则表达式模式，匹配以指定字符结尾的部分，并保留这些字符
    pattern = f'([^{chars}]*[{chars}])'

    # 使用re.findall找到所有匹配的部分
    segments = re.findall(pattern, txt)

    # 处理最后一部分，如果没有以指定字符结尾
    last_segment = txt[len(''.join(segments)):]
    if last_segment:
        segments.append(last_segment)

    # 合并超过maxlen长度的段落
    result = []
    current_segment = ''

    for segment in segments:
        if len(current_segment) + len(segment) <= maxlen:
            current_segment += segment
        else:
            result.append(current_segment)
            current_segment = segment

    if current_segment:
        result.append(current_segment)

    return result

def text_splitline(text, chars='。；？?！!', maxlen=64):
    ''' 对文本进行重新分行，拆分后按行组合方式，最大长度maxlen=64；
    '''

    # 先预处理加上换行符
    text = text.replace("\r", "").replace("\n", "")
    text = re.sub(f"([{chars}])", r"\1\n", text)
    # 按符号进行分行
    lines = text.splitlines()

    # 重新计算分行：按长度
    ret = []
    last_seg = ""
    for line in lines:
        if last_seg == "":
            last_seg += line
            continue

        if len(last_seg) + len(line) > maxlen:
            ret.append(last_seg)
            last_seg = line
        else:
            last_seg += line

    if last_seg!="":
        ret.append(last_seg)
    return ret

def test_split():
    # 示例用法
    text = "这是一个示例文本。这个文本需要被拆分成多段；每一段的最大长度不能超过设定的值。"
    text = "针对红薯汁加工过程易褐变、风味易伤失、后浑浊现象严重、粘度大难过滤和纤维素、淀粉含量高，不能直接压榨成汁等技术难点，明确生物酶、膜超滤、超高温瞬时杀菌和护色、酶解等生物工程关键技术，首次研制出浓缩红薯清汁大规模生产新产品，制备出可溶性固形物含量60.5°BX、pH4.0-6.0的浓缩红薯清汁。在国内外，首次研究出浓缩红薯清汁加工产业化节电、节水、节煤、降耗生产新工艺，设计创建出产能3000吨/月标准化生产线，于2005年完成设备选型、成套设备配置、安装调试，并当年批量生产248吨，是国内外唯一产业化生产浓缩红薯清汁的企业，产品质量（内控）合格率达99.68%以上。企业不断地进行系统工艺优化、设备升级等技术改造，共投入研发经费920.7万元，使生产总成本降低了5.6%。企业节能减排成效显著，其中，吨浓缩红薯汁耗电123.53度、总节电31.1%，吨节煤0.445吨、节煤率57%，2009年吨浓缩红薯汁节水12.34吨、吨耗水6.96吨，仅为2007年耗水量55%，达到发达国家果蔬汁加工吨耗水4-7吨水平，显著地优于中国吨耗水10-15吨指标，“三”废排放均达国家标准。创新性地开发出红薯去皮前处理、0.5:1料液比、2-5mm破碎度、0.07%Vc护色、55℃0.25%淀粉酶水解、0.1%糖化酶、0.15%果胶酶防浓缩后浑浊、0.17%活性炭脱色、0.2%膨润土脱胶、8min超滤、120-125℃瞬间杀菌等新技术。红薯清汁中不含有果胶和淀粉，浊度、透光率、色值等均达最佳值，且保留了红薯原有天然风味。产品色值≤0.14、浊度≤2.0NTU；优化了超滤浓缩设备，使可溶性固形物含量达60.1-60.50BX，透光率≤97%。5年累计生产出口浓缩红薯清汁2.35万吨，产品全部出口美国，出口价格1400美元/吨，实现销售收入2.27亿元。企业获利0.91亿元，国家出口退税0.24亿元，农民获利0.65亿元，国家创汇0.33亿美元，国家税收741.77万元。"
    # segments = text_split_with_regex(text, chars='。；', maxlen=20)
    # text = text.replace("。", "。\n")
    segments = text_splitline(text, maxlen=64)
    print(segments)

#-----------------------------------------

def getFiles (workpath, fileExt=[]):
    ''' 单目录遍历，返回所有子目录和文件
    get all files and floders in a path
    fileExt: ['.png','.jpg','.jpeg'] ['png','jpg','jpeg']
    return:
       return a list, include floders and files , like [['./aa'],['./aa/abc.txt']]
    '''
    # 扩展名处理：小写，去点
    fileExt = [x.lower().replace('.', '') for x in fileExt]

    try:
        lstFiles = []
        lstFloders = []

        if os.path.isdir(workpath):
            if not workpath.endswith("/"): workpath += "/"
            for dirname in os.listdir(workpath):
                file_path = os.path.join(workpath, dirname)
                if os.path.isfile(file_path):
                    if fileExt:
                        ext = os.path.splitext(dirname)[1][1:].lower()
                        if ext in fileExt:
                           lstFiles.append (file_path)
                    else:
                        lstFiles.append (file_path)
                if os.path.isdir(file_path):
                    lstFloders.append (file_path)

        elif os.path.isfile(workpath):
            lstFiles.append(workpath)
        else:
            return None

        lstRet = [lstFloders, lstFiles]
        return lstRet
    except Exception as e :
        return [[], []]

def get_all_folders(workpath, order=0):
    '''递归返回目录下的所有目录，包括子目录；
    order：返回顺序, 0:从浅到深； 1:从深到浅
    get all folder include subfolders
    return:
       return a Generator, include all folder, like ['./a/b','./b/bb']
    '''

    try:
        if os.path.isdir(workpath):
            for dirname in os.listdir(workpath):
                # 2024/10/29 在linux下，中文目录会出现： Can't mix strings and bytes in path components
                if type(dirname)==bytes:
                    dirname = dirname.decode('utf-8')

                file_path = os.path.join(workpath, dirname)
                if os.path.isdir(file_path):
                    # 从浅到深：先输出当前目录
                    if order==0:
                        yield file_path

                    yield from get_all_folders(file_path, order=order)

                    if order==1:
                        # 从深到浅：先输出子目录；
                        yield file_path
    except Exception as e :
        print(e)
        pass

def getAllFiles_Generator (workpath, fileExt=[]):
    '''递归返回目录下的所有文件，包括子目录下的文件
    get all files in a folder, include subfolders
    fileExt: ['png','jpg','jpeg'] ['.png','.jpg','.bmp']
    return:
       return a Generator, include all files , like ['./a/abc.txt','./b/bb.txt']
    '''
    # 扩展名处理：小写，去点
    fileExt = [x.lower().replace('.','') for x in fileExt]
    try:
        if os.path.isdir(workpath):
            for dirname in os.listdir(workpath):
                # 2024/10/29 在linux下，中文目录会出现： Can't mix strings and bytes in path components
                if type(dirname)==bytes:
                    dirname = dirname.decode('utf-8')
                file_path = os.path.join(workpath, dirname)
                if os.path.isfile(file_path):
                    if fileExt:
                        ext = os.path.splitext(dirname)[1][1:].lower()
                        if ext in fileExt:
                           yield file_path
                    else:
                        yield file_path
                if os.path.isdir(file_path):
                    yield from getAllFiles_Generator(file_path, fileExt)
    except Exception as e :
        print(e)
        pass

def rel_file1(workpath, fname, outpath, out_filename='', remain_deep=1, abspath=0):
    ''' 生成相对的文件路径并保持目录结构
    将workpath下的fname文件，生成到outpath目录下,
    文件改名为out_filename；out_filename为空则保留原文件名
    保留最后remain_deep级目录及子目录结构，
    abspath: 是否输出绝对路径
    '''

    spath, sname = os.path.split(fname)
    # 计算相对路径：remain_deep=保留的目录结构深度
    if remain_deep<=1: remain_deep=1
    remain_path = '../' * remain_deep
    tpath = os.path.join(workpath, remain_path)
    rpath = os.path.relpath(spath, tpath)
    # 计算新的目录
    folder = os.path.join(outpath, rpath)
    # print('rpath:', rpath)
    # print('folder:', folder)
    # 创建目录
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    # 计算新的文件路径
    if out_filename == '':
        out_filename = sname
    fout = os.path.join(folder, out_filename)
    # 返回绝对路径
    if abspath:
        fout = os.path.abspath(fout)
    return fout

def rel_file(workpath, fname, outpath, out_filename='', remain_deep=1, abspath=0):
    ''' 生成相对的文件路径并保持目录结构
    对于基础目录：workpath
    将workpath下的fname文件，生成到outpath目录下,
    保留最后remain_deep级目录及子目录结构，
    文件改名为out_filename；out_filename为空则保留原文件名, 仅修改后缀；
    abspath： 是否返回绝对路径
    '''

    spath, sname = os.path.split(fname)
    # 计算相对路径：remain_deep=保留的目录结构深度

    if remain_deep>0:
        remain_path = workpath
        tpath = workpath
    else:
        remain_path = '../' * abs(remain_deep)
        tpath = os.path.join(workpath, remain_path)
    rpath = os.path.relpath(spath, tpath)

    # 计算新的目录
    folder = os.path.join(outpath, rpath)
    # print('rpath:', rpath)
    # print('folder:', folder)
    # 创建目录
    if not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    # 计算新的文件路径
    if out_filename == '':
        out_filename = sname
    fout = os.path.join(folder, out_filename)
    # 返回绝对路径
    if abspath:
        fout = os.path.abspath(fout)
    return fout

# -----------------------------------------

def api_post_data (url, data, timeout=30, data_format='json', headers=None, method="post"):
    ''' 向URL发送数据并返回json格式化结果
    '''
    method = method.lower()
    try:
        if method=='post':
            if data_format=='form':
                if timeout>0:
                    res = requests.post(url, headers=headers, data=data, timeout=timeout)
                else:
                    res = requests.post(url, headers=headers, data=data)
            if data_format=='json':
                if timeout>0:
                    res = requests.post(url, headers=headers, json=data, timeout=timeout)
                else:
                    res = requests.post(url, headers=headers, json=data)
            # res.status_code
            res.encoding = 'utf-8'
            ret = res.json()
            # ret = json.loads(res.text)
        elif method=='get':
            res = requests.get(url, json=data, timeout=timeout, headers=headers)
            ret = res.json()

        return ret
    except Exception as e:
        print(e)
        return None

# -----------------------------------------

def pre_format (path):
    '''对目录下的文件遍历，处理文本内容清洗（含HTML格式去除）
    '''
    intTotalLines = 0
    lstF = getFiles(path)

    for fname in lstF[1] :
        print('Processing file:%s' % (fname))
        txt = readtxtfile(fname)
        txt = fmtText(txt)
        savetofile(txt, fname)
    print('Total: %d File(s)' % (len(lstF[1]) ) )

def pre_clean (path):
    '''批量处理目录下文件，对文本字符清洗 '''

    intTotalLines = 0
    lstF = getFiles(path)

    for fname in lstF[1] :
        print('Processing file:%s' % (fname))
        txt = readtxtfile(fname)
        txt = txtfilter(txt)
        savetofile(txt, fname)
    print('Total: %d File(s)' % (len(lstF[1]) ) )

# 删除文件
def delete_file(filename):
    try:
        os.remove(filename)
        # print(f'File:{filename} deleted success')
    except OSError as e:
        pass
        # print(f'Error deleting file {filename}:{e}')


def batch_rename (path, intBegin=1):
    '''
    文件批量重命名，对目录下(不含子目录)的所有文件按序号开始命名；
    序号会根据文件的数量自动在前面补0，例如有1000个文件，则第一个文件名为：0001.txt
    执行过程中将输出重命名信息，例如：
       [./dat/akdjf.txt] =rename=> [./dat/0023.txt]
    参数：
       path        目录。不会处理子目录；
       intBegin    开始序号。默认=1，即从1开始命名。
    返回
       无返回值
    '''

    # 命名的开始序号, intBegin = 1
    lstF = getFiles(path)
    lstRen = []
    intFNWidth = len(str(len(lstF[1])))
    for f in lstF[1] :
        #扩展名
        if f.rfind('.')>=0:
            strExt = f[f.rindex ('.'):]
        else:
            strExt = ''

        #生成新的文件名
        # 2019/1/16 按最大长度在前面补0，这样文件名排序看起来方便；例如：0023
        nfname = os.path.join(path , str(intBegin).zfill(intFNWidth)) + strExt
        print('[%s] =rename=> [%s]' %(f,nfname))
        intBegin += 1

        # 判断是否目标与源文件同名, 例如 1.txt==>1.txt
        if f == nfname:
            continue

        # 判断是否在重复列表中
        if f in lstRen :
            f = f + '.ren'

        # To do 判断是否会重名，也就是判断是否已经存在目标文件，存在则重命名
        if os.path.exists(nfname):
            #添加到重名列表中,然后改名
            lstRen.append(nfname)
            os.rename(nfname, nfname + '.ren' )

        os.rename(f, nfname)

        # 调试用
        if intBegin>10:
            pass
            #break

def blankfile (fname):
    ''' 判断是否为空文件； 空文件是指替换了空格，制表符后内容为空的文件
    '''
    pass
    txt = readtxtfile(fname)
    txt = delspace(txt)
    txt = txt.replace('\n','')
    txt = txt.replace('\r','')
    if txt == "":
        return fname
    else:
        return ''

def delblankfile (path, isDel = False):
    '''  删除目录下的空文件
    '''
    lstF = getFiles(path)
    for f in lstF[1] :
        print('\rfile:%s' % f,end = '')
        #print('file:%s' % f)
        if blankfile(f):
            print('\rblank file: %s' % f)
            if isDel:
                os.remove(f)
            else:
                os.rename(f, f+'.del')
    print('\r'+' '*60)

def txtmd5 (txt):
    ''' 计算文本的MD5值
    '''
    strMD5 = hashlib.md5(txt.encode(encoding='UTF-8')).hexdigest()
    return strMD5

def SameFile (dicHash, strFileName, strBody):
    '''
    判断内容相同的文件，使用MD5进行计算
    参数：
        dicHash        哈希表，用来存放文件名与哈希值对应关系；
        strFileName    文件名，用来标识文件，也可用完整路径；
        strBody        文件内容
    返回：
        None 则表示没有重复，并且会更新哈希表
        重复时返回重复的文件名
    '''

    strMD5 = txtmd5(strBody)
    if strMD5 in dicHash.keys():
        # 冲突表示重复，返回对应的值
        return dicHash[strMD5]
    else:
        dicHash[strMD5] = strFileName
        return None

def FindSameFile (path, isDel=False):
    '''
    检查目录下文件内容是否相同,使用MD5值来判断文件的相同。
    相同的文件可以直接删除或者改名为"原文件名.same",
    同时输出提示信息,例如：
        File [./dat/1.txt] =same=> [./dat/92.txt]
    参数:
       path    要检查的目录；只检查该目录不包含子目录；
       isDel   是否要删除，默认为否。 为“是”时直接删除文件，为“否”时将文件改名
    返回：
       无
    '''

    dicHash = {}
    lstF = getFiles(path)
    for fname in lstF[1] :
        print('\rcheck file:%s' % fname,end = '')
        txt = readtxtfile(fname)
        strSame = SameFile(dicHash,fname,txt)
        if strSame:
            print('\rFile [%s] =same=> [%s] ' % (fname,strSame))
            if isDel:
                os.remove(fname)
            else:
                os.rename(fname, fname + '.same')
            #break
    print('\r'+' '*60)


def sysCRLF ():
    ''' 根据系统返回换行符
    '''
    if os.name == 'nt':
        strCRLF = '\n'
    else:
        strCRLF = '\r\n'
    return strCRLF

def get_randstr (strlen=10):
    '''
    生成随机的字符串，可用于文件名等
    参数：
        strlen  字符串长度，默认为10
    返回：
        成功返回 生成的字符串
        失败返回 None
    '''

    try:
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(strlen, strlen)))
        return ran_str
    except Exception as e :
        logging.error('Error in get_randstr: '+ traceback.format_exc())
        return None

def autofilename (pre='', ext=''):
    '''根据时间自动生成文件名， pre为前缀，ext为后缀
    '''
    s = list(range(48,58)) + list(range(65,91)) + list(range(97,123))
    tmp = ''.join(map(chr, random.sample(s, 5)))
    filename = '%s%s%s' % (pre, time.strftime('%Y%m%d%H%M%S',time.localtime()) + tmp, ext)
    return filename

def pre_process (path, addFirstLine=0):
    '''
    文本预处理，删除文件中的空格，空行，并按句子分行，然后在每句前面加上标签0；
    '''

    i = 0
    lstF = getFiles(path)
    for fname in lstF[1] :
        #print('\rProcessing file:%s' % fname,end = '')
        print('Processing file:%s' % fname)
        txt = readtxtfile(fname)
        #按句子拆分
        lstLine = cut_sent(txt)

        if addFirstLine:
            #2019/1/17 加上分类列
            #lstLine = [ '0\t'+x for x in lstLine ]
            #2019/1/22改为调用函数实现
            lstLine = pre_addcolumn(lstLine)

        # 2019/1/17 发现一个坑,linux下和windows下的"\n"竟然不一样,只好用os.name来判断，
        strCRLF = sysCRLF()
        txt = strCRLF.join(lstLine)

        #保存到文件
        if addFirstLine:
            txt = "label\ttxt\n" + txt

        savetofile(txt, fname )
        i += 1
        #if i>9:
        #    pass
            #break
    #print('\r'+' '*60)
    print('Total files: %d' % i)

def pre_NER (txt):
    ''' NER标注数据生成：把文本拆分成一个字符一行
    '''
    lstL = list(txt)
    strRet = sysCRLF().join(lstL)
    return strRet

def pre_addcolumn (lsttxt, lineBegin=1):
    '''
    每行加上空列，参数可指定空列在行首还是行尾,默认为行首
    参数： lsttxt 每行的list
    lineBegin： 1表示空列加在前面；
    '''
    pass
    if lineBegin:
        lstLine = [ '0\t'+x for x in lsttxt ]
    else:
        lstLine = [ x+'\t0' for x in lsttxt ]
    return lstLine

def pre_allzero (lsttxt,lineNo=1):
    ''' 判断数据文件第N列是否全为0 ，默认N=1
    '''
    ret = True
    for line in lsttxt:
        lstW = line.split('\t')
        if lstW[lineNo-1] != 0:
            ret = False
            break
    return ret

def pd_datCheck (lstFile, drop_dup=0, header=None):
    '''
    使用pandas对样本数据文件进行检查；
    drop_dup=1删除重复数据
    '''
    try:
        print("正在检查数据文件: %s \n" % lstFile)
        print(header)
        df = pd.read_csv(lstFile, delimiter="\t", header=header)
        print("数据基本情况".center(30,'-'))
        print(df.index)
        print(df.columns)
        #print(df.head())
        print('正在检查重复数据：...')
        dfrep = df[df.duplicated()]
        print('重复数据行数:%d ' % len(dfrep))
        if len(dfrep)>0:
            print(dfrep)
        if drop_dup and len(dfrep) :
            print('正在删除重复数据：...')
            df = df.drop_duplicates()
            df.to_csv(lstFile, index=0, sep='\t')
        print('-'*30)
        print("数据分布情况".center(30,'-'))
        dfc = df[df.columns[0]].value_counts()
        print('数值分类个数：%d' % len(dfc))
        print('-'*30)
        print(dfc)
        print('\n')
        print("空值情况".center(30,'-'))
        dfn = df[df.isnull().values==True]
        print('空值记录条数: %d ' % len(dfn))
        if len(dfn)>0:
            print('空记录'.center(30,'-'))
            print(dfn.head())
        print('\n')
        return 0
    except Exception as e :
        print("Error in pd_dat:")
        print(e)
        return -1


def pd_datSample (lstFile):
    '''使用pandas 对数据进行打乱'''

    try:
        print("正在随机化数据: %s" % lstFile)
        df = pd.read_csv(lstFile, delimiter="\t", header=None)
        df = df.sample(frac=1)
        #df.sample(frac=1).reset_index(drop=True)
        df.to_csv(lstFile, index=0, sep = '\t', header=None)
        return 0
    except Exception as e :
        print("Error in pd_datSample:")
        print(e)
        return -1

def pre_labelcount (lsttxt, columnindex=0, labelvalue='0'):
    '''统计文本中某类标签情况
    '''

    intLabel = 0
    for line in lsttxt:
        lstW = line.split('\t')
        if lstW[columnindex] == str(labelvalue):
            intLabel += 1
    return intLabel

def str2List (strText, sp=','):
    ''' 字符串转化为整数型List,用于参数传递
    # 默认拆分符号为英文逗号","
    样例：str2List("1,2,3,4,5") ==> [1,2,3,4,5]
    '''
    try:
        ret = strText.split(sp)
        ret = [int(x) for x in ret]
        return ret
    except Exception as e :
        print("Error in str2List:")
        print(e)
        return None

#-----------------------------------------
# 以下是拆分数据相关方法

def splitset(datfile, outpath, lstScale=[7,2,1]):
    '''将指定的数据文件（文本文件）按指定的比例拆分成三个数据集(train,dev,test)
    默认比例为 train:dev:test = 6:2:2
    自动将文件保存到当前目录下；
    参数：datfile
    返回：保存为 'train.tsv','dev.tsv','test.tsv'
    '''
    if len(lstScale)!=3:
        return -1
    txt = readtxtfile(datfile)
    lstLines = txt.splitlines()
    intLines = len(lstLines)-1
    # 取出第一行
    strFirstLine = lstLines[0]

    #切分数据集
    lstS = [sum(lstScale[:x])/sum(lstScale) for x in range(1,len(lstScale)+1)]
    lstPos = [0] + [int(x*intLines) for x in lstS] #
    lstFile = ['train.tsv','dev.tsv','test.tsv']
    for i in range (len(lstFile)):
        lstDat = lstLines[lstPos[i]+1:lstPos[i+1]+1]
        if lstDat:
            fName = os.path.join(outpath, lstFile[i])
            savetofile(strFirstLine + '\n' + '\n'.join(lstDat),fName)
            print('%d  Lines data save to: %s' % (len(lstDat), fName) )


'''
对total个数据，按scale的比例进行拆分，返回切片结果
测试样例：
    get_cut_pos (781, [7,2,1])
返回：[(0, 547), (547, 703), (703, 781)]

测试样例：
get_cut_pos(837, [70,30,10])
返回：[(0, 533), (533, 761), (761, 837)]
'''
def get_cut_pos (total, scale):
    s = sum(scale)
    pos = [round(x*total/s) for x in scale]
    if sum(pos)!=total:
        pos[-1] += total-sum(pos)
    pos = [sum(pos[:i+1]) for i in range(len(pos))]
    cut = list(zip([0] + pos, pos))
    return cut

def split_dataframe(df, outpath, scale=[7,2,1]):
    '''DataFrame 按比例拆分，保存成训练集数据
    '''

    if not os.path.exists(outpath):
        os.makedirs(outpath)
    # 随机打乱
    dfn = df.sample(frac=1)
    # 计算拆分位置
    cutpos = get_cut_pos(dfn.shape[0], scale)
    file_out = ['train.tsv', 'valid.tsv', 'test.tsv']
    # 逐一保存到文件
    for i, pos in enumerate(cutpos):
        df_tmp = dfn.iloc[pos[0]:pos[1]]
        df_tmp.to_csv(os.path.join(outpath, file_out[i]), index=0, sep='\t', header=None)

def df_data_analyze(df, index=0):
    print("数据分布情况".center(30, '-'))
    dfc = df[df.columns[index]].value_counts()
    print('数据分布情况:\n', dfc)
    print('数值分类个数：%d' % len(dfc))
    print('-' * 30)
    df = dfc.to_frame().reset_index()
    return df

def data_split(train_df, n_folds, col_idx=-1, random_state=111):
    # 采用分层抽样的方式，从训练集中抽取1/n_folds作为验证集
    from sklearn.model_selection import StratifiedKFold
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_state)

    X_trn = pd.DataFrame()
    X_val = pd.DataFrame()

    fieldname = train_df.columns[col_idx]
    for train_index, test_index in skf.split(train_df.copy(), train_df[fieldname]):
        X_trn, X_val = train_df.iloc[train_index], train_df.iloc[test_index]
        break
    return X_trn.copy(), X_val.copy()

def save_data_split(df, n_folds, outpath, col_idx=0, random_state=111):
    ''' 对DataFrame使用分层法抽取数据，然后保存到目录
    '''

    df_train, df_vaild = data_split(df, n_folds, col_idx=col_idx, random_state=random_state)
    # df_data_analyze(df_train, col_idx)

    # 随机打乱
    df_train = df_train.sample(frac=1, random_state=random_state)
    df_vaild = df_vaild.sample(frac=1, random_state=random_state)

    if not os.path.exists(outpath):
        os.makedirs(outpath)

    # 保存数据
    file_out = ['train.tsv', 'valid.tsv', 'test.tsv']
    train_fn = os.path.join(outpath, file_out[0])
    df_train.to_csv(train_fn, sep='\t', index=0)

    vaild_fn = os.path.join(outpath, file_out[1])
    df_vaild.to_csv(vaild_fn, sep='\t', index=0)
    print('分层抽取数据集已生成:%s'%outpath)

# -----------------------------------------

def LabelCount (path, renfile=0):
    ''' 统计目录下所有文件的label分布情况
    '''
    pass
    lstF = getFiles(path)
    intTotalLines = 0
    intLabelLines = 0

    for fname in lstF[1] :
        txt = readtxtfile(fname)
        lsttxt = txt.splitlines()
        intLines = len(lsttxt)
        intTotalLines += intLines

        # blnZero = pre_allzero(lsttxt)
        # 统计第0列有多少个"1"
        intLabel = pre_labelcount (lsttxt,0,"1")
        intLabelLines += intLabel
        # 如果renfile开关为1，并且 文件中没有标注，并且文件名不包含"-blank"
        # 那么就改名
        if renfile and not intLabel and (not '-blank' in fname):
            os.rename(fname, fname[:-4] + '-blank' + fname[-4:] )

        print('Processing file:%20s ==> %5d lines, label count: %4d (%2.2f%%) ' % (fname,intLines,intLabel , intLabel*100/intLines ))
    print('%d File(s) ,Total: %d line(s), Laebls: %d (%2.2f%%)' % ( len(lstF[1]),intTotalLines,intLabelLines, intLabelLines*100/intTotalLines ) )

def DatCheck (path, header=None):
    '''按目录进行标注数据检查 2019/2/22'''

    lstF = getFiles(path)
    intTotalLines = 0

    for fname in lstF[1] :
        print("Check Dat File: %s" % fname)
        pd_datCheck(fname, header=header)
    return 0

def linesCount (path):
    '''文本行数统计'''

    lstF = getFiles(path)
    intTotalLines = 0

    for fname in lstF[1] :
        txt = readtxtfile(fname)
        intLines = len(txt.splitlines())
        intTotalLines += intLines
        print('Processing file:%s ==> %d lines' % (fname,intLines))
    print('%d File(s) ,Total: %d line(s)' % ( len(lstF[1]),intTotalLines ) )

def filemerge (path, outfile):
    '''
    文件合并,将目录下的所有文件按行合并
    自动处理文件开头与结尾：第2个文件开始,如果首行与第一个文件相同，则删除第一行
    最终结果输出到参数2指定的文件中；
    '''

    if not outfile:
        return 0
    lstF = getFiles(path)
    intTotalLines = 0
    strFline = ''
    with open(outfile, 'a', encoding='utf-8') as fw:
        for fname in lstF[1] :
            txt = readtxtfile(fname)
            lstLines = txt.splitlines()
            intLines = len(lstLines)
            if intTotalLines == 0:
                strFline = lstLines[0] #记录第一个文件的首行
            else:
                # 第2个文件开始,如果首行与第一个文件相同，则删除第一行
                if lstLines[0]==strFline:
                    lstLines = lstLines[1:]
                    txt = '\n'.join(lstLines)
            if intTotalLines>1: #第2个文件开始加换行,否则开头会有一个空行
                fw.write(sysCRLF())
            fw.write(txt)
            intTotalLines += intLines
            #print('Processing file:%s ==> %d lines ' % (fname,intLines), end = '')
            print('Processing file:%s ==> %d lines ' % (fname,intLines))
    print('\n%d File(s) ,Total: %d line(s)' % (len(lstF[1]),intTotalLines ) )
    print('merge files to %s' % outfile)

#-----------------------------------------

def batch_doc2txt (path, outpath=''):
    ''' 目录(含子目录)下所有文件批量word（.doc,.docx)转txt
    参数：
    path:目录名；
    outpath: 输出目录，默认为空表示源目录
    '''
    from win32com import client as wc
    try:
        #lstFile = getFiles(path)
        lstFile = getAllFiles_Generator(path)#, ['doc','docx']

        strExt = ''
        txtfile = ''
        # 生成目录 txt 用于保存转换后的文件
        if outpath == '':
            new_dir = os.path.join(path, './txt') #'/txt'
        else:
            new_dir = outpath

        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        wordapp = wc.Dispatch('Word.Application')
        # for ft in lstFile[1]:
        for ft in lstFile:
            # 扩展名
            strExt = ''
            if f.rfind('.')>=0:
                strExt = f[f.rindex ('.'):].lower()

            if strExt in ['.doc','.docx']:
                print('正在转换: %s' % ft)
                txtfile = ft[:ft.rindex ('.')]+'.txt'
                txtfile = os.path.abspath(os.path.join(new_dir, txtfile))
                # 判断是否已转换
                if not os.path.isfile(txtfile):
                    try:
                        # 打开文件
                        fname = os.path.abspath(ft)
                        doc = wordapp.Documents.Open(fname)
                        # 为了让python可以在后续操作中r方式读取txt和不产生乱码，参数为4
                        doc.SaveAs(txtfile, 4)
                        doc.Close()
                        print('转换成功：%s' % ( txtfile) )
                    except Exception as e:
                        print('文件转换失败:', e)
                    finally:
                        pass
                else:
                    print('%s 已存在，跳过。' % txtfile )

    finally:
        wordapp.Quit()


def getFieldFromJson (obj, columns, mainname='items', subname=''):
    ''' 从json格式中读取字段
    '''

    result = []
    if mainname:
        lstobj = obj['result'][mainname]
        for x in lstobj:
            dt = []
            for col in columns:
                if subname:
                    if col in x[subname].keys():
                        dt.append(x[subname][col])
                    else:
                        dt.append("")
                else:
                    if col in x.keys():
                        dt.append(x[col])
                    else:
                        dt.append("")
            result.append(dt)
    else:
        # 只有一级的情况
        lstobj = obj['result']
        dt = []
        for col in columns:
            if subname:
                if col in lstobj[subname].keys():
                    dt.append(lstobj[subname][col])
                else:
                    dt.append("")
            else:
                if col in lstobj.keys():
                    dt.append(lstobj[col])
                else:
                    dt.append("")
        result.append(dt)
    return result

#-----------------------------------------

def dict_reverse(data:dict, overwrite=0):
    ''' 字典反转，即把key和value对调
    overwrite：重复值是否覆盖,默认：不覆盖
    '''
    ndict = {}
    for k,value in data.items():
        if type(value)==list:
            for v in value:
                if not v in ndict.keys():
                    ndict[v] = k
                else:
                    if overwrite==1:
                        # 重复值覆盖方式
                        ndict[v] = k
                    else:
                        # 重复值不覆盖方式
                        pass
        else:
            ndict[value] = k
    return ndict

def test_dict_reverse():
	''' 单元测试
	'''
	d = {"a":[1,2,3], 'b':[3,5,6,7], 'c':[8,9,10]}
	print('data:%s'%d)
	ret = dict_reverse(d)
	print('overwrite=0, result=%s'%ret)
	ans = {1: 'a', 2: 'a', 3: 'a', 5: 'b', 6: 'b', 7: 'b', 8: 'c', 9: 'c', 10: 'c'}
	assert ret == ans

	ret = dict_reverse(d, overwrite=1)
	print('overwrite=1, result=%s'%ret)
	ans1 = {1: 'a', 2: 'a', 3: 'b', 5: 'b', 6: 'b', 7: 'b', 8: 'c', 9: 'c', 10: 'c'}
	assert ret == ans1

def sorted_dict_by_keys(data:dict, keys:list):
    ''' 字典重新排序，key按keys的顺序进行排序，未出现的放在最后。
    '''
    length = len(keys)
    key_fun = lambda x: keys.index(x[0]) if x[0] in keys else length+1

    ndata = sorted(data.items(), key=key_fun) #, reverse=True
    ret = dict(ndata)
    return ret

def list_dedup(data:list):
    '''列表元素去重：保留原有的顺序, 重复数据删除
    '''
    try:
        ndat = dict.fromkeys(data)
        ret = list(ndat.keys())
    except Exception as e:
        ret = data
    return ret

def show_long_text(text, cut=50):
    ''' 超长的文本截取首尾。
    '''
    if len(text) > cut*2:
        ret = text[:cut] + '......' + text[-cut:]
    else:
        ret = text
    return ret

def open_image_show(image_filename):
    ''' 在windows系统中使用关联程序打开图像文件显示
    '''
    if os.name!='nt': return
    try:
        pimg = os.path.abspath(image_filename)
        if os.path.exists(pimg):
            os.system(f"explorer \"{pimg}\"")
    except Exception as e:
        pass

def init_logging(log_filename:str="./logs/server.log", level=logging.DEBUG, interval=1, backupCount=7):
    ''' 设置日志，按日期保存日志，默认：每1天一个日志，保留7天；
    '''
    from logging.handlers import TimedRotatingFileHandler

    # Write to log file: logging.DEBUG, INFO
    '''
    logfilename = 'server_%s.log' % time.strftime('%Y%m%d',time.localtime())
    logging.basicConfig(level=logging.DEBUG,
                format='[%(asctime)s] %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=os.path.join(log_path, logfilename),
                filemode='a'
                )
    '''

    # 日志切割：按日期
    log_path = os.path.dirname (log_filename)
    mkfold(log_path)
    # logging.handlers.
    time_rota_handler = TimedRotatingFileHandler(
                filename=log_filename,
                when='d',                       # 时间单位，周：w；天:d；时: h；分：m；秒: s
                interval=interval,              # 间隔多久切一个
                backupCount=backupCount,        # 备份日志保留个数，多余自动删除
                encoding='utf-8')

    time_rota_handler.setFormatter(
        logging.Formatter(
            # fmt='%(asctime)s - %(filename)s - %(levelname)s - %(module)s[%(lineno)d]:  %(message)s',
            fmt='[%(asctime)s] %(filename)s - %(levelname)s - %(module)s [line:%(lineno)d]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))

    logger = logging.getLogger('')
    logger.setLevel(level=level)
    # 清除已有的处理器以防重复添加
    if not logger.handlers:
        logger.addHandler(time_rota_handler)
        print('set logging ok!')

    # 关闭 Matplotlib的调试信息
    # logging.getLogger('matplotlib').setLevel(logging.ERROR)

# -----------------------------------------

# SSE 消息包装
def get_yield_data(content, event="message", newline=0, delay=0):
    ''' 生成SSE消息内容
    参数：newline: 是否换行显示；默认0
    '''
    if type(content) == str and newline:
        content = "\n\n" + content

    yield_data = json.dumps({"event":event, "content":content})
    if delay>0: time.sleep(delay)
    yield yield_data

def yield_texts(texts, newline=1, interval=0.1):
    ''' 生成多行SSE消息
    '''
    if type(texts) == list:
        for txt in texts:
            if not txt:continue
            yield from get_yield_data(txt, newline=newline)
            if interval>0: time.sleep(interval)
    elif type(texts) == str:
        for txt in texts.splitlines():
            if not txt:continue
            yield from get_yield_data(txt, newline=newline)
            if interval>0: time.sleep(interval)


if __name__ == '__main__':
    pass

