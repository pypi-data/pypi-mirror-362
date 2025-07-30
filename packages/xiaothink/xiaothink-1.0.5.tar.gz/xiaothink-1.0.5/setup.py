
import setuptools
with open("README.md", "r",encoding='utf-8') as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="xiaothink",  # 模块名称
    version="1.0.5",  # 当前版本
    author="Ericsjq",  # 作者
    author_email="xiaothink@foxmail.com",  # 作者邮箱
    description="一个AI工具包，帮助用户快速调用小思框架（Xiaothink）相关接口。",  # 模块简介
    long_description=long_description,  # 模块详细介绍
    long_description_content_type="text/markdown",  # 模块详细介绍格式
    packages=setuptools.find_packages(),  # 自动找到项目中导入的模块
    # 模块相关的元数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'tensorflow',
        'numpy',
    ],
    python_requires='>=3',

)
