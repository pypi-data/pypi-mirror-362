from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pcreq",  # 替换为你的包名（PyPI 上唯一）
    version="0.1.0",
    author="pcreq",
    author_email="lhuashan1@163.com",
    description="一个简单的Python包示例",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pcreq/pcreq",  # 项目主页
    project_urls={  # 可选
        "Bug Tracker": "https://github.com/pcreq/pcreq/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),  # 自动发现所有模块
    python_requires=">=3.6",
    install_requires=[
        # 依赖项，例如：
        # "requests>=2.20.0",
    ],
    include_package_data=True,
    license="MIT",
)
