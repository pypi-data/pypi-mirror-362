from setuptools import setup, find_packages

setup(
    name="tamil-lang",
    version="1.0.0",
    description="A simple Tamil programming language interpreter",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Kamalnath.S",
    author_email="kamalnath9443348610@gmail.com",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
  'console_scripts': [
    'tamil = tamil.__main__:main'
  ],
},

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
