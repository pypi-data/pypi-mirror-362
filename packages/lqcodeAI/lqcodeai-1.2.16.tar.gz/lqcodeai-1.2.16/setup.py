from setuptools import setup, find_packages

setup(
    name="lqcodeAI",
    version="1.2.16",
    author="TivonFeng",
    author_email="tivonfeng@163.com",
    description="绿旗编程AI课程SDK",
    long_description=open("README.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/TivonFeng/lqcode",
    packages=find_packages(),
    package_data={
        'lqcodeAI': ['*.json', '*.yaml', '*.yml'],
    },
    include_package_data=True,
    install_requires=[
        'requests>=2.25.1',
        'cozepy>=0.13.1',
    ],
    extras_require={
        'streamlit': ['streamlit>=1.0.0'],
    },
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'lqcodeAI=lqcodeAI.cli:main',
        ],
    },
) 