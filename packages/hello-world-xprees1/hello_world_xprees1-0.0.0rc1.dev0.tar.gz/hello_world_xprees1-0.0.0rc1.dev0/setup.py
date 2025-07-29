from setuptools import setup, find_packages, Extension

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

module = Extension(
    "helloworld",
    sources=["helloworld.c"],
)

setup(
    name="hello_world_xprees1",  # 替换为你的包名
    version="0.0.0rc1-dev",
    author="xprees1",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    ext_modules=[module]
)