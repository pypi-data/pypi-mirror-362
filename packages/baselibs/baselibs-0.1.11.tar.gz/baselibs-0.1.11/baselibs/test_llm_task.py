#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

import logging
from llm_task import LLM_TASK

def test_llm_task():
    cfg = [
        "http://192.168.15.111:3000/v1",    # one-api
        "sk-pLLG2ucf61sKFjMxA0Fd11E88c734427A078Bc554e516e26",
        "qwen-turbo"
    ]
    base_url, api_key, model = cfg

    prompt_template = """
    # 请根据用户的关键词生成一首五言绝句
    # 输出格式：请使用JSON格式输出,格式为：{"result":"生成结果"}。
    # 关键词：
    $keyword$
    """
    model = "qwq-32b"
    model = "qwen3-32b" 
    print(f"model:{model}")

    llm = LLM_TASK(api_key, base_url=base_url, model=model, prompt_template=prompt_template)
    parm = {"$keyword$":"春天 浓雾 郑成功 动荡 国际形势"}
    print(f"parm:{parm}")
    result = llm.predict(parm)
    print(result)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_llm_task()
