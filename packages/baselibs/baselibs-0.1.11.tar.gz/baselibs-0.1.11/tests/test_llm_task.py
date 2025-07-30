#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

from baselibs.llm_task import LLM_TASK

def test_llm_task():
    cfg = [
        "http://192.168.15.111:3000/v1", # one-api
        "sk-GQtwF5ag8p6m8wWf1232B8D5E17f4455A5C14e7a2d393aEe",
        "deepseek-chat"
    ]
    base_url, api_key, model = cfg

    prompt_template = """
    # 请根据用户的关键词生成一首五言绝句
    # 关键词：
    {keyword}
    """

    llm = LLM_TASK(api_key, base_url=base_url, model=model, prompt_template=prompt_template)
    parm = {"{keyword}":"春天 浓雾 郑成功 动荡 国际形势"}
    result = llm.predict(parm)
    print(result)

if __name__ == '__main__':
    pass
    test_llm_task()
