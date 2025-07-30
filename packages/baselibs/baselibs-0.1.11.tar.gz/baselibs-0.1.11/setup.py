#!/usr/bin/env python3
#coding:utf-8

__author__ = 'xmxoxo<xmxoxo@qq.com>'

# import setuptools
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# 读取 requirements.txt 文件中的依赖项
with open('baselibs/requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

# 导入静态文件
file_data = []

setup(
    name='baselibs',
    version='0.1.11',
    description='baselibs',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='baselibs',
    # py_modules=['baselibs'], # 单个模块
    # install_requires=[],
    
    install_requires=requirements,  # 从 requirements.txt 文件中读取的依赖项
    packages=find_packages(),
    # include_package_data=True,
    author='He xi',
    author_email='xmhexi@qq.com',
    url='https://github.com/xmxoxo/baselibs',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable'
        'Development Status :: 4 - Beta',  # 当前开发进度等级（测试版，正式版等）
        'Intended Audience :: Developers',  # 模块适用人群
        'Topic :: Software Development :: Code Generators',  # 给模块加话题标签
        'License :: OSI Approved :: MIT License',  # 模块的license
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    project_urls={  # 项目相关的额外链接
        'Blog': 'https://blog.csdn.net/xmxoxo',
    },
    entry_points={}
)



