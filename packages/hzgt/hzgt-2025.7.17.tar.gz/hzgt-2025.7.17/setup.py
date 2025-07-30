import os.path

from setuptools import setup, find_packages

from hzgt import version

# 包的总结
short_description = "A toolbox that includes MQTT, MYSQL, FTP encapsulation, and other gadgets"
# 包的详细说明
# 读取setup.md的内容
long_description = open("README.md", encoding="utf-8").read()


setup(
    name="hzgt",  # 包的分发名称
    version=version,  # 包的版本
    author="HZGT",  # 包的作者
    author_email="2759444274@qq.com",  # 包的作者的邮箱

    description=short_description,  # 用于介绍包的总结
    long_description=long_description,  # 包的详细说明
    long_description_content_type="text/plain",  # 索引类型长描述
    url="https://github.com/HZGT/hzgt",  # 项目主页的URL

    packages=find_packages(),
    package_data={  # 额外包含的文件
        'hzgt': [
            os.path.join("__version", "version.txt"),
            os.path.join("tools", "extensions_map.ini"),
            os.path.join("tools", "rsa.js"),
            os.path.join("tools", "favicon.ico"),
        ]
    },
    include_package_data=True,
    data_files=[
        ("hzgt", [
            'README.md',
            'LICENSE'
        ])
    ],  # 指定打包的文件

    install_requires=[
        'click',
        'requests', 'tqdm',
        "pymysql",  # MYSQL
        # "cryptography", # MYSQL
        # "psycopg2-binary",  # POSTGRESQL
        "paho-mqtt",  # MQTT
        "pyftpdlib",  # FTP
        # "PyExecJS",  # js
        "dotenv",  # AutoConfig

    ],  # 需要安装的依赖包
    extras_require={
        "MYSQL": "cryptography",
    },  # 深度使用的包, 手动安装

    python_requires='>=3.8',  # python版本限制

    scripts=['hzgt/cmdline.py'],  # 添加为命令行
    entry_points={
        'console_scripts': [
            'hzgt=hzgt.cmdline:losf'  # 命令行前提命令=入口程序名称:入口函数
        ]
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # 元数据
)

"""
参数	说明
name	包名称
version	包版本
author	程序的作者
author_email	程序的作者的邮箱地址
maintainer	维护者
maintainer_email	维护者的邮箱地址
url	程序的官网地址
license	程序的授权信息
description	程序的简单描述
long_description	程序的详细描述
platforms	程序适用的软件平台列表
classifiers	程序的所属分类列表
keywords	程序的关键字列表
packages	需要处理的包目录(通常为包含 __init__.py 的文件夹)
py_modules	需要打包的 Python 单文件列表
download_url	程序的下载地址
cmdclass	添加自定义命令
package_data	指定包内需要包含的数据文件
include_package_data	自动包含包内所有受版本控制(cvs/svn/git)的数据文件
exclude_package_data	当 include_package_data 为 True 时该选项用于排除部分文件
data_files	打包时需要打包的数据文件，如图片，配置文件等
ext_modules	指定扩展模块
scripts	指定可执行脚本,安装时脚本会被安装到系统 PATH 路径下
package_dir	指定哪些目录下的文件被映射到哪个源码包
entry_points	动态发现服务和插件
python_requires	指定运行时需要的Python版本
requires	指定依赖的其他包
provides	指定可以为哪些模块提供依赖
install_requires	安装时需要安装的依赖包
extras_require	当前包的高级/额外特性需要依赖的分发包
tests_require	在测试时需要使用的依赖包
setup_requires	指定运行 setup.py 文件本身所依赖的包
dependency_links	指定依赖包的下载地址
"""
