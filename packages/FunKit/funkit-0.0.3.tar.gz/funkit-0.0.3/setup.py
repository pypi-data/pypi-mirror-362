from setuptools import setup, find_packages


# 读取 README 文件内容，用于在 PyPI 上显示项目描述
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


# 配置 setup 函数的参数
setup(
    # 包的名称，用户在安装时使用这个名称
    name='FunKit',

    # 包的版本号，遵循语义化版本规范
    version='0.0.3',

    # 包的简要描述，显示在 PyPI 上，包含中英文
    description='一个功能强大的 Python 装饰器工具包 | A powerful Python decorator toolkit',

    # 包的详细描述，通常从 README 文件中读取
    long_description=long_description,

    # 详细描述的内容类型，这里使用 Markdown 格式
    long_description_content_type='text/markdown',

    # 包的作者姓名
    author='cxfjh',

    # 作者的电子邮件地址
    author_email='2449579731@qq.com',

    # 项目的主页 URL
    url='https://github.com/cxfjh/FunKit',

    # 包所依赖的 Python 版本范围
    python_requires='>=3.6',

    # 包的依赖列表
    install_requires=[
        "psutil"
    ],

    # 自动查找包和子包，确保所有相关文件都被包含
    packages=find_packages(),

    # 包的分类信息，帮助用户在 PyPI 上找到你的包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    # 包的关键词，帮助用户在搜索时找到你的包，包含中英文
    keywords=['decorator', 'toolkit', 'fun', 'kit', 'funkit', 'funkit', '装饰器', '工具包', '函数', '函数式编程', 'FunKit'],

    # 包的许可证名称
    license='MIT',
)