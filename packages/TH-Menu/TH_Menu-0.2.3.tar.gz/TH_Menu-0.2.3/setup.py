from setuptools import setup, find_packages

setup(
    name="TH_Menu",
    version="0.2.3",
    author="Ivan (Thomson Hate)",
    description="Умная система вложенных меню с кнопкой 'Назад' для nextcord",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Thomson-Hate/TH-Menu/blob/main/README.md",
    packages=find_packages(),
    install_requires=[
        "nextcord>=2.5.0",
        "requests>=2.0.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Framework :: AsyncIO",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.8",
)
