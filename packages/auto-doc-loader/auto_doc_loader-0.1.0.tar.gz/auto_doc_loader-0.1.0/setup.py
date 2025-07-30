from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='auto_doc_loader',
    version='0.1.0',
    description='AutoLoader for structured and unstructured documents using LangChain',
    author='Maran M',
    author_email='mahemaran99@gmail.com',
    url = 'https://github.com/Mahemaran/auto_loader',
    license="Apache 2.0",
    packages=find_packages(),
    install_requires=[
        'langchain',
        'langchain-unstructured'],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],

)
