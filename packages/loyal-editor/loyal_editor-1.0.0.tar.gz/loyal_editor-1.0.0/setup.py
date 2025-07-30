from setuptools import setup, find_packages

setup(
    name="loyal-editor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["colorama"],
    entry_points={
        "console_scripts": ["loyal=loyaleditor.cli:main"],
    },
    author="Ваше имя",
    description="Терминальный текстовый редактор с нумерацией строк",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)