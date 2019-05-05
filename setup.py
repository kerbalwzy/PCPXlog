# coding:utf-8
# 引用包管理工具setuptools，其中find_packages可以帮我们便捷的找到自己代码中编写的库
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pcpxlog',
    version='0.1',
    author='WangZhongYing',
    author_email='kerbalwzy@gmail.com',
    url='https://github.com/kerbalwzy/PCPXlog',

    keywords=('cpxlog', 'pcpxlog', 'kerbalwzy', 'wangzhongying'),
    description='Simple configuration allows log output to console, file, database at the same time',
    long_description=long_description,
    long_description_content_type="text/markdown",

    license='Mozilla Public License Version 2.0',
    python_requires='>=3',
    install_requires=['pymongo'],
    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'cpxConfigDemo=pcpxlog.cpxUtils:create_conf_py_file'
        ]
    }

)
