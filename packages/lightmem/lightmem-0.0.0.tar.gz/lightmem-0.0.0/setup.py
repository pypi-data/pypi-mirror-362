from setuptools import setup, find_packages
 
setup(
    name="lightmem",  # 包名，pip install 时用这个
    version="0.0.0",
    description="A light agent memory",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Jizhan fang",
    author_email="fangjizhan@zju.edu.cn",
    url="https://github.com/zjunlp/LightMem",  # 可选：放 GitHub 仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)