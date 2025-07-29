from setuptools import setup, find_packages

setup(
    name="aminobot",  
    version="0.1.1",  
    description="",   
    author="DarkCat",  
    author_email="",  
    url="",  
    packages=find_packages(),  
    install_requires=[
        "requests>=2.0.0",  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  
)
