from setuptools import setup, find_packages

setup(
    name='pts_utils',  # 包名称
    version='0.1',      # 版本
    packages=find_packages(),  # 自动查找包
    py_modules=['pts_utils'],  # 列出你想包含的模块文件
    install_requires=[],  # 依赖包列表，如果没有可以为空
)
