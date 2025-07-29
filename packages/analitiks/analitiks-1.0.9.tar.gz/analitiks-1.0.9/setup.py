from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name='analitiks',
    version='1.0.9',
    packages=find_packages(),
    install_requires=[
    "psycopg2-binary",
    "sqlalchemy",
    "telebot",
    "requests",
    "openpyxl",
    "numpy",
    "pandas",
    "matplotlib",
    "seaborn",
    "xlrd",
    "xlwt",
    "pymysql",
],
    author='DREAM',
    author_email='dream9565@mail.ru',
    description='Библиотека для Аналитика',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
