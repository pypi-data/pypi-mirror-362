from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='shipxy-api',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    author="White",
    author_email="249898979@qq.com",
    description="亿海蓝Elane船讯网sdk https://www.shipxy.com/",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
