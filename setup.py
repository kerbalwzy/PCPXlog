# coding:utf-8
# 引用包管理工具setuptools，其中find_packages可以帮我们便捷的找到自己代码中编写的库
from setuptools import setup, find_packages

setup(
    name='pcpxlog',  # 包名称，之后如果上传到了pypi，则需要通过该名称下载
    version='0.1',  # version只能是数字，其他字符则会报错
    keywords=('cpxlog', 'pcpxlog', 'kerbalwzy'),
    description='Simple configuration allows log output to console, file, database at the same time',
    long_description='',
    license='Mozilla Public License Version 2.0',  # 遵循的协议
    install_requires=['pymongo'],  # 这里面填写项目用到的第三方依赖
    author='wangzhongying',
    author_email='kerbalwzy@gmail.com',
    packages=find_packages(),  # 项目内所有自己编写的库
    platforms='any',
    url='https://github.com/kerbalwzy/PCPXlog',  # 项目链接,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'miniframe=miniFrame.script:main'
        ]
    },
)
