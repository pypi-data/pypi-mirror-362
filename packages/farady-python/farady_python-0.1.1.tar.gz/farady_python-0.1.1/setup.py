from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="farady-python",  # PyPI上唯一标识（必须小写+下划线）
    version="0.1.1",  # 遵循语义化版本 (semver.org)
    author="Tinger",
    author_email="email@tingerx.com",
    description="Farady Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tinger-X/Farady-Python",
    packages=find_packages(),  # 自动发现包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python版本要求
    install_requires=[  # 依赖库
        "matplotlib"
    ]
)
