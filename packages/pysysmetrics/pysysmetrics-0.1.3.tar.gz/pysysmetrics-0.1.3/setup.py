from setuptools import setup, find_packages

setup(
    name="pysysmetrics",
    version="0.1.3",
    description="CLI tool to monitor CPU and GPU memory usage of Python processes",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Aditya Thiyyagura",
    author_email="thiyyaguraadityareddy@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "psutil",
        "pynvml"
    ],
    entry_points={
        "console_scripts": [
            "pysysmetrics=pysysmetrics.cli.main:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Monitoring",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
)