# -*- coding:utf-8 -*-

import setuptools
import os

# README.md 파일 읽기
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "elio board python uart interface"

setuptools.setup(
    name="elio-uart",
    version="0.0.3",
    license='MIT',
    author="elio robotics",
    author_email="caram88@mobilian.biz",
    description="elioboard python uart interface",
    long_description=read_readme(),
    url="https://github.com/johnsnow-nam/elio-uart",
    packages=setuptools.find_packages(),
    install_requires=['pyserial'],
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=2.7',
)
