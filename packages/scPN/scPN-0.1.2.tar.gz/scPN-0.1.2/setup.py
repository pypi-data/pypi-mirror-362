from setuptools import setup, find_packages

setup(
    name='scPN',                # 包名 (pip install my_package)
    version='0.1.2',
    packages=find_packages(),         # 自动找到 my_package 目录
    install_requires=[
        'numpy','scvelo','scanpy','numpy','scipy','torch','pandas','leidenalg','joblib'                  # 可选：依赖库
    ],
    author='Zhen Zhou',
    author_email='zz20020101@sjtu.edu.cn',
    description='A package for single cell pseudotime',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ZHOUZHEN2002/scPN/tree/master',  # 可选：GitHub 项目地址
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
