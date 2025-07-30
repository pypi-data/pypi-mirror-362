from setuptools import setup, find_packages

setup(
    name="project_logger",
    version="1.1.1",
    packages=find_packages(),
    install_requires=[
        "pymysql",
        "dbutils",
    ],
    author="Funnel",
    author_email="sunn61676@gmail.com",
    description="A security logging package for Python projects",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)