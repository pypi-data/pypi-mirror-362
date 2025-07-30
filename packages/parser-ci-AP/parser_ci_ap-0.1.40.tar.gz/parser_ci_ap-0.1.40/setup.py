from setuptools import setup, find_packages

setup(
    name="parser-ci-AP",                         # Название пакета (на PyPI)
    version="0.1.40",                          # Версия
    description="C code parser based on Clang",  # Краткое описание
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Александр",
    author_email="sanyapetrooo@gmail.com",
    url="https://github.com/yourusername/parser-ci",  # (если есть)
    license="MIT",
    packages=find_packages(),                # Автоматически находит parser_ci_AP
    include_package_data=True,
    install_requires=[
        "chardet==5.2.0",
        "libclang==18.1.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
)