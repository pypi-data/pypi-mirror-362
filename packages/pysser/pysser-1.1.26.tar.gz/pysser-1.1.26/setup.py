from setuptools import setup, find_packages ,Extension


setup(
    name="pysser",
    version="1.1.26",
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的库所需的其他Python包
        "pyserial==3.5",
    ],
    author="nbigbug",
    author_email="nbigbug@126.com",
    description="A special ser",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX :: Linux',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)