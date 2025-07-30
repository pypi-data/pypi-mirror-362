#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

import openai
import os
import random
import re
import json
import logging

# 过滤思维链内容 think
filter_think = lambda text: re.sub(r'<think>.*?</think>', '', str(text), flags=re.DOTALL) if text else ""

def split_think(text:str) -> tuple:
    ''' 拆分思维链内容
    '''
    result = text
    think_text = ""
    # think_match = re.findall(r'(<think>(.*?)</think>)', text, flags=re.DOTALL)
    think_match = re.search(r'<think>(.*?)</think>', text, flags=re.DOTALL)
    if think_match :
        # think_text = think_find[0][1]
        # result = text.replace(think_find[0][0], '')
        think_text = think_match.group(1)
        result = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return result, think_text

# LLM 大模型任务类
class LLM_TASK():
    def __init__(self, api_key, base_url="", 
            proxys=None, prompt_template='', model="", 
            use_system_prompt=0, result_replace_dict={}):

        # 提示词模板
        prompt_template = re.sub(r"\n +", r"\n", prompt_template)
        self.prompt_template = prompt_template

        # api key
        self.api_key = api_key
        # 模型名称
        self.model = model
        self.use_system_prompt = use_system_prompt  # 是否使用系统提示词

        # token使用时统计
        self.total_tokens = 0
        self.usages = []

        # 调试
        self.debug = 0

        # 自定义结果替换：字典
        self.result_replace_dict = result_replace_dict
        
        self.base_url = base_url
        if proxys:
            os.environ['HTTP_PROXY'] = proxys
            os.environ['HTTPS_PROXY'] = proxys
        self.client = openai.OpenAI(api_key=self.api_key, base_url=self.base_url)

    @staticmethod
    def clear_text(txt, key, pos=0) -> str:
        # 用于清理格式
        if pos==0: # 开头
            if txt.startswith(key): txt = txt[len(key):]
        else: # 结尾
            if txt.endswith(key): txt = txt[:-len(key)]
        return txt

    @staticmethod
    def haschar(text: str, avoid: str) -> bool:
        ''' 判断text中是否包含avoid中的任意一个字符；
        '''
        text_chars = set(text)
        void_chars = set(avoid)
        # 利用集合的交集操作，如果text的字符集合与void的字符集合有交集，则说明text包含void中的字符
        return bool(text and avoid and text_chars.intersection(void_chars))

    @staticmethod
    def replace_dict (txt:str, dictKey:dict, isreg=0) -> str:
        '''按字典进行批量替换
        isreg: 是否启用正则
        '''
        tmptxt = txt
        for k, v in dictKey.items():
            if isreg:
                tmptxt = re.sub(k, v, tmptxt)
            else:
                tmptxt = tmptxt.replace(k, v)
        return tmptxt

    def txt2json(self, text):
        ''' 把文本解析成JSON，用于处理大模型输出的各类异常格式；
        '''
        try:
            # 增加：自定义替换； 2024/5/8
            if self.result_replace_dict:
                text = self.replace_dict (text, self.result_replace_dict)
            # 过滤 "<think>"  qwq模型特定
            text = filter_think(text)

            # 去掉各行的空格及换行
            text = ''.join([x.strip() for x in text.splitlines()])

            # 格式化处理
            text = self.clear_text(text, '```json', 0)
            text = self.clear_text(text, '```', 0)
            text = self.clear_text(text, '```', 1)
            # 单引号换成双引号 (2025/5/12 去掉)
            # text = text.replace("'", '"')
            # 标准列表
            npat = r"^\[ *(\"[\w\- _\\u4E00-\\u9FA5]+\"( *, *)?)+ *\]$"
            nret = re.match(npat, text)
            if nret:
                jdat = json.loads(text)
                return jdat

            # 如果不含括号引号等: "{}[]"，则判断为纯文本，转换成列表
            ## 处理[abc, "其它"] 这样的格式

            # 注意：处理："[tec]"这样的格式 2024/11/1
            pat = r"^\[([\w,\-'\" _\\u4E00-\\u9FA5]+)\]$"
            mret = re.match(pat, text)
            if mret:
                if self.debug:
                    print(f'found format:{text}')
                tmp = mret[0][1:-1].replace(" ", "")
                items = [x.replace("\"", "") for x in tmp.split(",")]
                text = '["' + '","'.join(items) + '"]'
                if self.debug:
                    print(f'fixed format:{text}')
            elif not self.haschar(text,  "{}[]\"'"):
                text = f"[\"{text}\"]"

            # 如果以引号开头和结尾，则认为是纯文本，将其头尾加上[]转化为列表
            elif (text.startswith('"') and text.endswith('"')) or \
                (text.startswith("'") and text.endswith("'")):
                text = f"[{text}]"
            if self.debug:
                print(f'debug: {type(text)}, {text}\n')

            # 转为JSON格式
            jdat = json.loads(text)
            return jdat
        except Exception as e:
            print("text: ", text)
            print('error on txt2json:', e)
            # 格式不正确时返回原文本
            return text

    def call_with_messages(self, prompt, history=[],
                system_prompt='', token_count=None):
        ''' OpenAI接口调用LLM
        '''
        messages = []
        if system_prompt != '':
            messages.append({'role': 'system', 'content': system_prompt})
        else:
            messages = [{'role': 'system', 'content': 'You are a helpful assistant.'}]

        # 添加历史记录
        if history:
            messages.extend(history)
        # 添加用户问题
        messages.append({'role': 'user', 'content': prompt})

        # 兼容阿里百炼模型：qwq, qwen3模型 2025/7/15
        extra_body = None
        stream=False
        if "qwen3-" in self.model:
            extra_body = {"enable_thinking": False}
        
        if "qwq-" in self.model:
            stream=True
            # extra_body = {"enable_thinking": False}

        # 调用LLM
        try:
            ret_content = ''
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                seed=random.randint(0, 1000),
                temperature=0.1,        # 默认值=0.8
                extra_body=extra_body,
                stream=stream
            )
            if stream:
                # 流式返回
                think_text = ""
                for chunk in response:
                    if hasattr(chunk, "choices"):
                        choices = chunk.choices
                        if choices:
                            delta = choices[0].delta
                            # 思考过程
                            if hasattr(delta, 'reasoning_content') and delta.reasoning_content:
                                reasoning_content = delta.reasoning_content
                                think_text += reasoning_content
                                logging.debug(f'reasoning_content:{reasoning_content}')
                                                        
                            # 回复内容
                            elif hasattr(delta, 'content') and delta.content:
                                content = delta.content
                                ret_content += content
                                logging.debug(f'content:{content}')

            else:
                # 非流式返回
                if response:
                    ret_content = response.choices[0].message.content

                    # 记录token使用量
                    if not token_count is None:
                        usage = dict(response.usage)
                        token_count.add_token(usage)
                else:
                    # 出错返回空
                    pass
                    '''
                    print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                        response.request_id, response.status_code,
                        response.code, response.message
                    ))
                    '''
            return ret_content
        except Exception as e:
            print(e)
            return ""

    def add_token(self, usage:dict):
        ''' 添加token使用量
        '''
        self.usages.append(dict(usage))
        total_tokens = usage.get('total_tokens', 0)
        self.total_tokens += total_tokens

    def predict(self, parm:dict):
        ''' 执行任务
        '''

        # 生成提示词
        if self.use_system_prompt:
            query = ''.join(parm.values())
            ret = self.call_with_messages(query,
                        system_prompt=self.prompt_template,
                        token_count=self)
        else:
            prompt_text = self.replace_dict(self.prompt_template, parm)
            print('prompt_text:', prompt_text)
            ret = self.call_with_messages(prompt_text, token_count=self)

        if self.debug:
            print('model ret:', ret)

        # 转换解析JSON
        jdat = self.txt2json(ret)
        return jdat

if __name__ == '__main__':
    pass


