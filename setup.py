from setuptools import setup, find_packages

setup(
    name="every-day-helper",
    version="1.0.0",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "every-day-helper=main:main",
        ],
    },
    install_requires=[
        "prompt_toolkit==3.0.48",
        "tabulate==0.9.0",
        "wcwidth==0.2.13",
        "setuptools==75.8.0"
    ],  
    author="Nataliia Smalchenko, Andrii Veremii, Oleksandr Mamrenko, Maryna Korbet ",
    author_email="yarokrilka@gmail.com",
    description="A convenient system for organizing and managing contacts and notes.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nataliia-smalchenko/every-day-helper", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6, <4",
)